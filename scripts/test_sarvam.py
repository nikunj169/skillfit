"""Smoke test for the Sarvam AI Saarika ASR integration.

Usage:
  python scripts/test_sarvam.py [--language kn|hi]

The script reads SKILLFIT_SARVAM_API_KEY from the environment or from
backend/.env, generates one second of silence as a WAV file, and sends
it to the Sarvam speech-to-text endpoint. A successful HTTP 200 response
confirms the key is valid and the endpoint is reachable.
"""
import argparse
import io
import os
import sys
import wave


def _load_api_key() -> str | None:
    key = os.environ.get("SKILLFIT_SARVAM_API_KEY")
    if key:
        return key
    env_path = os.path.join(os.path.dirname(__file__), "..", "backend", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SKILLFIT_SARVAM_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return None


def _make_silence_wav(duration_sec: float = 1.0, sample_rate: int = 16000) -> bytes:
    buf = io.BytesIO()
    num_samples = int(sample_rate * duration_sec)
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(b"\x00\x00" * num_samples)
    return buf.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description="Sarvam ASR smoke test")
    parser.add_argument(
        "--language",
        choices=["kn", "hi"],
        default="kn",
        help="Language code to test (kn = Kannada, hi = Hindi). Default: kn",
    )
    args = parser.parse_args()

    api_key = _load_api_key()
    if not api_key:
        print(
            "ERROR: SKILLFIT_SARVAM_API_KEY is not set.\n"
            "Set it in your environment or in backend/.env before running this test."
        )
        sys.exit(1)

    import httpx  # already in requirements.txt

    lang_code = "kn-IN" if args.language == "kn" else "hi-IN"
    print(f"Sarvam ASR smoke test — language: {lang_code}")
    print("Sending 1 second of silence to https://api.sarvam.ai/speech-to-text ...")

    wav_bytes = _make_silence_wav()
    try:
        response = httpx.post(
            "https://api.sarvam.ai/speech-to-text",
            headers={"api-subscription-key": api_key},
            files={"file": ("test.wav", wav_bytes, "audio/wav")},
            data={"language_code": lang_code, "model": "saaras:v1"},
            timeout=15.0,
        )
        print(f"HTTP {response.status_code}")
        try:
            print(response.json())
        except Exception:
            print(response.text)

        if response.status_code == 200:
            print("\nSarvam ASR is reachable and the key is accepted.")
        else:
            print("\nSarvam returned a non-200 status — check your API key and quota.")
            sys.exit(1)
    except httpx.TimeoutException:
        print("ERROR: Request to Sarvam timed out after 15 seconds.")
        sys.exit(1)
    except httpx.RequestError as exc:
        print(f"ERROR: Network error reaching Sarvam: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
