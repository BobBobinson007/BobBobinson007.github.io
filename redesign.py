#!/usr/bin/env python3
"""
Rewrite index.html with minimalistic topic banner and remove supporter crap.
"""
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# --- REMOVE SUPPORTER CSS ---
import re
html = re.sub(
    r'  \.supporter-card.*?\n  \.supporter-done.*?\n',
    '',
    html,
    flags=re.DOTALL
)

# --- REMOVE TOPIC BANNER CSS ---
html = re.sub(
    r'  /\* ===== TOPIC BANNER.*?\n  \.topic-now \.theme-dot.*?\n\n',
    '',
    html,
    flags=re.DOTALL
)

# --- ADD MINIMAL TOPIC DOT ROW CSS ---
topic_css = """  /* ===== Tägliches Thema (minimal) ===== */
  .theme-row { display: flex; align-items: center; gap: 12px; margin: 14px 0 18px; justify-content: flex-end; }
  .theme-dots { display: flex; gap: 5px; align-items: center; }
  .theme-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--date-color); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); flex-shrink: 0; }
  .theme-dot.today { width: 8px; height: 8px; }
  .theme-label { font-size: 11px; color: var(--date-color); letter-spacing: 0.2px; transition: color 0.3s; }
  .theme-label strong { font-weight: 500; }
  .colormode .theme-label { color: var(--tag-hover); }

"""
html = html.replace(
    "  .toggle.on::after { transform: translateX(20px); }\n\n",
    "  .toggle.on::after { transform: translateX(20px); }\n" + topic_css
)

# --- REPLACE TOPIC BAR HTML ---
old_topic_html = """<!-- ===== Tägliche Themenleiste ===== -->
<div class="topic-bar" id="topicBar"></div>
<div class="topic-now" id="topicNow"></div>"""

new_topic_html = """<!-- ===== Tägliches Thema ===== -->
<div class="theme-row" id="themeRow">
  <div class="theme-dots" id="themeDots"></div>
  <div class="theme-label" id="themeLabel">Heute: <strong> </strong></div>
</div>"""

html = html.replace(old_topic_html, new_topic_html)

# --- REMOVE SUPPORTER HTML from settings ---
html = re.sub(
    r'    <div class="settings-section-title">Supporter.*?    </div>\n\n',
    '',
    html,
    flags=re.DOTALL
)

# --- REMOVE SUPPORTER JS ---
html = re.sub(
    r'let isSupporter = .*?\nlet supporterEmailSaved = .*?\n',
    '',
    html
)
html = re.sub(
    r'// Supporter status\n.*?supporterDone\.style\.display = \'block\';\n',
    '',
    html
)
html = re.sub(
    r'/\* ===== SUPPORTER SIGNUP =====.*?1500\);\n}\);\n\n',
    '',
    html,
    flags=re.DOTALL
)

# --- REPLACE TOPIC BAR JS ---
old_topic_js = """/* ===== WOCHENPLAN / TOPIC-BANNER ===== */
// Map: Monday=0..Sunday=6 → schedule day 1..6,0
const DAY_MAP = {0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:0};
const DAY_NAMES = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'];

// Fallback schedule eingebettet (wird online durch schedule.json ersetzt)
let scheduleData = [
  {day:1, label:'Mo', name:'KI & Agenten', emoji:'🧠', color:'#FF2D55', desc:'Moltbook, KI-Papers, Agent-News'},
  {day:2, label:'Di', name:'Open Source & Coding', emoji:'🔧', color:'#007AFF', desc:'GitHub, Selfhosting, Linux'},
  {day:3, label:'Mi', name:'Tech-News 🇩🇪', emoji:'📰', color:'#34C759', desc:'heise, golem, Datenschutz'},
  {day:4, label:'Do', name:'Nerd-Wissen', emoji:'🤓', color:'#FF9500', desc:'Wikipedia, Comics, Obsidian'},
  {day:5, label:'Fr', name:'Agent-Ecosystem', emoji:'🦞', color:'#5856D6', desc:'OpenClaw, Moltbook Deep Dive'},
  {day:6, label:'Sa', name:'Netzwerk & Heimserver', emoji:'🏠', color:'#00C7BE', desc:'FRITZ!Box, Proxmox, Pi-hole'},
  {day:0, label:'So', name:'Rückblick & Ausblick', emoji:'📅', color:'#FF3B30', desc:'Wochen-Resumée, Vorschau'}
];

function initTopicBar(schedule) {
  const bar = document.getElementById('topicBar');
  const now = document.getElementById('topicNow');
  const today = new Date().getDay(); // 0=Sun, 1=Mon...
  const todaySched = DAY_MAP[today];
  
  // Pills bauen (Mo-So)
  bar.innerHTML = schedule.map(d => {
    const isToday = d.day === todaySched;
    const classes = isToday ? 'topic-pill today' : 'topic-pill inactive';
    return `<div class="${classes}" style="${isToday ? 'background:'+d.color : ''}" data-day="${d.day}">
      <span class="day-label">${d.label}</span>
      <span class="day-name">${d.emoji} ${d.name}</span>
    </div>`;
  }).join('');
  
  // Heute-Text
  const todayEntry = schedule.find(d => d.day === todaySched);
  if (todayEntry) {
    now.innerHTML = `<span class="theme-dot" style="background:${todayEntry.color}"></span>
      <span class="emoji">${todayEntry.emoji}</span>
      <span class="theme-name">${todayEntry.name}</span>
      <span class="theme-desc">· ${todayEntry.desc}</span>`;
    now.style.display = 'flex';
  }
}

// schedule.json laden, fallback auf eingebettete Daten
fetch('/schedule.json')
  .then(r => r.json())
  .then(d => { scheduleData = d.schedule; initTopicBar(scheduleData); })
  .catch(() => initTopicBar(scheduleData));
"""

new_topic_js = """/* ===== Tägliches Thema (minimal) ===== */
const DAY_LABELS = ['So','Mo','Di','Mi','Do','Fr','Sa'];
const DAY_SCHED = {0:'Rückblick',1:'KI & Agenten',2:'Open Source & Coding',3:'Tech-News',4:'Nerd-Wissen',5:'Agent-Ecosystem',6:'Netzwerk & Heimserver'};
const DAY_COLORS = {0:'#FF3B30',1:'#FF2D55',2:'#007AFF',3:'#34C759',4:'#FF9500',5:'#5856D6',6:'#00C7BE'};

function initTheme() {
  const dots = document.getElementById('themeDots');
  const label = document.getElementById('themeLabel');
  const today = new Date().getDay();

  dots.innerHTML = DAY_LABELS.map((d, i) => {
    const isToday = i === today;
    const color = isToday ? DAY_COLORS[i] : 'var(--date-color)';
    return `<span class="theme-dot${isToday ? ' today' : ''}" style="background:${color}" title="${d}"></span>`;
  }).join('');

  label.innerHTML = `Heute: <strong>${DAY_SCHED[today]}</strong>`;
}

// Try loading schedule.json (adds color+description), else use defaults
fetch('/schedule.json').then(r => r.json()).then(d => {
  d.schedule.forEach(s => { DAY_SCHED[s.day] = s.name; DAY_COLORS[s.day] = s.color; });
  initTheme();
}).catch(() => initTheme());
"""

html = html.replace(old_topic_js, new_topic_js)

# --- Also remove supporter from DOM references ---
html = re.sub(
    r'const supporterForm = .*?\nconst supporterEmail = .*?\nconst supporterBtn = .*?\nconst supporterMsg = .*?\nconst supporterDone = .*?\n',
    '',
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html rewritten – minimal topic dots + no supporter")