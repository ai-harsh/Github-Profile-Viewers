# Team-Ai

> Fast, multi-threaded profile viewer built on [Patchright](https://github.com/nicksonfas/patchright) — undetectable browser automation.

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey.svg)
![Views](https://komarev.com/ghpvc/?username=ai-harsh&label=Repo%20Views&color=brightgreen&style=flat&repo=Github-Profile-Viewers)

---

## What it does

Spawns multiple Chromium windows in parallel threads, each opening configurable tabs to load a target profile. Views and errors are tracked live in the console title bar.

```
Team-Ai | Views : 1628 | errors : 12          ← window title, updates in real-time
```

```
[19:30:05] - [ + ] - [ $ ]  -> Viewed ai-harsh        ->  Window 1 | Tab 1
[19:30:06] - [ + ] - [ $ ]  -> Viewed ai-harsh        ->  Window 1 | Tab 2
[19:30:07] - [ + ] - [ $ ]  -> Viewing the page       ->  Window 1 | 6s
[19:30:13] - [ + ] - [ $ ]  -> Successfully Got Views ->  10
[19:30:13] - [ + ] - [ $ ]  -> Cycle complete          ->  #1 | +50 views | Total: 50
[19:30:16] - [ - ] - [ $ ]  -> Failed To Load Tab     ->  Window 3 | Tab 4
```

---

## Setup

```bash
pip install patchright
patchright install chromium
```

## Usage

```bash
python main.py
```

You'll be asked for the thread count (number of parallel browser windows). That's it — the tool handles the rest.

Press **Ctrl+C** to stop cleanly.

---

## Config

All settings are at the top of `main.py`:

```python
PROFILE_URL = "https://github.com/ai-harsh/ai-harsh"
TABS        = 10       # tabs per browser window
WAIT_TIME   = 6        # seconds to hold pages open
CYCLES      = 9999     # number of cycles (set high for continuous)
DELAY       = 3        # pause between cycles
```

Thread count is configured at runtime.

---

## How it works

1. Launches `N` threads, each running its own Patchright (Playwright) browser instance
2. Each browser opens `TABS` pages pointed at the target URL
3. Waits `WAIT_TIME` seconds for pages to register, then closes the browser
4. Repeats for `CYCLES` rounds with `DELAY` between each

All counters are thread-safe. The console window title updates after every action.

### Why Patchright?

Patchright is a patched build of Playwright that strips automation indicators — no `navigator.webdriver` flag, no leaked Chrome DevTools Protocol signals. Standard Playwright and Selenium get flagged; Patchright doesn't.

---

## Requirements

- Python 3.8+
- Patchright (`pip install patchright`)
- Chromium (installed via `patchright install chromium`)

---

## Disclaimer

For educational and personal use only. Respect the terms of service of any website you interact with.

---

**[Team-Ai](https://github.com/ai-harsh)** · Built for speed.
