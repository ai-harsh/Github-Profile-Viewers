#!/usr/bin/env python3
"""
Team-Ai  ·  Threaded Profile Loader  (Patchright)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Install:
    pip install patchright
    patchright install chromium
"""

from patchright.sync_api import sync_playwright
import threading, time, sys, os
from datetime import datetime

# Enable ANSI on Windows
try:
    os.system("")
except Exception:
    pass

# ─── ANSI COLOURS ─────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
WHITE   = "\033[97m"
GREY    = "\033[90m"
ORANGE  = "\033[38;5;214m"

# ─── FIXED CONFIG ─────────────────────
PROFILE_URL = "https://github.com/ai-harsh/ai-harsh"
TABS        = 10
WAIT_TIME   = 6
CYCLES      = 9999
DELAY       = 3

# ─── THREAD-SAFE COUNTERS ────────────
lock   = threading.Lock()
views  = 0
errors = 0

def ts():
    return datetime.now().strftime("%H:%M:%S")

def title_bar():
    """Update the Windows console window title."""
    with lock:
        v, e = views, errors
    title = f"Team-Ai | Views : {v} | errors : {e}"
    if os.name == "nt":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

def _prefix_ok():
    return (
        f"{GREY}[{CYAN}{ts()}{GREY}]{RESET}"
        f" {GREY}-{RESET}"
        f" {GREY}[{RESET} {GREEN}+{RESET} {GREY}]{RESET}"
        f" {GREY}-{RESET}"
        f" {GREY}[{RESET} {YELLOW}${RESET} {GREY}]{RESET}"
    )

def _prefix_err():
    return (
        f"{GREY}[{CYAN}{ts()}{GREY}]{RESET}"
        f" {GREY}-{RESET}"
        f" {GREY}[{RESET} {RED}-{RESET} {GREY}]{RESET}"
        f" {GREY}-{RESET}"
        f" {GREY}[{RESET} {YELLOW}${RESET} {GREY}]{RESET}"
    )

def log(action, data, action_color=GREEN):
    print(f"{_prefix_ok()}  {GREY}->{RESET} {action_color}{action}{RESET} {GREY}->{RESET}  {CYAN}{data}{RESET}")
    title_bar()

def log_err(action, data):
    print(f"{_prefix_err()}  {GREY}->{RESET} {RED}{action}{RESET} {GREY}->{RESET}  {CYAN}{data}{RESET}")
    title_bar()

# ─── PATCHRIGHT WORKER ────────────────
def window_worker(wid, results):
    global views, errors
    loaded = 0

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 800})

            # First tab
            page = context.new_page()
            page.goto(PROFILE_URL, wait_until="domcontentloaded")
            loaded += 1
            with lock:
                views += 1
            log("Viewed ai-harsh", f"Window {wid} | Tab 1", GREY)

            # Remaining tabs
            for i in range(2, TABS + 1):
                try:
                    p = context.new_page()
                    p.goto(PROFILE_URL, wait_until="domcontentloaded")
                    loaded += 1
                    with lock:
                        views += 1
                    log("Viewed ai-harsh", f"Window {wid} | Tab {i}", GREY)
                except Exception:
                    with lock:
                        errors += 1
                    log_err("Failed To Load Tab", f"Window {wid} | Tab {i}")

            log("Viewing the page", f"Window {wid} | {WAIT_TIME}s", ORANGE)
            time.sleep(WAIT_TIME)
            log("Successfully Got Views", f"{loaded}", GREEN)

            browser.close()

    except Exception as e:
        with lock:
            errors += 1
        log_err("Window crashed", f"Window {wid} | {e}")

    results[wid] = loaded

# ─── CYCLE ────────────────────────────
def run_cycle(cycle_num, windows):
    log("Launching Cycle", f"#{cycle_num} | {windows} threads", CYAN)

    threads = []
    results = {}

    for w in range(1, windows + 1):
        t = threading.Thread(target=window_worker, args=(w, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    cycle_loads = sum(results.values())
    with lock:
        v, e = views, errors
    log("Cycle complete", f"#{cycle_num} | +{cycle_loads} views | Total: {v}", GREEN)

# ─── MAIN ─────────────────────────────
def main():
    os.system("cls" if os.name == "nt" else "clear")

    print(f" {CYAN}{BOLD}Team-Ai{RESET}  {GREY}|{RESET}  {WHITE}Threaded Profile Loader{RESET}")
    print(f" {GREY}{'━' * 50}{RESET}")
    print()
    while True:
        raw = input(f" {YELLOW}⚙{RESET}  {WHITE}Enter number of threads:{RESET} ").strip()
        if raw == "":
            windows = 5
            break
        try:
            windows = int(raw)
            if 1 <= windows <= 50:
                break
            print(f" {RED}  Must be between 1 and 50{RESET}")
        except ValueError:
            print(f" {RED}  Enter a valid number{RESET}")

    os.system("cls" if os.name == "nt" else "clear")
    title_bar()

    for cycle in range(1, CYCLES + 1):
        run_cycle(cycle, windows)

        if cycle < CYCLES:
            log("Waiting before next cycle", f"{DELAY}s", YELLOW)
            time.sleep(DELAY)

    with lock:
        v, e = views, errors
    print(f"\n {GREEN}Done!{RESET}  Views: {GREEN}{v}{RESET}  |  Errors: {RED}{e}{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        with lock:
            v, e = views, errors
        print(f"\n\n {YELLOW}Stopped.{RESET}  Views: {GREEN}{v}{RESET}  |  Errors: {RED}{e}{RESET}")
