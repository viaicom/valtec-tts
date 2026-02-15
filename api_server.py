#!/usr/bin/env python3

import argparse
import io

import soundfile as sf
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from valtec_tts import TTS


class SynthesizeRequest(BaseModel):
    text: str
    speaker: str | None = None
    speed: float = 1.0
    noise_scale: float = 0.667
    noise_scale_w: float = 0.8
    sdp_ratio: float = 0.0


def create_app(model_path: str | None, device: str) -> FastAPI:
    tts = TTS(model_path=model_path, device=device)
    app = FastAPI(title="Valtec TTS Inference API")

    @app.get("/health")
    def health():
        return {"status": "ok", "speakers": tts.list_speakers()}

    @app.post("/synthesize", response_class=Response)
    def synthesize(req: SynthesizeRequest):
        if not req.text.strip():
            raise HTTPException(status_code=400, detail="text must not be empty")

        try:
            audio, sr = tts.synthesize(
                text=req.text.strip(),
                speaker=req.speaker,
                speed=req.speed,
                noise_scale=req.noise_scale,
                noise_scale_w=req.noise_scale_w,
                sdp_ratio=req.sdp_ratio,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        buffer = io.BytesIO()
        sf.write(buffer, audio, sr, format="WAV")
        return Response(content=buffer.getvalue(), media_type="audio/wav")

    return app


def parse_args():
    parser = argparse.ArgumentParser(description="Valtec TTS pure inference API")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--model_path", type=str, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    app = create_app(args.model_path, args.device)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
