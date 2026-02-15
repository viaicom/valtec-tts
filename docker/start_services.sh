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
set +e
wait -n "$API_PID" "$GRADIO_PID"
EXIT_STATUS=$?
set -e
if ! kill -0 "$API_PID" 2>/dev/null; then
  echo "API service exited (first-exit status: ${EXIT_STATUS})."
fi
if ! kill -0 "$GRADIO_PID" 2>/dev/null; then
  echo "Gradio service exited (first-exit status: ${EXIT_STATUS})."
fi
kill "$API_PID" "$GRADIO_PID" 2>/dev/null || true
wait
