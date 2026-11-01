#!/usr/bin/env bash
# ==============================================================================
# One-Click Setup & Deployment for Anime Multiverse Live Wallpaper
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
GWE_DIR="$HOME/.local/share/gnome-wallpaper-engine/backgrounds"
TARGET_NAME="azur_multiverse_odyssey.mp4"

echo "=========================================================="
echo "   Anime Multiverse Live Wallpaper Engine - Setup"
echo "=========================================================="

# 1. Check system dependencies
echo "[1/4] Checking system tools..."
for tool in ffmpeg mpv; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "[WARN] '$tool' is not installed."
        echo "Install via: sudo apt install $tool (Debian/Ubuntu) or sudo pacman -S $tool (Arch)"
    else
        echo "  ✓ $tool found: $(command -v "$tool")"
    fi
done

# 2. Make all scripts executable
echo "[2/4] Setting execution permissions..."
chmod +x "$SCRIPT_DIR"/*.sh "$SCRIPT_DIR"/*.py 2>/dev/null || true

# 3. Deploy to GNOME Wallpaper Engine (if directory exists or can be created)
echo "[3/4] Configuring wallpaper file location..."
mkdir -p "$GWE_DIR"

if [ -f "$GWE_DIR/$TARGET_NAME" ]; then
    echo "  ✓ Master wallpaper is already present in GNOME Wallpaper Engine directory: $GWE_DIR/$TARGET_NAME"
elif [ -f "$ROOT_DIR/$TARGET_NAME" ]; then
    echo "  → Copying wallpaper to GNOME Wallpaper Engine directory..."
    cp "$ROOT_DIR/$TARGET_NAME" "$GWE_DIR/"
    [ -f "$ROOT_DIR/${TARGET_NAME%.*}-thumb.jpg" ] && cp "$ROOT_DIR/${TARGET_NAME%.*}-thumb.jpg" "$GWE_DIR/"
else
    echo "  → Wallpaper not found locally. Fetching via download script..."
    "$SCRIPT_DIR/download_release.sh" || true
fi

# 4. GNOME integration or systemd user service setup
echo "[4/4] Setting up wallpaper auto-start..."
if command -v gsettings >/dev/null 2>&1 && gsettings list-schemas | grep -q "gnome-wallpaper-engine"; then
    echo "  → Activating via GNOME Wallpaper Engine extension..."
    gsettings set org.gnome.shell.extensions.gnome-wallpaper-engine current-wallpaper "$TARGET_NAME"
    echo "  ✓ Wallpaper activated in GNOME Wallpaper Engine!"
else
    echo "  → Setting up systemd user service for standalone auto-start..."
    SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SYSTEMD_USER_DIR"
    cat <<EOF > "$SYSTEMD_USER_DIR/anime-wallpaper.service"
[Unit]
Description=Anime Multiverse Live Wallpaper
After=graphical-session.target

[Service]
Type=simple
ExecStart=$SCRIPT_DIR/run_wallpaper.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
    systemctl --user daemon-reload 2>/dev/null || true
    echo "  ✓ User service created: ~/.config/systemd/user/anime-wallpaper.service"
    echo "  Enable on boot via: systemctl --user enable --now anime-wallpaper.service"
fi

echo "=========================================================="
echo "   Setup Complete! Enjoy your live wallpaper!"
echo "=========================================================="
