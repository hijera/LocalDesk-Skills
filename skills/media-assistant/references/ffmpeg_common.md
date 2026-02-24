# FFmpeg: Common Operations

Reference for frequently used ffmpeg commands. For full documentation, see [ffmpeg.org](https://ffmpeg.org/documentation.html).

## Getting ffmpeg Path

Before running ffmpeg, get the executable path:

```bash
python scripts/get_ffmpeg_path.py
```

Use the output as the ffmpeg executable path in run_command. If ffmpeg is not found: `pip install imageio-ffmpeg`

## Basic Operations

### Convert video format

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mkv
```

### Trim video (by time)

```bash
# Start at 10s, duration 30s
ffmpeg -i input.mp4 -ss 10 -t 30 -c copy output.mp4

# Start at 10s, end at 40s
ffmpeg -i input.mp4 -ss 10 -to 40 -c copy output.mp4
```

### Resize video

```bash
# Scale to 1280x720
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4

# Scale to half size
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" -c:a copy output.mp4
```

### Extract frames to images

```bash
# One frame per second
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png

# Frame at 5.5 seconds
ffmpeg -ss 5.5 -i input.mp4 -vframes 1 frame.png
```

### Create GIF from video

```bash
# Simple conversion (may be large)
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" output.gif

# With palette for better quality
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i input.mp4 -i palette.png -lavfi "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```

### Extract audio

```bash
ffmpeg -i input.mp4 -vn -acodec copy output.aac
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3
```

### Image sequence to video

```bash
ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

### Screenshot at specific time

```bash
ffmpeg -ss 00:01:30 -i input.mp4 -vframes 1 screenshot.png
```

## General Pattern

```bash
ffmpeg -i input [options] output
```

- `-i` input file
- `-c:v` video codec (libx264, copy, etc.)
- `-c:a` audio codec (aac, copy, etc.)
- `-vf` video filters
- `-ss` seek to position (before -i for fast seek)
- `-t` duration
- `-to` end time
