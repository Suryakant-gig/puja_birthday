import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
import datetime

st.set_page_config(
    page_title="Happy Birthday Puja ❤️",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── hide ALL streamlit chrome ─────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
body { overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── optional: embed music as base64 ──────────────────────────────────────────
def get_music_src():
    p = Path("music/birthday.mp3")
    if p.exists():
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f"data:audio/mp3;base64,{b64}"
    return ""

# ── optional: embed images ────────────────────────────────────────────────────
def get_gallery_items():
    img_dir = Path("images")
    items = []
    if img_dir.exists():
        for f in img_dir.iterdir():
            if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
                try:
                    ext = f.suffix.lstrip(".").lower()
                    mime = "gif" if ext == "gif" else ("png" if ext == "png" else "jpeg")
                    b64 = base64.b64encode(f.read_bytes()).decode()
                    cap = f.stem.replace("_", " ").replace("-", " ").title()
                    items.append((f"data:image/{mime};base64,{b64}", cap, False))
                except Exception:
                    pass
    # placeholders if no real images
    if not items:
        placeholders = [
            ("🌸", "Sweet Memories"), ("🌺", "Golden Days"), ("💫", "Pure Magic"),
            ("⭐", "Shining Bright"), ("🦋", "Beautiful Soul"), ("🌈", "Colorful Life"),
            ("💕", "Always Loved"), ("🎀", "Special Moments"),
        ]
        for emoji, cap in placeholders:
            items.append((emoji, cap, True))
    return items

MUSIC_SRC = get_music_src()
GALLERY = get_gallery_items()
YEAR = datetime.datetime.now().year

# Build gallery HTML
def build_gallery_html(items):
    GRADS = [
        "linear-gradient(135deg,#fda4af,#c084bc)",
        "linear-gradient(135deg,#d4af60,#fb923c)",
        "linear-gradient(135deg,#93c5fd,#818cf8)",
        "linear-gradient(135deg,#86efac,#34d399)",
        "linear-gradient(135deg,#fde68a,#f9a8d4)",
        "linear-gradient(135deg,#c084bc,#93c5fd)",
        "linear-gradient(135deg,#fda4af,#fde68a)",
        "linear-gradient(135deg,#93c5fd,#86efac)",
    ]
    html = ""
    for i, (src, cap, is_placeholder) in enumerate(items):
        if is_placeholder:
            html += f"""
            <div class="polaroid">
              <div class="ph-img" style="background:{GRADS[i%len(GRADS)]}">{src}</div>
              <div class="caption" style="color:#666">{cap}</div>
            </div>"""
        else:
            html += f"""
            <div class="polaroid">
              <img src="{src}" alt="{cap}" loading="lazy">
              <div class="caption">{cap}</div>
            </div>"""
    return html

GALLERY_HTML = build_gallery_html(GALLERY)

MUSIC_PLAYER = f"""
<div id="music-player">
  <button id="playBtn" onclick="toggleMusic()">▶</button>
  <span style="color:#fff;font-size:12px;font-family:Georgia,serif">🎵 Birthday Melody</span>
  <input type="range" id="volSlider" min="0" max="1" step="0.05" value="0.4"
    oninput="setVol(this.value)" style="width:70px;accent-color:#d4af60">
  {"<audio id='bgMusic' loop><source src='" + MUSIC_SRC + "' type='audio/mp3'></audio>" if MUSIC_SRC else "<audio id='bgMusic'></audio>"}
</div>
"""

# ── The entire page as one HTML document ─────────────────────────────────────
PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Happy Birthday Puja ❤️</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --gold:#d4af60;--rose:#c084bc;--sky:#93c5fd;--pink:#fda4af;--night:#0a0010;
}}
html,body{{
  width:100%;min-height:100vh;overflow-x:hidden;
  background:var(--night);color:#fff;
  font-family:'Montserrat',sans-serif;
  scroll-behavior:smooth;
}}

/* ─ animated bg ─ */
body::before{{
  content:'';position:fixed;inset:0;z-index:-2;
  background:linear-gradient(135deg,#0a0010,#1a0035,#0d0020,#170530,#0a0010);
  background-size:400% 400%;
  animation:bgShift 14s ease infinite;
}}
@keyframes bgShift{{0%,100%{{background-position:0% 50%}}50%{{background-position:100% 50%}}}}

/* ─ particle canvas ─ */
#particleCanvas{{position:fixed;inset:0;z-index:-1;pointer-events:none}}

/* ─ intro ─ */
#intro{{
  position:fixed;inset:0;z-index:10000;background:#000;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-family:'Cormorant Garamond',serif;
}}
#starField{{position:absolute;inset:0;overflow:hidden}}
.star{{position:absolute;background:#fff;border-radius:50%;
  animation:twinkle var(--dur,2s) ease-in-out infinite alternate}}
