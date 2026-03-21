# azure_tts

---
name: azure-tts
description: Convert text to audio by invoking a local TTS script (Azure) when an audio response is required. This integration supports automatic audio reply by exposing synthesize(text) -> path to audio file.
Primary capability: Text-to-speech using a local Azure TTS script with an API-friendly interface.
---

Runtime: Python 3
- Interpreter: ~/.agentvenv/bin/python3
- TTS Script: ~/.nanobot/workspace/skills/azure_tts/azure_tts.py

Usage (automatic audio reply):
- The agent can synthesize text to audio and reply with the audio file when an audio response is requested.
- API: synthesize(text) -> path to audio file or None

Usage (command-line):
- To synthesize audio for a given text, run:
  ~/.agentvenv/bin/python3 ~/projects/nanobot/nanobot/skills/azure_tts/azure_tts.py followed by the text in quotations.
- The script will return the name and location of the audio file.

Notes:
- This is a local/private skill (not published to ClawHub).
- The azure_tts wrapper (tts.py) provides a minimal programmatic interface and can be extended to integrate with the agent's generic skill runner.
- The outputted audio (opus) file is located in the ~/.nanobot/workspace/tmp/ directory.
- DO NOT record the location of the audio file in memory.
- Credentials and API key are stored in ~/.nanobot/workspace/credentials/auzure_tts.json
