# ==============================================================================
# Dockerfile: Anime Multiverse Live Wallpaper Engine
# Provides a self-contained container for building and playing the 1080p60 wallpaper
# ==============================================================================

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install runtime and rendering dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    mpv \
    python3 \
    python3-pil \
    python3-pip \
    mesa-utils \
    libgl1-mesa-dri \
    libgl1 \
    libegl1 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt || true

COPY scripts/ ./scripts/
COPY config/ ./config/
COPY assets/ ./assets/

RUN chmod +x ./scripts/*.sh ./scripts/*.py

# Default entrypoint runs the wallpaper script or renderer
ENTRYPOINT ["/app/scripts/run_wallpaper.sh"]