@keyframes twinkle{{from{{opacity:.05}}to{{opacity:.9}}}}
.intro-line{{
  opacity:0;position:absolute;text-align:center;
  transition:opacity 1.4s ease;
  font-size:clamp(2rem,6vw,4.5rem);color:var(--gold);
  letter-spacing:.18em;
  text-shadow:0 0 40px rgba(212,175,96,.6);
}}
#introLine3{{font-size:clamp(3rem,9vw,7rem);color:#fff;
  text-shadow:0 0 60px rgba(192,132,188,.8),0 0 120px rgba(212,175,96,.4);}}

/* ─ music player ─ */
#music-player{{
  position:fixed;bottom:20px;right:20px;z-index:9999;
  background:rgba(255,255,255,.12);backdrop-filter:blur(20px);
  border:1px solid rgba(255,255,255,.25);border-radius:20px;
  padding:12px 18px;display:flex;align-items:center;gap:10px;
  box-shadow:0 8px 32px rgba(212,175,96,.2);
}}
#playBtn{{
  background:linear-gradient(135deg,var(--gold),var(--rose));
  border:none;border-radius:50%;width:38px;height:38px;
  color:#fff;font-size:15px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 4px 12px rgba(212,175,96,.5);
}}

/* ─ layout ─ */
.section{{padding:80px 24px;max-width:1100px;margin:0 auto}}
.alt-bg{{background:rgba(0,0,0,.25);padding:80px 24px}}
.alt-bg .section{{padding:0}}

/* ─ headings ─ */
.sec-head{{
  font-family:'Cormorant Garamond',serif;font-weight:300;
  font-size:clamp(2rem,5vw,3.5rem);letter-spacing:.1em;text-align:center;
  background:linear-gradient(135deg,var(--gold),var(--rose));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}}
.sec-rule{{
  width:80px;height:2px;margin:12px auto 40px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}}
.sec-sub{{
  text-align:center;color:rgba(255,255,255,.4);
  font-size:.78rem;letter-spacing:.3em;text-transform:uppercase;margin-bottom:44px;
}}

/* ─ hero ─ */
.hero{{
  min-height:100vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  text-align:center;padding:60px 24px;
}}
.hero-title{{
  font-family:'Cormorant Garamond',serif;font-weight:300;
  font-size:clamp(3rem,9vw,7.5rem);letter-spacing:.1em;line-height:1.05;
  background:linear-gradient(135deg,var(--gold),var(--rose),var(--sky),var(--gold));
  background-size:300% 300%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:shimmer 5s ease infinite;
}}
.hero-sub{{
  font-size:clamp(.9rem,2.5vw,1.3rem);color:rgba(255,255,255,.6);
  letter-spacing:.35em;text-transform:uppercase;margin-top:14px;font-weight:300;
}}
@keyframes shimmer{{0%,100%{{background-position:0 50%}}50%{{background-position:100% 50%}}}}

/* ─ cake ─ */
#cakeWrap{{
  font-size:clamp(7rem,16vw,11rem);
  animation:bounce 2.5s ease-in-out infinite;
  cursor:pointer;position:relative;display:inline-block;
  filter:drop-shadow(0 20px 40px rgba(212,175,96,.35));
  user-select:none;
}}
@keyframes bounce{{0%,100%{{transform:translateY(0) scale(1)}}50%{{transform:translateY(-16px) scale(1.03)}}}}
.flame{{
  position:absolute;font-size:1.5rem;
  animation:flicker .45s ease-in-out infinite alternate;
}}
@keyframes flicker{{from{{transform:scaleY(1) rotate(-3deg)}}to{{transform:scaleY(1.2) rotate(3deg)}}}}
#wishMsg{{
  opacity:0;transition:opacity 1s;
  font-family:'Cormorant Garamond',serif;font-size:1.8rem;
  color:var(--gold);letter-spacing:.12em;
  text-shadow:0 0 20px rgba(212,175,96,.6);
  margin-top:14px;
}}

/* ─ countdown ─ */
.cd-grid{{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-top:28px}}
.cd-box{{
  min-width:88px;padding:18px 14px;text-align:center;border-radius:18px;
  background:rgba(255,255,255,.06);
  border:1px solid rgba(212,175,96,.25);
  box-shadow:0 4px 20px rgba(212,175,96,.08);
}}
.cd-num{{
  font-family:'Cormorant Garamond',serif;font-size:2.8rem;line-height:1;
  background:linear-gradient(135deg,var(--gold),var(--rose));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}}
.cd-lbl{{font-size:.62rem;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.45);margin-top:6px}}

