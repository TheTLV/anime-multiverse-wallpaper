#!/usr/bin/env bash
# ==============================================================================
# Anime Multiverse Live Wallpaper - Standalone Runner
# Runs seamless 1080p60 hardware-accelerated wallpaper via mpv
# Compatible with Wayland (GNOME, Sway, Hyprland) and X11 (KDE, XFCE, i3)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DEFAULT_WALLPAPER="$HOME/.local/share/gnome-wallpaper-engine/backgrounds/azur_multiverse_odyssey.mp4"
FALLBACK_WALLPAPER="$ROOT_DIR/azur_multiverse_odyssey.mp4"

WALLPAPER_FILE="${1:-$DEFAULT_WALLPAPER}"

if [ ! -f "$WALLPAPER_FILE" ] && [ -f "$FALLBACK_WALLPAPER" ]; then
    WALLPAPER_FILE="$FALLBACK_WALLPAPER"
fi

if [ ! -f "$WALLPAPER_FILE" ]; then
    echo "[ERROR] Wallpaper file not found: $WALLPAPER_FILE"
    echo "Please download the pre-rendered release via: ./scripts/download_release.sh"
    echo "Or render it using: ./scripts/render_wallpaper.py"
    exit 1
fi

echo "[LAUNCHER] Starting Anime Multiverse Wallpaper..."
echo "[LAUNCHER] File: $WALLPAPER_FILE"

# Detect display server
if [ -n "${WAYLAND_DISPLAY:-}" ]; then
    echo "[LAUNCHER] Display server: Wayland ($WAYLAND_DISPLAY)"
    GPU_CONTEXT="wayland"
else
    echo "[LAUNCHER] Display server: X11 ($DISPLAY)"
    GPU_CONTEXT="x11"
fi

# Detect screen geometry (default to 1920x1080)
GEOMETRY="${GEOMETRY:-1920x1080+0+0}"

# Check for existing wallpaper player and terminate it
pkill -f "gwe-wallpaper-multiverse" 2>/dev/null || true

# Launch MPV with optimal low-overhead, hardware-accelerated parameters
exec mpv \
    --vo=gpu \
    --gpu-context="$GPU_CONTEXT" \
    --hwdec=auto \
    --no-border \
    --loop-file=inf \
    --no-audio \
    --force-window=immediate \
    --title=gwe-wallpaper-multiverse \
    --geometry="$GEOMETRY" \
    --keepaspect=yes \
    --keepaspect-window=no \
    --no-auto-window-resize \
    --panscan=1.0 \
    --video-unscaled=no \
    --osc=no \
    --osd-bar=no \
    --input-default-bindings=no \
    --input-vo-keyboard=no \
    --cursor-autohide=no \
    --no-terminal \
    "$WALLPAPER_FILE"
