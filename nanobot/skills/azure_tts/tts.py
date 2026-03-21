#!/home/sachin/.agentvenv/bin/python3

"""#!/usr/bin/env python3

Azure TTS wrapper for nanobot
- Reads credentials from /home/sachin/.nanobot/workspace/credentials/azure_tts.json
- synthesize_text(text, voice=None, fmt=None, output_path=None)
- Azure returns Opus audio directly when using an Opus output format

Notes:
- Requires network access
- Requires the `requests` Python package
"""
import json
import os
import time
from xml.sax.saxutils import escape

import requests
import sys

CREDENTIALS_PATH = "/home/sachin/.nanobot/workspace/credentials/azure_tts.json"
SYN_ENDPOINT_TEMPLATE = "https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
DEFAULT_OUTPUT_FORMAT = "ogg-24khz-16bit-mono-opus"
HEADERS = {
    "Content-Type": "application/ssml+xml",
    "User-Agent": "nanobot-azure-tts",
}


def _load_credentials():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _validate_credentials(region, key):
    if not region or not key:
        raise RuntimeError("Azure credentials not configured properly. Set region and key in azure_tts.json.")
    if region.startswith("<") or key.startswith("<"):
        raise RuntimeError("Azure credentials still contain placeholders. Update region and subscription_key in azure_tts.json.")


def _build_ssml(text, voice, lang="en-US"):
    safe_text = escape(text)
    safe_voice = escape(voice, {'"': '&quot;'})
    safe_lang = escape(lang, {'"': '&quot;'})
    return (
        f"<speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang=\"{safe_lang}\">"
        f"<voice name=\"{safe_voice}\">{safe_text}</voice>"
        f"</speak>"
    )


def _ensure_output_dir():
    out_dir = "/tmp/nanobot_azure_tts"
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def synthesize_text(text, voice=None, fmt=None, output_path=None):
    cred = _load_credentials()
    region = cred.get("region", "").strip()
    key = cred.get("subscription_key", "").strip()
    default_voice = cred.get("default_voice", "en-US-AriaNeural")
    default_fmt = cred.get("output_format", DEFAULT_OUTPUT_FORMAT)

    _validate_credentials(region, key)

    if voice is None:
        voice = default_voice
    if fmt is None:
        fmt = default_fmt

    endpoint = SYN_ENDPOINT_TEMPLATE.format(region=region)
    ssml = _build_ssml(text, voice)

    headers = dict(HEADERS)
    headers["Ocp-Apim-Subscription-Key"] = key
    headers["X-Microsoft-OutputFormat"] = fmt

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            data=ssml.encode("utf-8"),
            stream=True,
            timeout=60,
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Azure TTS request failed: {e}") from e

    if response.status_code != 200:
        raise RuntimeError(f"Azure TTS request failed: {response.status_code} {response.text}")

    content_type = response.headers.get("Content-Type", "")
    if "audio" not in content_type.lower() and content_type:
        raise RuntimeError(f"Azure TTS returned unexpected content type: {content_type}")

    if output_path is None:
        output_path=f"/home/sachin/.nanobot/workspace/tmp/{int(time.time())}.opus"

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)

    return output_path

# Check if at least one argument (after the script name) is provided
if len(sys.argv) > 1:
    print(synthesize_text(sys.argv[1]))
else:
    print("No text inputted to convert.")