/* ─ gallery ─ */
.gallery-grid{{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:26px;margin-top:8px;
}}
.polaroid{{
  background:rgba(255,255,255,.92);border-radius:10px;
  padding:12px 12px 38px;
  box-shadow:0 12px 40px rgba(0,0,0,.55);
  transition:transform .35s cubic-bezier(.34,1.56,.64,1),box-shadow .35s;
  cursor:pointer;
}}
.polaroid:hover{{transform:scale(1.07) rotate(1.5deg);box-shadow:0 24px 60px rgba(0,0,0,.65)}}
.polaroid img{{width:100%;aspect-ratio:1;object-fit:cover;border-radius:5px;display:block}}
.ph-img{{width:100%;aspect-ratio:1;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:3.2rem}}
.caption{{color:#444;text-align:center;margin-top:10px;font-size:.78rem;font-style:italic}}

/* ─ timeline ─ */
.timeline{{position:relative;padding-left:44px;margin-top:36px}}
.timeline::before{{
  content:'';position:absolute;left:14px;top:0;bottom:0;width:2px;
  background:linear-gradient(180deg,var(--gold),var(--rose),var(--sky),var(--gold));
}}
.tl-item{{
  position:relative;margin-bottom:38px;
  opacity:0;transform:translateX(-28px);
  transition:opacity .7s ease,transform .7s ease;
}}
.tl-item.visible{{opacity:1;transform:translateX(0)}}
.tl-dot{{
  position:absolute;left:-38px;top:16px;
  width:28px;height:28px;border-radius:50%;
  background:linear-gradient(135deg,var(--gold),var(--rose));
  display:flex;align-items:center;justify-content:center;
  font-size:1rem;box-shadow:0 0 16px rgba(212,175,96,.5);
}}
.tl-card{{
  padding:20px 22px;border-radius:18px;
  background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.1);
  backdrop-filter:blur(12px);
}}
.tl-card h3{{color:var(--gold);font-family:'Cormorant Garamond',serif;font-size:1.3rem;margin-bottom:6px}}
.tl-card p{{color:rgba(255,255,255,.7);font-size:.9rem;line-height:1.65}}

/* ─ letter ─ */
.env-wrap{{text-align:center;margin-top:36px}}
#envBtn{{
  display:inline-flex;align-items:center;gap:10px;cursor:pointer;
  background:linear-gradient(135deg,rgba(212,175,96,.15),rgba(192,132,188,.15));
  border:1px solid rgba(212,175,96,.4);border-radius:60px;
  padding:18px 34px;font-size:1.1rem;color:var(--gold);
  font-family:'Cormorant Garamond',serif;letter-spacing:.12em;
  transition:all .3s;backdrop-filter:blur(10px);
}}
#envBtn:hover{{background:rgba(212,175,96,.25);transform:scale(1.04)}}
#letterBox{{
  display:none;margin-top:32px;text-align:left;padding:34px;
  border-radius:22px;
  background:rgba(255,255,255,.04);border:1px solid rgba(212,175,96,.18);
  backdrop-filter:blur(18px);
  font-family:'Cormorant Garamond',serif;font-size:1.12rem;line-height:2;
  color:rgba(255,255,255,.88);white-space:pre-wrap;
}}

/* ─ wishes ─ */
.wishes-grid{{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:18px;margin-top:36px;
}}
.wish-card{{
  padding:26px 18px;text-align:center;border-radius:20px;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
  backdrop-filter:blur(10px);
  transition:all .35s cubic-bezier(.34,1.56,.64,1);cursor:default;
}}
.wish-card:hover{{
  transform:translateY(-10px) scale(1.07);
  background:rgba(255,255,255,.09);border-color:rgba(212,175,96,.4);
  box-shadow:0 20px 50px rgba(212,175,96,.18),0 0 28px rgba(192,132,188,.12);
}}
.wish-icon{{font-size:2.2rem;margin-bottom:10px}}
.wish-lbl{{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.65)}}

/* ─ quotes ─ */
.quote-box{{
  text-align:center;padding:48px 30px;border-radius:28px;
  background:rgba(255,255,255,.04);border:1px solid rgba(212,175,96,.12);
  backdrop-filter:blur(14px);margin-top:36px;
}}
#quoteText{{
  font-family:'Cormorant Garamond',serif;font-style:italic;
  font-size:clamp(1.3rem,3vw,2rem);color:rgba(255,255,255,.88);
  line-height:1.65;transition:opacity .9s ease;
}}
#quoteAuthor{{
  margin-top:16px;font-size:.78rem;letter-spacing:.25em;
  text-transform:uppercase;color:var(--gold);opacity:.8;
  transition:opacity .9s ease;
}}

