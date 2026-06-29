# 🎂 Happy Birthday Puja — Premium Cinematic Birthday Website

A luxury interactive birthday experience built with Streamlit.

## ✨ Features

- **Cinematic Intro** — Stars appear on a black screen, then "A Special Day" → "Happy Birthday" → "PUJA ❤️"
- **Animated Background** — Floating hearts, stars, balloons, confetti particles on a canvas
- **Animated Hero** — Bouncing birthday cake with flickering candles; click to blow them out!
- **Live Countdown** — Hours/minutes/seconds remaining in the birthday day
- **Photo Gallery** — Polaroid-style cards with hover zoom; auto-loads from `images/` folder
- **Memory Timeline** — Scroll-triggered animated cards: Childhood → School → College → Today → Future
- **Birthday Letter** — Click the envelope to open and typewriter-animate the letter
- **Wishes Section** — Glowing hover cards for Health, Success, Happiness, etc.
- **Surprise Button** — Launches real canvas fireworks + floating emojis + reveals "I Love You Sister ❤️"
- **Rotating Quotes** — Fades through 8 inspirational birthday quotes every 8 seconds
- **Music Player** — Fixed bottom-right player with play/pause/volume; auto-starts on first interaction
- **Glassmorphism UI** — Frosted glass cards, gradient animations, rose-gold/lavender palette

## 📁 Folder Structure

```
Birthday/
├── app.py              ← Main application (this file)
├── requirements.txt
├── README.md
├── images/             ← Drop photos here (jpg/png/gif/webp)
│   └── (your photos)
└── music/
    └── birthday.mp3    ← Add background music here
```

## 🚀 Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploying to Streamlit Community Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as the main file
4. Deploy!

> **Note on music:** Streamlit Community Cloud cannot serve local binary files directly.
> For music on cloud, host the `.mp3` on a CDN or use a public URL in the audio `src`.

## 📸 Adding Photos

Drop any `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp` images into the `images/` folder.
The gallery automatically detects and displays them as polaroid cards.

## 🎨 Color Palette

| Name | Hex |
|------|-----|
| Light Gold | `#d4af60` |
| Rose Lavender | `#c084bc` |
| Sky Blue | `#93c5fd` |
| Soft Pink | `#fda4af` |
| Deep Night | `#0a0010` |

---

Made with ❤️ · Especially for **Puja** · By Your Brother
