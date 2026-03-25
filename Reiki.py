# ═══════════════════════════════════════════════════════════════════════════════
#  🌟 REIKI STUDIO — Complete Healing Arts Application  (v2 — all bugs fixed)
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json, os, io, wave as wav_lib, math
import streamlit.components.v1 as components

# ── CONFIG ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Reiki Studio", page_icon="☯", layout="wide",
                   initial_sidebar_state="expanded")

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Raleway', sans-serif; }
.stApp { background: linear-gradient(135deg,#0d0d1a 0%,#12102a 50%,#0d1a1a 100%); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0a0a1f 0%,#0d1a2a 100%) !important;
    border-right: 1px solid rgba(167,139,250,0.15) !important;
}
section[data-testid="stSidebar"] * { color: #c4b5fd !important; }
section[data-testid="stSidebar"] .stRadio label { font-size:14px !important; padding:4px 0; }

.reiki-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 12px; padding: 20px; margin: 8px 0;
}
.reiki-card h3 { font-family:'Cinzel',serif; color:#e9d5ff; margin-bottom:12px; font-size:16px; }

.metric-row { display:flex; gap:12px; flex-wrap:wrap; margin:12px 0; }
.metric-box {
    flex:1; min-width:120px; background:rgba(139,92,246,0.1);
    border:1px solid rgba(139,92,246,0.25); border-radius:10px; padding:16px 12px; text-align:center;
}
.metric-box .m-val { font-size:28px; font-weight:700; color:#a78bfa; }
.metric-box .m-lab { font-size:11px; color:#7c6f9e; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }

.page-title {
    font-family:'Cinzel',serif; font-size:26px; font-weight:700;
    background:linear-gradient(135deg,#a78bfa,#34d399,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:4px;
}
.page-sub { color:#6b7280; font-size:14px; margin-bottom:24px; }

.stButton > button {
    background:linear-gradient(135deg,rgba(139,92,246,0.3),rgba(59,130,246,0.3)) !important;
    border:1px solid rgba(139,92,246,0.4) !important; color:#e9d5ff !important;
    border-radius:8px !important; font-family:'Raleway',sans-serif !important; font-weight:600 !important;
}
.stButton > button:hover {
    background:linear-gradient(135deg,rgba(139,92,246,0.5),rgba(59,130,246,0.5)) !important;
}
.stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
    background:rgba(255,255,255,0.05) !important; border:1px solid rgba(139,92,246,0.3) !important;
    color:#e9d5ff !important; border-radius:8px !important;
}
.stTabs [data-baseweb="tab-list"] { background:rgba(255,255,255,0.03) !important; border-radius:8px; }
.stTabs [data-baseweb="tab"] { color:#9ca3af !important; }
.stTabs [aria-selected="true"] { color:#a78bfa !important; }
.divider { border-top:1px solid rgba(139,92,246,0.15); margin:16px 0; }
</style>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────────────────────────
CHAKRAS = {
    "Root":{"num":1,"sanskrit":"Muladhara","color":"#ef4444","bg":"rgba(239,68,68,0.12)",
            "element":"Earth","frequency":396,"note":"C",
            "affirmations":["I am safe and secure","I am grounded in the present","I have everything I need","My body is my home"],
            "ailments":["Lower back pain","Anxiety & fear","Financial stress","Chronic fatigue","Immune issues"],
            "crystals":["Red Jasper","Black Tourmaline","Obsidian","Garnet","Smoky Quartz"],
            "hand_position":"Place both hands on the lower abdomen, fingers pointing downward toward the earth",
            "description":"The foundation of our energy system, Muladhara governs survival instincts, security, and our physical connection to the earth.",
            "body_pct":86,"emoji":"🔴",
            "foods":["Red apples","Beets","Tomatoes","Root vegetables","Protein-rich foods"],
            "yoga":["Mountain Pose (Tadasana)","Warrior I","Child's Pose (Balasana)","Squat (Malasana)"],
            "imbalanced_signs":"Feeling fearful, anxious, or disconnected from your body"},
    "Sacral":{"num":2,"sanskrit":"Svadhisthana","color":"#f97316","bg":"rgba(249,115,22,0.12)",
              "element":"Water","frequency":417,"note":"D",
              "affirmations":["I embrace pleasure and joy","I am creative and inspired","I flow with life","My emotions are valid"],
              "ailments":["Hip tension","Lower back pain","Creative blocks","Relationship issues","Sexual dysfunction"],
              "crystals":["Carnelian","Orange Calcite","Moonstone","Sunstone","Peach Selenite"],
              "hand_position":"Hands on the lower abdomen, about 2 inches below the navel, palms facing inward",
              "description":"The center of creativity, pleasure, and emotional intelligence. Svadhisthana rules our relationships, passions, and joy.",
              "body_pct":74,"emoji":"🟠",
              "foods":["Oranges","Mangoes","Coconut","Almonds","Sweet potatoes"],
              "yoga":["Pigeon Pose","Goddess Pose","Bound Angle (Baddha Konasana)","Hip Circles"],
              "imbalanced_signs":"Emotional instability, creative blocks, or feeling numb to pleasure"},
    "Solar Plexus":{"num":3,"sanskrit":"Manipura","color":"#eab308","bg":"rgba(234,179,8,0.12)",
                    "element":"Fire","frequency":528,"note":"E",
                    "affirmations":["I am confident and powerful","I trust my decisions","I am worthy of my dreams","I stand in my truth"],
                    "ailments":["Digestive issues","Low self-esteem","Control issues","Procrastination","Anger problems"],
                    "crystals":["Citrine","Yellow Calcite","Tiger's Eye","Amber","Golden Topaz"],
                    "hand_position":"Hands on the upper abdomen, just above the navel, channeling warmth into the solar plexus",
                    "description":"The seat of personal power, self-confidence, and willpower. Manipura governs how we assert ourselves in the world.",
                    "body_pct":61,"emoji":"🟡",
                    "foods":["Bananas","Corn","Pineapple","Ginger","Turmeric"],
                    "yoga":["Boat Pose (Navasana)","Plank","Sun Salutation","Warrior III"],
                    "imbalanced_signs":"Feeling powerless, overly controlling, or lacking self-confidence"},
    "Heart":{"num":4,"sanskrit":"Anahata","color":"#22c55e","bg":"rgba(34,197,94,0.12)",
             "element":"Air","frequency":639,"note":"F",
             "affirmations":["I am love and I radiate love","I forgive myself and others","My heart is open","I give and receive freely"],
             "ailments":["Heart conditions","Loneliness and grief","Trust issues","Co-dependency","Immune disorders"],
             "crystals":["Rose Quartz","Green Aventurine","Malachite","Emerald","Rhodonite"],
             "hand_position":"One or both hands over the heart center, feeling warmth radiate outward",
             "description":"The bridge between earth and spirit, Anahata is the center of love, compassion, and connection.",
             "body_pct":49,"emoji":"💚",
             "foods":["Leafy greens","Broccoli","Green tea","Kiwi","Avocado"],
             "yoga":["Camel Pose","Bridge Pose","Cobra (Bhujangasana)","Wild Thing"],
             "imbalanced_signs":"Difficulty with intimacy, holding onto grief, or feeling closed off"},
    "Throat":{"num":5,"sanskrit":"Vishuddha","color":"#3b82f6","bg":"rgba(59,130,246,0.12)",
              "element":"Ether/Sound","frequency":741,"note":"G",
              "affirmations":["I speak my truth with clarity","I am heard and understood","My voice matters","I express myself authentically"],
              "ailments":["Throat infections","Communication difficulties","Shyness","Neck tension","Thyroid issues"],
              "crystals":["Lapis Lazuli","Aquamarine","Blue Lace Agate","Sodalite","Celestite"],
              "hand_position":"Hands lightly on the throat, or held just in front of the neck without touching",
              "description":"The center of authentic self-expression, communication, and truth. Vishuddha governs how we express our inner world.",
              "body_pct":36,"emoji":"🔵",
              "foods":["Blueberries","Figs","Blackberries","Herbal teas","Sea vegetables"],
              "yoga":["Fish Pose (Matsyasana)","Shoulder Stand","Lion's Breath","Neck rolls"],
              "imbalanced_signs":"Fear of speaking up, talking too much, or inability to listen"},
    "Third Eye":{"num":6,"sanskrit":"Ajna","color":"#8b5cf6","bg":"rgba(139,92,246,0.12)",
                 "element":"Light","frequency":852,"note":"A",
                 "affirmations":["I trust my intuition","I see beyond the obvious","I am connected to inner wisdom","My mind is clear"],
                 "ailments":["Headaches","Confusion & poor focus","Nightmares","Lack of intuition","Eye strain"],
                 "crystals":["Amethyst","Labradorite","Purple Fluorite","Azurite","Iolite"],
                 "hand_position":"Fingertips at the center of the forehead, slightly above and between the eyebrows",
                 "description":"The seat of intuition, imagination, and spiritual perception. Ajna allows us to see beyond the physical.",
                 "body_pct":22,"emoji":"🔮",
                 "foods":["Eggplant","Purple cabbage","Dark chocolate","Goji berries","Walnuts"],
                 "yoga":["Child's Pose","Dolphin Pose","Eagle Pose","Forward folds"],
                 "imbalanced_signs":"Overthinking, lack of focus, ignoring intuitive signals"},
    "Crown":{"num":7,"sanskrit":"Sahasrara","color":"#a855f7","bg":"rgba(168,85,247,0.12)",
             "element":"Consciousness","frequency":963,"note":"B",
             "affirmations":["I am connected to all that is","I am divinely guided","I trust the universe","I am one with pure consciousness"],
             "ailments":["Depression","Spiritual disconnection","Closed-mindedness","Existential confusion","Isolation"],
             "crystals":["Clear Quartz","Selenite","Lepidolite","Sugilite","Howlite"],
             "hand_position":"Hands hovering just above the crown of the head, not touching, channeling divine energy",
             "description":"Our connection to universal consciousness and spiritual enlightenment. Sahasrara transcends the individual self.",
             "body_pct":8,"emoji":"✨",
             "foods":["Fasting","Light fruit","Herbal teas","Sun-energized water","Raw foods"],
             "yoga":["Headstand (Sirsasana)","Savasana","Lotus Pose","Meditation"],
             "imbalanced_signs":"Feeling spiritually cut off, overly materialistic, or nihilistic"},
}

HAND_POSITIONS = [
    {"position":1, "name":"Crown",              "chakra":"Crown",       "duration":5,
     "instruction":"Place hands lightly above or on top of the head. Intention: divine connection, clarity."},
    {"position":2, "name":"Eyes / Forehead",    "chakra":"Third Eye",   "duration":5,
     "instruction":"Hands over the eyes and forehead. Intention: intuition, mental clarity, releasing worry."},
    {"position":3, "name":"Temples",            "chakra":"Third Eye",   "duration":5,
     "instruction":"Cup hands over the temples. Intention: calming the mind, releasing tension."},
    {"position":4, "name":"Back of Head",       "chakra":"Third Eye",   "duration":5,
     "instruction":"One hand on forehead, one on back of skull. Intention: integrating the nervous system."},
    {"position":5, "name":"Throat",             "chakra":"Throat",      "duration":5,
     "instruction":"Hands gently on or hovering at the throat. Intention: authentic expression, clear communication."},
    {"position":6, "name":"Heart",              "chakra":"Heart",       "duration":5,
     "instruction":"Both hands over the heart center. Intention: love, compassion, emotional healing."},
    {"position":7, "name":"Solar Plexus",       "chakra":"Solar Plexus","duration":5,
     "instruction":"Hands on upper abdomen. Intention: confidence, personal power, releasing fear."},
    {"position":8, "name":"Navel / Sacral",     "chakra":"Sacral",      "duration":5,
     "instruction":"Hands below the navel. Intention: creativity, emotional balance, vitality."},
    {"position":9, "name":"Hip Flexors",        "chakra":"Root",        "duration":5,
     "instruction":"Hands on hip crease / lower pelvis. Intention: grounding, safety, stability."},
    {"position":10,"name":"Knees",              "chakra":"Root",        "duration":5,
     "instruction":"Cup hands over the knees. Intention: flexibility, forward movement, letting go."},
    {"position":11,"name":"Feet",               "chakra":"Root",        "duration":5,
     "instruction":"Hold the feet or place hands over them. Intention: deep grounding, earth connection."},
    {"position":12,"name":"Closing Integration","chakra":"Heart",       "duration":3,
     "instruction":"Hands in prayer at heart. Breathe deeply. Give thanks. Seal the session with love and light."},
]

SYMBOLS = {
    "Cho Ku Rei":{"meaning":"Power Symbol — Place the Power of the Universe Here",
        "uses":["Amplifies Reiki energy","Cleanses a space","Seals a healing session","Protects auras and spaces"],
        "level":"Level II","color":"#f97316",
        "svg_path":"""<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <line x1="60" y1="10" x2="60" y2="70" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
            <line x1="60" y1="25" x2="85" y2="25" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
            <path d="M60,40 Q95,40 95,60 Q95,80 60,80 Q25,80 25,60 Q25,45 45,42" fill="none" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
            <path d="M45,42 Q58,40 60,55" fill="none" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
        </svg>""",
        "how_to_draw":["Start at the top center","Draw a vertical line downward","Create a horizontal line to the right","Coil counter-clockwise around the center line (3 times)","End at the center"],
        "affirmation":"I call upon the power of the universe to amplify and focus healing energy here and now."},
    "Sei He Ki":{"meaning":"Mental/Emotional Symbol — God and Humanity Coming Together",
        "uses":["Emotional healing","Mental clarity","Releasing trauma","Addictions & habits","Relationship healing"],
        "level":"Level II","color":"#a78bfa",
        "svg_path":"""<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <path d="M20,30 Q40,15 60,30 Q80,45 100,30" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
            <path d="M20,50 Q40,35 60,50 Q80,65 100,50" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
            <path d="M20,70 Q40,55 60,70 Q80,85 100,70" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
            <path d="M60,30 L60,95" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-dasharray="4,3"/>
        </svg>""",
        "how_to_draw":["Draw a curved wave from top-left to right","Continue downward with a serpentine motion","Add a mirrored wave below","Unite at the base"],
        "affirmation":"Mind, body, and spirit align in perfect harmony. All emotional patterns are healed and released."},
    "Hon Sha Ze Sho Nen":{"meaning":"Distance Symbol — The Buddha in Me Contacts the Buddha in You",
        "uses":["Sending Reiki across distance & time","Healing past traumas","Future intention setting","Connecting with distant clients"],
        "level":"Level II","color":"#34d399",
        "svg_path":"""<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <rect x="35" y="10" width="50" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <rect x="40" y="28" width="40" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <rect x="45" y="46" width="30" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <rect x="50" y="64" width="20" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <polygon points="60,82 40,105 80,105" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linejoin="round"/>
            <line x1="60" y1="10" x2="60" y2="82" stroke="#34d399" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.5"/>
        </svg>""",
        "how_to_draw":["Draw three horizontal bars (top)","A pagoda-like tower of stacked shapes","A vertical center line connecting all","Base triangle at the bottom"],
        "affirmation":"Time and space are no barrier to love. I send healing light across all dimensions to reach you now."},
    "Dai Ko Myo":{"meaning":"Master Symbol — Great Shining Light",
        "uses":["Spiritual enlightenment","Soul healing","Attunements","Master-level work","Healing the source of illness"],
        "level":"Master Level","color":"#fbbf24",
        "svg_path":"""<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <circle cx="60" cy="62" r="38" fill="none" stroke="#fbbf24" stroke-width="2.5"/>
            <line x1="60" y1="10" x2="60" y2="24" stroke="#fbbf24" stroke-width="3" stroke-linecap="round"/>
            <line x1="60" y1="10" x2="50" y2="22" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
            <line x1="60" y1="10" x2="70" y2="22" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
            <line x1="45" y1="62" x2="75" y2="62" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
            <line x1="60" y1="47" x2="60" y2="77" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="60" cy="62" r="8" fill="none" stroke="#fbbf24" stroke-width="2"/>
            <circle cx="60" cy="62" r="3" fill="#fbbf24" opacity="0.7"/>
        </svg>""",
        "how_to_draw":["Draw a large circle (wholeness)","Three radiating lines upward (light)","A cross in the center (integration)","Surrounding lotus petals"],
        "affirmation":"I am a clear and perfect channel for the great shining light of universal healing energy."},
}

PRECEPTS = [
    "Just for today, I will not anger.",
    "Just for today, I will not worry.",
    "Just for today, I will be grateful.",
    "Just for today, I will do my work honestly.",
    "Just for today, I will be kind to every living thing.",
]

REIKI_LEVELS = {
    "Level I — Shoden":  {"desc":"First Degree. Physical healing, self-treatment, direct hands-on practice.","color":"#22c55e"},
    "Level II — Okuden": {"desc":"Second Degree. Distance healing, symbols, mental/emotional work.","color":"#3b82f6"},
    "Master — Shinpiden":{"desc":"Master/Teacher level. Attunements, Master symbol, teaching others.","color":"#a855f7"},
}
LEVEL_SYMBOLS = {
    "Level I — Shoden":  [],
    "Level II — Okuden": ["Cho Ku Rei","Sei He Ki","Hon Sha Ze Sho Nen"],
    "Master — Shinpiden":["Cho Ku Rei","Sei He Ki","Hon Sha Ze Sho Nen","Dai Ko Myo"],
}

# ── PERSISTENCE ─────────────────────────────────────────────────────────────────
DATA_DIR = "reiki_data"
os.makedirs(DATA_DIR, exist_ok=True)

def _path(fn): return os.path.join(DATA_DIR, fn)
def load_json(fn, default):
    p = _path(fn)
    if os.path.exists(p):
        try:
            with open(p) as f: return json.load(f)
        except: pass
    return default
def save_json(fn, data):
    with open(_path(fn), "w") as f: json.dump(data, f, indent=2, default=str)

# ── SESSION STATE ───────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "clients":         load_json("clients.json",  []),
        "energy_entries":  load_json("energy_diary.json", []),
        "journal_entries": load_json("chakra_journal.json", []),
        "attunement":      load_json("attunement.json",
                                     {"level":"Level I — Shoden","hours":0,
                                      "practice_log":[],"symbols_learned":[],"milestones":[]}),
        "sessions":        load_json("sessions.json", []),
        "med_script":      "",           # FIX: persist meditation script across rerenders
        "med_script_color":"#a78bfa",
        "timer_pos":       1,            # FIX: timer position controlled by session state
        "enc_sel":         "Heart",      # encyclopedia selection
        "dh_active":       False,        # distance healing
        "dh_recipient":    "",
        "dh_intent":       "",
        "dh_duration":     15,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# ── HELPERS ─────────────────────────────────────────────────────────────────────
def page_header(title, subtitle=""):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-sub">{subtitle}</div>', unsafe_allow_html=True)

def body_svg(highlighted=None, size=320):
    keys = list(CHAKRAS.keys())
    vals = list(CHAKRAS.values())
    dots = []
    for i, c in enumerate(vals):
        name = keys[i]
        cy   = int(c["body_pct"] / 100 * 400)
        hl   = (highlighted == name)
        alpha = 1.0 if (highlighted is None or hl) else 0.2
        r     = 14 if hl else 10
        gstyle = 'style="filter:url(#glow)"' if hl else ""
        dots.append(f'<circle cx="80" cy="{cy}" r="{r}" fill="{c["color"]}" opacity="{alpha}" {gstyle}/>')
        dots.append(f'<text x="100" y="{cy+4}" font-size="11" fill="{c["color"]}" opacity="{alpha}" font-family="Raleway">{name}</text>')
    return f"""<svg viewBox="0 0 160 400" width="{size//2}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <defs><filter id="glow"><feGaussianBlur stdDeviation="4" result="cb"/>
  <feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <ellipse cx="80" cy="32" rx="22" ry="28" fill="none" stroke="rgba(167,139,250,0.35)" stroke-width="2"/>
  <rect x="70" y="58" width="20" height="18" rx="3" fill="none" stroke="rgba(167,139,250,0.35)" stroke-width="2"/>
  <path d="M35,76 Q30,120 28,180 Q26,230 30,280 L55,280 L55,380 L75,380 L75,280 L85,280 L85,380 L105,380 L105,280 L130,280 Q134,230 132,180 Q130,120 125,76 Z"
        fill="none" stroke="rgba(167,139,250,0.35)" stroke-width="2"/>
  <path d="M35,80 Q10,130 12,200" fill="none" stroke="rgba(167,139,250,0.25)" stroke-width="2"/>
  <path d="M125,80 Q150,130 148,200" fill="none" stroke="rgba(167,139,250,0.25)" stroke-width="2"/>
  <line x1="80" y1="8" x2="80" y2="380" stroke="rgba(167,139,250,0.15)" stroke-width="1" stroke-dasharray="4,4"/>
  {"".join(dots)}
</svg>"""

def make_wav(freq, duration, sr=44100, pure=False):
    t = np.linspace(0, duration, int(sr * duration), False)
    if pure:
        audio = np.sin(2 * np.pi * freq * t) * 0.7
    else:
        audio = (0.50*np.sin(2*np.pi*freq*t) + 0.20*np.sin(2*np.pi*freq*2*t)
               + 0.15*np.sin(2*np.pi*freq*0.5*t) + 0.10*np.sin(2*np.pi*freq*3*t)
               + 0.05*np.sin(2*np.pi*freq*4*t))
    audio /= max(np.max(np.abs(audio)), 1e-6) * 1.4
    fade = min(int(sr * 1.5), len(audio) // 4)
    audio[:fade]  *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)
    buf = io.BytesIO()
    with wav_lib.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    buf.seek(0)
    return buf.read()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — SESSION TIMER
# ══════════════════════════════════════════════════════════════════════════════
def page_session_timer():
    page_header("⏱️ Session Timer & Guide", "Follow the hand position sequence with guided timers")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        session_type = st.selectbox("Session Type",
            ["Self-Treatment (Full 12 Positions)","Short Session (Chakra Focus)","Client Session"])
        if session_type == "Short Session (Chakra Focus)":
            focus_chk = st.selectbox("Focus Chakra", list(CHAKRAS.keys()))
            positions = [p for p in HAND_POSITIONS if p["chakra"] == focus_chk] or HAND_POSITIONS
        else:
            positions = HAND_POSITIONS
        duration_per = st.slider("Minutes per position", 1, 15, 5)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        if st.button("📝 Save Session", use_container_width=True):
            st.session_state.sessions.append({
                "date": str(date.today()), "type": session_type,
                "positions": len(positions), "duration": len(positions)*duration_per, "notes": ""})
            save_json("sessions.json", st.session_state.sessions)
            st.success(f"Saved! {len(positions)} × {duration_per} min")
        tot_s = len(st.session_state.sessions)
        tot_m = sum(s.get("duration",0) for s in st.session_state.sessions)
        st.markdown(f"""<div class="metric-row">
            <div class="metric-box"><div class="m-val">{tot_s}</div><div class="m-lab">Sessions</div></div>
            <div class="metric-box"><div class="m-val">{tot_m}</div><div class="m-lab">Total Min</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        n = len(positions)
        # FIX: clamp position to valid range
        if st.session_state.timer_pos < 1: st.session_state.timer_pos = 1
        if st.session_state.timer_pos > n: st.session_state.timer_pos = n

        # FIX: Prev/Next update session state then rerun — no broken number_input dependency
        nb1, nb2, nb3 = st.columns([1,2,1])
        with nb1:
            if st.session_state.timer_pos > 1:
                if st.button("← Prev", use_container_width=True):
                    st.session_state.timer_pos -= 1
                    st.rerun()
        with nb2:
            st.markdown(f"<div style='text-align:center;color:#a78bfa;padding:8px 0;font-size:13px;'>"
                        f"Position {st.session_state.timer_pos} of {n}</div>", unsafe_allow_html=True)
        with nb3:
            if st.session_state.timer_pos < n:
                if st.button("Next →", use_container_width=True):
                    st.session_state.timer_pos += 1
                    st.rerun()

        jump = st.selectbox("Jump to", range(1, n+1),
                            index=st.session_state.timer_pos - 1,
                            format_func=lambda x: f"#{x} — {positions[x-1]['name']}")
        if jump != st.session_state.timer_pos:
            st.session_state.timer_pos = jump
            st.rerun()

        pos = positions[st.session_state.timer_pos - 1]
        chk = CHAKRAS.get(pos["chakra"], CHAKRAS["Heart"])
        col = chk["color"]
        sec = duration_per * 60

        components.html(f"""
        <div style="font-family:'Raleway',sans-serif;text-align:center;padding:20px;
                    background:rgba(255,255,255,0.03);border-radius:16px;
                    border:1px solid rgba(167,139,250,0.2);">
          <div style="font-size:22px;font-weight:700;color:{col};margin-bottom:4px;">{pos['name']}</div>
          <div style="font-size:13px;color:#9ca3af;margin-bottom:16px;">
            {pos['chakra']} &nbsp;·&nbsp; {chk['emoji']}</div>
          <div id="tmr" style="font-size:80px;font-weight:300;color:white;letter-spacing:-2px;
               line-height:1;text-shadow:0 0 30px {col}55;">{duration_per:02d}:00</div>
          <div style="width:80%;margin:10px auto;height:4px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;">
            <div id="prg" style="height:100%;width:0%;background:{col};border-radius:2px;transition:width 1s linear;"></div>
          </div>
          <div style="display:flex;gap:10px;justify-content:center;margin:18px 0;">
            <button id="sb" onclick="startT()"
              style="padding:12px 28px;background:{col}33;border:1px solid {col}88;color:{col};
                     border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;">▶ START</button>
            <button onclick="pauseT()"
              style="padding:12px 20px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);
                     color:#9ca3af;border-radius:8px;font-size:14px;cursor:pointer;">⏸ PAUSE</button>
            <button onclick="resetT()"
              style="padding:12px 20px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);
                     color:#9ca3af;border-radius:8px;font-size:14px;cursor:pointer;">↺ RESET</button>
          </div>
          <div id="st" style="font-size:13px;color:#6b7280;min-height:20px;"></div>
          <div style="margin-top:16px;padding:14px;background:rgba(255,255,255,0.03);
                      border-radius:10px;border-left:3px solid {col};text-align:left;">
            <div style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Instruction</div>
            <div style="font-size:14px;color:#d1d5db;line-height:1.6;">{pos['instruction']}</div>
          </div>
        </div>
        <script>
        let tot={sec},rem={sec},iv=null,run=false;
        const p=n=>n.toString().padStart(2,'0');
        function startT(){{if(run)return;run=true;document.getElementById('sb').style.opacity='0.4';
          document.getElementById('st').textContent='✦ Session in progress...';
          iv=setInterval(()=>{{rem--;document.getElementById('tmr').textContent=p(Math.floor(rem/60))+':'+p(rem%60);
          document.getElementById('prg').style.width=((tot-rem)/tot*100).toFixed(1)+'%';
          if(rem<=0){{clearInterval(iv);run=false;document.getElementById('st').innerHTML='✅ Complete! Move to next.';
          document.getElementById('sb').style.opacity='1';playBell();}}}},1000);}}
        function pauseT(){{if(iv){{clearInterval(iv);iv=null;run=false;}}
          document.getElementById('sb').style.opacity='1';document.getElementById('st').textContent='⏸ Paused';}}
        function resetT(){{clearInterval(iv);iv=null;run=false;rem=tot;
          document.getElementById('tmr').textContent=p(Math.floor(tot/60))+':'+p(tot%60);
          document.getElementById('tmr').style.textShadow='0 0 30px {col}55';
          document.getElementById('prg').style.width='0%';document.getElementById('st').textContent='';
          document.getElementById('sb').style.opacity='1';}}
        function playBell(){{try{{const c=new(window.AudioContext||window.webkitAudioContext)();
          [0,.35,.7].forEach(d=>{{const o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);
          o.frequency.value={chk['frequency']};o.type='sine';g.gain.setValueAtTime(.4,c.currentTime+d);
          g.gain.exponentialRampToValueAtTime(.001,c.currentTime+d+2.5);o.start(c.currentTime+d);o.stop(c.currentTime+d+2.5);}}}});}}catch(e){{}}}}
        </script>""", height=480)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — CHAKRA ASSESSMENT JOURNAL
# ══════════════════════════════════════════════════════════════════════════════
def page_chakra_journal():
    page_header("📔 Chakra Assessment Journal", "Track your energy body over time")
    tab1, tab2, tab3 = st.tabs(["🖊️ New Entry","📊 History & Trends","🗂️ All Entries"])

    with tab1:
        c1, c2 = st.columns([1,2])
        with c1:
            sel = st.selectbox("Select chakra to assess", list(CHAKRAS.keys()))
            st.markdown(body_svg(sel), unsafe_allow_html=True)
        with c2:
            chk = CHAKRAS[sel]
            st.markdown(f"""<div class="reiki-card" style="border-color:{chk['color']}44;">
                <h3 style="color:{chk['color']};">{chk['emoji']} {sel} — {chk['sanskrit']}</h3>
                <p style="color:#9ca3af;font-size:13px;line-height:1.6;">{chk['description']}</p>
            </div>""", unsafe_allow_html=True)
            energy  = st.slider("Energy Level",     0, 10, 5)
            balance = st.slider("Perceived Balance", 0, 10, 5)
            senses  = st.multiselect("Physical Sensations",
                ["Tingling","Warmth","Coolness","Pulsing","Numbness","Tightness","Openness","Pressure","Vibration","Nothing"])
            notes   = st.text_area("Session notes", height=90, placeholder="What did you feel?")
            if st.button("💾 Save Journal Entry", use_container_width=True):
                st.session_state.journal_entries.append({
                    "date":str(date.today()),"chakra":sel,"energy":energy,"balance":balance,
                    "sensations":senses,"notes":notes,"timestamp":datetime.now().isoformat()})
                save_json("chakra_journal.json", st.session_state.journal_entries)
                st.success(f"✅ {sel} chakra saved for {date.today()}")

    # FIX: use if/else inside tab2, never `return` (would skip tab3)
    with tab2:
        entries = st.session_state.journal_entries
        if not entries:
            st.info("📝 No journal entries yet. Start logging in the New Entry tab!")
        else:
            df = pd.DataFrame(entries)
            df["date"] = pd.to_datetime(df["date"])
            fig = go.Figure()
            for name, data in CHAKRAS.items():
                cdf = df[df["chakra"]==name].sort_values("date")
                if len(cdf):
                    fig.add_trace(go.Scatter(x=cdf["date"], y=cdf["balance"], name=name,
                        mode="lines+markers", line=dict(color=data["color"], width=2), marker=dict(size=6)))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9ca3af", title="Balance Score Over Time",
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0,10]))
            st.plotly_chart(fig, use_container_width=True)
            latest = df.sort_values("date").groupby("chakra").last().reset_index()
            if len(latest) >= 3:
                fig2 = go.Figure(go.Scatterpolar(
                    r=latest["balance"].tolist()+[latest["balance"].iloc[0]],
                    theta=latest["chakra"].tolist()+[latest["chakra"].iloc[0]],
                    fill="toself", fillcolor="rgba(139,92,246,0.15)",
                    line=dict(color="#a78bfa",width=2)))
                fig2.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(range=[0,10],gridcolor="rgba(255,255,255,0.08)",color="#6b7280"),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.08)",color="#9ca3af")),
                    paper_bgcolor="rgba(0,0,0,0)", showlegend=False, title="Chakra Balance Radar")
                st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        entries = st.session_state.journal_entries
        if not entries:
            st.info("No entries yet.")
        else:
            for e in reversed(entries[-20:]):
                ch  = CHAKRAS.get(e["chakra"],{})
                col = ch.get("color","#a78bfa")
                st.markdown(f"""<div class="reiki-card" style="border-left:3px solid {col};">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                        <span style="color:{col};font-weight:600;">{ch.get('emoji','')} {e['chakra']}</span>
                        <span style="color:#6b7280;font-size:12px;">{e['date']}</span>
                    </div>
                    <div style="display:flex;gap:24px;margin-bottom:6px;">
                        <span style="color:#9ca3af;font-size:13px;">Energy: <b style="color:{col};">{e.get('energy','?')}/10</b></span>
                        <span style="color:#9ca3af;font-size:13px;">Balance: <b style="color:{col};">{e.get('balance','?')}/10</b></span>
                    </div>
                    <div style="color:#6b7280;font-size:12px;">Sensations: {', '.join(e.get('sensations',[])) or '—'}</div>
                    {f'<div style="color:#9ca3af;font-size:13px;margin-top:6px;font-style:italic;">{e["notes"]}</div>' if e.get("notes") else ""}
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — ATTUNEMENT TRACKER
# ══════════════════════════════════════════════════════════════════════════════
def page_attunement_tracker():
    page_header("🎯 Attunement Tracker", "Track your Reiki journey through all levels")
    att = st.session_state.attunement
    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        new_level = st.selectbox("Reiki Level", list(REIKI_LEVELS.keys()),
                                 index=list(REIKI_LEVELS.keys()).index(att.get("level","Level I — Shoden")))
        if new_level != att.get("level"):
            att["level"] = new_level; save_json("attunement.json", att)
        ld = REIKI_LEVELS[new_level]
        st.markdown(f"""<div style="padding:10px;background:{ld['color']}18;border-radius:8px;
                            border:1px solid {ld['color']}44;margin:8px 0;">
            <div style="color:{ld['color']};font-weight:600;">{new_level}</div>
            <div style="color:#9ca3af;font-size:13px;margin-top:4px;">{ld['desc']}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("### Log Practice Hours")
        with st.form("log_hrs"):
            add_hrs  = st.number_input("Hours", min_value=0.0, step=0.5, value=0.0)
            note_txt = st.text_input("Note (optional)")
            if st.form_submit_button("➕ Log"):
                att["hours"] = att.get("hours",0) + add_hrs
                att.setdefault("practice_log",[]).append(
                    {"date":str(date.today()),"hours":add_hrs,"note":note_txt})
                save_json("attunement.json", att)
                st.success(f"Logged {add_hrs}h  (Total: {att['hours']:.1f}h)")
        total_h = att.get("hours",0)
        st.markdown(f"""<div class="metric-row">
            <div class="metric-box"><div class="m-val">{total_h:.1f}</div><div class="m-lab">Total Hrs</div></div>
            <div class="metric-box"><div class="m-val">{len(att.get('practice_log',[]))}</div><div class="m-lab">Entries</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        level_keys = list(REIKI_LEVELS.keys())
        cur_idx    = level_keys.index(att["level"])
        ph = "<div style='display:flex;gap:8px;margin:16px 0;'>"
        for i,(lk,ld2) in enumerate(REIKI_LEVELS.items()):
            act = i <= cur_idx
            ph += f"""<div style="flex:1;text-align:center;padding:16px 8px;
                          background:{ld2['color']+'22' if act else 'rgba(255,255,255,0.03)'};
                          border:1px solid {ld2['color'] if act else 'rgba(255,255,255,0.1)'};border-radius:8px;">
                <div style="font-size:22px;margin-bottom:6px;">{"✨" if act else "○"}</div>
                <div style="font-size:11px;font-weight:600;color:{'#fff' if act else '#4b5563'};line-height:1.4;">{lk}</div>
            </div>"""
        ph += "</div>"
        st.markdown(ph, unsafe_allow_html=True)

        to_learn = LEVEL_SYMBOLS.get(att["level"],[])
        if not to_learn:
            st.info("Level I focuses on energy channeling without symbols.")
        else:
            learned     = list(att.get("symbols_learned",[]))
            learned_new = list(learned)
            st.markdown("### Symbols for Your Level")
            for sym in to_learn:
                sd  = SYMBOLS[sym]; cs = sd["color"]
                val = st.checkbox(sym, value=(sym in learned), key=f"sym_{sym}")
                if val and sym not in learned_new: learned_new.append(sym)
                elif not val and sym in learned_new: learned_new.remove(sym)
                st.markdown(f'<div style="margin:-6px 0 8px 24px;padding:6px 10px;background:{cs}11;'
                            f'border-radius:6px;border:1px solid {cs}33;font-size:12px;color:#9ca3af;">'
                            f'{sd["meaning"]}</div>', unsafe_allow_html=True)
            # FIX: only save if actually changed
            if learned_new != learned:
                att["symbols_learned"] = learned_new
                save_json("attunement.json", att)

        if att.get("practice_log"):
            log_df = pd.DataFrame(att["practice_log"])
            log_df["date"] = pd.to_datetime(log_df["date"])
            log_df = log_df.sort_values("date")
            log_df["cumulative"] = log_df["hours"].cumsum()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=log_df["date"], y=log_df["hours"],
                name="Session", marker_color="#8b5cf6", opacity=0.7))
            fig.add_trace(go.Scatter(x=log_df["date"], y=log_df["cumulative"],
                name="Cumulative", line=dict(color="#34d399",width=2), yaxis="y2"))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9ca3af", height=240, title="Practice Log",
                yaxis2=dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)"),
                legend=dict(bgcolor="rgba(0,0,0,0)"), margin=dict(t=30))
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — CHAKRA ENCYCLOPEDIA
# ══════════════════════════════════════════════════════════════════════════════
def page_encyclopedia():
    page_header("📚 Chakra Encyclopedia", "Comprehensive reference for all 7 energy centers")
    cols = st.columns(7)
    for i,(name,data) in enumerate(CHAKRAS.items()):
        with cols[i]:
            if st.button(data["emoji"], key=f"enc_{name}", use_container_width=True, help=name):
                st.session_state["enc_sel"] = name
                st.rerun()

    sel   = st.session_state.get("enc_sel","Heart")
    chk   = CHAKRAS[sel]
    color = chk["color"]

    st.markdown(f"""<div style="padding:20px;background:{color}0d;border:1px solid {color}44;
                        border-radius:12px;margin:16px 0;">
        <div style="display:flex;align-items:center;gap:20px;">
            <div style="font-size:48px;">{chk['emoji']}</div>
            <div>
                <div style="font-size:24px;font-weight:700;color:{color};font-family:'Cinzel',serif;">{sel}</div>
                <div style="color:#9ca3af;font-size:14px;">{chk['sanskrit']} · #{chk['num']} · {chk['note']} · {chk['frequency']} Hz</div>
                <div style="color:#6b7280;font-size:13px;margin-top:4px;">Element: {chk['element']}</div>
            </div>
        </div>
        <p style="color:#d1d5db;margin-top:16px;font-size:14px;line-height:1.7;">{chk['description']}</p>
        <div style="margin-top:10px;padding:10px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid {color};">
            <span style="color:{color};font-size:12px;font-weight:600;">⚠ Imbalance: </span>
            <span style="color:#9ca3af;font-size:13px;">{chk['imbalanced_signs']}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown("**✨ Affirmations**")
        for a in chk["affirmations"]:
            st.markdown(f'<div style="color:#d1d5db;font-size:13px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.05);">&ldquo;{a}&rdquo;</div>', unsafe_allow_html=True)
    with c2:
        st.markdown("**💎 Crystals**")
        for c_item in chk["crystals"]:
            st.markdown(f"<div style='color:{color};font-size:13px;padding:4px 0;'>◆ {c_item}</div>", unsafe_allow_html=True)
        st.markdown("**🌿 Yoga**")
        for pose in chk["yoga"][:3]:
            st.markdown(f"<div style='color:#9ca3af;font-size:12px;padding:2px 0;'>• {pose}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("**⚕ Ailments**")
        for a in chk["ailments"]:
            st.markdown(f"<div style='color:#f87171;font-size:13px;padding:4px 0;'>• {a}</div>", unsafe_allow_html=True)
        st.markdown("**🙌 Hand Position**")
        st.markdown(f"<div style='color:#9ca3af;font-size:13px;font-style:italic;line-height:1.5;margin-top:4px;'>{chk['hand_position']}</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("**🍎 Foods**")
        for food in chk["foods"]:
            st.markdown(f"<div style='color:#34d399;font-size:13px;padding:4px 0;'>• {food}</div>", unsafe_allow_html=True)
        st.markdown("**🎵 Frequency**")
        st.markdown(f"<div style='font-size:32px;font-weight:700;color:{color};margin-top:4px;'>{chk['frequency']} Hz</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — SYMBOL TRAINER
# ══════════════════════════════════════════════════════════════════════════════
def page_symbol_trainer():
    page_header("✍️ Symbol Trainer","Learn and practice the sacred Reiki symbols")
    st.info("💡 Reiki symbols are traditionally taught by a Reiki Master. This trainer is for study purposes.")

    sel   = st.selectbox("Choose Symbol", list(SYMBOLS.keys()))
    sym   = SYMBOLS[sel]
    color = sym["color"]

    c1,c2 = st.columns([1,2])
    with c1:
        st.markdown(f"""<div class="reiki-card" style="border-color:{color}44;text-align:center;">
            <div style="color:{color};font-family:'Cinzel',serif;font-size:18px;font-weight:700;margin-bottom:12px;">{sel}</div>
            {sym['svg_path']}
            <div style="color:#a78bfa;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-top:8px;">{sym['level']}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="reiki-card">
            <div style="color:{color};font-weight:600;font-size:15px;margin-bottom:10px;">{sym['meaning']}</div>
            <div style="color:#9ca3af;font-size:13px;font-style:italic;padding:10px;background:rgba(255,255,255,0.03);
                        border-radius:8px;border-left:3px solid {color};margin-bottom:14px;line-height:1.7;">
                &ldquo;{sym['affirmation']}&rdquo;</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("**🔑 Uses**")
        for u in sym["uses"]:
            st.markdown(f"<div style='color:#d1d5db;font-size:13px;padding:2px 0;'>▹ {u}</div>", unsafe_allow_html=True)
        st.markdown("**✏️ How to Draw**")
        for i,step in enumerate(sym["how_to_draw"],1):
            st.markdown(f"<div style='color:#a78bfa;font-size:13px;padding:4px 0;'><span style='color:{color};font-weight:700;'>{i}.</span> {step}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎮 Practice Canvas")
    # FIX: added undo, opacity control, proper touch support
    components.html(f"""
    <div style="font-family:'Raleway',sans-serif;">
      <div style="display:flex;gap:10px;margin-bottom:10px;align-items:center;flex-wrap:wrap;">
        <label style="color:#9ca3af;font-size:12px;">Color</label>
        <input type="color" id="pc" value="{color}" style="width:32px;height:26px;border:none;cursor:pointer;">
        <label style="color:#9ca3af;font-size:12px;margin-left:6px;">Size</label>
        <input type="range" id="ps" min="1" max="20" value="4" style="width:70px;">
        <label style="color:#9ca3af;font-size:12px;margin-left:6px;">Opacity</label>
        <input type="range" id="po" min="10" max="100" value="90" style="width:70px;">
        <button onclick="clr()" style="padding:5px 12px;background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.4);color:#f87171;border-radius:6px;cursor:pointer;font-size:12px;">🗑 Clear</button>
        <button onclick="undo()" style="padding:5px 12px;background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.4);color:#a78bfa;border-radius:6px;cursor:pointer;font-size:12px;">↩ Undo</button>
        <span id="ss" style="color:{color};font-size:12px;"></span>
      </div>
      <canvas id="cv" width="680" height="320"
        style="background:rgba(255,255,255,0.03);border:1px solid rgba(139,92,246,0.25);
               border-radius:10px;cursor:crosshair;display:block;touch-action:none;"></canvas>
    </div>
    <script>
    const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
    let draw=false,strokes=0,snaps=[];
    function snap(){{snaps.push(ctx.getImageData(0,0,cv.width,cv.height));if(snaps.length>30)snaps.shift();}}
    function h2r(h,a){{const r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);return'rgba('+r+','+g+','+b+','+a+')';}}
    function gx(e){{return e.clientX-cv.getBoundingClientRect().left;}}
    function gy(e){{return e.clientY-cv.getBoundingClientRect().top;}}
    function setStyle(){{ctx.lineWidth=document.getElementById('ps').value;ctx.strokeStyle=h2r(document.getElementById('pc').value,document.getElementById('po').value/100);ctx.lineCap='round';ctx.lineJoin='round';}}
    cv.addEventListener('mousedown',e=>{{snap();draw=true;ctx.beginPath();ctx.moveTo(gx(e),gy(e));}});
    cv.addEventListener('mousemove',e=>{{if(!draw)return;setStyle();ctx.lineTo(gx(e),gy(e));ctx.stroke();}});
    cv.addEventListener('mouseup',()=>{{draw=false;strokes++;document.getElementById('ss').textContent='Strokes: '+strokes;}});
    cv.addEventListener('mouseleave',()=>draw=false);
    cv.addEventListener('touchstart',e=>{{e.preventDefault();snap();draw=true;const t=e.touches[0];ctx.beginPath();ctx.moveTo(gx(t),gy(t));}},{{passive:false}});
    cv.addEventListener('touchmove',e=>{{e.preventDefault();if(!draw)return;const t=e.touches[0];setStyle();ctx.lineTo(gx(t),gy(t));ctx.stroke();}},{{passive:false}});
    cv.addEventListener('touchend',()=>draw=false);
    function clr(){{ctx.clearRect(0,0,cv.width,cv.height);strokes=0;snaps=[];document.getElementById('ss').textContent='';}}
    function undo(){{if(snaps.length>0){{ctx.putImageData(snaps.pop(),0,0);strokes=Math.max(0,strokes-1);document.getElementById('ss').textContent='Strokes: '+strokes;}}}}
    </script>""", height=400)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — GUIDED MEDITATION BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def page_meditation_builder():
    page_header("🧘 Guided Meditation Builder","Compose personalized Reiki meditation sessions")
    col1,col2 = st.columns([1,2])

    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        duration      = st.slider("Duration (minutes)", 5, 60, 20)
        focus_chakra  = st.selectbox("Focus Chakra", ["All (Full Body)"]+list(CHAKRAS.keys()))
        intention     = st.text_input("Intention", placeholder="e.g. Release anxiety...")
        st.markdown("**Precepts to include**")
        precept_sel   = [p for i,p in enumerate(PRECEPTS) if st.checkbox(p, key=f"prec_{i}", value=True)]
        st.markdown("**Components**")
        incl_breath   = st.checkbox("Opening Breathwork",    value=True)
        incl_ground   = st.checkbox("Grounding Exercise",    value=True)
        incl_symbols  = st.checkbox("Symbol Visualizations", value=True)
        incl_affm     = st.checkbox("Chakra Affirmations",   value=True)
        incl_close    = st.checkbox("Gratitude Closing",     value=True)
        # FIX: generate button stores result in session_state — survives download button rerender
        if st.button("✨ Generate Script", use_container_width=True):
            chk   = CHAKRAS.get(focus_chakra)
            col_s = chk["color"] if chk else "#a78bfa"
            parts = [f"## 🌟 Reiki Meditation — {focus_chakra}\n*Duration: {duration} minutes*"]
            if intention: parts.append(f"\n> **Intention:** *{intention}*")
            if incl_breath: parts.append("""\n---\n### 🌬️ Opening Breathwork\nFind a comfortable position. Take three deep cleansing breaths — inhale 4, hold 2, exhale 6. Feel your body relax. You are safe here.""")
            if incl_ground: parts.append("""\n---\n### 🌍 Grounding\nImagine roots extending from your spine into the heart of the earth. You are grounded. You are supported.""")
            if precept_sel:
                parts.append("\n---\n### 📜 The Five Reiki Precepts\n")
                for p in precept_sel: parts.append(f'> *"{p}"*\n')
            if chk:
                parts.append(f"\n---\n### {chk['emoji']} {focus_chakra} Chakra Activation\n"
                              f"Bring awareness to your {chk['hand_position'].lower()}. "
                              f"Visualize a sphere of light at the {chk['sanskrit']}. "
                              f"With each breath, this light grows warmer and brighter.")
                if incl_affm:
                    parts.append("\n**Affirmations:**")
                    for a in chk["affirmations"]: parts.append(f'> *"{a}"*')
            if incl_symbols and focus_chakra != "All (Full Body)":
                parts.append("""\n---\n### ✨ Symbol Integration\nVisualize Cho Ku Rei above your head, amplifying the healing energy. See it descend and seal the healing in love.""")
            if incl_close:
                parts.append("""\n---\n### 🙏 Gratitude & Closing\nBring hands to heart. Feel gratitude for this practice. Take three gentle breaths, wiggle fingers and toes, slowly open your eyes.\n\n*Namaste. 🙏*""")
            st.session_state["med_script"]       = "\n".join(parts)
            st.session_state["med_script_color"] = col_s
        if st.button("🗑️ Clear Script", use_container_width=True):
            st.session_state["med_script"] = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # FIX: render from session_state — always visible, not lost on download button click
        if st.session_state.get("med_script"):
            script = st.session_state["med_script"]
            col_s  = st.session_state.get("med_script_color","#a78bfa")
            st.markdown(f'<div class="reiki-card" style="border-color:{col_s}44;">', unsafe_allow_html=True)
            st.markdown(script)
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button("⬇️ Download Script (.md)", script,
                               file_name="reiki_meditation.md", mime="text/markdown",
                               use_container_width=True)
        else:
            st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
            st.markdown("Configure your session on the left, then click **Generate**.\n\n**The Five Reiki Precepts:**")
            for p in PRECEPTS: st.markdown(f'> *"{p}"*')
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 7 — ENERGY DIARY
# ══════════════════════════════════════════════════════════════════════════════
def page_energy_diary():
    page_header("📊 Energy Diary","Daily check-ins with correlation insights")
    tab1,tab2 = st.tabs(["📝 Daily Check-in","📈 Insights & Correlations"])

    with tab1:
        # FIX: practice_min no longer conditionally rendered inside form (widget ID stability)
        with st.form("daily_checkin"):
            c1,c2 = st.columns(2)
            with c1:
                entry_date = st.date_input("Date", value=date.today())
                energy     = st.slider("Energy Level",      1, 10, 5)
                mood       = st.slider("Mood / Emotions",   1, 10, 5)
                physical   = st.slider("Physical Wellness", 1, 10, 5)
                sleep_q    = st.slider("Sleep Quality",     1, 10, 5)
            with c2:
                practiced    = st.checkbox("Did Reiki today?")
                practice_min = st.number_input("Practice minutes (0 if none)", 0, 120, 0)
                chakra_focus = st.selectbox("Main chakra focus", ["None"]+list(CHAKRAS.keys()))
                intentions   = st.text_area("Intentions & feelings", height=75)
                gratitude    = st.text_area("Gratitude notes", height=55)
            if st.form_submit_button("💾 Save Check-in"):
                entry = {"date":str(entry_date),"energy":energy,"mood":mood,"physical":physical,
                         "sleep":sleep_q,"practiced":practiced,"practice_min":int(practice_min),
                         "chakra_focus":chakra_focus,"intentions":intentions,"gratitude":gratitude}
                st.session_state.energy_entries = [
                    e for e in st.session_state.energy_entries if e["date"] != str(entry_date)]
                st.session_state.energy_entries.append(entry)
                save_json("energy_diary.json", st.session_state.energy_entries)
                st.success(f"✅ Check-in saved for {entry_date}!")

    # FIX: if/else instead of return inside tab block
    with tab2:
        entries = st.session_state.energy_entries
        if len(entries) < 3:
            st.info("📊 Log at least 3 check-ins to see insights and correlations.")
            rng = np.random.default_rng(42)
            sdates = [date.today() - timedelta(days=x) for x in range(14,0,-1)]
            sdf = pd.DataFrame({"date":sdates,"energy":rng.integers(3,9,14),"mood":rng.integers(4,9,14)})
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=sdf["date"],y=sdf["energy"],name="Energy (sample)",line=dict(color="#a78bfa",width=2),mode="lines+markers"))
            fig.add_trace(go.Scatter(x=sdf["date"],y=sdf["mood"],name="Mood (sample)",line=dict(color="#34d399",width=2),mode="lines+markers"))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",font_color="#9ca3af",
                title="Sample Preview — log 3+ entries to see your data",legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            df = pd.DataFrame(entries).sort_values("date")
            df["date"] = pd.to_datetime(df["date"])
            for col in ["energy","mood","physical","sleep"]:
                if col in df.columns: df[col] = pd.to_numeric(df[col], errors="coerce")
            reiki_days = int(df["practiced"].sum()) if "practiced" in df.columns else 0
            st.markdown(f"""<div class="metric-row">
                <div class="metric-box"><div class="m-val">{len(df)}</div><div class="m-lab">Days Logged</div></div>
                <div class="metric-box"><div class="m-val">{df['energy'].mean():.1f}</div><div class="m-lab">Avg Energy</div></div>
                <div class="metric-box"><div class="m-val">{df['mood'].mean():.1f}</div><div class="m-lab">Avg Mood</div></div>
                <div class="metric-box"><div class="m-val">{reiki_days}</div><div class="m-lab">Reiki Days</div></div>
            </div>""", unsafe_allow_html=True)
            fig = go.Figure()
            for cn,cc,lbl in [("energy","#a78bfa","Energy"),("mood","#34d399","Mood"),("physical","#f97316","Physical"),("sleep","#3b82f6","Sleep")]:
                if cn in df.columns:
                    fig.add_trace(go.Scatter(x=df["date"],y=df[cn],name=lbl,mode="lines+markers",line=dict(color=cc,width=2)))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9ca3af",height=300,title="Wellness Over Time",
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)",range=[0,11]))
            st.plotly_chart(fig, use_container_width=True)
            if "practiced" in df.columns and reiki_days > 0:
                rdf = df[df["practiced"]==True]; ndf = df[df["practiced"]==False]
                if len(rdf)>0 and len(ndf)>0:
                    cats=["Energy","Mood","Physical","Sleep"]
                    fig2 = go.Figure(data=[
                        go.Bar(name="Reiki Days",     x=cats,y=[rdf[c].mean()  for c in["energy","mood","physical","sleep"]],marker_color="#a78bfa",opacity=0.8),
                        go.Bar(name="Non-Reiki Days", x=cats,y=[ndf[c].mean()  for c in["energy","mood","physical","sleep"]],marker_color="#374151",opacity=0.8),
                    ])
                    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                        font_color="#9ca3af",barmode="group",title="Reiki Practice Correlation",
                        legend=dict(bgcolor="rgba(0,0,0,0)"),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.05)",range=[0,10]))
                    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 8 — CLIENT MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_client_management():
    page_header("👥 Client Management","Professional client records and session tracking")
    tab1,tab2,tab3 = st.tabs(["👤 Clients","📋 New Session","📁 Session History"])

    with tab1:
        c1,c2 = st.columns([1,2])
        with c1:
            st.markdown("#### Add New Client")
            with st.form("new_client"):
                name    = st.text_input("Full Name *")
                dob     = st.date_input("Date of Birth", value=date(1985,1,1))
                phone   = st.text_input("Phone")
                email   = st.text_input("Email")
                concern = st.text_area("Primary concerns", height=70)
                level   = st.selectbox("Practitioner Level",["Level I","Level II","Master"])
                if st.form_submit_button("✅ Add Client"):
                    if name.strip():
                        used = {c.get("id",0) for c in st.session_state.clients}
                        new_id = max(used, default=0)+1
                        st.session_state.clients.append({
                            "id":new_id,"name":name.strip(),"dob":str(dob),
                            "phone":phone,"email":email,"concern":concern,
                            "level":level,"added":str(date.today())})
                        save_json("clients.json", st.session_state.clients)
                        st.success(f"Added {name.strip()}!")
                    else:
                        st.error("Name is required.")
        with c2:
            st.markdown(f"#### Client List ({len(st.session_state.clients)} clients)")
            if not st.session_state.clients:
                st.info("No clients yet.")
            for client in st.session_state.clients:
                csess = [s for s in st.session_state.sessions if s.get("client_id")==client.get("id")]
                with st.expander(f"👤 {client['name']}  ·  {len(csess)} sessions"):
                    cc1,cc2 = st.columns(2)
                    with cc1:
                        st.write(f"📅 {client.get('dob','—')}"); st.write(f"📞 {client.get('phone','—')}"); st.write(f"✉️ {client.get('email','—')}")
                    with cc2:
                        st.write(f"🎯 {client.get('level','—')}"); st.write(f"📋 Added: {client.get('added','—')}")
                    if client.get("concern"): st.markdown(f"*{client['concern']}*")
                    if st.button("🗑️ Remove", key=f"del_{client['id']}"):
                        st.session_state.clients = [c for c in st.session_state.clients if c["id"]!=client["id"]]
                        save_json("clients.json", st.session_state.clients); st.rerun()

    # FIX: use if/else not return — ensures tab3 always renders
    with tab2:
        if not st.session_state.clients:
            st.info("Add clients first in the Clients tab.")
        else:
            with st.form("new_session_form"):
                cn = {c["name"]:c["id"] for c in st.session_state.clients}
                sel_c  = st.selectbox("Client", list(cn.keys()))
                sdate  = st.date_input("Session Date")
                sdur   = st.number_input("Duration (minutes)", 30, 180, 60)
                cwrk   = st.multiselect("Chakras Worked", list(CHAKRAS.keys()))
                techs  = st.multiselect("Techniques Used",
                    ["Full Body Scan","Byosen Scanning","Distant Healing","Cho Ku Rei","Sei He Ki",
                     "Hon Sha Ze Sho Nen","Crystals","Sound","Aura Clearing"])
                fb     = st.text_area("Client Feedback", height=70)
                pn     = st.text_area("Practitioner Notes (private)", height=70)
                fu     = st.text_input("Follow-up recommendations")
                if st.form_submit_button("💾 Save Session"):
                    st.session_state.sessions.append({
                        "client_id":cn[sel_c],"client_name":sel_c,"date":str(sdate),
                        "duration":int(sdur),"chakras":cwrk,"techniques":techs,
                        "client_feedback":fb,"prac_notes":pn,"followup":fu,"type":"Client Session"})
                    save_json("sessions.json", st.session_state.sessions)
                    st.success(f"✅ Session saved for {sel_c}")

    with tab3:
        csessions = [s for s in st.session_state.sessions if s.get("client_id")]
        if not csessions:
            st.info("No client sessions logged yet.")
        else:
            fc = st.selectbox("Filter by client", ["All"]+sorted({s["client_name"] for s in csessions}))
            fil = csessions if fc=="All" else [s for s in csessions if s["client_name"]==fc]
            for s in reversed(fil[-30:]):
                st.markdown(f"""<div class="reiki-card">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                        <span style="color:#a78bfa;font-weight:600;">👤 {s.get('client_name','Unknown')}</span>
                        <span style="color:#6b7280;font-size:12px;">📅 {s.get('date','?')} · {s.get('duration','?')} min</span>
                    </div>
                    <div style="color:#9ca3af;font-size:13px;">Chakras: {', '.join(s.get('chakras',[])) or '—'}</div>
                    <div style="color:#9ca3af;font-size:13px;margin-top:2px;">Techniques: {', '.join(s.get('techniques',[])) or '—'}</div>
                    {f'<div style="color:#d1d5db;font-size:13px;margin-top:6px;font-style:italic;">Feedback: {s["client_feedback"]}</div>' if s.get("client_feedback") else ""}
                    {f'<div style="color:#6b7280;font-size:12px;margin-top:4px;">Follow-up: {s["followup"]}</div>' if s.get("followup") else ""}
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 9 — SOUNDSCAPE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_soundscape():
    page_header("🎵 Chakra Soundscape Generator","Generate healing frequencies for each energy center")
    c1,c2 = st.columns([1,2])

    with c1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        sel   = st.selectbox("Chakra", list(CHAKRAS.keys()))
        chk   = CHAKRAS[sel]; color = chk["color"]; base = chk["frequency"]
        st.markdown(f"""<div style="text-align:center;padding:16px;background:{color}18;
                            border-radius:10px;border:1px solid {color}44;margin:10px 0;">
            <div style="font-size:36px;">{chk['emoji']}</div>
            <div style="font-size:28px;font-weight:700;color:{color};">{base} Hz</div>
            <div style="color:#9ca3af;font-size:12px;margin-top:4px;">Solfeggio · Note {chk['note']}</div>
        </div>""", unsafe_allow_html=True)
        custom = st.number_input("Custom frequency (Hz)", 20, 20000, base, step=1)
        dur    = st.slider("Duration (seconds)", 5, 60, 15)
        wtype  = st.selectbox("Waveform",["Harmonics (rich, warm)","Pure Sine (clean)"])
        if st.button("▶ Generate & Play", use_container_width=True):
            with st.spinner("Generating..."):
                wav = make_wav(custom, dur, pure=("Pure" in wtype))
            st.audio(wav, format="audio/wav")
            st.success(f"🎵 {custom} Hz · {dur}s")
            st.download_button("⬇️ Download WAV", wav,
                               file_name=f"{sel.lower().replace(' ','_')}_{custom}hz.wav",
                               mime="audio/wav", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("### All Chakra Frequencies")
        fh = "<div style='display:flex;flex-direction:column;gap:8px;'>"
        for name,data in CHAKRAS.items():
            c = data["color"]
            fh += f"""<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;
                        background:{c}0d;border:1px solid {c}33;border-radius:8px;">
                <span style="font-size:20px;width:26px;">{data['emoji']}</span>
                <div style="flex:1;">
                    <div style="color:{c};font-weight:600;font-size:14px;">{name} — {data['sanskrit']}</div>
                    <div style="color:#6b7280;font-size:11px;">Element: {data['element']} · Note: {data['note']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:22px;font-weight:700;color:{c};">{data['frequency']}</div>
                    <div style="color:#6b7280;font-size:10px;">Hz</div>
                </div>
            </div>"""
        fh += "</div>"
        st.markdown(fh, unsafe_allow_html=True)
        st.markdown("### Waveform Preview")
        sv = st.selectbox("Visualize", list(CHAKRAS.keys()), key="vis_c")
        vd = CHAKRAS[sv]; tv = np.linspace(0,.05,2000); fv = vd["frequency"]
        wv = .5*np.sin(2*np.pi*fv*tv) + .2*np.sin(2*np.pi*fv*2*tv) + .15*np.sin(2*np.pi*fv*.5*tv)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tv*1000, y=wv, mode="lines", line=dict(color=vd["color"],width=1.5)))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
            font_color="#9ca3af",height=150,margin=dict(t=10,b=30),
            xaxis=dict(title="ms",gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 10 — DISTANCE HEALING BOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_distance_healing():
    page_header("🌐 Distance Healing Board","Send Reiki energy across time and space")
    st.markdown("""<div class="reiki-card" style="border-color:rgba(34,211,238,0.3);background:rgba(34,211,238,0.04);">
        <div style="color:#67e8f9;font-size:13px;line-height:1.7;">
        <b style="color:#22d3ee;">Hon Sha Ze Sho Nen</b> — Time and space are illusions. Through this symbol,
        Reiki energy can be sent to any person, place, or time — past, present, or future.
        </div></div>""", unsafe_allow_html=True)

    c1,c2 = st.columns([1,2])
    with c1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        rec  = st.text_input("Recipient Name", value=st.session_state.get("dh_recipient",""))
        loc  = st.text_input("Location (optional)")
        intent = st.text_area("Healing Intention",
            value=st.session_state.get("dh_intent",""),
            placeholder="Surround [name] in healing white light...", height=80)
        dur  = st.slider("Duration (minutes)", 5, 30, value=st.session_state.get("dh_duration",15))
        st.multiselect("Healing Focus",
            ["Physical Healing","Emotional Release","Mental Clarity","Spiritual Alignment",
             "Past Trauma","Future Protection","Relationship Healing","Abundance"])
        # FIX: store in session_state first, then rerun so board renders with correct values
        if st.button("🌟 Load onto Board", use_container_width=True):
            st.session_state.update({"dh_recipient":rec,"dh_intent":intent,
                                     "dh_duration":dur,"dh_active":True})
            st.rerun()
        if st.session_state.get("dh_active"):
            if st.button("✖ Clear Board", use_container_width=True):
                st.session_state.update({"dh_active":False,"dh_recipient":"","dh_intent":""})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        srec  = st.session_state.get("dh_recipient","")
        sdur  = int(st.session_state.get("dh_duration",15))
        sint  = st.session_state.get("dh_intent","")
        active= st.session_state.get("dh_active",False)

        # Pre-build SVG fragments cleanly
        cv = list(CHAKRAS.values())
        dots  = "".join(f'<circle cx="{int(250+10*math.cos(2*math.pi*i/7))}" cy="{int(175+i*10)}" r="4" fill="{cv[i]["color"]}" opacity="0.8" filter="url(#fg)"/>' for i in range(7))
        geo   = "".join(f'<line x1="250" y1="210" x2="{int(250+180*math.cos(2*math.pi*i/12))}" y2="{int(210+180*math.sin(2*math.pi*i/12))}" stroke="rgba(167,139,250,0.08)" stroke-width="1"/>' for i in range(12))
        fol   = "".join(f'<circle cx="{int(250+60*math.cos(2*math.pi*i/6))}" cy="{int(210+60*math.sin(2*math.pi*i/6))}" r="60" fill="none" stroke="rgba(139,92,246,0.12)" stroke-width="1"/>' for i in range(6))
        rtxt  = f'<text x="250" y="375" text-anchor="middle" fill="rgba(216,180,254,0.9)" font-size="14" font-weight="600" font-family="Raleway">{srec[:28]}</text>' if srec else ""
        smsg  = (f"Sending healing to: {srec}" if srec else "Board ready — set intention and click Load") if active else "Set an intention and click Load onto Board"

        components.html(f"""
        <div style="font-family:'Raleway',sans-serif;">
          <svg viewBox="0 0 500 400" width="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <radialGradient id="rbg" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0d0d1a"/>
              </radialGradient>
              <filter id="fg"><feGaussianBlur stdDeviation="3" result="cb"/>
              <feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
              <filter id="fgg"><feGaussianBlur stdDeviation="6" result="cb"/>
              <feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
            </defs>
            <rect width="500" height="400" fill="url(#rbg)" rx="12"/>
            <circle cx="250" cy="200" r="180" fill="none" stroke="rgba(167,139,250,0.08)" stroke-width="1"/>
            <circle cx="250" cy="200" r="150" fill="none" stroke="rgba(167,139,250,0.10)" stroke-width="1"/>
            <circle cx="250" cy="200" r="120" fill="none" stroke="rgba(167,139,250,0.12)" stroke-width="1"/>
            {geo}{fol}
            <circle cx="250" cy="200" r="60"  fill="none" stroke="rgba(139,92,246,0.12)" stroke-width="1"/>
            <circle cx="250" cy="200" r="40"  fill="rgba(139,92,246,0.06)" filter="url(#fgg)"/>
            <circle cx="250" cy="200" r="24"  fill="rgba(167,139,250,0.18)" filter="url(#fg)"/>
            <circle cx="250" cy="200" r="10"  fill="rgba(216,180,254,0.85)" filter="url(#fg)"/>
            <text x="250" y="38" text-anchor="middle" fill="rgba(167,139,250,0.8)" font-size="13" font-family="Raleway">DISTANCE HEALING BOARD</text>
            <text x="250" y="56" text-anchor="middle" fill="rgba(139,92,246,0.6)" font-size="10" font-family="Raleway" letter-spacing="2">HON SHA ZE SHO NEN</text>
            {rtxt}{dots}
          </svg>
          <div style="margin-top:14px;padding:18px;background:rgba(139,92,246,0.08);
                      border:1px solid rgba(139,92,246,0.25);border-radius:12px;text-align:center;">
            <div style="font-size:12px;color:#6b7280;margin-bottom:8px;">{smsg}</div>
            <div id="dht" style="font-size:52px;font-weight:300;color:white;letter-spacing:-1px;">{sdur:02d}:00</div>
            <div style="width:80%;margin:8px auto;height:3px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;">
              <div id="dhp" style="height:100%;width:0%;background:#a78bfa;border-radius:2px;transition:width 1s linear;"></div>
            </div>
            <div style="display:flex;gap:10px;justify-content:center;margin-top:12px;">
              <button onclick="startDH()" id="dhs"
                style="padding:10px 24px;background:rgba(139,92,246,0.2);border:1px solid rgba(139,92,246,0.5);
                       color:#c4b5fd;border-radius:8px;cursor:pointer;font-size:13px;">▶ Begin</button>
              <button onclick="pauseDH()"
                style="padding:10px 18px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);
                       color:#6b7280;border-radius:8px;cursor:pointer;font-size:13px;">⏸ Pause</button>
              <button onclick="resetDH()"
                style="padding:10px 18px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);
                       color:#6b7280;border-radius:8px;cursor:pointer;font-size:13px;">↺ Reset</button>
            </div>
            <div id="dhs2" style="margin-top:10px;color:#6b7280;font-size:12px;min-height:18px;"></div>
          </div>
        </div>
        <script>
        let dt={sdur*60},dr={sdur*60},di=null,drun=false;
        const p2=n=>n.toString().padStart(2,'0');
        function startDH(){{if(drun)return;drun=true;document.getElementById('dhs').style.opacity='0.4';
          document.getElementById('dhs2').textContent='✦ Healing energy is flowing...';
          di=setInterval(()=>{{dr--;document.getElementById('dht').textContent=p2(Math.floor(dr/60))+':'+p2(dr%60);
          document.getElementById('dhp').style.width=((dt-dr)/dt*100).toFixed(1)+'%';
          if(dr<=0){{clearInterval(di);drun=false;document.getElementById('dht').textContent='✓ DONE';
          document.getElementById('dht').style.color='#34d399';
          document.getElementById('dhs2').textContent='💚 Complete. Seal with Cho Ku Rei.';
          document.getElementById('dhs').style.opacity='1';playB();}}}},1000);}}
        function pauseDH(){{if(di){{clearInterval(di);di=null;drun=false;}}document.getElementById('dhs').style.opacity='1';document.getElementById('dhs2').textContent='⏸ Paused';}}
        function resetDH(){{pauseDH();dr=dt;document.getElementById('dht').textContent=p2(Math.floor(dt/60))+':'+p2(dt%60);document.getElementById('dht').style.color='white';document.getElementById('dhp').style.width='0%';document.getElementById('dhs2').textContent='';}}
        function playB(){{try{{const c=new(window.AudioContext||window.webkitAudioContext)();
          [0,.45,.9,1.35].forEach((d,i)=>{{const o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);
          o.frequency.value=[528,639,741,963][i];o.type='sine';g.gain.setValueAtTime(.35,c.currentTime+d);
          g.gain.exponentialRampToValueAtTime(.001,c.currentTime+d+3);o.start(c.currentTime+d);o.stop(c.currentTime+d+3);}}}});}}catch(e){{}}}}
        </script>""", height=660)

    if sint:
        st.markdown(f"""<div class="reiki-card" style="border-color:rgba(139,92,246,0.3);text-align:center;">
            <div style="color:#9ca3af;font-size:11px;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Active Intention</div>
            <div style="color:#e9d5ff;font-size:15px;font-style:italic;line-height:1.7;">&ldquo;{sint}&rdquo;</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