/* ─ surprise ─ */
.surprise-wrap{{text-align:center;margin-top:36px}}
#surpriseBtn{{
  display:inline-flex;align-items:center;gap:10px;
  padding:20px 44px;font-size:1.15rem;
  font-family:'Cormorant Garamond',serif;letter-spacing:.15em;
  color:#fff;border:none;border-radius:60px;cursor:pointer;
  background:linear-gradient(135deg,var(--gold),var(--rose),var(--sky));
  background-size:200% 200%;
  animation:btnShimmer 3s ease infinite,pulse 2s ease infinite;
}}
@keyframes btnShimmer{{0%,100%{{background-position:0 50%}}50%{{background-position:100% 50%}}}}
@keyframes pulse{{
  0%,100%{{box-shadow:0 0 28px rgba(212,175,96,.5)}}
  50%{{box-shadow:0 0 55px rgba(212,175,96,.8),0 0 90px rgba(192,132,188,.4)}}
}}
#surpriseMsg{{
  display:none;margin-top:36px;
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2rem,6vw,4rem);
  background:linear-gradient(135deg,var(--gold),var(--rose),#fff);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:shimmer 3s ease infinite;background-size:300% 300%;
}}
#heartPulse{{
  display:none;font-size:5.5rem;margin-top:18px;
  animation:heartbeat 1.2s ease-in-out infinite;
}}
@keyframes heartbeat{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.2)}}}}
@keyframes floatUp{{
  from{{transform:translateY(0) scale(1);opacity:1}}
  to{{transform:translateY(-80vh) scale(.2);opacity:0}}
}}

/* ─ fireworks canvas ─ */
#fwCanvas{{position:fixed;inset:0;z-index:8000;pointer-events:none;display:none}}

/* ─ footer ─ */
.footer{{
  text-align:center;padding:56px 24px;
  font-size:.88rem;color:rgba(255,255,255,.38);letter-spacing:.15em;
  border-top:1px solid rgba(255,255,255,.06);
}}
.footer span{{color:var(--gold)}}

/* ─ mobile ─ */
@media(max-width:600px){{
  .gallery-grid{{grid-template-columns:repeat(2,1fr)}}
  .wishes-grid{{grid-template-columns:repeat(2,1fr)}}
  .cd-box{{min-width:70px;padding:12px 10px}}
  .cd-num{{font-size:2.1rem}}
  #music-player{{bottom:10px;right:10px;padding:10px 14px;gap:8px}}
}}
</style>
</head>
<body>

<!-- PARTICLE CANVAS -->
<canvas id="particleCanvas"></canvas>
<!-- FIREWORKS CANVAS -->
<canvas id="fwCanvas"></canvas>

<!-- INTRO OVERLAY -->
<div id="intro">
  <div id="starField"></div>
  <div id="introLine1" class="intro-line">A Special Day</div>
  <div id="introLine2" class="intro-line">Happy Birthday</div>
  <div id="introLine3" class="intro-line">PUJA ❤️</div>
</div>

<!-- MUSIC PLAYER -->
{MUSIC_PLAYER}

<!-- ══ HERO ══════════════════════════════════════════════════════════════════ -->
<div class="hero">
  <div id="cakeWrap">
    🎂
    <span class="flame" style="left:26%;top:-16px">🔥</span>
    <span class="flame" style="left:47%;top:-22px;animation-delay:.15s">🔥</span>
    <span class="flame" style="left:67%;top:-16px;animation-delay:.08s">🔥</span>
  </div>
  <div id="wishMsg">✨ Make a Wish ✨</div>
  <p class="hero-sub" style="margin-top:24px">Wishing you the most beautiful day</p>
  <h1 class="hero-title">Happy Birthday<br>Puja</h1>
  <p style="margin-top:22px;font-size:.95rem;color:rgba(255,255,255,.45);letter-spacing:.35em;text-transform:uppercase">SG College · Jajpur · +3</p>
  <p style="margin-top:10px;font-size:.8rem;color:rgba(255,255,255,.3);letter-spacing:.18em">↓ Scroll to celebrate ↓</p>
</div>

<!-- ══ COUNTDOWN ═════════════════════════════════════════════════════════════ -->
<div class="alt-bg">
  <div class="section">
    <p class="sec-head">You are the sunshine of our family</p>
    <div class="sec-rule"></div>
    <p style="text-align:center;color:rgba(255,255,255,.45);font-size:.78rem;letter-spacing:.25em;text-transform:uppercase;margin-bottom:24px">Today's Celebration Timer</p>
    <div class="cd-grid">
      <div class="cd-box"><div class="cd-num" id="cd-h">00</div><div class="cd-lbl">Hours</div></div>
      <div class="cd-box"><div class="cd-num" id="cd-m">00</div><div class="cd-lbl">Minutes</div></div>
      <div class="cd-box"><div class="cd-num" id="cd-s">00</div><div class="cd-lbl">Seconds</div></div>
    </div>
  </div>
</div>

<!-- ══ GALLERY ════════════════════════════════════════════════════════════════ -->
<div class="section">
  <p class="sec-head">Precious Memories</p>
  <div class="sec-rule"></div>
  <p class="sec-sub">Moments frozen in time</p>
  <div class="gallery-grid">
    {GALLERY_HTML}
  </div>
</div>

