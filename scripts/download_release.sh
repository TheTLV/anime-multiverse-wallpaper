#!/usr/bin/env bash
# ==============================================================================
# Download Pre-rendered Master Video from GitHub Releases
# ==============================================================================

set -euo pipefail

REPO="TheTLV/anime-multiverse-wallpaper"
RELEASE_TAG="v1.0.0"
TARGET_FILE="azur_multiverse_odyssey.mp4"
DEST_DIR="$HOME/.local/share/gnome-wallpaper-engine/backgrounds"
mkdir -p "$DEST_DIR"

echo "[DOWNLOAD] Fetching pre-rendered wallpaper release ($RELEASE_TAG)..."

if command -v gh >/dev/null 2>&1; then
    echo "Using GitHub CLI (gh)..."
    gh release download "$RELEASE_TAG" --repo "$REPO" --pattern "$TARGET_FILE" --dir "$DEST_DIR" --clobber
    echo "[SUCCESS] Wallpaper saved to $DEST_DIR/$TARGET_FILE"
else
    DOWNLOAD_URL="https://github.com/$REPO/releases/download/$RELEASE_TAG/$TARGET_FILE"
    echo "Using curl: $DOWNLOAD_URL"
    curl -L --progress-bar -o "$DEST_DIR/$TARGET_FILE" "$DOWNLOAD_URL"
    echo "[SUCCESS] Wallpaper downloaded to $DEST_DIR/$TARGET_FILE"
fi