def main():
    st.sidebar.markdown("""<div style="text-align:center;padding:20px 10px 24px;">
        <div style="font-size:36px;margin-bottom:6px;">☯</div>
        <div style="font-family:'Cinzel',serif;font-size:18px;font-weight:700;color:#e9d5ff;">Reiki Studio</div>
        <div style="font-size:11px;color:#4b5563;letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Healing Arts Suite</div>
    </div>""", unsafe_allow_html=True)

    PAGES = {
        "⏱️  Session Timer":       page_session_timer,
        "📔  Chakra Journal":       page_chakra_journal,
        "🎯  Attunement Tracker":   page_attunement_tracker,
        "📚  Chakra Encyclopedia":  page_encyclopedia,
        "✍️   Symbol Trainer":       page_symbol_trainer,
        "🧘  Meditation Builder":   page_meditation_builder,
        "📊  Energy Diary":         page_energy_diary,
        "👥  Client Management":    page_client_management,
        "🎵  Soundscape Generator": page_soundscape,
        "🌐  Distance Healing":     page_distance_healing,
    }
    st.sidebar.markdown("<div style='color:#4b5563;font-size:10px;letter-spacing:2px;text-transform:uppercase;padding:0 12px;margin-bottom:8px;'>NAVIGATION</div>", unsafe_allow_html=True)
    choice = st.sidebar.radio("", list(PAGES.keys()), label_visibility="collapsed")
    st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    tc = len(st.session_state.clients)
    ts = len(st.session_state.sessions)
    te = len(st.session_state.energy_entries)
    th = st.session_state.attunement.get("hours",0)

    st.sidebar.markdown(f"""<div style="padding:16px 12px;">
        <div style="font-size:10px;color:#4b5563;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">PRACTICE STATS</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div style="background:rgba(139,92,246,0.1);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:20px;font-weight:700;color:#a78bfa;">{tc}</div><div style="font-size:10px;color:#4b5563;">Clients</div></div>
            <div style="background:rgba(52,211,153,0.1);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:20px;font-weight:700;color:#34d399;">{ts}</div><div style="font-size:10px;color:#4b5563;">Sessions</div></div>
            <div style="background:rgba(251,191,36,0.1);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:20px;font-weight:700;color:#fbbf24;">{th:.0f}h</div><div style="font-size:10px;color:#4b5563;">Practice</div></div>
            <div style="background:rgba(59,130,246,0.1);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:20px;font-weight:700;color:#60a5fa;">{te}</div><div style="font-size:10px;color:#4b5563;">Diary</div></div>
        </div></div>""", unsafe_allow_html=True)

    PAGES[choice]()

if __name__ == "__main__":
    main()
