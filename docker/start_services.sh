#!/usr/bin/env bash
set -euo pipefail

api_args=(
  "--host" "0.0.0.0"
  "--port" "${API_PORT:-8000}"
  "--device" "${DEVICE:-cpu}"
)

if [[ -n "${MODEL_PATH:-}" ]]; then
  api_args+=("--model_path" "${MODEL_PATH}")
fi

python api_server.py "${api_args[@]}" &
API_PID=$!

python demo_gradio.py \
  --port "${GRADIO_PORT:-7860}" \
  --device "${DEVICE:-cpu}" &
GRADIO_PID=$!

trap 'kill "$API_PID" "$GRADIO_PID"' SIGINT SIGTERM
wait -n
kill "$API_PID" "$GRADIO_PID" || true
wait
