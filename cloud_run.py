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

# ─── Step 3: Check required environment variables ────────────────────────────
required_vars = ["TELEGRAM_TOKEN", "AUTHORIZED_CHAT_ID"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing env vars: {', '.join(missing)}")
    print("   Telegram remote control will not work without these.")
else:
    print("✅ Telegram env vars found")

# ─── Step 4: Check REMOTION_PROJECT_PATH ─────────────────────────────────────
remotion_path = os.getenv("REMOTION_PROJECT_PATH")
if remotion_path:
    if Path(remotion_path).exists():
        print(f"✅ Remotion project found at: {remotion_path}")
    else:
        print(f"⚠️  REMOTION_PROJECT_PATH set but folder not found: {remotion_path}")
else:
    print("⚠️  REMOTION_PROJECT_PATH not set")

# ─── Step 5: Auto-answer interactive mode prompt (select mode 1 = Autonomous) ─
sys.stdin = io.StringIO("1\n")

# ─── Step 6: Launch the main server ──────────────────────────────────────────
print("🦁 Launching RemoQwen-MCP server (Eternal Watcher)...")
print("─" * 50)

try:
    exec(open("run.py").read())
except KeyboardInterrupt:
    print("\n👋 Server stopped by user.")
except Exception as e:
    print(f"❌ Server crashed: {e}")
    sys.exit(1)
  
