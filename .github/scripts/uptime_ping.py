#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server-Uptime-Pinger für minxserver.duckdns.org.

Läuft per GitHub Actions alle 5 Minuten (extern, von GitHub-Servern).
Macht einen echten Minecraft-Server-List-Ping (TCP + MC-Protokoll) und
speichert das Ergebnis kompakt in uptime_data.json:

  days:   Pro Tag aggregates (up/down/ms) über 90 Tage
  recent: Rohwerte der letzten ~24h (5-Min-Raster) für den Verlauf

Das JSON bleibt klein (~30 KB), damit Git-Deltas pro Ping winzig bleiben.
Läuft auf dem eigenen Branch "uptime-data" (nicht main, damit nicht
bei jedem Ping das Pages-Deployment triggert).
"""
import json
import os
import socket
import struct
import sys
import time
from datetime import datetime, timedelta, timezone

HOST = "minxserver.duckdns.org"
PORT = 25565
TIMEOUT = 8.0            # Sekunden pro Ping
RETENTION_DAYS = 90      # Aggregate behalten
RECENT_HOURS = 24        # Rohwerte behalten (5-Min-Raster → ~288)
RECENT_MAX = 288

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
DATA_PATH = os.path.join(ROOT, "uptime_data.json")


# ---------- Minecraft Server List Ping (roh, ohne Libraries) ----------

def _varint(n: int) -> bytes:
    out = b""
    n &= 0xFFFFFFFF  # negative Werte (z.B. Protokoll -1) als 32-Bit-Zweierkomplement
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out += bytes([b | 0x80])
        else:
            return out + bytes([b])


def _read_varint(data: bytes, i: int):
    n = 0
    shift = 0
    while True:
        if i >= len(data) or shift > 28:
            raise ValueError("VarInt zu lang/EOF")
        b = data[i]
        i += 1
        n |= (b & 0x7F) << shift
        if not (b & 0x80):
            return n, i
        shift += 7


def _read_varint_stream(sock) -> int:
    n = 0
    shift = 0
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError("EOF bei VarInt")
        n |= (b[0] & 0x7F) << shift
        if not (b[0] & 0x80):
            return n
        shift += 7
        if shift > 28:
            raise ValueError("VarInt zu lang")


def _read_exact(sock, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("EOF beim Lesen")
        data += chunk
    return data


def mc_ping(host: str, port: int, timeout: float):
    """Echter MC-Ping. Gibt (ok, ms, info) zurück."""
    t0 = time.monotonic()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.settimeout(timeout)
        host_b = host.encode()
        hs = (_varint(0xFFFFFFFF)         # Protokoll -1 (Status)
              + _varint(len(host_b)) + host_b
              + struct.pack(">H", port)
              + _varint(1))                 # Next State: Status
        # Paket: [Länge][Paket-ID 0x00][Daten]
        sock.sendall(_varint(len(hs) + 1) + b"\x00" + hs)
        sock.sendall(_varint(1) + b"\x00")  # Status-Request
        total = _read_varint_stream(sock)
        body = _read_exact(sock, total)
        # Antwort-Paket: ID (VarInt) + String-Länge (VarInt) + JSON
        _, i = _read_varint(body, 0)
        slen, i = _read_varint(body, i)
        raw = body[i:i + slen].decode("utf-8", "replace")
        info = json.loads(raw)
        ms = round((time.monotonic() - t0) * 1000)
        players = info.get("players") or {}
        return True, ms, {
            "p": players.get("online"),
            "mx": players.get("max"),
            "v": (info.get("version") or {}).get("name"),
        }
    except Exception as e:
        return False, None, {"err": str(e)[:100]}


# ---------- Daten verwalten ----------

def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"days": {}, "recent": []}


def main():
    now = datetime.now(timezone.utc)
    ok, ms, info = mc_ping(HOST, PORT, TIMEOUT)
    data = load_data()

    # 1) Tages-Aggregate aktualisieren
    day = now.strftime("%Y-%m-%d")
    d = data["days"].setdefault(day, {"up": 0, "down": 0, "ms_sum": 0, "ms_n": 0})
    if ok:
        d["up"] += 1
        if ms is not None:
            d["ms_sum"] += ms
            d["ms_n"] += 1
    else:
        d["down"] += 1

    # 2) Rohwerte der letzten 24h
    cutoff = (now - timedelta(hours=RECENT_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sample = {"t": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "ok": ok}
    if ms is not None:
        sample["ms"] = ms
    if ok and info.get("p") is not None:
        sample["p"] = info["p"]
    data["recent"] = [s for s in data["recent"] if s["t"] >= cutoff]
    data["recent"].append(sample)

    # 3) Alte Tages-Aggregate weg
    cutoff_day = (now - timedelta(days=RETENTION_DAYS)).strftime("%Y-%m-%d")
    data["days"] = {k: v for k, v in data["days"].items() if k >= cutoff_day}

    data["generated"] = sample["t"]
    data["host"] = HOST
    data["port"] = PORT

    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, DATA_PATH)

    status = "OK" if ok else "DOWN"
    print(f"{sample['t']}  {status}  ms={ms}  players={info.get('p')}")


if __name__ == "__main__":
    main()
