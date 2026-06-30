import streamlit as st
import base64
import datetime
import random
from pathlib import Path

st.set_page_config(
    page_title="Happy Birthday Puja ❤️",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── session state ─────────────────────────────────────────────────────────
if "candles_blown" not in st.session_state:
    st.session_state.candles_blown = False
if "letter_open" not in st.session_state:
    st.session_state.letter_open = False
if "surprise_shown" not in st.session_state:
    st.session_state.surprise_shown = False
if "quote_idx" not in st.session_state:
    st.session_state.quote_idx = 0

# ── global CSS (pure CSS, no JS needed — animations run on their own) ──────
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { visibility: hidden; }

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Montserrat:wght@300;400;600&display=swap');

:root {
  --gold:#d4af60; --rose:#c084bc; --sky:#93c5fd; --pink:#fda4af; --night:#0a0010;
}

.stApp {
  background: linear-gradient(135deg,#0a0010,#1a0035,#0d0020,#170530,#0a0010);
  background-size: 400% 400%;
  animation: bgShift 16s ease infinite;
  font-family: 'Montserrat', sans-serif;
}
@keyframes bgShift {0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}

h1, .hero-title {
  font-family: 'Cormorant Garamond', serif !important;
  font-weight: 300 !important;
  text-align: center;
  letter-spacing: .08em;
  background: linear-gradient(135deg, var(--gold), var(--rose), var(--sky), var(--gold));
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 5s ease infinite;
  font-size: clamp(2.5rem, 7vw, 5.5rem) !important;
}
@keyframes shimmer {0%,100%{background-position:0 50%}50%{background-position:100% 50%}}

.hero-sub {
  text-align: center; color: rgba(255,255,255,.55);
  letter-spacing: .35em; text-transform: uppercase;
  font-size: .9rem; margin-bottom: 6px;
}

.cake-emoji {
  font-size: 7rem; text-align: center; display: block;
  animation: bounce 2.5s ease-in-out infinite;
  filter: drop-shadow(0 20px 30px rgba(212,175,96,.35));
}
@keyframes bounce {0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-14px) scale(1.03)}}

