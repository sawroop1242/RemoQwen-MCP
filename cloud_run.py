import os
import sys
import base64
import io
from pathlib import Path

print("🚀 RemoQwen-MCP — Cloud Launcher Starting...")

# ─── Step 1: Setup rclone config from environment variable ───────────────────
rclone_config_b64 = os.getenv("RCLONE_CONFIG_BASE64")

if rclone_config_b64:
    try:
        config_dir = Path.home() / ".config" / "rclone"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "rclone.conf"
        config_path.write_bytes(base64.b64decode(rclone_config_b64))
        print("✅ rclone config loaded from RCLONE_CONFIG_BASE64")
    except Exception as e:
        print(f"⚠️  rclone config failed: {e}")
else:
    print("⚠️  RCLONE_CONFIG_BASE64 not set — Google Drive upload will not work")

# ─── Step 2: Set cloud environment flags ─────────────────────────────────────
os.environ.setdefault("MCP_MODE", "autonomous")
os.environ.setdefault("HEADLESS", "true")
os.environ.setdefault("LOG_LEVEL", "INFO")

# ─── Step 3: Fix PORT for Render ─────────────────────────────────────────────
render_port = os.getenv("PORT", "8000")
os.environ["PORT"] = render_port
os.environ["HOST"] = "0.0.0.0"
print(f"✅ Server will bind to 0.0.0.0:{render_port}")

# ─── Step 4: Check required environment variables ────────────────────────────
required_vars = ["TELEGRAM_TOKEN", "AUTHORIZED_CHAT_ID"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing env vars: {', '.join(missing)}")
else:
    print("✅ Telegram env vars found")

# ─── Step 5: Setup REMOTION_PROJECT_PATH safely ──────────────────────────────
# /tmp is always writable on Render, Railway, and any cloud server
# Do NOT use /app — Render does not allow writing there
remotion_path = os.getenv("REMOTION_PROJECT_PATH", "/tmp/my-video")

try:
    Path(remotion_path).mkdir(parents=True, exist_ok=True)
    os.environ["REMOTION_PROJECT_PATH"] = remotion_path
    print(f"✅ Remotion project folder ready: {remotion_path}")
except PermissionError:
    fallback = "/tmp/my-video"
    print(f"⚠️  Permission denied for {remotion_path} — using fallback: {fallback}")
    Path(fallback).mkdir(parents=True, exist_ok=True)
    os.environ["REMOTION_PROJECT_PATH"] = fallback
    print(f"✅ Fallback folder ready: {fallback}")

# ─── Step 6: Auto-answer ALL interactive prompts ─────────────────────────────
# Prompt 1: Mode selection  → "1" (Fully Autonomous)
# Prompt 2: Enable Telegram → "Y"
# Prompt 3+: any others    → "Y"
sys.stdin = io.StringIO("1\nY\nY\nY\n")
print("✅ Interactive prompts will be auto-answered")

# ─── Step 7: Launch the main server ──────────────────────────────────────────
print("🦁 Launching RemoQwen-MCP server (Eternal Watcher)...")
print("─" * 50)

try:
    exec(open("run.py").read())
except KeyboardInterrupt:
    print("\n👋 Server stopped.")
except Exception as e:
    print(f"❌ Server crashed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
