#!/bin/bash
# Decodes the base64 rclone config from env var and saves it
if [ -n "$RCLONE_CONFIG_BASE64" ]; then
  mkdir -p ~/.config/rclone
  echo "$RCLONE_CONFIG_BASE64" | base64 -d > ~/.config/rclone/rclone.conf
  echo "✅ rclone config loaded from env"
fi
