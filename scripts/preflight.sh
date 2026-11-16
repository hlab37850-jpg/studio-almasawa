#!/usr/bin/env bash
# Read-only environment probe. Does not install packages or modify the project.
set +e
echo "=== SYSTEM ==="
date -u +"UTC %Y-%m-%dT%H:%M:%SZ" 2>/dev/null || true
uname -a 2>/dev/null || true
echo "ARCH=$(uname -m 2>/dev/null)"
echo "OS=$(uname -s 2>/dev/null)"
echo
echo "=== GPU ==="
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
  echo "NVIDIA_SMI_EXIT=$?"
else
  echo "NVIDIA_SMI=NOT_FOUND"
fi
echo
echo "=== RUNTIME TOOLS ==="
for tool in python3 python node npm ffmpeg ffprobe git curl; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '%s=' "$tool"
    case "$tool" in
      python3|python) "$tool" --version 2>&1 ;;
      node|npm|git) "$tool" --version 2>&1 ;;
      ffmpeg|ffprobe) "$tool" -version 2>&1 | head -n 1 ;;
      curl) "$tool" --version 2>&1 | head -n 1 ;;
    esac
  else
    echo "$tool=NOT_FOUND"
  fi
done
echo
echo "=== PYTHON PACKAGES ==="
if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY'
import importlib.util
for name in ("torch", "diffusers", "edge_tts", "TTS", "faster_whisper", "whisperx", "camel_tools", "mishkal"):
    print(f"{name}={'AVAILABLE' if importlib.util.find_spec(name) else 'NOT_INSTALLED'}")
try:
    import torch
    print(f"torch_version={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"cuda_device={torch.cuda.get_device_name(0)}")
        print(f"cuda_vram_bytes={torch.cuda.get_device_properties(0).total_memory}")
except Exception as exc:
    print(f"torch_probe_error={type(exc).__name__}: {exc}")
PY
fi
echo
echo "=== NETWORK (HTTPS HEAD, 10s timeout) ==="
if command -v curl >/dev/null 2>&1; then
  for url in https://github.com https://pypi.org https://huggingface.co https://www.microsoft.com; do
    code=$(curl -L -I -sS --max-time 10 -o /dev/null -w '%{http_code}' "$url" 2>&1)
    rc=$?
    printf '%s HTTP=%s CURL_EXIT=%s\n' "$url" "$code" "$rc"
  done
else
  echo "NETWORK_PROBE=SKIPPED_CURL_NOT_FOUND"
fi
echo
echo "=== DISK ==="
df -h . 2>/dev/null || true
echo
echo "=== PROJECT ROOT ==="
pwd
find . -maxdepth 2 -type f -not -path './.git/*' -print 2>/dev/null | sort | head -n 200
