import os
import re
import sys
import subprocess

try:
    import yt_dlp
except ImportError:
    print("  yt-dlp not found, installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
    import yt_dlp


SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "Youtube Videos")


RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def banner():
    print(f"""
{CYAN}{BOLD}  ╔═══════════════════════════════════════════════════╗
  ║       🎬  YouTube Downloader  v3.0                ║
  ║           Powered by yt-dlp + ffmpeg              ║
  ╚═══════════════════════════════════════════════════╝{RESET}
""")


def section(title):
    print(f"\n{CYAN}{'─' * 52}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{CYAN}{'─' * 52}{RESET}")


def ok(msg):
    print(f"\n{GREEN}  ✅  {msg}{RESET}")


def warn(msg):
    print(f"{YELLOW}  ⚠   {msg}{RESET}")


def err(msg):
    print(f"{RED}  ❌  {msg}{RESET}")


def detail(label, value):
    print(f"  {DIM}{label:<14}{RESET}{BOLD}{value}{RESET}")


def ask(msg):
    return input(f"\n{CYAN}  ›{RESET} {msg} ").strip()



def update_yt_dlp():
    section("Checking yt-dlp")
    print(f"  {DIM}Making sure yt-dlp is up to date...{RESET}")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", "yt-dlp"],
        capture_output=True, text=True
    )
    if "Successfully installed" in result.stdout:
        ok("yt-dlp updated to the latest version")
    else:
        ok("yt-dlp is already up to date")


def progress_hook(d):
    if d["status"] == "downloading":
        percent    = d.get("_percent_str", "?").strip()
        speed      = d.get("_speed_str",   "?").strip()
        eta        = d.get("_eta_str",     "?").strip()
        size       = d.get("_total_bytes_str",
                     d.get("_total_bytes_estimate_str", "?")).strip()
        downloaded = d.get("downloaded_bytes", 0)
        total      = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
        filled     = int(downloaded / total * 30)
        bar        = f"{GREEN}{'█' * filled}{DIM}{'░' * (30 - filled)}{RESET}"
        print(
            f"\r  {bar}  {BOLD}{percent:>6}{RESET}  "
            f"{DIM}↓ {speed:<12}  ETA {eta:<8}  {size}{RESET}",
            end="", flush=True
        )
    elif d["status"] == "finished":
        fname = os.path.basename(d.get("filename", ""))
        print(f"\r{' ' * 80}\r", end="")
        ok(f"Saved: {fname}")
    elif d["status"] == "error":
        print()
        err("Something went wrong with this file.")



RESOLUTIONS = [
    ("4K  / 2160p",      2160),
    ("2K  / 1440p",      1440),
    ("1080p  (Full HD)", 1080),
    ("720p   (HD)",       720),
    ("480p   (SD)",       480),
    ("360p",              360),
    ("240p",              240),
    ("144p   (lowest)",   144),
]


def pick_quality(url):
    print(f"\n  {DIM}Checking available resolutions...{RESET}")

    try:
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True,
                                "skip_download": True, "noplaylist": True}) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        err(f"Could not check formats: {e}")
        return "bestvideo+bestaudio/best"

    formats     = info.get("formats", [])
    available_h = sorted(
        {f["height"] for f in formats
         if f.get("height") and f.get("vcodec") != "none"},
        reverse=True
    )

    if not available_h:
        warn("Couldn't read resolutions — will grab the best available.")
        return "bestvideo+bestaudio/best"

    known_h    = {h for _, h in RESOLUTIONS}
    menu       = [(lbl, h) for lbl, h in RESOLUTIONS if h in available_h]

    for h in available_h:
        if h not in known_h:
            menu.append((f"{h}p", h))
    menu.sort(key=lambda x: x[1], reverse=True)

    print(f"\n  {BOLD}{'#':<4} {'Resolution':<24} {'Status'}{RESET}")
    print(f"  {'─'*4} {'─'*24} {'─'*10}")
    for i, (lbl, _) in enumerate(menu, 1):
        print(f"  {BOLD}{i:<4}{RESET} {lbl:<24} {GREEN}● available{RESET}")
    print(f"\n  {DIM}[0]  Best available (auto){RESET}")

    while True:
        raw = ask(f"Pick a resolution [0-{len(menu)}]  (Enter = best):")
        if raw == "" or raw == "0":
            return "bestvideo+bestaudio/best"
        if raw.isdigit() and 1 <= int(raw) <= len(menu):
            chosen_h   = menu[int(raw) - 1][1]
            chosen_lbl = menu[int(raw) - 1][0].strip()
            ok(f"Selected: {chosen_lbl}")
            return (
                f"bestvideo[height<={chosen_h}][ext=mp4]+bestaudio[ext=m4a]/"
                f"bestvideo[height<={chosen_h}]+bestaudio/"
                f"best[height<={chosen_h}]/best"
            )
        warn("Please enter a number from the list.")



