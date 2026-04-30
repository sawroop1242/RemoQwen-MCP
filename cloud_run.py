# Add at top of cloud_run.py
import subprocess
subprocess.run(["bash", "setup_rclone.sh"])

# cloud_run.py — headless cloud launcher (no interactive prompts)
import os
import sys

# Force autonomous mode (no terminal input needed)
os.environ.setdefault("MCP_MODE", "autonomous")
os.environ.setdefault("HEADLESS", "true")

# Patch stdin so interactive prompts are skipped
import io
sys.stdin = io.StringIO("1\n")  # auto-select mode 1 (Fully Autonomous)

# Now import and run the server
exec(open("run.py").read())
