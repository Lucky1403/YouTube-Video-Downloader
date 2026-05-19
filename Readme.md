# 🎬 YouTube Video Downloader

A simple Command-line(CLI) tool to download YouTube videos,playlists and audio, built with Python and yt-dlp. No GUI, no bloat — just run it, paste a link, and you're done.

---

## What it does

- Downloads any YouTube video in mp4 format
- Extracts audio as mp3 if you only want the song
- Lets you pick a specific resolution (144p all the way up to 4K) — only shows resolutions the video actually has, so no dead options
- Supports full playlist downloads
- Shows a live progress bar with speed, ETA, and file size while downloading
- Auto-updates yt-dlp every time you run it so it never breaks from YouTube's frequent changes
- Saves everything to `Downloads/Youtube Videos` on your machine — folder is created automatically on first run

---

## Requirements

You need two things installed before running this:

**Python 3.8+**
Download from [python.org](https://www.python.org/downloads/). During installation on Windows, make sure to check *"Add Python to PATH"*.

**ffmpeg**
Required for merging video and audio streams (YouTube serves them separately for anything above 360p).

- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Extract the zip and move the folder somewhere like `C:\ffmpeg`
- Add `C:\ffmpeg\bin` to your system PATH:
  - Open *System Properties → Environment Variables*
  - Find `Path` under System Variables, click Edit
  - Add a new entry: `C:\ffmpeg\bin`
- To verify it worked, open a terminal and type `ffmpeg` — you should see version info

> yt-dlp installs itself automatically the first time you run the script, so you don't need to install that manually.

---

## How to use

```
python yt_downloader.py
```

The script walks you through four steps:

1. **Paste the URL** — works with single videos and playlist links
2. **Choose type** — video (mp4) or audio only (mp3)
3. **Choose quality** — pick best available, or select a specific resolution/bitrate from a menu
4. **Playlist** — if the link is a playlist, choose whether to grab the whole thing or just the one video

Your files land in `~/Downloads/Youtube Videos/`.

---

## Example session

```
  ╔═══════════════════════════════════════════════════╗
  ║       🎬  YouTube Downloader  v3.0                ║
  ║           Powered by yt-dlp + ffmpeg              ║
  ╚═══════════════════════════════════════════════════╝

  ──────────────────────────────────────────────────────
  Step 1  ›  Video URL
  ──────────────────────────────────────────────────────

  › Paste a YouTube video or playlist URL: https://youtu.be/xxxxx

  ──────────────────────────────────────────────────────
  Step 3  ›  Video Quality
  ──────────────────────────────────────────────────────

  #    Resolution               Status
  ──── ──────────────────────── ──────────
  1    1080p  (Full HD)         ● available
  2    720p   (HD)              ● available
  3    480p   (SD)              ● available

  [0]  Best available (auto)

  › Pick a resolution [0-3]: 1

  ████████████████░░░░░░░░░░░░░░   54%   ↓ 3.1 MiB/s  ETA 9s   87 MiB

  ✅  Saved: Video Title Here.mp4
```

---

## Troubleshooting

**`ffmpeg not found` error**
ffmpeg isn't installed or isn't on your PATH. Follow the setup steps above and try again.

**Download fails with a long error message**
yt-dlp might still be outdated from a cached version. Run this once manually:
```
python -m pip install --upgrade --force-reinstall yt-dlp
```
Then try the script again.

**Video downloads but has no audio (or vice versa)**
This means ffmpeg isn't working properly. Re-check that `C:\ffmpeg\bin` is in your PATH and that typing `ffmpeg` in a terminal gives output.

**Playlist downloads only one video**
At the playlist prompt, make sure to type `Y`. The script defaults to single-video mode to avoid accidentally downloading hundreds of files.

---

## Notes

- Downloaded files can be large since the script grabs the highest quality streams/requested quality and merges them.
- This tool is for personal use only. Don't download content you don't have the right to download.

---

## Tech used

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the engine that handles all the YouTube interaction
- [ffmpeg](https://ffmpeg.org/) — merges separate video and audio tracks into a single file
- Python standard library only (os, re, sys, subprocess) — no extra dependencies beyond yt-dlp