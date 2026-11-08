# Twilio + Deepgram Real-time Speech-to-Text

**Live transcription of phone calls: Twilio streams the caller's audio over a WebSocket, and Deepgram returns transcripts while the person is still speaking.**

This is the speech-to-text foundation for voice bots. The companion repository [realtime-voice-ai-orchestrator](https://github.com/lavanya1402/realtime-voice-ai-orchestrator) adds call sessions, an LLM call report and a monitoring dashboard.

## How it works

```mermaid
flowchart LR
  A[Caller] -->|Phone call| B[Twilio Voice]
  B -->|Webhook /voice| C[FastAPI server.py]
  C -->|TwiML Stream| B
  B -->|Media Streams, mu-law 8 kHz| D[/media WebSocket]
  D -->|audio frames| E[Deepgram live STT]
  E -->|interim + final transcripts| D
  D --> F[Console: transcripts and latency]
```

1. A call reaches Twilio, which calls `/voice`. The server answers with TwiML that opens a media stream to `/media`.
2. `/media` receives the caller's audio (mu-law, 8 kHz, mono) and forwards each frame to Deepgram's live streaming API over a second WebSocket.
3. Deepgram sends back interim and final transcripts. The server logs each final transcript, the **time to first transcript**, and the **transcript latency**.

## Run locally

```bash
pip install -r requirements.txt
cp .env.example .env      # add DEEPGRAM_API_KEY and Twilio details
uvicorn server:app --reload --port 8000
ngrok http 8000           # set NGROK_DOMAIN in .env to this domain
```

Set your Twilio number's voice webhook to `https://<NGROK_DOMAIN>/voice`, or start an outbound test call with `python make_call.py` (uses `TO_NUMBER` and `FROM_NUMBER` from `.env`).

## Files

| File | Purpose |
|---|---|
| `server.py` | FastAPI app: `/voice` webhook and `/media` WebSocket bridge to Deepgram |
| `make_call.py` | Places an outbound test call through Twilio |
| `app/`, `ui/dashboard.py` | Early version of the session API and Streamlit dashboard, continued in the orchestrator repo |
| `.env.example` | Environment variables needed (never commit real keys) |

## Author

Built by [Lavanya Srivastava](https://github.com/lavanya1402), Lavanya AI Consultancy.
