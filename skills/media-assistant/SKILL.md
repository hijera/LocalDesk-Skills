---
name: media-assistant
description: Process video, images, and audio using ffmpeg. Use when users need to convert formats, trim videos, resize, extract frames, create GIFs, extract audio, or any media manipulation. Covers video files (.mp4, .mkv, .avi, .webm), images (.png, .jpg, .gif), and audio (.mp3, .aac, .wav).
compatibility: Requires Python 3 and ffmpeg (system install or pip install imageio-ffmpeg)
---

# Media Assistant

Toolkit for working with video, images, and audio using ffmpeg. Use this skill when the user asks to process media files: convert formats, trim, resize, extract frames, create GIFs, or similar tasks.

## Prerequisites

**FFmpeg** must be available. Two options:

1. **imageio-ffmpeg** (recommended, no system install):
   ```bash
   pip install imageio-ffmpeg
   ```
   This downloads the ffmpeg binary for your platform.

2. **System ffmpeg**: Install from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

**Check availability:**
```bash
python scripts/get_ffmpeg_path.py
```
If this fails, run `pip install imageio-ffmpeg` first.

## Workflow

1. **Get ffmpeg path** (if using run_command with explicit path):
   ```bash
   python scripts/get_ffmpeg_path.py
   ```

2. **Run ffmpeg** via `run_command`:
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 output.mkv
   ```
   If ffmpeg is in PATH (system install), use directly. If using imageio-ffmpeg, pass the path:
   ```bash
   "$(python scripts/get_ffmpeg_path.py)" -i input.mp4 -c:v libx264 output.mkv
   ```

3. **Or use execute_python** with subprocess, passing the path from `get_ffmpeg_path()`.

## Basic Operations

### Convert format
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mkv
```

### Trim video (by time)
```bash
ffmpeg -i input.mp4 -ss 10 -t 30 -c copy output.mp4
```

### Resize video
```bash
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4
```

### Extract frames
```bash
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png
ffmpeg -ss 5.5 -i input.mp4 -vframes 1 frame.png
```

### Create GIF from video
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" output.gif
```

### Extract audio
```bash
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3
```

### Image sequence to video
```bash
ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

## Full Documentation

For all ffmpeg capabilities (filters, codecs, streaming, etc.), see the official documentation:
- [ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)
- [ffmpeg.org/ffmpeg.html](https://ffmpeg.org/ffmpeg.html) — command-line options

## Reference

See [references/ffmpeg_common.md](references/ffmpeg_common.md) for more examples and patterns.