.sec-head {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-size: clamp(1.8rem, 4vw, 3rem);
  text-align: center;
  background: linear-gradient(135deg, var(--gold), var(--rose));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-top: 10px;
}
.sec-rule {
  width: 70px; height: 2px; margin: 10px auto 30px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

.glass-card {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(212,175,96,.25);
  border-radius: 18px;
  padding: 22px 18px;
  backdrop-filter: blur(10px);
  text-align: center;
  transition: transform .3s ease;
}
.glass-card:hover { transform: translateY(-6px); border-color: rgba(212,175,96,.55); }

.polaroid {
  background: rgba(255,255,255,.93);
  border-radius: 10px;
  padding: 10px 10px 28px;
  box-shadow: 0 10px 30px rgba(0,0,0,.5);
  text-align: center;
}
.polaroid img { width: 100%; border-radius: 6px; object-fit: cover; aspect-ratio: 1; }
.polaroid .cap { color: #444; font-style: italic; font-size: .85rem; margin-top: 8px; }
.polaroid .ph { font-size: 3rem; padding: 30px 0; }

.tl-card {
  background: rgba(255,255,255,.05);
  border-left: 3px solid var(--gold);
  border-radius: 0 14px 14px 0;
  padding: 16px 20px;
  margin-bottom: 16px;
}
.tl-card h4 { color: var(--gold); font-family:'Cormorant Garamond',serif; margin-bottom:4px; font-size:1.2rem;}
.tl-card p { color: rgba(255,255,255,.7); font-size: .92rem; margin: 0; }

.letter-box {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(212,175,96,.25);
  border-radius: 20px;
  padding: 30px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.15rem;
  line-height: 1.9;
  color: rgba(255,255,255,.9);
  white-space: pre-wrap;
}

.quote-box {
  text-align: center;
  padding: 36px 24px;
  border-radius: 22px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(212,175,96,.18);
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: clamp(1.2rem, 2.6vw, 1.7rem);
  color: rgba(255,255,255,.88);
}
.quote-author { color: var(--gold); font-size: .85rem; letter-spacing:.2em; text-transform:uppercase; margin-top:14px; font-style:normal;}

.footer-note {
  text-align: center; color: rgba(255,255,255,.4);
  letter-spacing: .15em; padding: 30px 0 10px; font-size: .85rem;
}

div.stButton > button {
  background: linear-gradient(135deg, var(--gold), var(--rose), var(--sky));
  background-size: 200% 200%;
  color: #fff; border: none; border-radius: 50px;
  padding: 12px 30px; font-family:'Cormorant Garamond',serif;
  font-size: 1.05rem; letter-spacing: .1em;
  animation: btnShimmer 3s ease infinite;
  transition: transform .2s ease;
}
div.stButton > button:hover { transform: scale(1.04); }
@keyframes btnShimmer {0%,100%{background-position:0 50%}50%{background-position:100% 50%}}
</style>
""", unsafe_allow_html=True)

YEAR = datetime.datetime.now().year

# ── HERO ─────────────────────────────────────────────────────────────────
st.markdown('<span class="cake-emoji">🎂</span>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Wishing you the most beautiful day</p>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Happy Birthday<br>Puja</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:rgba(255,255,255,.45);letter-spacing:.3em;'
    'text-transform:uppercase;font-size:.85rem;margin-top:6px">SG College · Jajpur</p>',
    unsafe_allow_html=True,
)

st.write("")
col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("🕯️ Click to blow out the candles", use_container_width=True):
        st.session_state.candles_blown = True

if st.session_state.candles_blown:
    st.markdown(
        '<p style="text-align:center;color:var(--gold);font-family:\'Cormorant Garamond\',serif;'
        'font-size:1.6rem;margin-top:10px">✨ Make a Wish ✨</p>',
        unsafe_allow_html=True,
    )
    st.balloons()

st.write("---")

# ── TODAY'S DATE / OCCASION ──────────────────────────────────────────────
st.markdown('<p class="sec-head">You are the sunshine of our family</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)
today = datetime.date.today()
st.markdown(
    f'<p style="text-align:center;color:rgba(255,255,255,.6);font-size:1rem;'
    f'letter-spacing:.1em">Celebrating you today — {today.strftime("%B %d, %Y")} 🎉</p>',
    unsafe_allow_html=True,
)

st.write("---")

# ── GALLERY ───────────────────────────────────────────────────────────────
st.markdown('<p class="sec-head">Cherished Memories</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

img_dir = Path("images")
images = []
if img_dir.exists():
    for f in sorted(img_dir.iterdir()):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            images.append(f)

if images:
    cols = st.columns(4)
    for i, f in enumerate(images):
        with cols[i % 4]:
            st.image(str(f), use_container_width=True)
            st.markdown(
                f'<p class="polaroid .cap" style="text-align:center;color:rgba(255,255,255,.6);'
                f'font-style:italic;font-size:.85rem">{f.stem.replace("_", " ").title()}</p>',
                unsafe_allow_html=True,
            )
else:
    placeholders = [
        ("🌸", "Sweet Memories"), ("🌺", "Golden Days"), ("💫", "Pure Magic"), ("⭐", "Shining Bright"),
        ("🦋", "Beautiful Soul"), ("🌈", "Colorful Life"), ("💕", "Always Loved"), ("🎀", "Special Moments"),
    ]
    cols = st.columns(4)
    for i, (emoji, cap) in enumerate(placeholders):
        with cols[i % 4]:
            st.markdown(
                f'<div class="polaroid"><div class="ph">{emoji}</div>'
                f'<div class="cap">{cap}</div></div>',
                unsafe_allow_html=True,
            )
    st.caption("Drop your photos into the `images/` folder to replace these placeholders.")

st.write("---")

# ── TIMELINE ─────────────────────────────────────────────────────────────
st.markdown('<p class="sec-head">A Journey of Growth</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

timeline = [
    ("👶 Childhood", "A bundle of joy and endless curiosity, filling our home with laughter."),
    ("🎒 School Days", "Growing into a bright, determined girl with dreams bigger than the sky."),
    ("🎓 College", "Now shaping her future at SG College, Jajpur — focused and unstoppable."),
    ("🌟 Today", "A strong, kind, hardworking person we are endlessly proud of."),
    ("🚀 The Future", "Wherever life takes you, may it be full of light, love, and success."),
]
for title, desc in timeline:
    st.markdown(
        f'<div class="tl-card"><h4>{title}</h4><p>{desc}</p></div>',
        unsafe_allow_html=True,
    )

st.write("---")

# ── LETTER ────────────────────────────────────────────────────────────────
st.markdown('<p class="sec-head">A Letter For You</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("💌 Open the Letter", use_container_width=True):
        st.session_state.letter_open = True

if st.session_state.letter_open:
    letter = (
        "Dear Puja,\n\n"
        "Happy Birthday! 🎂\n\n"
        "Today is not just another day — it is a celebration of someone who brings warmth, "
        "kindness, and happiness wherever she goes.\n\n"
        "Watching you grow into such a strong, caring, and hardworking person has always made "
        "me so proud.\n\n"
        "I wish you endless happiness, good health, success in your studies at SG College Jajpur, "
        "beautiful friendships, and a future brighter than your dreams.\n\n"
        "No matter how much life changes, you'll always have my love, my support, and my deepest "
        "respect.\n\n"
        "May your smile never fade.\n"
        "May your dreams always find their way.\n\n"
        "Happy Birthday once again. 🌸\n\n"
        "With all my love,\n"
        "Your Brother ❤️"
    )
    st.markdown(f'<div class="letter-box">{letter}</div>', unsafe_allow_html=True)

st.write("---")

# ── WISHES ────────────────────────────────────────────────────────────────
st.markdown('<p class="sec-head">Wishes For You</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

wishes = [
    ("💪", "Health"), ("🏆", "Success"), ("😊", "Happiness"), ("💖", "Love"),
    ("🌟", "Confidence"), ("🤝", "Friendship"), ("📚", "Wisdom"), ("✨", "Magic"),
]
cols = st.columns(4)
for i, (emoji, label) in enumerate(wishes):
    with cols[i % 4]:
        st.markdown(
            f'<div class="glass-card"><div style="font-size:2rem">{emoji}</div>'
            f'<div style="margin-top:6px;letter-spacing:.15em;text-transform:uppercase;'
            f'font-size:.8rem;color:rgba(255,255,255,.7)">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("---")

# ── QUOTES ────────────────────────────────────────────────────────────────
st.markdown('<p class="sec-head">A Little Inspiration</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

quotes = [
    ("The more you praise and celebrate your life, the more there is in life to celebrate.", "Oprah Winfrey"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("Count your age by friends, not years. Count your life by smiles, not tears.", "John Lennon"),
    ("A sister is both your mirror and your opposite.", "Elizabeth Fishel"),
    ("Today is the oldest you've ever been, and the youngest you'll ever be again.", "Eleanor Roosevelt"),
    ("Sisters are different flowers from the same garden.", "Unknown"),
    ("May you live all the days of your life.", "Jonathan Swift"),
    ("Your future is as bright as your faith.", "Thomas S. Monson"),
]
q_text, q_author = quotes[st.session_state.quote_idx]
st.markdown(
    f'<div class="quote-box">"{q_text}"<div class="quote-author">— {q_author}</div></div>',
    unsafe_allow_html=True,
)
col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("🔄 Next Quote", use_container_width=True):
        st.session_state.quote_idx = (st.session_state.quote_idx + 1) % len(quotes)
        st.rerun()

st.write("---")

# ── SURPRISE ──────────────────────────────────────────────────────────────
st.markdown('<p class="sec-head">One Last Surprise</p>', unsafe_allow_html=True)
st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("🎁 Click for a Surprise", use_container_width=True):
        st.session_state.surprise_shown = True

if st.session_state.surprise_shown:
    st.snow()
    st.balloons()
    st.markdown(
        '<p style="text-align:center;font-family:\'Cormorant Garamond\',serif;'
        'font-size:clamp(1.8rem,5vw,3rem);background:linear-gradient(135deg,var(--gold),'
        'var(--rose),#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'margin-top:20px">I Love You Sister ❤️</p>',
        unsafe_allow_html=True,
    )

st.write("---")

# ── MUSIC ─────────────────────────────────────────────────────────────────
music_path = Path("music/birthday.mp3")
if music_path.exists():
    st.markdown('<p class="sec-head">Background Melody</p>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.audio(str(music_path))
    st.write("---")

# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown(
    f'<p class="footer-note">Made with ❤️ · Especially for Puja · By Your Brother · {YEAR}</p>',
    unsafe_allow_html=True,
)