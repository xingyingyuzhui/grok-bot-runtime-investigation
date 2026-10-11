#!/usr/bin/env bash
# Usage: launch.sh <app> [extra mcp flags]   app = photocraft|vectorcraft|filmcraft|lightcraft|pdfcraft|effectcraft|designcraft|wordcraft|gridcraft|deckcraft|cadcraft|soundcraft
# Starts that app's built-in MCP server on stdio (headless engine). Work dir: /workspace/media-mcp/work
set -e; app="$1"; shift || true; W="${CRAFT_WORKDIR:-/workspace/media-mcp/work}"; mkdir -p "$W"
bin=$(ls /workspace/artcraft/$app/*/bin/$app-cli 2>/dev/null | head -1)
[ -x "$bin" ] || { echo "unknown app: $app" >&2; exit 2; }
case $app in
  photocraft)  exec "$bin" mcp --automation-read-root / --automation-write-root "$W" "$@";;
  vectorcraft) exec "$bin" mcp --headless "$@";;
  pdfcraft)    exec "$bin" mcp --root / "$@";;
  *)           exec "$bin" mcp "$@";;
esac