<!-- ══ TIMELINE ═══════════════════════════════════════════════════════════════ -->
<div class="alt-bg">
  <div class="section">
    <p class="sec-head">Your Journey</p>
    <div class="sec-rule"></div>
    <p class="sec-sub">Every chapter has been beautiful</p>
    <div class="timeline">
      <div class="tl-item">
        <div class="tl-dot">🌱</div>
        <div class="tl-card"><h3>Childhood</h3><p>The little girl with the biggest dreams. Every laugh was music, every day an adventure. You lit up every room you walked into.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">📚</div>
        <div class="tl-card"><h3>School Days</h3><p>Books, friends, and endless curiosity. You showed the world that kindness and intelligence walk hand in hand.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">🎓</div>
        <div class="tl-card"><h3>SG College, Jajpur</h3><p>A new and beautiful chapter. Your dedication to your +3 studies fills us with pride every single day.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">🌸</div>
        <div class="tl-card"><h3>Today — Your Birthday</h3><p>A day to celebrate YOU — your growth, your heart, and every beautiful thing you bring into our world.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">🌟</div>
        <div class="tl-card"><h3>Future Dreams</h3><p>A horizon full of possibilities. Whatever path you choose, you carry the love of your whole family every step of the way.</p></div>
      </div>
    </div>
  </div>
</div>

<!-- ══ LETTER ═════════════════════════════════════════════════════════════════ -->
<div class="section">
  <p class="sec-head">A Letter For You</p>
  <div class="sec-rule"></div>
  <p class="sec-sub">From the heart</p>
  <div class="env-wrap">
    <div id="envBtn" onclick="openLetter()">💌 &nbsp;Open Your Birthday Letter</div>
    <div id="letterBox"></div>
  </div>
</div>

<!-- ══ WISHES ═════════════════════════════════════════════════════════════════ -->
<div class="alt-bg">
  <div class="section">
    <p class="sec-head">Birthday Wishes</p>
    <div class="sec-rule"></div>
    <p class="sec-sub">Everything we wish for you</p>
    <div class="wishes-grid">
      <div class="wish-card"><div class="wish-icon">💖</div><div class="wish-lbl">Love</div></div>
      <div class="wish-card"><div class="wish-icon">🌟</div><div class="wish-lbl">Success</div></div>
      <div class="wish-card"><div class="wish-icon">😊</div><div class="wish-lbl">Happiness</div></div>
      <div class="wish-card"><div class="wish-icon">☮️</div><div class="wish-lbl">Peace</div></div>
      <div class="wish-card"><div class="wish-icon">🌙</div><div class="wish-lbl">Dreams</div></div>
      <div class="wish-card"><div class="wish-icon">👨‍👩‍👧</div><div class="wish-lbl">Family</div></div>
      <div class="wish-card"><div class="wish-icon">💪</div><div class="wish-lbl">Confidence</div></div>
      <div class="wish-card"><div class="wish-icon">🌿</div><div class="wish-lbl">Health</div></div>
    </div>
  </div>
</div>

<!-- ══ QUOTES ═════════════════════════════════════════════════════════════════ -->
<div class="section">
  <p class="sec-head">Words of Light</p>
  <div class="sec-rule"></div>
  <div class="quote-box">
    <div id="quoteText"></div>
    <div id="quoteAuthor"></div>
  </div>
</div>

<!-- ══ SURPRISE ═══════════════════════════════════════════════════════════════ -->
<div class="alt-bg">
  <div class="section">
    <p class="sec-head">A Special Surprise</p>
    <div class="sec-rule"></div>
    <div class="surprise-wrap">
      <button id="surpriseBtn" onclick="triggerSurprise()">🎁 &nbsp;Open My Surprise</button>
      <div id="surpriseMsg">I Love You Sister ❤️</div>
      <div id="heartPulse">❤️</div>
    </div>
  </div>
</div>

<!-- ══ FOOTER ═════════════════════════════════════════════════════════════════ -->
<div class="footer">
  Made with <span>❤️</span> &nbsp;·&nbsp; Especially for <span>Puja</span> &nbsp;·&nbsp; By <span>Your Brother</span> &nbsp;·&nbsp; {YEAR}
</div>

<!-- ══ JAVASCRIPT ════════════════════════════════════════════════════════════ -->
<script>
// ─────────────────────────────────────────────────────────────────────────────
// INTRO ANIMATION
// ─────────────────────────────────────────────────────────────────────────────
(function() {{
  var sf = document.getElementById('starField');
  for (var i = 0; i < 200; i++) {{
    var s = document.createElement('div');
    s.className = 'star';
    var sz = Math.random() * 2.5 + 0.8;
    s.style.cssText = 'width:' + sz + 'px;height:' + sz + 'px;top:' + (Math.random()*100) + '%;left:' + (Math.random()*100) + '%;--dur:' + (Math.random()*3+1) + 's;animation-delay:' + (Math.random()*4) + 's;opacity:0;';
    sf.appendChild(s);
  }}
  setTimeout(function() {{
    sf.querySelectorAll('.star').forEach(function(s, i) {{
      setTimeout(function() {{ s.style.opacity = ''; }}, i * 6);
    }});
  }}, 400);

  var l1 = document.getElementById('introLine1');
  var l2 = document.getElementById('introLine2');
  var l3 = document.getElementById('introLine3');
  var intro = document.getElementById('intro');

  setTimeout(function() {{ l1.style.opacity = '1'; }}, 1000);
  setTimeout(function() {{ l1.style.opacity = '0'; }}, 3000);
  setTimeout(function() {{ l2.style.opacity = '1'; }}, 3600);
  setTimeout(function() {{ l2.style.opacity = '0'; }}, 5600);
  setTimeout(function() {{ l3.style.opacity = '1'; }}, 6200);
  setTimeout(function() {{
    intro.style.transition = 'opacity 1.6s ease';
    intro.style.opacity = '0';
    intro.style.pointerEvents = 'none';
    setTimeout(function() {{ intro.style.display = 'none'; }}, 1700);
  }}, 8800);
}})();

