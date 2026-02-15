#!/usr/bin/env python3

import argparse
import json
import urllib.request


def parse_args():
    parser = argparse.ArgumentParser(description="Valtec TTS API Python client example")
    parser.add_argument("--url", default="http://localhost:8000/synthesize", help="Inference API URL")
    parser.add_argument("--text", default="Xin chào, đây là ví dụ gọi API Valtec TTS")
    parser.add_argument("--speaker", default=None)
    parser.add_argument("--output", default="client_output.wav")
    return parser.parse_args()


def main():
    args = parse_args()
    payload = {"text": args.text}
    if args.speaker:
        payload["speaker"] = args.speaker

    request = urllib.request.Request(
        args.url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=300) as response:
        audio_bytes = response.read()

    with open(args.output, "wb") as output_file:
        output_file.write(audio_bytes)

    print(f"Saved synthesized audio to: {args.output}")


if __name__ == "__main__":
    main()
