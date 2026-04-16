"""Cross-platform notification sound (short beep)."""

import platform
import subprocess
import sys


def play_notification() -> None:
    """Play a short notification sound. Fails silently if unavailable."""
    try:
        _play()
    except Exception:
        pass


def _play() -> None:
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.Beep(880, 180)
    elif system == "Darwin":
        subprocess.Popen(["afplay", "/System/Library/Sounds/Ping.aiff"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # Linux — try paplay / aplay / speaker-test fallbacks
        for cmd in [
            ["paplay", "/usr/share/sounds/freedesktop/stereo/message.oga"],
            ["aplay", "/usr/share/sounds/alsa/Front_Center.wav"],
        ]:
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                return
            except FileNotFoundError:
                continue
        # Last resort: terminal bell
        print("\a", end="", flush=True)