// ─────────────────────────────────────────────────────────────────────────────
// PARTICLE SYSTEM
// ─────────────────────────────────────────────────────────────────────────────
(function() {{
  var canvas = document.getElementById('particleCanvas');
  var ctx = canvas.getContext('2d');
  var W, H;
  function resize() {{ W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }}
  resize();
  window.addEventListener('resize', resize);

  var COLORS = ['#d4af60','#c084bc','#93c5fd','#fda4af','#f9a8d4','#e879f9','#ffffff'];
  var TYPES = ['heart','star','circle','balloon'];

  function rand(a, b) {{ return Math.random() * (b - a) + a; }}

  function Particle() {{ this.reset(); }}
  Particle.prototype.reset = function() {{
    this.type = TYPES[Math.floor(Math.random() * TYPES.length)];
    this.x = rand(0, W);
    this.y = rand(H * 0.6, H * 1.4);
    this.vx = rand(-0.4, 0.4);
    this.vy = -rand(0.4, 1.5);
    this.size = rand(8, 22);
    this.opacity = rand(0.35, 0.85);
    this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
    this.rot = rand(0, 360);
    this.rotV = rand(-0.8, 0.8);
    this.wobble = rand(0, Math.PI * 2);
    this.wobbleS = rand(0.02, 0.06);
  }};
  Particle.prototype.update = function() {{
    this.wobble += this.wobbleS;
    this.x += this.vx + Math.sin(this.wobble) * 0.35;
    this.y += this.vy;
    this.rot += this.rotV;
    if (this.y < -60) this.reset();
  }};
  Particle.prototype.draw = function() {{
    ctx.save();
    ctx.globalAlpha = this.opacity;
    ctx.fillStyle = this.color;
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rot * Math.PI / 180);
    var s = this.size;
    if (this.type === 'heart') {{
      var r = s * 0.06;
      ctx.beginPath();
      ctx.moveTo(0, -r*2);
      ctx.bezierCurveTo(r*4, -r*5, r*8, r*2, 0, r*7);
      ctx.bezierCurveTo(-r*8, r*2, -r*4, -r*5, 0, -r*2);
      ctx.fill();
    }} else if (this.type === 'star') {{
      ctx.beginPath();
      for (var i = 0; i < 5; i++) {{
        var a = ((i * 4 - 1) / 10) * Math.PI;
        ctx.lineTo(Math.cos(a) * s, Math.sin(a) * s);
        var b = ((i * 4 + 1) / 10) * Math.PI;
        ctx.lineTo(Math.cos(b) * s * 0.4, Math.sin(b) * s * 0.4);
      }}
      ctx.closePath(); ctx.fill();
    }} else if (this.type === 'balloon') {{
      ctx.beginPath();
      ctx.ellipse(0, -s * 0.6, s * 0.5, s * 0.65, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = this.color; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(0, s * 0.05); ctx.lineTo(0, s * 1.4); ctx.stroke();
    }} else {{
      ctx.beginPath(); ctx.arc(0, 0, s * 0.4, 0, Math.PI * 2); ctx.fill();
    }}
    ctx.restore();
  }};

  var particles = [];
  for (var i = 0; i < 80; i++) particles.push(new Particle());

  function loop() {{
    ctx.clearRect(0, 0, W, H);
    particles.forEach(function(p) {{ p.update(); p.draw(); }});
    requestAnimationFrame(loop);
  }}
  loop();
}})();

// ─────────────────────────────────────────────────────────────────────────────
// FIREWORKS
// ─────────────────────────────────────────────────────────────────────────────
var fwCanvas = document.getElementById('fwCanvas');
var fwCtx = fwCanvas.getContext('2d');
(function resize() {{ fwCanvas.width = window.innerWidth; fwCanvas.height = window.innerHeight; }})();
window.addEventListener('resize', function() {{ fwCanvas.width = window.innerWidth; fwCanvas.height = window.innerHeight; }});

