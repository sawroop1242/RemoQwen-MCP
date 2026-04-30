# src/tools/gdrive_ops.py
import subprocess
import os
from pathlib import Path

def upload_to_gdrive(local_path: str, gdrive_folder: str = "RemoQwen-Renders") -> dict:
    """Upload a file or folder to Google Drive using rclone."""
    rclone_remote = os.getenv("RCLONE_REMOTE_NAME", "gdrive")
    destination = f"{rclone_remote}:{gdrive_folder}"

    result = subprocess.run(
        ["rclone", "copy", local_path, destination, "--progress"],
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode == 0:
        return {
            "success": True,
            "message": f"✅ Uploaded to Google Drive: {destination}",
            "output": result.stdout
        }
    else:
        return {
            "success": False,
            "message": f"❌ Upload failed",
            "error": result.stderr
        }

def list_gdrive_folder(gdrive_folder: str = "RemoQwen-Renders") -> dict:
    """List files in a Google Drive folder via rclone."""
    rclone_remote = os.getenv("RCLONE_REMOTE_NAME", "gdrive")
    result = subprocess.run(
        ["rclone", "ls", f"{rclone_remote}:{gdrive_folder}"],
        capture_output=True, text=True, timeout=60
    )
    return {"files": result.stdout, "error": result.stderr}
