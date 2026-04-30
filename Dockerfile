# ─── Base Image ───────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ─── System Dependencies ──────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    bash \
    unzip \
    ffmpeg \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# ─── Install Node.js 20 ───────────────────────────────────────────────────────
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && node --version \
    && npm --version

# ─── Install rclone ───────────────────────────────────────────────────────────
RUN curl https://rclone.org/install.sh | bash \
    && rclone --version

# ─── Set Working Directory ────────────────────────────────────────────────────
WORKDIR /app

# ─── Copy Project Files ───────────────────────────────────────────────────────
COPY . .

# ─── Install Python Dependencies ──────────────────────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ─── Create writable folders ──────────────────────────────────────────────────
RUN mkdir -p /tmp/my-video /tmp/renders

# ─── Expose Port ──────────────────────────────────────────────────────────────
EXPOSE 8000

# ─── Start Command ────────────────────────────────────────────────────────────
CMD ["python", "cloud_run.py"]