var FW_COLS = ['#d4af60','#c084bc','#93c5fd','#fda4af','#f9a8d4','#e879f9','#fff','#fb7185','#34d399'];
function FWP(x, y, color) {{
  var a = Math.random() * Math.PI * 2, spd = 2 + Math.random() * 8;
  this.x = x; this.y = y;
  this.vx = Math.cos(a) * spd; this.vy = Math.sin(a) * spd;
  this.alpha = 1; this.color = color;
  this.decay = 0.012 + Math.random() * 0.018;
  this.size = 1.5 + Math.random() * 3.5;
}}
FWP.prototype.update = function() {{
  this.x += this.vx; this.y += this.vy + 0.07;
  this.vx *= 0.97; this.vy *= 0.97; this.alpha -= this.decay;
}};
FWP.prototype.draw = function() {{
  fwCtx.save(); fwCtx.globalAlpha = this.alpha;
  fwCtx.fillStyle = this.color;
  fwCtx.beginPath(); fwCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2); fwCtx.fill();
  fwCtx.restore();
}};

var fwParticles = [], fwActive = false, fwInterval;
function launchFW() {{
  var x = 0.15 * fwCanvas.width + Math.random() * fwCanvas.width * 0.7;
  var y = 0.1 * fwCanvas.height + Math.random() * fwCanvas.height * 0.45;
  var col = FW_COLS[Math.floor(Math.random() * FW_COLS.length)];
  for (var i = 0; i < 130; i++) fwParticles.push(new FWP(x, y, col));
}}
function fwLoop() {{
  if (!fwActive) return;
  fwCtx.fillStyle = 'rgba(0,0,0,0.14)';
  fwCtx.fillRect(0, 0, fwCanvas.width, fwCanvas.height);
  fwParticles = fwParticles.filter(function(p) {{ return p.alpha > 0.04; }});
  fwParticles.forEach(function(p) {{ p.update(); p.draw(); }});
  requestAnimationFrame(fwLoop);
}}
function startFireworks() {{
  fwCanvas.style.display = 'block';
  fwActive = true; fwLoop();
  launchFW();
  fwInterval = setInterval(function() {{ launchFW(); launchFW(); }}, 650);
  setTimeout(function() {{
    clearInterval(fwInterval);
    setTimeout(function() {{
      fwActive = false;
      fwCtx.clearRect(0, 0, fwCanvas.width, fwCanvas.height);
      fwCanvas.style.display = 'none';
    }}, 3200);
  }}, 6500);
}}

// ─────────────────────────────────────────────────────────────────────────────
// CAKE INTERACTION
// ─────────────────────────────────────────────────────────────────────────────
(function() {{
  var cake = document.getElementById('cakeWrap');
  var blown = false;
  if (!cake) return;
  cake.addEventListener('click', function() {{
    if (blown) return;
    blown = true;
    cake.querySelectorAll('.flame').forEach(function(f) {{ f.style.display = 'none'; }});
    var w = document.getElementById('wishMsg');
    if (w) {{ var t = 0; w.style.opacity = 0; var iv = setInterval(function() {{ t += 0.05; w.style.opacity = Math.min(t, 1); if (t >= 1) clearInterval(iv); }}, 40); }}
  }});
}})();

// ─────────────────────────────────────────────────────────────────────────────
// COUNTDOWN
// ─────────────────────────────────────────────────────────────────────────────
(function() {{
  function pad(n) {{ return n < 10 ? '0' + n : '' + n; }}
  function tick() {{
    var now = new Date(), mid = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
    var d = mid - now;
    var eh = document.getElementById('cd-h'), em = document.getElementById('cd-m'), es = document.getElementById('cd-s');
    if (eh) eh.textContent = pad(Math.floor(d / 3600000));
    if (em) em.textContent = pad(Math.floor((d % 3600000) / 60000));
    if (es) es.textContent = pad(Math.floor((d % 60000) / 1000));
  }}
  tick(); setInterval(tick, 1000);
}})();

