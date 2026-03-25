# ═══════════════════════════════════════════════════════════════════════════════
#  🌟 REIKI STUDIO — Complete Healing Arts Application
#  All features: Timer, Journal, Attunement, Encyclopedia, Symbols,
#  Meditation, Energy Diary, Client Management, Soundscape, Distance Healing
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import json, os, io, wave as wav_lib, math
import streamlit.components.v1 as components

# ── CONFIG ──────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Reiki Studio", page_icon="☯", layout="wide",
                   initial_sidebar_state="expanded")

# ── GLOBAL CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Raleway', sans-serif; }

.stApp { background: linear-gradient(135deg, #0d0d1a 0%, #12102a 50%, #0d1a1a 100%); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1f 0%, #0d1a2a 100%) !important;
    border-right: 1px solid rgba(167,139,250,0.15) !important;
}
section[data-testid="stSidebar"] * { color: #c4b5fd !important; }
section[data-testid="stSidebar"] .stRadio label { font-size:14px !important; padding: 4px 0; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    color: #e9d5ff !important; cursor: pointer;
}

/* Cards */
.reiki-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    backdrop-filter: blur(10px);
}
.reiki-card h3 {
    font-family: 'Cinzel', serif;
    color: #e9d5ff;
    margin-bottom: 12px;
    font-size: 16px;
}

/* Metric cards */
.metric-row { display: flex; gap: 12px; flex-wrap: wrap; margin: 12px 0; }
.metric-box {
    flex: 1; min-width: 120px;
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 10px;
    padding: 16px 12px;
    text-align: center;
}
.metric-box .m-val { font-size: 28px; font-weight: 700; color: #a78bfa; }
.metric-box .m-lab { font-size: 11px; color: #7c6f9e; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

/* Page title */
.page-title {
    font-family: 'Cinzel', serif;
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #34d399, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.page-sub { color: #6b7280; font-size: 14px; margin-bottom: 24px; }

/* Chakra colors */
.chakra-root    { color: #ef4444 !important; }
.chakra-sacral  { color: #f97316 !important; }
.chakra-solar   { color: #eab308 !important; }
.chakra-heart   { color: #22c55e !important; }
.chakra-throat  { color: #3b82f6 !important; }
.chakra-third   { color: #8b5cf6 !important; }
.chakra-crown   { color: #a855f7 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(139,92,246,0.3), rgba(59,130,246,0.3)) !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    color: #e9d5ff !important;
    border-radius: 8px !important;
    font-family: 'Raleway', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(139,92,246,0.5), rgba(59,130,246,0.5)) !important;
    border-color: rgba(167,139,250,0.6) !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    color: #e9d5ff !important;
    border-radius: 8px !important;
}
.stSlider > div > div > div { background: rgba(139,92,246,0.3) !important; }
.stSlider > div > div > div > div { background: #a78bfa !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03) !important; border-radius: 8px; }
.stTabs [data-baseweb="tab"] { color: #9ca3af !important; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; }

.divider { border-top: 1px solid rgba(139,92,246,0.15); margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────────────────────────
CHAKRAS = {
    "Root":         {"num":1, "sanskrit":"Muladhara",    "color":"#ef4444", "bg":"rgba(239,68,68,0.12)",
                     "element":"Earth",       "frequency":396, "note":"C",
                     "affirmations":["I am safe and secure","I am grounded in the present","I have everything I need","My body is my home"],
                     "ailments":["Lower back pain","Anxiety & fear","Financial stress","Chronic fatigue","Immune issues"],
                     "crystals":["Red Jasper","Black Tourmaline","Obsidian","Garnet","Smoky Quartz"],
                     "hand_position":"Place both hands on the lower abdomen, fingers pointing downward toward the earth",
                     "description":"The foundation of our energy system, Muladhara governs survival instincts, security, and our physical connection to the earth. When balanced, you feel safe, grounded, and provided for.",
                     "body_pct":86, "emoji":"🔴",
                     "foods":["Red apples","Beets","Tomatoes","Root vegetables","Protein-rich foods"],
                     "yoga":["Mountain Pose (Tadasana)","Warrior I (Virabhadrasana I)","Child's Pose (Balasana)","Squat (Malasana)"],
                     "imbalanced_signs":"Feeling fearful, anxious, or disconnected from your body"},
    "Sacral":       {"num":2, "sanskrit":"Svadhisthana", "color":"#f97316", "bg":"rgba(249,115,22,0.12)",
                     "element":"Water",       "frequency":417, "note":"D",
                     "affirmations":["I embrace pleasure and joy","I am creative and inspired","I flow with life","My emotions are valid"],
                     "ailments":["Hip tension","Lower back pain","Creative blocks","Relationship issues","Sexual dysfunction"],
                     "crystals":["Carnelian","Orange Calcite","Moonstone","Sunstone","Peach Selenite"],
                     "hand_position":"Hands on the lower abdomen, about 2 inches below the navel, palms facing inward",
                     "description":"The center of creativity, pleasure, and emotional intelligence. Svadhisthana rules our relationships, passions, and ability to experience joy and flow.",
                     "body_pct":74, "emoji":"🟠",
                     "foods":["Oranges","Mangoes","Coconut","Almonds","Sweet potatoes"],
                     "yoga":["Pigeon Pose (Kapotasana)","Goddess Pose (Utkata Konasana)","Bound Angle (Baddha Konasana)","Hip Circles"],
                     "imbalanced_signs":"Emotional instability, creative blocks, or feeling numb to pleasure"},
    "Solar Plexus": {"num":3, "sanskrit":"Manipura",     "color":"#eab308", "bg":"rgba(234,179,8,0.12)",
                     "element":"Fire",        "frequency":528, "note":"E",
                     "affirmations":["I am confident and powerful","I trust my decisions","I am worthy of my dreams","I stand in my truth"],
                     "ailments":["Digestive issues","Low self-esteem","Control issues","Procrastination","Anger problems"],
                     "crystals":["Citrine","Yellow Calcite","Tiger's Eye","Amber","Golden Topaz"],
                     "hand_position":"Hands on the upper abdomen, just above the navel, channeling warmth into the solar plexus",
                     "description":"The seat of personal power, self-confidence, and willpower. Manipura governs how we assert ourselves in the world and our sense of identity.",
                     "body_pct":61, "emoji":"🟡",
                     "foods":["Bananas","Corn","Pineapple","Ginger","Turmeric","Chamomile tea"],
                     "yoga":["Boat Pose (Navasana)","Plank (Kumbhakasana)","Sun Salutation (Surya Namaskar)","Warrior III"],
                     "imbalanced_signs":"Feeling powerless, overly controlling, or lacking self-confidence"},
    "Heart":        {"num":4, "sanskrit":"Anahata",      "color":"#22c55e", "bg":"rgba(34,197,94,0.12)",
                     "element":"Air",         "frequency":639, "note":"F",
                     "affirmations":["I am love and I radiate love","I forgive myself and others","My heart is open","I give and receive freely"],
                     "ailments":["Heart conditions","Loneliness and grief","Trust issues","Co-dependency","Immune disorders"],
                     "crystals":["Rose Quartz","Green Aventurine","Malachite","Emerald","Rhodonite"],
                     "hand_position":"One or both hands over the heart center, feeling warmth radiate outward",
                     "description":"The bridge between earth and spirit, Anahata is the center of love, compassion, and connection. It governs our capacity to give and receive love unconditionally.",
                     "body_pct":49, "emoji":"💚",
                     "foods":["Leafy greens","Broccoli","Green tea","Kiwi","Avocado"],
                     "yoga":["Camel Pose (Ustrasana)","Bridge Pose (Setu Bandhasana)","Cobra (Bhujangasana)","Wild Thing"],
                     "imbalanced_signs":"Difficulty with intimacy, holding onto grief, or feeling closed off"},
    "Throat":       {"num":5, "sanskrit":"Vishuddha",    "color":"#3b82f6", "bg":"rgba(59,130,246,0.12)",
                     "element":"Ether/Sound", "frequency":741, "note":"G",
                     "affirmations":["I speak my truth with clarity","I am heard and understood","My voice matters","I express myself authentically"],
                     "ailments":["Throat infections","Communication difficulties","Shyness","Neck tension","Thyroid issues"],
                     "crystals":["Lapis Lazuli","Aquamarine","Blue Lace Agate","Sodalite","Celestite"],
                     "hand_position":"Hands lightly on the throat, or held just in front of the neck without touching",
                     "description":"The center of authentic self-expression, communication, and truth. Vishuddha governs how we express our inner world and listen deeply to others.",
                     "body_pct":36, "emoji":"🔵",
                     "foods":["Blueberries","Figs","Blackberries","Herbal teas","Sea vegetables"],
                     "yoga":["Fish Pose (Matsyasana)","Shoulder Stand (Sarvangasana)","Lion's Breath (Simhasana)","Neck rolls"],
                     "imbalanced_signs":"Fear of speaking up, talking too much, or inability to listen"},
    "Third Eye":    {"num":6, "sanskrit":"Ajna",         "color":"#8b5cf6", "bg":"rgba(139,92,246,0.12)",
                     "element":"Light",       "frequency":852, "note":"A",
                     "affirmations":["I trust my intuition","I see beyond the obvious","I am connected to inner wisdom","My mind is clear and focused"],
                     "ailments":["Headaches","Confusion & poor focus","Nightmares","Lack of intuition","Eye strain"],
                     "crystals":["Amethyst","Labradorite","Purple Fluorite","Azurite","Iolite"],
                     "hand_position":"Fingertips at the center of the forehead, slightly above and between the eyebrows",
                     "description":"The seat of intuition, imagination, and spiritual perception. Ajna allows us to see beyond the physical and access deeper wisdom.",
                     "body_pct":22, "emoji":"🔮",
                     "foods":["Eggplant","Purple cabbage","Dark chocolate","Goji berries","Walnuts"],
                     "yoga":["Child's Pose (Balasana)","Dolphin Pose","Eagle Pose (Garudasana)","Forward folds"],
                     "imbalanced_signs":"Overthinking, lack of focus, ignoring intuitive signals"},
    "Crown":        {"num":7, "sanskrit":"Sahasrara",    "color":"#a855f7", "bg":"rgba(168,85,247,0.12)",
                     "element":"Consciousness","frequency":963, "note":"B",
                     "affirmations":["I am connected to all that is","I am divinely guided","I trust the universe","I am one with pure consciousness"],
                     "ailments":["Depression","Spiritual disconnection","Closed-mindedness","Existential confusion","Isolation"],
                     "crystals":["Clear Quartz","Selenite","Lepidolite","Sugilite","Howlite"],
                     "hand_position":"Hands hovering just above the crown of the head, not touching, channeling divine energy",
                     "description":"Our connection to universal consciousness, higher self, and spiritual enlightenment. Sahasrara transcends the individual self and connects us to the infinite.",
                     "body_pct":8, "emoji":"✨",
                     "foods":["Fasting","Light fruit","Herbal teas","Sun-energized water","Raw foods"],
                     "yoga":["Headstand (Sirsasana)","Savasana","Lotus Pose (Padmasana)","Meditation"],
                     "imbalanced_signs":"Feeling spiritually cut off, overly materialistic, or nihilistic"},
}

HAND_POSITIONS = [
    {"position": 1,  "name": "Crown",             "chakra": "Crown",       "duration": 5,
     "instruction": "Place hands lightly above or on top of the head. Intention: divine connection, clarity, higher guidance."},
    {"position": 2,  "name": "Eyes / Forehead",   "chakra": "Third Eye",   "duration": 5,
     "instruction": "Hands over the eyes and forehead, gently. Intention: intuition, mental clarity, releasing worry."},
    {"position": 3,  "name": "Temples",            "chakra": "Third Eye",   "duration": 5,
     "instruction": "Cup hands over the sides of the head / temples. Intention: calming the mind, releasing tension."},
    {"position": 4,  "name": "Back of Head",       "chakra": "Third Eye",   "duration": 5,
     "instruction": "One hand on forehead, one on back of skull. Intention: integrating the nervous system."},
    {"position": 5,  "name": "Throat",             "chakra": "Throat",      "duration": 5,
     "instruction": "Hands gently on or hovering at the throat. Intention: authentic expression, clear communication."},
    {"position": 6,  "name": "Heart",              "chakra": "Heart",       "duration": 5,
     "instruction": "Both hands over the heart center. Intention: love, compassion, emotional healing."},
    {"position": 7,  "name": "Solar Plexus",       "chakra": "Solar Plexus","duration": 5,
     "instruction": "Hands on upper abdomen. Intention: confidence, personal power, releasing fear."},
    {"position": 8,  "name": "Navel / Sacral",     "chakra": "Sacral",      "duration": 5,
     "instruction": "Hands below the navel. Intention: creativity, emotional balance, vitality."},
    {"position": 9,  "name": "Hip Flexors",        "chakra": "Root",        "duration": 5,
     "instruction": "Hands on hip crease / lower pelvis. Intention: grounding, safety, stability."},
    {"position": 10, "name": "Knees",              "chakra": "Root",        "duration": 5,
     "instruction": "Cup hands over the knees. Intention: flexibility, forward movement, letting go."},
    {"position": 11, "name": "Feet",               "chakra": "Root",        "duration": 5,
     "instruction": "Hold the feet or place hands over them. Intention: deep grounding, earth connection."},
    {"position": 12, "name": "Closing Integration","chakra": "Heart",       "duration": 3,
     "instruction": "Hands in prayer at heart. Breath deeply. Give thanks. Seal the session with love and light."},
]

SYMBOLS = {
    "Cho Ku Rei": {
        "meaning": "Power Symbol — Place the Power of the Universe Here",
        "uses": ["Amplifies Reiki energy", "Cleanses a space", "Seals a healing session", "Protects auras and spaces"],
        "level": "Level II",
        "how_to_draw": ["Start at the top center", "Draw a vertical line downward", "Create a horizontal line to the right", "Coil counter-clockwise around the center line (3 times)", "End at the center"],
        "color": "#f97316",
        "svg_path": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <line x1="60" y1="10" x2="60" y2="70" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
            <line x1="60" y1="25" x2="85" y2="25" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
            <path d="M60,40 Q95,40 95,60 Q95,80 60,80 Q25,80 25,60 Q25,45 45,42" fill="none" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
            <path d="M45,42 Q58,40 60,55" fill="none" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
        </svg>""",
        "affirmation": "I call upon the power of the universe to amplify and focus healing energy here and now.",
    },
    "Sei He Ki": {
        "meaning": "Mental/Emotional Symbol — God and Humanity Coming Together",
        "uses": ["Emotional healing","Mental clarity","Releasing trauma","Addictions & habits","Relationship healing"],
        "level": "Level II",
        "how_to_draw": ["Draw a curved wave from top-left to right", "Continue downward with a serpentine motion", "Add a mirrored wave below", "Unite at the base"],
        "color": "#a78bfa",
        "svg_path": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <path d="M20,30 Q40,15 60,30 Q80,45 100,30" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
            <path d="M20,50 Q40,35 60,50 Q80,65 100,50" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
            <path d="M20,70 Q40,55 60,70 Q80,85 100,70" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
            <path d="M60,30 L60,95" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-dasharray="4,3"/>
        </svg>""",
        "affirmation": "Mind, body, and spirit align in perfect harmony. All emotional patterns are healed and released.",
    },
    "Hon Sha Ze Sho Nen": {
        "meaning": "Distance Symbol — The Buddha in Me Contacts the Buddha in You",
        "uses": ["Sending Reiki across distance & time","Healing past traumas","Future intention setting","Connecting with distant clients"],
        "level": "Level II",
        "how_to_draw": ["Draw three horizontal bars (top)", "A pagoda-like tower of stacked shapes", "A vertical center line connecting all", "Base triangle at the bottom"],
        "color": "#34d399",
        "svg_path": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <rect x="35" y="10" width="50" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <rect x="40" y="28" width="40" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <rect x="45" y="46" width="30" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <rect x="50" y="64" width="20" height="10" rx="2" fill="none" stroke="#34d399" stroke-width="2.5"/>
            <polygon points="60,82 40,105 80,105" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linejoin="round"/>
            <line x1="60" y1="10" x2="60" y2="82" stroke="#34d399" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.5"/>
        </svg>""",
        "affirmation": "Time and space are no barrier to love. I send healing light across all dimensions to reach you now.",
    },
    "Dai Ko Myo": {
        "meaning": "Master Symbol — Great Shining Light / The Treasure House of the Great Beaming Light",
        "uses": ["Spiritual enlightenment","Soul healing","Attunements","Master-level work","Healing the source of illness"],
        "level": "Master Level",
        "how_to_draw": ["Draw a large circle (wholeness)", "Three radiating lines upward (light)", "A cross in the center (integration)", "Surrounding lotus petals"],
        "color": "#fbbf24",
        "svg_path": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <circle cx="60" cy="62" r="38" fill="none" stroke="#fbbf24" stroke-width="2.5"/>
            <line x1="60" y1="10" x2="60" y2="24" stroke="#fbbf24" stroke-width="3" stroke-linecap="round"/>
            <line x1="60" y1="10" x2="50" y2="22" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
            <line x1="60" y1="10" x2="70" y2="22" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
            <line x1="45" y1="62" x2="75" y2="62" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
            <line x1="60" y1="47" x2="60" y2="77" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="60" cy="62" r="8" fill="none" stroke="#fbbf24" stroke-width="2"/>
            <circle cx="60" cy="62" r="3" fill="#fbbf24" opacity="0.7"/>
        </svg>""",
        "affirmation": "I am a clear and perfect channel for the great shining light of universal healing energy.",
    },
}

PRECEPTS = [
    "Just for today, I will not anger.",
    "Just for today, I will not worry.",
    "Just for today, I will be grateful.",
    "Just for today, I will do my work honestly.",
    "Just for today, I will be kind to every living thing.",
]

REIKI_LEVELS = {
    "Level I — Shoden":   {"desc": "First Degree. Physical healing, self-treatment, direct hands-on practice.", "color": "#22c55e"},
    "Level II — Okuden":  {"desc": "Second Degree. Distance healing, symbols, mental/emotional work.",          "color": "#3b82f6"},
    "Master — Shinpiden": {"desc": "Master/Teacher level. Attunements, Master symbol, teaching others.",        "color": "#a855f7"},
}

LEVEL_SYMBOLS = {
    "Level I — Shoden":   [],
    "Level II — Okuden":  ["Cho Ku Rei", "Sei He Ki", "Hon Sha Ze Sho Nen"],
    "Master — Shinpiden": ["Cho Ku Rei", "Sei He Ki", "Hon Sha Ze Sho Nen", "Dai Ko Myo"],
}

# ── PERSISTENCE ──────────────────────────────────────────────────────────────────
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

# ── SESSION STATE INIT ───────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "clients":        load_json("clients.json", []),
        "energy_entries": load_json("energy_diary.json", []),
        "journal_entries":load_json("chakra_journal.json", []),
        "attunement":     load_json("attunement.json",
                                    {"level":"Level I — Shoden","hours":0,
                                     "practice_log":[],"symbols_learned":[],
                                     "milestones":[]}),
        "sessions":       load_json("sessions.json", []),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── HELPERS ──────────────────────────────────────────────────────────────────────
def page_header(title, subtitle=""):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-sub">{subtitle}</div>', unsafe_allow_html=True)

def chakra_color(name): return CHAKRAS.get(name, {}).get("color", "#a78bfa")

def generate_tone(frequency: float, duration: int = 15, sr: int = 44100) -> bytes:
    t = np.linspace(0, duration, int(sr * duration), False)
    audio = (0.50 * np.sin(2*np.pi*frequency*t)
           + 0.20 * np.sin(2*np.pi*frequency*2*t)
           + 0.15 * np.sin(2*np.pi*frequency*0.5*t)
           + 0.10 * np.sin(2*np.pi*frequency*3*t)
           + 0.05 * np.sin(2*np.pi*frequency*4*t))
    audio /= np.max(np.abs(audio)) * 1.4
    fade = int(sr * 1.5)
    audio[:fade]  *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)
    audio_int = (audio * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wav_lib.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(audio_int.tobytes())
    buf.seek(0)
    return buf.read()

def body_svg(highlighted=None, size=320):
    """Human silhouette with 7 chakra dots."""
    W, H = 160, 400
    chakra_list = list(CHAKRAS.values())
    dots = []
    for c in chakra_list:
        cy = int(c["body_pct"] / 100 * H)
        alpha = 1.0 if (highlighted is None or highlighted == list(CHAKRAS.keys())[chakra_list.index(c)]) else 0.25
        glow = "filter:url(#glow)" if (highlighted and highlighted == list(CHAKRAS.keys())[chakra_list.index(c)]) else ""
        r = 14 if (highlighted == list(CHAKRAS.keys())[chakra_list.index(c)]) else 10
        dots.append(f'<circle cx="80" cy="{cy}" r="{r}" fill="{c["color"]}" opacity="{alpha}" style="{glow}"/>')
        dots.append(f'<text x="100" y="{cy+4}" font-size="11" fill="{c["color"]}" opacity="{alpha}" font-family="Raleway">{list(CHAKRAS.keys())[chakra_list.index(c)]}</text>')
    dots_html = "\n".join(dots)
    return f"""<svg viewBox="0 0 {W} {H}" width="{size//2}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="coloredBlur"/>
    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Head -->
  <ellipse cx="80" cy="32" rx="22" ry="28" fill="none" stroke="rgba(167,139,250,0.35)" stroke-width="2"/>
  <!-- Neck -->
  <rect x="70" y="58" width="20" height="18" rx="3" fill="none" stroke="rgba(167,139,250,0.35)" stroke-width="2"/>
  <!-- Body -->
  <path d="M35,76 Q30,120 28,180 Q26,230 30,280 L55,280 L55,380 L75,380 L75,280 L85,280 L85,380 L105,380 L105,280 L130,280 Q134,230 132,180 Q130,120 125,76 Z"
        fill="none" stroke="rgba(167,139,250,0.35)" stroke-width="2"/>
  <!-- Arms -->
  <path d="M35,80 Q10,130 12,200" fill="none" stroke="rgba(167,139,250,0.25)" stroke-width="2"/>
  <path d="M125,80 Q150,130 148,200" fill="none" stroke="rgba(167,139,250,0.25)" stroke-width="2"/>
  <!-- Chakra spine line -->
  <line x1="80" y1="8" x2="80" y2="380" stroke="rgba(167,139,250,0.15)" stroke-width="1" stroke-dasharray="4,4"/>
  {dots_html}
</svg>"""

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — SESSION TIMER
# ══════════════════════════════════════════════════════════════════════════════
def page_session_timer():
    page_header("⏱️ Session Timer & Guide", "Follow the hand position sequence with guided timers")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        st.markdown("### 🙌 Session Setup")
        session_type = st.selectbox("Session Type", ["Self-Treatment (Full 12 Positions)", "Short Session (Chakra Focus)", "Client Session"])
        if session_type == "Short Session (Chakra Focus)":
            chosen_chakra = st.selectbox("Focus Chakra", list(CHAKRAS.keys()))
            positions = [p for p in HAND_POSITIONS if p["chakra"] == chosen_chakra]
        else:
            positions = HAND_POSITIONS
        duration_per = st.slider("Minutes per position", 1, 15, 5)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Session Log")
        if st.button("📝 Save Session", use_container_width=True):
            entry = {"date": str(date.today()), "type": session_type,
                     "positions": len(positions), "duration": len(positions)*duration_per,
                     "notes": ""}
            st.session_state.sessions.append(entry)
            save_json("sessions.json", st.session_state.sessions)
            st.success(f"Session saved! {len(positions)} positions × {duration_per} min")
        total_sessions = len(st.session_state.sessions)
        total_min = sum(s.get("duration", 0) for s in st.session_state.sessions)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="m-val">{total_sessions}</div><div class="m-lab">Sessions</div></div>
            <div class="metric-box"><div class="m-val">{total_min}</div><div class="m-lab">Total Min</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        pos_idx = st.number_input("Position #", min_value=1, max_value=len(positions), value=1, step=1) - 1
        pos = positions[pos_idx]
        chakra_data = CHAKRAS.get(pos["chakra"], CHAKRAS["Heart"])
        color = chakra_data["color"]
        secs = duration_per * 60

        timer_html = f"""
        <div style="font-family:'Raleway',sans-serif; text-align:center; padding:20px;
                    background:rgba(255,255,255,0.03); border-radius:16px;
                    border:1px solid rgba(167,139,250,0.2);">
          <div style="font-size:12px; letter-spacing:2px; color:#6b7280; text-transform:uppercase; margin-bottom:6px;">
            Position {pos['position']} of {len(positions)}
          </div>
          <div style="font-size:22px; font-weight:700; color:{color}; margin-bottom:4px;">
            {pos['name']}
          </div>
          <div style="font-size:13px; color:#9ca3af; margin-bottom:20px;">
            Chakra: {pos['chakra']} &nbsp;·&nbsp; {chakra_data['emoji']}
          </div>
          <div id="timer" style="font-size:80px; font-weight:300; color:white;
               letter-spacing:-2px; line-height:1; margin:16px 0;
               text-shadow: 0 0 30px {color}55;">
            {duration_per:02d}:00
          </div>
          <div style="width:80%; margin:12px auto; height:4px; background:rgba(255,255,255,0.08); border-radius:2px; overflow:hidden;">
            <div id="progress" style="height:100%; width:0%; background:{color}; border-radius:2px; transition:width 1s linear;"></div>
          </div>
          <div style="margin:20px 0; display:flex; gap:12px; justify-content:center;">
            <button id="startBtn" onclick="startTimer()"
              style="padding:12px 32px; background:{color}33; border:1px solid {color}88;
                     color:{color}; border-radius:8px; font-size:14px; font-weight:600;
                     cursor:pointer; font-family:'Raleway',sans-serif; letter-spacing:1px;">
              ▶ START
            </button>
            <button onclick="pauseTimer()"
              style="padding:12px 24px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15);
                     color:#9ca3af; border-radius:8px; font-size:14px; cursor:pointer; font-family:'Raleway',sans-serif;">
              ⏸ PAUSE
            </button>
            <button onclick="resetTimer()"
              style="padding:12px 24px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15);
                     color:#9ca3af; border-radius:8px; font-size:14px; cursor:pointer; font-family:'Raleway',sans-serif;">
              ↺ RESET
            </button>
          </div>
          <div id="status" style="font-size:13px; color:#6b7280; height:20px;"></div>
          <div style="margin-top:20px; padding:16px; background:rgba(255,255,255,0.03);
                      border-radius:10px; border-left:3px solid {color}; text-align:left;">
            <div style="font-size:11px; color:#6b7280; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Instruction</div>
            <div style="font-size:14px; color:#d1d5db; line-height:1.6;">{pos['instruction']}</div>
          </div>
        </div>
        <script>
        let total = {secs};
        let remaining = {secs};
        let interval = null;
        let running = false;
        function startTimer() {{
            if (running) return;
            running = true;
            document.getElementById('startBtn').style.opacity = '0.4';
            document.getElementById('status').textContent = '✦ Session in progress...';
            interval = setInterval(() => {{
                remaining--;
                updateDisplay();
                let pct = ((total - remaining) / total * 100).toFixed(1);
                document.getElementById('progress').style.width = pct + '%';
                if (remaining <= 0) {{
                    clearInterval(interval); running = false;
                    document.getElementById('timer').style.textShadow = '0 0 40px #22c55e';
                    document.getElementById('status').innerHTML = '✅ Position complete! Move to next.';
                    document.getElementById('startBtn').style.opacity = '1';
                    playBell();
                }}
            }}, 1000);
        }}
        function pauseTimer() {{
            if (interval) {{ clearInterval(interval); interval = null; running = false; }}
            document.getElementById('startBtn').style.opacity = '1';
            document.getElementById('status').textContent = '⏸ Paused';
        }}
        function resetTimer() {{
            clearInterval(interval); interval = null; running = false;
            remaining = total;
            document.getElementById('timer').textContent = pad(Math.floor(total/60)) + ':' + pad(total%60);
            document.getElementById('timer').style.textShadow = '0 0 30px {color}55';
            document.getElementById('progress').style.width = '0%';
            document.getElementById('status').textContent = '';
            document.getElementById('startBtn').style.opacity = '1';
        }}
        function pad(n) {{ return n.toString().padStart(2,'0'); }}
        function updateDisplay() {{
            document.getElementById('timer').textContent = pad(Math.floor(remaining/60)) + ':' + pad(remaining%60);
        }}
        function playBell() {{
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                [0, 0.3, 0.6].forEach(delay => {{
                    const osc = ctx.createOscillator(); const gain = ctx.createGain();
                    osc.connect(gain); gain.connect(ctx.destination);
                    osc.frequency.value = {chakra_data['frequency']};
                    osc.type = 'sine';
                    gain.gain.setValueAtTime(0.4, ctx.currentTime + delay);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 2.5);
                    osc.start(ctx.currentTime + delay);
                    osc.stop(ctx.currentTime + delay + 2.5);
                }});
            }} catch(e) {{}}
        }}
        </script>
        """
        components.html(timer_html, height=520)

        # Navigation between positions
        c1, c2, c3 = st.columns([1,2,1])
        with c1:
            if pos_idx > 0:
                if st.button("← Previous"):
                    st.session_state["_pos"] = pos_idx - 1
        with c3:
            if pos_idx < len(positions) - 1:
                if st.button("Next →"):
                    st.session_state["_pos"] = pos_idx + 1

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — CHAKRA ASSESSMENT JOURNAL
# ══════════════════════════════════════════════════════════════════════════════
def page_chakra_journal():
    page_header("📔 Chakra Assessment Journal", "Track your energy body over time")

    tab1, tab2, tab3 = st.tabs(["🖊️ New Entry", "📊 History & Trends", "🗂️ All Entries"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("#### Chakra Body Map")
            sel_chakra = st.selectbox("Select chakra to assess", list(CHAKRAS.keys()))
            st.markdown(body_svg(sel_chakra), unsafe_allow_html=True)

        with col2:
            chakra = CHAKRAS[sel_chakra]
            st.markdown(f"""<div class="reiki-card" style="border-color:{chakra['color']}44;">
                <h3 style="color:{chakra['color']};">{chakra['emoji']} {sel_chakra} — {chakra['sanskrit']}</h3>
                <p style="color:#9ca3af; font-size:13px; line-height:1.6;">{chakra['description']}</p>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"#### Energy Assessment — {sel_chakra}")
            energy_level  = st.slider("Energy Level",    0, 10, 5, help="0=depleted, 10=overactive/blocked")
            balance_score = st.slider("Perceived Balance",0, 10, 5, help="0=very imbalanced, 10=perfectly balanced")

            st.markdown("**Physical Sensations**")
            sensations = st.multiselect("Select any you feel:",
                ["Tingling","Warmth","Coolness","Pulsing","Numbness","Tightness","Openness","Pressure","Vibration","Nothing"])

            notes = st.text_area("Session notes & observations", height=100,
                                 placeholder="What did you feel? What came up?")

            if st.button("💾 Save Journal Entry", use_container_width=True):
                entry = {
                    "date": str(date.today()), "chakra": sel_chakra,
                    "energy": energy_level, "balance": balance_score,
                    "sensations": sensations, "notes": notes,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.journal_entries.append(entry)
                save_json("chakra_journal.json", st.session_state.journal_entries)
                st.success(f"✅ {sel_chakra} chakra entry saved for {date.today()}")

    with tab2:
        entries = st.session_state.journal_entries
        if not entries:
            st.info("📝 No journal entries yet. Start logging in the 'New Entry' tab!")
            return
        df = pd.DataFrame(entries)
        df["date"] = pd.to_datetime(df["date"])

        st.markdown("#### Balance Score Over Time by Chakra")
        fig = go.Figure()
        for chk_name, chk_data in CHAKRAS.items():
            cdf = df[df["chakra"] == chk_name].sort_values("date")
            if len(cdf):
                fig.add_trace(go.Scatter(x=cdf["date"], y=cdf["balance"],
                    name=chk_name, mode="lines+markers",
                    line=dict(color=chk_data["color"], width=2),
                    marker=dict(size=6)))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#9ca3af", legend=dict(bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0,10]))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Current Chakra Balance Radar")
        latest = df.sort_values("date").groupby("chakra").last().reset_index()
        if len(latest) >= 3:
            fig2 = go.Figure(go.Scatterpolar(
                r=latest["balance"].tolist() + [latest["balance"].iloc[0]],
                theta=latest["chakra"].tolist() + [latest["chakra"].iloc[0]],
                fill="toself", fillcolor="rgba(139,92,246,0.15)",
                line=dict(color="#a78bfa", width=2)))
            fig2.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[0,10], gridcolor="rgba(255,255,255,0.08)", color="#6b7280"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", color="#9ca3af")),
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        entries = st.session_state.journal_entries
        if entries:
            for e in reversed(entries[-20:]):
                chakra = CHAKRAS.get(e["chakra"], {})
                color  = chakra.get("color","#a78bfa")
                senses = ", ".join(e.get("sensations",[])) or "—"
                st.markdown(f"""<div class="reiki-card" style="border-left:3px solid {color};">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span style="color:{color}; font-weight:600;">{chakra.get('emoji','')} {e['chakra']}</span>
                        <span style="color:#6b7280; font-size:12px;">{e['date']}</span>
                    </div>
                    <div style="display:flex; gap:24px; margin-bottom:8px;">
                        <span style="color:#9ca3af; font-size:13px;">Energy: <b style="color:{color};">{e.get('energy','?')}/10</b></span>
                        <span style="color:#9ca3af; font-size:13px;">Balance: <b style="color:{color};">{e.get('balance','?')}/10</b></span>
                    </div>
                    <div style="color:#6b7280; font-size:12px;">Sensations: {senses}</div>
                    {f'<div style="color:#9ca3af; font-size:13px; margin-top:8px; font-style:italic;">{e["notes"]}</div>' if e.get("notes") else ""}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No entries yet.")

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — ATTUNEMENT TRACKER
# ══════════════════════════════════════════════════════════════════════════════
def page_attunement_tracker():
    page_header("🎯 Attunement Tracker", "Track your Reiki journey through all levels")
    att = st.session_state.attunement

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        st.markdown("### Current Level")
        new_level = st.selectbox("Reiki Level", list(REIKI_LEVELS.keys()),
                                 index=list(REIKI_LEVELS.keys()).index(att.get("level", "Level I — Shoden")))
        att["level"] = new_level
        ldata = REIKI_LEVELS[new_level]
        st.markdown(f"""<div style="padding:12px; background:{ldata['color']}18; border-radius:8px;
                                    border:1px solid {ldata['color']}44; margin:8px 0;">
            <div style="color:{ldata['color']}; font-weight:600; margin-bottom:4px;">{new_level}</div>
            <div style="color:#9ca3af; font-size:13px; line-height:1.5;">{ldata['desc']}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### Practice Hours")
        add_hrs = st.number_input("Add practice hours", min_value=0.0, step=0.5, value=0.0)
        note_txt = st.text_input("Note (optional)")
        if st.button("➕ Log Hours"):
            att["hours"] = att.get("hours", 0) + add_hrs
            att["practice_log"].append({"date": str(date.today()), "hours": add_hrs, "note": note_txt})
            save_json("attunement.json", att)
            st.success(f"Logged {add_hrs}h!")

        total_h = att.get("hours", 0)
        st.markdown(f"""<div class="metric-row">
            <div class="metric-box"><div class="m-val">{total_h:.1f}</div><div class="m-lab">Total Hours</div></div>
            <div class="metric-box"><div class="m-val">{len(att.get('practice_log',[]))}</div><div class="m-lab">Sessions</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Level progress visualization
        st.markdown("### Level Progress Path")
        level_keys = list(REIKI_LEVELS.keys())
        cur_idx = level_keys.index(att["level"])
        progress_html = "<div style='display:flex; align-items:center; gap:0; margin:16px 0;'>"
        for i, (lk, ld) in enumerate(REIKI_LEVELS.items()):
            active = i <= cur_idx
            bg = ld["color"] if active else "rgba(255,255,255,0.05)"
            bc = ld["color"] if active else "rgba(255,255,255,0.1)"
            tc = "#fff" if active else "#4b5563"
            progress_html += f"""
            <div style="flex:1; text-align:center; padding:16px 8px;
                        background:{bg}22; border:1px solid {bc};
                        border-radius:8px; margin:0 4px;">
                <div style="font-size:22px; margin-bottom:6px;">{"✨" if active else "○"}</div>
                <div style="font-size:11px; font-weight:600; color:{tc}; line-height:1.4;">{lk}</div>
            </div>"""
        progress_html += "</div>"
        st.markdown(progress_html, unsafe_allow_html=True)

        # Symbols to learn
        st.markdown("### Symbols for Your Level")
        learned = att.get("symbols_learned", [])
        to_learn = LEVEL_SYMBOLS.get(att["level"], [])
        if not to_learn:
            st.info("Level I focuses on energy channeling without symbols. Deepen your hands-on practice!")
        else:
            for sym in to_learn:
                sym_data = SYMBOLS[sym]
                checked = sym in learned
                c1, c2 = st.columns([0.08, 0.92])
                with c1:
                    if st.checkbox("", value=checked, key=f"sym_{sym}"):
                        if sym not in learned: learned.append(sym)
                    else:
                        if sym in learned: learned.remove(sym)
                with c2:
                    col = sym_data["color"]
                    st.markdown(f"""<div style="padding:10px 14px; background:{col}11; border-radius:8px;
                                        border:1px solid {col}33; margin-bottom:4px;">
                        <span style="color:{col}; font-weight:600;">{sym}</span>
                        <span style="color:#6b7280; font-size:12px; margin-left:12px;">{sym_data['meaning']}</span>
                    </div>""", unsafe_allow_html=True)
            att["symbols_learned"] = learned
            save_json("attunement.json", att)

        # Practice log chart
        if att.get("practice_log"):
            st.markdown("### Practice Log")
            log_df = pd.DataFrame(att["practice_log"])
            log_df["date"] = pd.to_datetime(log_df["date"])
            log_df = log_df.sort_values("date")
            log_df["cumulative"] = log_df["hours"].cumsum()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=log_df["date"], y=log_df["hours"],
                name="Session", marker_color="#8b5cf6", opacity=0.7))
            fig.add_trace(go.Scatter(x=log_df["date"], y=log_df["cumulative"],
                name="Cumulative", line=dict(color="#34d399", width=2), yaxis="y2"))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9ca3af", height=220,
                yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(0,0,0,0)"),
                legend=dict(bgcolor="rgba(0,0,0,0)"), margin=dict(t=10))
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — CHAKRA ENCYCLOPEDIA
# ══════════════════════════════════════════════════════════════════════════════
def page_encyclopedia():
    page_header("📚 Chakra Encyclopedia", "Comprehensive reference for all 7 energy centers")

    cols = st.columns(7)
    selected = st.session_state.get("enc_sel", "Heart")
    for i, (name, data) in enumerate(CHAKRAS.items()):
        with cols[i]:
            if st.button(data["emoji"], key=f"enc_{name}", use_container_width=True,
                         help=name):
                st.session_state["enc_sel"] = name
                selected = name

    chakra = CHAKRAS[selected]
    color = chakra["color"]

    st.markdown(f"""<div style="padding:20px; background:{color}0d; border:1px solid {color}44;
                        border-radius:12px; margin:16px 0;">
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="font-size:48px;">{chakra['emoji']}</div>
            <div>
                <div style="font-size:24px; font-weight:700; color:{color}; font-family:'Cinzel',serif;">
                    {selected}
                </div>
                <div style="color:#9ca3af; font-size:14px;">{chakra['sanskrit']} · #{chakra['num']} · Note: {chakra['note']} · {chakra['frequency']} Hz</div>
                <div style="color:#6b7280; font-size:13px; margin-top:4px;">Element: {chakra['element']}</div>
            </div>
        </div>
        <p style="color:#d1d5db; margin-top:16px; font-size:14px; line-height:1.7;">{chakra['description']}</p>
        <div style="margin-top:12px; padding:12px; background:rgba(255,255,255,0.03);
                    border-radius:8px; border-left:3px solid {color};">
            <span style="color:{color}; font-size:12px; font-weight:600;">⚠ Signs of Imbalance: </span>
            <span style="color:#9ca3af; font-size:13px;">{chakra['imbalanced_signs']}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"**✨ Affirmations**")
        for a in chakra["affirmations"]:
            st.markdown(f'<div style="color:#d1d5db; font-size:13px; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.05);">&ldquo;{a}&rdquo;</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"**💎 Crystals**")
        for c_item in chakra["crystals"]:
            st.markdown(f"<div style='color:{color}; font-size:13px; padding:4px 0;'>◆ {c_item}</div>", unsafe_allow_html=True)
        st.markdown(f"**🌿 Yoga Poses**")
        for pose in chakra["yoga"][:3]:
            st.markdown(f"<div style='color:#9ca3af; font-size:12px; padding:3px 0;'>• {pose}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"**⚕ Associated Ailments**")
        for a in chakra["ailments"]:
            st.markdown(f"<div style='color:#f87171; font-size:13px; padding:4px 0;'>• {a}</div>", unsafe_allow_html=True)
        st.markdown(f"**🙌 Hand Position**")
        st.markdown(f"<div style='color:#9ca3af; font-size:13px; font-style:italic; line-height:1.5; margin-top:4px;'>{chakra['hand_position']}</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"**🍎 Supportive Foods**")
        for food in chakra["foods"]:
            st.markdown(f"<div style='color:#34d399; font-size:13px; padding:4px 0;'>• {food}</div>", unsafe_allow_html=True)
        st.markdown(f"**🎵 Healing Frequency**")
        st.markdown(f"<div style='font-size:32px; font-weight:700; color:{color}; margin-top:4px;'>{chakra['frequency']} Hz</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — SYMBOL TRAINER
# ══════════════════════════════════════════════════════════════════════════════
def page_symbol_trainer():
    page_header("✍️ Symbol Trainer", "Learn and practice the sacred Reiki symbols")

    st.info("💡 Reiki symbols are traditionally taught by a Reiki Master. This trainer shows their meaning, uses, and drawing guidelines for study purposes.")

    sel_sym = st.selectbox("Choose Symbol", list(SYMBOLS.keys()))
    sym = SYMBOLS[sel_sym]
    color = sym["color"]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""<div class="reiki-card" style="border-color:{color}44; text-align:center;">
            <div style="color:{color}; font-family:'Cinzel',serif; font-size:18px; font-weight:700; margin-bottom:12px;">
                {sel_sym}
            </div>
            {sym['svg_path']}
            <div style="color:#a78bfa; font-size:11px; letter-spacing:1px; text-transform:uppercase; margin-top:8px;">
                {sym['level']}
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="reiki-card">
            <div style="color:{color}; font-weight:600; font-size:15px; margin-bottom:12px;">
                {sym['meaning']}
            </div>
            <div style="color:#9ca3af; font-size:13px; font-style:italic; padding:12px; background:rgba(255,255,255,0.03);
                        border-radius:8px; border-left:3px solid {color}; margin-bottom:16px; line-height:1.7;">
                "{sym['affirmation']}"
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"**🔑 Uses & Applications**")
        for use in sym["uses"]:
            st.markdown(f"<div style='color:#d1d5db; font-size:13px; padding:3px 0;'>▹ {use}</div>", unsafe_allow_html=True)

        st.markdown(f"**✏️ How to Draw**")
        for i, step in enumerate(sym["how_to_draw"], 1):
            st.markdown(f"<div style='color:#a78bfa; font-size:13px; padding:5px 0;'><span style='color:{color}; font-weight:700;'>{i}.</span> {step}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎮 Practice Canvas")
    st.markdown("Draw the symbol below. Focus your intention as you trace each stroke.")

    canvas_html = f"""
    <div style="font-family:'Raleway',sans-serif;">
      <div style="display:flex; gap:12px; margin-bottom:12px; align-items:center;">
        <label style="color:#9ca3af; font-size:13px;">Color:</label>
        <input type="color" id="penColor" value="{color}" style="width:36px; height:28px; border:none; background:none; cursor:pointer;">
        <label style="color:#9ca3af; font-size:13px; margin-left:12px;">Size:</label>
        <input type="range" id="penSize" min="1" max="20" value="4" style="width:100px;">
        <button onclick="clearCanvas()" style="margin-left:12px; padding:6px 16px;
          background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4);
          color:#f87171; border-radius:6px; cursor:pointer; font-size:12px;">Clear</button>
        <button onclick="downloadCanvas()" style="margin-left:8px; padding:6px 16px;
          background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.4);
          color:#4ade80; border-radius:6px; cursor:pointer; font-size:12px;">Save</button>
        <span id="status" style="margin-left:12px; color:{color}; font-size:12px;"></span>
      </div>
      <canvas id="drawCanvas" width="700" height="340"
        style="background:rgba(255,255,255,0.03); border:1px solid rgba(139,92,246,0.25);
               border-radius:10px; cursor:crosshair; display:block;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('drawCanvas');
    const ctx = canvas.getContext('2d');
    let drawing = false;
    let strokes = 0;

    canvas.addEventListener('mousedown', e => {{ drawing = true; ctx.beginPath(); ctx.moveTo(getX(e), getY(e)); }});
    canvas.addEventListener('mousemove', e => {{
        if (!drawing) return;
        ctx.lineWidth = document.getElementById('penSize').value;
        ctx.strokeStyle = document.getElementById('penColor').value;
        ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.lineTo(getX(e), getY(e)); ctx.stroke();
    }});
    canvas.addEventListener('mouseup', e => {{ drawing = false; strokes++; document.getElementById('status').textContent = 'Strokes: ' + strokes; }});
    canvas.addEventListener('mouseleave', () => drawing = false);

    // Touch support
    canvas.addEventListener('touchstart', e => {{ e.preventDefault(); const t = e.touches[0]; drawing = true; ctx.beginPath(); ctx.moveTo(getTX(t), getTY(t)); }});
    canvas.addEventListener('touchmove',  e => {{ e.preventDefault(); if(!drawing) return; const t = e.touches[0]; ctx.lineWidth = document.getElementById('penSize').value; ctx.strokeStyle = document.getElementById('penColor').value; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.lineTo(getTX(t), getTY(t)); ctx.stroke(); }});
    canvas.addEventListener('touchend',   e => {{ drawing = false; }});

    function getX(e) {{ return e.clientX - canvas.getBoundingClientRect().left; }}
    function getY(e) {{ return e.clientY - canvas.getBoundingClientRect().top; }}
    function getTX(t) {{ return t.clientX - canvas.getBoundingClientRect().left; }}
    function getTY(t) {{ return t.clientY - canvas.getBoundingClientRect().top; }}

    function clearCanvas() {{ ctx.clearRect(0,0,canvas.width,canvas.height); strokes=0; document.getElementById('status').textContent=''; }}

    function downloadCanvas() {{
        const link = document.createElement('a');
        link.download = '{sel_sym.replace(" ","_")}_practice.png';
        link.href = canvas.toDataURL();
        link.click();
    }}
    </script>
    """
    components.html(canvas_html, height=420)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — GUIDED MEDITATION BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def page_meditation_builder():
    page_header("🧘 Guided Meditation Builder", "Compose personalized Reiki meditation sessions")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        st.markdown("### Session Design")
        duration = st.slider("Total Duration (minutes)", 5, 60, 20)
        focus_chakra = st.selectbox("Primary Focus Chakra", ["All (Full Body)"] + list(CHAKRAS.keys()))
        intention = st.text_input("Set your Intention", placeholder="e.g. Release anxiety, attract abundance...")

        st.markdown("**Include Precepts**")
        precept_sel = []
        for i, p in enumerate(PRECEPTS):
            if st.checkbox(p, key=f"prec_{i}", value=True):
                precept_sel.append(p)

        st.markdown("**Components**")
        incl_breathing  = st.checkbox("Opening Breathwork",   value=True)
        incl_grounding  = st.checkbox("Grounding Exercise",   value=True)
        incl_symbols    = st.checkbox("Symbol Visualizations",value=True)
        incl_affirmations = st.checkbox("Chakra Affirmations", value=True)
        incl_closing    = st.checkbox("Gratitude Closing",     value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.button("✨ Generate Meditation Script", use_container_width=True):
            chakra = CHAKRAS.get(focus_chakra, None)
            color  = chakra["color"] if chakra else "#a78bfa"

            script_parts = []
            script_parts.append(f"## 🌟 Reiki Meditation — {focus_chakra} Focus\n*Duration: {duration} minutes*")
            if intention:
                script_parts.append(f"\n> **Intention:** *{intention}*")

            if incl_breathing:
                script_parts.append("""
---
### 🌬️ Opening Breathwork (2 minutes)
Find a comfortable position. Close your eyes gently. Take three deep, cleansing breaths — inhale for 4 counts, hold for 2, exhale for 6. With each exhale, release any tension from your day. Feel your body becoming heavy and relaxed. You are safe here.""")

            if incl_grounding:
                script_parts.append("""
---
### 🌍 Grounding (2 minutes)
Imagine roots extending from the base of your spine, down through the floor, through the earth's layers, anchoring deep in the heart of the earth. Feel the warm, stable energy of the earth rising up through these roots. You are grounded. You are supported. You belong here.""")

            if precept_sel:
                script_parts.append("\n---\n### 📜 The Five Reiki Precepts\n*Repeat each precept three times in your mind:*\n")
                for p in precept_sel:
                    script_parts.append(f'> *"{p}"*\n')

            if chakra:
                script_parts.append(f"""
---
### {chakra['emoji']} {focus_chakra} Chakra Activation
Bring your awareness to your {chakra['hand_position'].lower()}. Visualize a beautiful sphere of {color.replace('#','')} light at this center — the {chakra['sanskrit']}. With each breath, this light grows warmer, brighter, more vibrant. This is your {focus_chakra} chakra awakening.""")

                if incl_affirmations:
                    script_parts.append("\n**Affirmations — repeat slowly, feeling each one:**")
                    for aff in chakra["affirmations"]:
                        script_parts.append(f'> *"{aff}"*')

            if incl_symbols and focus_chakra != "All (Full Body)":
                script_parts.append("""
---
### ✨ Symbol Integration
Visualize the Cho Ku Rei symbol above your head, its power amplifying and focusing the healing energy. See it glow with pure white light as it descends to your focus area, sealing the healing in love.""")

            if incl_closing:
                script_parts.append(f"""
---
### 🙏 Gratitude & Closing (2 minutes)
Bring your hands together at your heart. Take a moment to feel gratitude — for this practice, for your body, for the universal energy flowing through you. When you are ready, take three gentle breaths. Wiggle your fingers and toes. Slowly open your eyes. Carry this peace with you.

*Namaste. The light in me honors the light in you.* 🙏""")

            full_script = "\n".join(script_parts)
            st.markdown(f"""<div class="reiki-card" style="border-color:{color if chakra else '#a78bfa'}44;">""",
                        unsafe_allow_html=True)
            st.markdown(full_script)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.download_button("⬇️ Download Script", full_script,
                                  file_name=f"reiki_meditation_{focus_chakra.lower().replace(' ','_')}.md",
                                  mime="text/markdown", use_container_width=True):
                pass
        else:
            st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
            st.markdown("### How to Use")
            st.markdown("""
Configure your session on the left, then click **Generate** to create a personalized meditation script you can follow or share.

**The Five Reiki Precepts** (Gokai) are the ethical foundations of Reiki practice:
            """)
            for p in PRECEPTS:
                st.markdown(f'> *"{p}"*')
            st.markdown("""
These are not rules but gentle reminders — invitations to live more mindfully, one moment at a time.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 7 — ENERGY DIARY
# ══════════════════════════════════════════════════════════════════════════════
def page_energy_diary():
    page_header("📊 Energy Diary", "Daily check-ins with correlation insights")

    tab1, tab2 = st.tabs(["📝 Daily Check-in", "📈 Insights & Correlations"])

    with tab1:
        with st.form("daily_checkin"):
            st.markdown("### Today's Check-in")
            c1, c2 = st.columns(2)
            with c1:
                entry_date  = st.date_input("Date", value=date.today())
                energy      = st.slider("Energy Level",     1, 10, 5)
                mood        = st.slider("Mood / Emotions",  1, 10, 5)
                physical    = st.slider("Physical Wellness",1, 10, 5)
                sleep       = st.slider("Sleep Quality",    1, 10, 5)
            with c2:
                practiced   = st.checkbox("Did Reiki today?")
                practice_min= st.number_input("Practice minutes", 0, 120, 20) if practiced else 0
                chakra_focus= st.selectbox("Main chakra focus", ["None"] + list(CHAKRAS.keys()))
                intentions  = st.text_area("Intentions & feelings", height=100)
                gratitude   = st.text_area("Gratitude notes",       height=80)

            if st.form_submit_button("💾 Save Check-in"):
                entry = {"date": str(entry_date), "energy": energy, "mood": mood,
                         "physical": physical, "sleep": sleep,
                         "practiced": practiced, "practice_min": practice_min,
                         "chakra_focus": chakra_focus, "intentions": intentions,
                         "gratitude": gratitude}
                # Avoid duplicate dates
                st.session_state.energy_entries = [
                    e for e in st.session_state.energy_entries if e["date"] != str(entry_date)]
                st.session_state.energy_entries.append(entry)
                save_json("energy_diary.json", st.session_state.energy_entries)
                st.success("✅ Check-in saved!")

    with tab2:
        entries = st.session_state.energy_entries
        if len(entries) < 3:
            st.info("📊 Log at least 3 check-ins to see insights and correlations.")
            # Show sample chart
            sample_dates = [(date.today() - timedelta(days=x)) for x in range(14, 0, -1)]
            sample = pd.DataFrame({"date": sample_dates,
                                   "energy": np.random.randint(3,9, 14),
                                   "mood":   np.random.randint(4,9, 14)})
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=sample["date"], y=sample["energy"], name="Energy (sample)",
                line=dict(color="#a78bfa", width=2), mode="lines+markers"))
            fig.add_trace(go.Scatter(x=sample["date"], y=sample["mood"], name="Mood (sample)",
                line=dict(color="#34d399", width=2), mode="lines+markers"))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9ca3af", title="Sample Data Preview",
                legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig, use_container_width=True)
            return

        df = pd.DataFrame(entries).sort_values("date")
        df["date"] = pd.to_datetime(df["date"])

        # Summary metrics
        avg_e = df["energy"].mean(); avg_m = df["mood"].mean()
        reiki_days = df["practiced"].sum() if "practiced" in df.columns else 0
        st.markdown(f"""<div class="metric-row">
            <div class="metric-box"><div class="m-val">{len(df)}</div><div class="m-lab">Days Logged</div></div>
            <div class="metric-box"><div class="m-val">{avg_e:.1f}</div><div class="m-lab">Avg Energy</div></div>
            <div class="metric-box"><div class="m-val">{avg_m:.1f}</div><div class="m-lab">Avg Mood</div></div>
            <div class="metric-box"><div class="m-val">{reiki_days}</div><div class="m-lab">Reiki Days</div></div>
        </div>""", unsafe_allow_html=True)

        fig = go.Figure()
        for col_name, col_color, label in [
            ("energy","#a78bfa","Energy"), ("mood","#34d399","Mood"),
            ("physical","#f97316","Physical"), ("sleep","#3b82f6","Sleep")]:
            if col_name in df.columns:
                fig.add_trace(go.Scatter(x=df["date"], y=df[col_name], name=label,
                    mode="lines+markers", line=dict(color=col_color, width=2)))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#9ca3af", height=280, title="Wellness Over Time",
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0,11]))
        st.plotly_chart(fig, use_container_width=True)

        # Reiki vs Non-Reiki comparison
        if "practiced" in df.columns and reiki_days > 0:
            reiki_df    = df[df["practiced"] == True]
            non_reiki_df= df[df["practiced"] == False]
            if len(reiki_df) > 0 and len(non_reiki_df) > 0:
                st.markdown("#### 🌟 Reiki Practice Correlation")
                cats = ["Energy","Mood","Physical","Sleep"]
                r_vals  = [reiki_df[c].mean()     for c in ["energy","mood","physical","sleep"]]
                nr_vals = [non_reiki_df[c].mean() for c in ["energy","mood","physical","sleep"]]
                fig2 = go.Figure(data=[
                    go.Bar(name="Reiki Days",    x=cats, y=r_vals,
                           marker_color="#a78bfa", opacity=0.8),
                    go.Bar(name="Non-Reiki Days",x=cats, y=nr_vals,
                           marker_color="#374151", opacity=0.8),
                ])
                fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#9ca3af", barmode="group",
                    legend=dict(bgcolor="rgba(0,0,0,0)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0,10]))
                st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 8 — CLIENT MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_client_management():
    page_header("👥 Client Management", "Professional client records and session tracking")

    tab1, tab2, tab3 = st.tabs(["👤 Clients", "📋 New Session", "📁 Session History"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("#### Add New Client")
            with st.form("new_client"):
                name    = st.text_input("Full Name")
                dob     = st.date_input("Date of Birth", value=date(1985, 1, 1))
                phone   = st.text_input("Phone")
                email   = st.text_input("Email")
                concern = st.text_area("Primary concerns / intake notes", height=80)
                level   = st.selectbox("Practitioner Level Serving",
                                       ["Level I","Level II","Master"])
                if st.form_submit_button("✅ Add Client"):
                    if name:
                        client = {"id": len(st.session_state.clients)+1,
                                  "name": name, "dob": str(dob), "phone": phone,
                                  "email": email, "concern": concern, "level": level,
                                  "added": str(date.today())}
                        st.session_state.clients.append(client)
                        save_json("clients.json", st.session_state.clients)
                        st.success(f"Added {name}!")
                    else:
                        st.error("Name is required.")

        with col2:
            st.markdown(f"#### Client List ({len(st.session_state.clients)} clients)")
            if not st.session_state.clients:
                st.info("No clients yet. Add your first client on the left!")
            for client in st.session_state.clients:
                # Count sessions for this client
                c_sessions = [s for s in st.session_state.sessions
                               if s.get("client_id") == client.get("id")]
                with st.expander(f"👤 {client['name']}  ·  {len(c_sessions)} sessions"):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.write(f"📅 DOB: {client.get('dob','—')}")
                        st.write(f"📞 {client.get('phone','—')}")
                        st.write(f"✉️ {client.get('email','—')}")
                    with cc2:
                        st.write(f"🎯 Level: {client.get('level','—')}")
                        st.write(f"📋 Added: {client.get('added','—')}")
                    if client.get("concern"):
                        st.markdown(f"*Concerns: {client['concern']}*")
                    if st.button(f"🗑️ Remove", key=f"del_{client['id']}"):
                        st.session_state.clients = [
                            c for c in st.session_state.clients if c["id"] != client["id"]]
                        save_json("clients.json", st.session_state.clients)
                        st.rerun()

    with tab2:
        if not st.session_state.clients:
            st.info("Add clients first.")
            return
        st.markdown("#### Log a Client Session")
        with st.form("new_session_form"):
            client_names = {c["name"]: c["id"] for c in st.session_state.clients}
            sel_client = st.selectbox("Client", list(client_names.keys()))
            session_date= st.date_input("Session Date")
            duration_m  = st.number_input("Duration (minutes)", 30, 180, 60)
            chakras_worked = st.multiselect("Chakras Worked", list(CHAKRAS.keys()))
            techniques  = st.multiselect("Techniques Used",
                ["Full Body Scan","Byosen Scanning","Distant Healing","Cho Ku Rei","Sei He Ki",
                 "Hon Sha Ze Sho Nen","Crystals","Sound","Aura Clearing"])
            client_feedback = st.text_area("Client Feedback / Reactions", height=80)
            prac_notes  = st.text_area("Practitioner Notes (private)", height=80)
            followup    = st.text_input("Follow-up recommendations")

            if st.form_submit_button("💾 Save Session"):
                session = {
                    "client_id": client_names[sel_client], "client_name": sel_client,
                    "date": str(session_date), "duration": duration_m,
                    "chakras": chakras_worked, "techniques": techniques,
                    "client_feedback": client_feedback, "prac_notes": prac_notes,
                    "followup": followup, "type": "Client Session"
                }
                st.session_state.sessions.append(session)
                save_json("sessions.json", st.session_state.sessions)
                st.success(f"✅ Session saved for {sel_client}")

    with tab3:
        client_sessions = [s for s in st.session_state.sessions if s.get("client_id")]
        if not client_sessions:
            st.info("No client sessions logged yet.")
            return
        filter_client = st.selectbox("Filter by client",
            ["All"] + list({s["client_name"] for s in client_sessions}))
        filtered = client_sessions if filter_client == "All" else \
                   [s for s in client_sessions if s["client_name"] == filter_client]
        for s in reversed(filtered[-30:]):
            chakras_str = ", ".join(s.get("chakras", [])) or "—"
            tech_str    = ", ".join(s.get("techniques", [])) or "—"
            st.markdown(f"""<div class="reiki-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="color:#a78bfa; font-weight:600;">👤 {s.get('client_name','Unknown')}</span>
                    <span style="color:#6b7280; font-size:12px;">📅 {s.get('date','?')} · {s.get('duration','?')} min</span>
                </div>
                <div style="color:#9ca3af; font-size:13px; margin-bottom:4px;">Chakras: {chakras_str}</div>
                <div style="color:#9ca3af; font-size:13px; margin-bottom:4px;">Techniques: {tech_str}</div>
                {f'<div style="color:#d1d5db; font-size:13px; font-style:italic; margin-top:8px;">Feedback: {s["client_feedback"]}</div>' if s.get("client_feedback") else ""}
                {f'<div style="color:#6b7280; font-size:12px; margin-top:6px;">Follow-up: {s["followup"]}</div>' if s.get("followup") else ""}
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 9 — SOUNDSCAPE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_soundscape():
    page_header("🎵 Chakra Soundscape Generator", "Generate healing frequencies for each energy center")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        st.markdown("### Generate Tone")
        sel_chakra = st.selectbox("Chakra", list(CHAKRAS.keys()))
        chakra = CHAKRAS[sel_chakra]
        color  = chakra["color"]
        base_freq = chakra["frequency"]
        st.markdown(f"""<div style="text-align:center; padding:16px; background:{color}18;
                            border-radius:10px; border:1px solid {color}44; margin:12px 0;">
            <div style="font-size:36px;">{chakra['emoji']}</div>
            <div style="font-size:28px; font-weight:700; color:{color};">{base_freq} Hz</div>
            <div style="color:#9ca3af; font-size:12px; margin-top:4px;">Solfeggio Frequency · Note {chakra['note']}</div>
        </div>""", unsafe_allow_html=True)

        custom_freq = st.number_input("Or custom frequency (Hz)", min_value=20, max_value=20000,
                                      value=base_freq, step=1)
        duration   = st.slider("Duration (seconds)", 5, 60, 15)
        tone_type  = st.selectbox("Waveform character",
            ["Harmonics (rich, warm)","Pure Sine (clean)"])

        if st.button("▶ Generate & Play", use_container_width=True):
            with st.spinner("Generating healing frequency..."):
                freq = custom_freq
                t  = np.linspace(0, duration, int(44100*duration), False)
                if "Pure" in tone_type:
                    audio = np.sin(2*np.pi*freq*t) * 0.7
                else:
                    audio = (0.50*np.sin(2*np.pi*freq*t)
                           + 0.20*np.sin(2*np.pi*freq*2*t)
                           + 0.15*np.sin(2*np.pi*freq*0.5*t)
                           + 0.10*np.sin(2*np.pi*freq*3*t)
                           + 0.05*np.sin(2*np.pi*freq*4*t))
                audio /= np.max(np.abs(audio)) * 1.4
                fade = min(int(44100*1.5), len(audio)//4)
                audio[:fade]  *= np.linspace(0,1,fade)
                audio[-fade:] *= np.linspace(1,0,fade)
                audio_bytes = (audio * 32767).astype(np.int16)
                buf = io.BytesIO()
                with wav_lib.open(buf,"wb") as wf:
                    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(44100)
                    wf.writeframes(audio_bytes.tobytes())
                buf.seek(0)
                st.audio(buf.read(), format="audio/wav")
                st.success(f"🎵 {freq} Hz · {duration}s · {tone_type.split('(')[0].strip()}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Frequency reference table
        st.markdown("### All Chakra Frequencies")
        freq_html = "<div style='display:flex; flex-direction:column; gap:8px;'>"
        for name, data in CHAKRAS.items():
            c = data["color"]
            freq_html += f"""
            <div style="display:flex; align-items:center; gap:12px; padding:12px 16px;
                        background:{c}0d; border:1px solid {c}33; border-radius:8px;">
                <span style="font-size:20px; width:28px;">{data['emoji']}</span>
                <div style="flex:1;">
                    <div style="color:{c}; font-weight:600; font-size:14px;">{name} — {data['sanskrit']}</div>
                    <div style="color:#6b7280; font-size:11px; margin-top:2px;">
                        Element: {data['element']} &nbsp;·&nbsp; Note: {data['note']}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:22px; font-weight:700; color:{c};">{data['frequency']}</div>
                    <div style="color:#6b7280; font-size:10px;">Hz</div>
                </div>
            </div>"""
        freq_html += "</div>"
        st.markdown(freq_html, unsafe_allow_html=True)

        st.markdown("### Waveform Visualization")
        sel_vis = st.selectbox("Visualize chakra", list(CHAKRAS.keys()), key="vis_chakra")
        vis_data = CHAKRAS[sel_vis]
        t_vis = np.linspace(0, 0.05, 2000)
        f = vis_data["frequency"]
        wave = (0.5*np.sin(2*np.pi*f*t_vis) + 0.2*np.sin(2*np.pi*f*2*t_vis)
               + 0.15*np.sin(2*np.pi*f*0.5*t_vis))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t_vis*1000, y=wave, mode="lines",
            line=dict(color=vis_data["color"], width=1.5)))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#9ca3af", height=150, margin=dict(t=10, b=30),
            xaxis=dict(title="ms", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 10 — DISTANCE HEALING BOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_distance_healing():
    page_header("🌐 Distance Healing Board", "Send Reiki energy across time and space")

    st.markdown("""<div class="reiki-card" style="border-color:rgba(34,211,238,0.3); background:rgba(34,211,238,0.04);">
        <div style="color:#67e8f9; font-size:13px; line-height:1.7;">
        <b style="color:#22d3ee;">Hon Sha Ze Sho Nen</b> — The Distance Symbol teaches us that time and space
        are illusions of the mind. Through this symbol, Reiki energy can be sent to any person, any place,
        any time — past, present, or future. All that is required is a clear intention and an open heart.
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="reiki-card">', unsafe_allow_html=True)
        st.markdown("### Set Intention")
        recipient_name = st.text_input("Recipient Name (person or situation)")
        recipient_loc  = st.text_input("Location / Description (optional)")
        healing_intent = st.text_area("Healing Intention",
            placeholder="e.g. Surround [name] in healing white light. Release all that no longer serves them...",
            height=100)
        session_dur    = st.slider("Session Duration (minutes)", 5, 30, 15)
        healing_type   = st.multiselect("Healing Focus",
            ["Physical Healing","Emotional Release","Mental Clarity",
             "Spiritual Alignment","Past Trauma","Future Protection",
             "Relationship Healing","Abundance"])

        if st.button("🌟 Begin Distance Session", use_container_width=True):
            st.session_state["dh_active"] = True
            st.session_state["dh_recipient"] = recipient_name
            st.session_state["dh_intent"] = healing_intent
            st.session_state["dh_duration"] = session_dur
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        recipient = st.session_state.get("dh_recipient", "")
        intent_text = st.session_state.get("dh_intent", "")
        dur = st.session_state.get("dh_duration", 15)

        # Pre-compute dynamic SVG fragments to avoid nested quote issues
        _cv = list(CHAKRAS.values())
        _chakra_dots = "".join(
            f'<circle cx="{int(250+10*math.cos(2*math.pi*i/7))}" cy="{int(175+i*10)}" '
            f'r="4" fill="{_cv[i]["color"]}" opacity="0.8" filter="url(#glow2)"/>'
            for i in range(7))
        _geo = "".join(
            f'<line x1="250" y1="210" x2="{int(250+180*math.cos(2*math.pi*i/12))}" '
            f'y2="{int(210+180*math.sin(2*math.pi*i/12))}" stroke="rgba(167,139,250,0.08)" stroke-width="1"/>'
            for i in range(12))
        _fol = "".join(
            f'<circle cx="{int(250+60*math.cos(2*math.pi*i/6))}" cy="{int(210+60*math.sin(2*math.pi*i/6))}" '
            f'r="60" fill="none" stroke="rgba(139,92,246,0.12)" stroke-width="1"/>'
            for i in range(6))
        _rtext = (f'<text x="250" y="380" text-anchor="middle" fill="rgba(216,180,254,0.9)" '
                  f'font-size="14" font-weight="600" font-family="Raleway">{recipient[:30]}</text>') if recipient else ""
        _ltext = (f'<text x="250" y="400" text-anchor="middle" fill="rgba(139,92,246,0.6)" '
                  f'font-size="10" font-family="Raleway">{recipient_loc[:40]}</text>') if recipient_loc else ""

        healing_board = f"""
        <div style="font-family:'Raleway',sans-serif; text-align:center;">
          <svg viewBox="0 0 500 420" width="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <radialGradient id="bg" cx="50%" cy="50%" r="50%">
                <stop offset="0%"   stop-color="#1e1b4b" stop-opacity="1"/>
                <stop offset="100%" stop-color="#0d0d1a"  stop-opacity="1"/>
              </radialGradient>
              <filter id="glow2">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
              <filter id="glow3">
                <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
                <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
            </defs>
            <rect width="500" height="420" fill="url(#bg)" rx="16"/>
            <circle cx="250" cy="210" r="180" fill="none" stroke="rgba(167,139,250,0.1)" stroke-width="1"/>
            <circle cx="250" cy="210" r="150" fill="none" stroke="rgba(167,139,250,0.12)" stroke-width="1"/>
            <circle cx="250" cy="210" r="120" fill="none" stroke="rgba(167,139,250,0.15)" stroke-width="1"/>
            {_geo}
            {_fol}
            <circle cx="250" cy="210" r="60" fill="none" stroke="rgba(139,92,246,0.12)" stroke-width="1"/>
            <circle cx="250" cy="210" r="40" fill="rgba(139,92,246,0.08)" filter="url(#glow3)"/>
            <circle cx="250" cy="210" r="25" fill="rgba(167,139,250,0.2)" filter="url(#glow2)"/>
            <circle cx="250" cy="210" r="12" fill="rgba(216,180,254,0.8)" filter="url(#glow2)"/>
            <text x="250" y="48" text-anchor="middle" fill="rgba(167,139,250,0.8)" font-size="13" font-family="Raleway">DISTANCE HEALING BOARD</text>
            <text x="250" y="68" text-anchor="middle" fill="rgba(139,92,246,0.6)" font-size="10" font-family="Raleway" letter-spacing="2">HON SHA ZE SHO NEN</text>
            {_rtext}
            {_ltext}
            {_chakra_dots}
          </svg>

          {'<div id="dh-active" style="display:block;">' if st.session_state.get("dh_active") else '<div id="dh-inactive" style="display:block;">'}
          {"" if not st.session_state.get("dh_active") else f"""
          <div style="margin-top:16px; padding:20px; background:rgba(139,92,246,0.08);
                      border:1px solid rgba(139,92,246,0.25); border-radius:12px;">
            <div style="font-size:13px; color:#9ca3af; margin-bottom:8px;">SENDING HEALING TO</div>
            <div style="font-size:20px; font-weight:700; color:#c4b5fd; margin-bottom:12px;">{recipient or 'Universal'}</div>
            <div id="dh-timer" style="font-size:48px; font-weight:300; color:white; letter-spacing:-1px;">{dur:02d}:00</div>
            <div style="display:flex; gap:10px; justify-content:center; margin-top:16px;">
              <button onclick="startDH()" style="padding:10px 28px; background:rgba(139,92,246,0.2);
                border:1px solid rgba(139,92,246,0.5); color:#c4b5fd; border-radius:8px; cursor:pointer; font-size:13px;">
                ▶ Begin
              </button>
              <button onclick="stopDH()" style="padding:10px 20px; background:rgba(255,255,255,0.05);
                border:1px solid rgba(255,255,255,0.15); color:#6b7280; border-radius:8px; cursor:pointer; font-size:13px;">
                ■ End
              </button>
            </div>
            <div id="dh-status" style="margin-top:12px; color:#6b7280; font-size:12px;"></div>
          </div>
          <script>
          let dhRemaining = {dur*60};
          let dhInterval = null;
          function startDH() {{
            if(dhInterval) return;
            document.getElementById('dh-status').textContent = '✦ Healing energy is flowing...';
            dhInterval = setInterval(()=>{{
              dhRemaining--;
              let m=Math.floor(dhRemaining/60), s=dhRemaining%60;
              document.getElementById('dh-timer').textContent = m.toString().padStart(2,'0')+':'+s.toString().padStart(2,'0');
              if(dhRemaining<=0){{
                clearInterval(dhInterval); dhInterval=null;
                document.getElementById('dh-timer').textContent='✓ COMPLETE';
                document.getElementById('dh-timer').style.color='#34d399';
                document.getElementById('dh-status').textContent='💚 Session complete. Seal with Cho Ku Rei.';
                playDHBells();
              }}
            }},1000);
          }}
          function stopDH() {{ clearInterval(dhInterval); dhInterval=null; document.getElementById('dh-status').textContent='Session ended.'; }}
          function playDHBells(){{
            try{{
              const ctx=new(window.AudioContext||window.webkitAudioContext)();
              [0,0.4,0.8,1.2].forEach((d,i)=>{{
                const o=ctx.createOscillator(), g=ctx.createGain();
                o.connect(g); g.connect(ctx.destination);
                o.frequency.value=[528,639,741,963][i]; o.type='sine';
                g.gain.setValueAtTime(0.35,ctx.currentTime+d);
                g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+d+3);
                o.start(ctx.currentTime+d); o.stop(ctx.currentTime+d+3);
              }});
            }}catch(e){{}}
          }}
          </script>
          """ }
          </div>
        </div>
        """
        components.html(healing_board, height=700)

    # Affirmation for the session
    if intent_text:
        st.markdown(f"""<div class="reiki-card" style="border-color:rgba(139,92,246,0.3); text-align:center;">
            <div style="color:#9ca3af; font-size:11px; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px;">Intention</div>
            <div style="color:#e9d5ff; font-size:15px; font-style:italic; line-height:1.7;">"{intent_text}"</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
def main():
    st.sidebar.markdown("""
    <div style="text-align:center; padding:20px 10px 24px;">
        <div style="font-size:36px; margin-bottom:6px;">☯</div>
        <div style="font-family:'Cinzel',serif; font-size:18px; font-weight:700; color:#e9d5ff;">Reiki Studio</div>
        <div style="font-size:11px; color:#4b5563; letter-spacing:2px; text-transform:uppercase; margin-top:4px;">Healing Arts Suite</div>
    </div>""", unsafe_allow_html=True)

    PAGES = {
        "⏱️  Session Timer":        page_session_timer,
        "📔  Chakra Journal":        page_chakra_journal,
        "🎯  Attunement Tracker":    page_attunement_tracker,
        "📚  Chakra Encyclopedia":   page_encyclopedia,
        "✍️   Symbol Trainer":        page_symbol_trainer,
        "🧘  Meditation Builder":    page_meditation_builder,
        "📊  Energy Diary":          page_energy_diary,
        "👥  Client Management":     page_client_management,
        "🎵  Soundscape Generator":  page_soundscape,
        "🌐  Distance Healing":      page_distance_healing,
    }

    st.sidebar.markdown("<div style='color:#4b5563; font-size:10px; letter-spacing:2px; text-transform:uppercase; padding:0 12px; margin-bottom:8px;'>NAVIGATION</div>", unsafe_allow_html=True)
    choice = st.sidebar.radio("", list(PAGES.keys()), label_visibility="collapsed")
    st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    total_clients  = len(st.session_state.clients)
    total_sessions = len(st.session_state.sessions)
    total_entries  = len(st.session_state.energy_entries)
    att_hours      = st.session_state.attunement.get("hours", 0)

    st.sidebar.markdown(f"""
    <div style="padding:16px 12px;">
        <div style="font-size:10px; color:#4b5563; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">PRACTICE STATS</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div style="background:rgba(139,92,246,0.1); border-radius:8px; padding:10px; text-align:center;">
                <div style="font-size:20px; font-weight:700; color:#a78bfa;">{total_clients}</div>
                <div style="font-size:10px; color:#4b5563;">Clients</div>
            </div>
            <div style="background:rgba(52,211,153,0.1); border-radius:8px; padding:10px; text-align:center;">
                <div style="font-size:20px; font-weight:700; color:#34d399;">{total_sessions}</div>
                <div style="font-size:10px; color:#4b5563;">Sessions</div>
            </div>
            <div style="background:rgba(251,191,36,0.1); border-radius:8px; padding:10px; text-align:center;">
                <div style="font-size:20px; font-weight:700; color:#fbbf24;">{att_hours:.0f}h</div>
                <div style="font-size:10px; color:#4b5563;">Practice</div>
            </div>
            <div style="background:rgba(59,130,246,0.1); border-radius:8px; padding:10px; text-align:center;">
                <div style="font-size:20px; font-weight:700; color:#60a5fa;">{total_entries}</div>
                <div style="font-size:10px; color:#4b5563;">Diary Logs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    PAGES[choice]()

if __name__ == "__main__":
    main()
