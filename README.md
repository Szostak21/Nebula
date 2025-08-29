# Nebula

High‑speed minimalist perspective runner built with **Python** and **Kivy**. You pilot a tiny ship racing forward over an infinite grid, dodging gaps and chasing a climbing score while the playfield warps in pseudo‑3D.

## 🎮 Core Gameplay
- Procedurally extending track: new tiles spawn ahead as you move
- Increasing speed curve tied to distance (score)
- One‑touch / two‑arrow controls (desktop & mobile friendly)
- Instant restart loop for fast iteration
- Built‑in tutorial messages for new players (auto hides once you reach a threshold)

## ✨ Features
- Perspective transform effect for lane lines & tiles
- Dynamic difficulty: gradual speed ramp up to a cap
- Best score persistence via simple text file
- Separate menus for Start and Modes (extensible for future variants)
- Clean separation of logic: build, update, transforms, user interaction modules

## 🗂 Project Structure
```
Nebula/
  audio/           # Sound effects & music (wav)
  fonts/           # Custom fonts (Eurostile, Sackers Gothic)
  images/          # Background art
  src/             # Game source + KV UI layouts
    main.py        # App bootstrap + root widget
    build.py       # Object creation helpers
    updates.py     # Per‑frame state updates & scoring
    transforms.py  # Perspective math utilities
    user_interactions.py # Input handlers
    menu.kv, modes.kv, nebula.kv # UI layout definitions
    best_score.txt # Simple persisted high score
  README.md
  .gitignore
```

## 🚀 Run Locally
Install dependencies (Kivy) and run the game:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install kivy
python src/main.py
```

## 🧩 Extending Modes
The `Modes` screen already lays out toggle placeholders (`toggle_button_1` ...). Ideas:
- Mirror mode (left/right swap)
- Narrow lanes (reduce spacing)
- Sudden death (higher speed cap)
- Color shift / dynamic themes

Each mode can map to flags on `MainWidget` and alter update math.

## 🛠 Technical Highlights
- Uses `resource_add_path` to simplify asset referencing (just font filenames)
- Perspective handled by transform utilities for consistent reuse
- Modular KV files keep visual structure declarative
- Minimal stateful persistence (text high score) to avoid DB overhead

## 📦 Packaging (Android / Desktop)
A `buildozer.spec` is present; to try Android packaging:
```bash
pip install buildozer
buildozer init   # (already done)
buildozer -v android debug
```
Outputs will appear under `.buildozer/` (ignored by git).

## 🧪 Possible Next Improvements
- Add unit tests for math in `transforms.py`
- Introduce sound management (preload & volume control)
- Particle / trail effects for the ship
- Settings persistence (JSON) instead of bare text
- CI workflow (GitHub Actions) to lint & package

## 📸 Screens / Media (Add Later)
Add GIF or short MP4 of gameplay for portfolio visibility.

## 🏷 License
Add a license you prefer (MIT recommended) before publishing.

## 🙋 About
This project showcases rapid prototyping of an arcade mechanic with Python + Kivy, emphasizing clean module separation, progressive difficulty, and portability for desktop/mobile.

---
Feel free to fork, experiment with new modes, or integrate new visual themes.