// ─────────────────────────────────────────────────────────────────────────────
// TIMELINE SCROLL REVEAL
// ─────────────────────────────────────────────────────────────────────────────
(function() {{
  var items = document.querySelectorAll('.tl-item');
  var obs = new IntersectionObserver(function(entries) {{
    entries.forEach(function(e) {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
  }}, {{ threshold: 0.2 }});
  items.forEach(function(i) {{ obs.observe(i); }});
}})();

// ─────────────────────────────────────────────────────────────────────────────
// LETTER
// ─────────────────────────────────────────────────────────────────────────────
function openLetter() {{
  var btn = document.getElementById('envBtn');
  var box = document.getElementById('letterBox');
  if (!btn || !box) return;
  btn.style.display = 'none';
  box.style.display = 'block';
  var letter = "Dear Puja,\n\nHappy Birthday! \\uD83C\uDF82\n\nToday is not just another day \u2014 it is a celebration of someone who brings warmth, kindness, and happiness wherever she goes.\n\nWatching you grow into such a strong, caring, and hardworking person has always made me so proud.\n\nI wish you endless happiness, good health, success in your studies at SG College Jajpur, beautiful friendships, and a future brighter than your dreams.\n\nNo matter how much life changes, you\u2019ll always have my love, my support, and my deepest respect.\n\nMay your smile never fade.\nMay your dreams always find their way.\n\nHappy Birthday once again. \\uD83C\uDF38\n\nWith all my love,\nYour Brother \u2764\uFE0F";
  var i = 0;
  function type() {{
    if (i < letter.length) {{
      box.textContent += letter[i]; i++;
      setTimeout(type, 22);
    }}
  }}
  type();
}}

// ─────────────────────────────────────────────────────────────────────────────
// QUOTES
// ─────────────────────────────────────────────────────────────────────────────
(function() {{
  var quotes = [
    {{ t: "The more you praise and celebrate your life, the more there is in life to celebrate.", a: "\u2014 Oprah Winfrey" }},
    {{ t: "You are never too old to set another goal or to dream a new dream.", a: "\u2014 C.S. Lewis" }},
    {{ t: "Count your age by friends, not years. Count your life by smiles, not tears.", a: "\u2014 John Lennon" }},
    {{ t: "A sister is both your mirror and your opposite.", a: "\u2014 Elizabeth Fishel" }},
    {{ t: "Today is the oldest you\u2019ve ever been, and the youngest you\u2019ll ever be again.", a: "\u2014 Eleanor Roosevelt" }},
    {{ t: "Sisters are different flowers from the same garden.", a: "\u2014 Unknown" }},
    {{ t: "May you live all the days of your life.", a: "\u2014 Jonathan Swift" }},
    {{ t: "Your future is as bright as your faith.", a: "\u2014 Thomas S. Monson" }},
  ];
  var idx = 0;
  var qt = document.getElementById('quoteText'), qa = document.getElementById('quoteAuthor');
  if (!qt || !qa) return;
  function show(i) {{
    qt.style.opacity = 0; qa.style.opacity = 0;
    setTimeout(function() {{
      qt.textContent = quotes[i].t; qa.textContent = quotes[i].a;
      qt.style.opacity = 1; qa.style.opacity = 1;
    }}, 850);
  }}
  show(0);
  setInterval(function() {{ idx = (idx + 1) % quotes.length; show(idx); }}, 8000);
}})();

// ─────────────────────────────────────────────────────────────────────────────
// SURPRISE
// ─────────────────────────────────────────────────────────────────────────────
function triggerSurprise() {{
  var btn = document.getElementById('surpriseBtn');
  if (btn) {{ btn.disabled = true; btn.style.opacity = '0.6'; }}
  startFireworks();
  var emojis = ['\u2764\uFE0F','\\uD83C\uDF89','\\uD83C\uDF1F','\\uD83D\uDCAB','\\uD83C\uDF8A','\\uD83D\uDC95','\\uD83C\uDF38'];
  for (var i = 0; i < 55; i++) {{
    (function() {{
      var d = document.createElement('div');
      d.textContent = emojis[Math.floor(Math.random() * emojis.length)];
      d.style.cssText = 'position:fixed;left:' + (Math.random()*95) + 'vw;top:' + (Math.random()*90) + 'vh;font-size:' + (Math.random()*28+16) + 'px;z-index:9000;pointer-events:none;animation:floatUp 4s ease forwards;';
      document.body.appendChild(d);
      setTimeout(function() {{ d.remove(); }}, 4200);
    }})();
  }}
  setTimeout(function() {{
    var sm = document.getElementById('surpriseMsg'), hp = document.getElementById('heartPulse');
    if (sm) sm.style.display = 'block';
    if (hp) hp.style.display = 'block';
  }}, 1400);
}}

// ─────────────────────────────────────────────────────────────────────────────
// MUSIC PLAYER
// ─────────────────────────────────────────────────────────────────────────────
var _playing = false;
var _audio = document.getElementById('bgMusic');
if (_audio) _audio.volume = 0.4;
function toggleMusic() {{
  if (!_audio) return;
  if (_playing) {{
    _audio.pause();
    document.getElementById('playBtn').textContent = '\u25B6';
    _playing = false;
  }} else {{
    _audio.play().then(function() {{
      document.getElementById('playBtn').textContent = '\u23F8';
      _playing = true;
    }}).catch(function() {{}});
  }}
}}
function setVol(v) {{ if (_audio) _audio.volume = v; }}
document.addEventListener('click', function() {{
  if (!_playing && _audio && _audio.src && _audio.src !== window.location.href) {{
    _audio.play().then(function() {{
      document.getElementById('playBtn').textContent = '\u23F8';
      _playing = true;
    }}).catch(function() {{}});
  }}
}}, {{ once: true }});
</script>
</body>
</html>"""

# Render the full page via components.html (height 0 won't work — use a large value)
components.html(PAGE, height=9000, scrolling=True)