AUDIO_QUALITIES = [
    ("320 kbps  — highest quality", "320"),
    ("256 kbps",                    "256"),
    ("192 kbps  — recommended",     "192"),
    ("128 kbps",                    "128"),
    ("96  kbps  — smallest file",   "96"),
]


def pick_audio_quality():
    print(f"\n  {BOLD}{'#':<4} Bitrate{RESET}")
    print(f"  {'─'*4} {'─'*30}")
    for i, (lbl, _) in enumerate(AUDIO_QUALITIES, 1):
        print(f"  {BOLD}{i:<4}{RESET} {lbl}")

    while True:
        raw = ask("Pick audio quality [1-5]  (Enter = 192 kbps):")
        if raw == "":
            return "192"
        if raw.isdigit() and 1 <= int(raw) <= len(AUDIO_QUALITIES):
            chosen = AUDIO_QUALITIES[int(raw) - 1]
            ok(f"Selected: {chosen[0].strip()}")
            return chosen[1]
        warn("Please enter a number from the list.")



def download(url, fmt, audio_only=False, audio_quality="192", playlist=False):

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        ok(f"Created folder: {SAVE_FOLDER}")

    base_opts = {
        "outtmpl"            : os.path.join(SAVE_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist"         : not playlist,
        "progress_hooks"     : [progress_hook],
        "merge_output_format": "mp4",
        "quiet"              : True,
        "no_warnings"        : True,
    }

    if audio_only:
        ydl_opts = {
            **base_opts,
            "format"         : "bestaudio/best",
            "postprocessors" : [{
                "key"             : "FFmpegExtractAudio",
                "preferredcodec"  : "mp3",
                "preferredquality": audio_quality,
            }],
        }
    else:
        ydl_opts = {**base_opts, "format": fmt}

    section("Video Info")
    try:
        with yt_dlp.YoutubeDL({**base_opts, "quiet": True}) as ydl:
            meta = ydl.extract_info(url, download=False)

        title    = meta.get("title",      "Unknown")
        uploader = meta.get("uploader",   "Unknown")
        duration = meta.get("duration",   0)
        views    = meta.get("view_count", 0)
        mins, secs = divmod(int(duration), 60)

        detail("Title",    title[:55] + ("…" if len(title) > 55 else ""))
        detail("Channel",  uploader)
        detail("Duration", f"{mins}m {secs:02d}s")
        detail("Views",    f"{views:,}" if views else "N/A")
        detail("Saving to", SAVE_FOLDER)

        if playlist and "entries" in meta:
            detail("Playlist", f"{len(list(meta['entries']))} videos")

    except Exception:
        warn("Couldn't fetch video info — carrying on anyway.")

    section("Downloading")
    print()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except yt_dlp.utils.DownloadError as e:
        err(f"Download failed: {e}")
        print(f"  {DIM}Tip: re-run the script, yt-dlp may fix itself after the update.{RESET}")
    except FileNotFoundError:
        err("ffmpeg not found!")
        print(f"  {DIM}Grab it from https://ffmpeg.org/download.html and add to PATH.{RESET}")
    except Exception as e:
        err(f"Unexpected error: {e}")



def main():
    banner()
    update_yt_dlp()

    section("Step 1  ›  Video URL")
    url = ask("Paste a YouTube video or playlist URL:")
    if not url:
        err("No URL entered. Exiting.")
        return

    section("Step 2  ›  Download Type")
    print(f"\n  {BOLD}1{RESET}  🎬  Video  (mp4)")
    print(f"  {BOLD}2{RESET}  🎵  Audio only  (mp3)")
    type_choice = ask("Select [1/2] :")
    audio_only  = type_choice == "2"

    fmt           = "bestvideo+bestaudio/best"
    audio_quality = "192"

    if audio_only:
        section("Step 3  ›  Audio Quality")
        audio_quality = pick_audio_quality()
    else:
        section("Step 3  ›  Video Quality")
        print(f"\n  {BOLD}1{RESET}  ⚡  Best available  (auto)")
        print(f"  {BOLD}2{RESET}  🎛   Choose a specific resolution")
        q_choice = ask("Select [1/2] :")
        if q_choice == "2":
            fmt = pick_quality(url)

    section("Step 4  ›  Playlist")
    pl_raw   = ask("Download the full playlist if this is a playlist link? [Y/N]:")
    playlist = pl_raw.lower() == "y"

    download(url, fmt, audio_only=audio_only, audio_quality=audio_quality, playlist=playlist)

    print(f"\n{CYAN}{'═' * 52}{RESET}")
    print(f"{BOLD}  🎉  Done!  Find your file in:{RESET}")
    print(f"  {DIM}{SAVE_FOLDER}{RESET}")
    print(f"{CYAN}{'═' * 52}{RESET}\n")


if __name__ == "__main__":
    main()