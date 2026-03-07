# 🎬 Interactive Mythos Director — Multimodal Storytelling Agent

An AI creative director powered by **Google Gemini** that builds evolving story worlds with interleaved text, images, and audio. Built for the **Gemini Live Agent Challenge**.

## 🎯 What is Interactive Mythos Director?

Interactive Mythos Director is a web app that:
- **Takes** a story prompt from the user (character, setting, tone)
- **Generates** cinematic narrative scenes with Gemini
- **Creates** visual assets from scene prompts (Imagen)
- **Produces** voice narration from story scripts (TTS)
- **Returns** a unified story package per turn (text + media URLs + choices)

The experience is designed like a digital storybook, not a plain chat.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React |
| **Backend** | Python (FastAPI) |
| **AI SDK** | Google GenAI SDK |
| **Models** | Gemini (logic), Imagen (images), optional Veo (cinematic clips) |
| **Deployment** | Google Cloud Run (containerized) |
| **Storage** | Google Cloud Storage (generated assets) |
| **Audio** | Google Cloud Text-to-Speech |

---

## 📁 Project Structure
```text
gen-ai/
├── README.md                    # This file
├── Dockerfile                   # Cloud Run deployment image
├── AGENTS.md                    # Local coding agent instructions
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint, routes
│   │   ├── director.py          # System prompt + orchestration logic
│   │   ├── media.py             # Imagen/TTS integration + GCS upload
│   │   └── schemas.py           # Request/response models
│   ├── requirements.txt
│   ├── .env                     # API keys and config (never commit)
│   └── .env.example
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx              # Main app flow
        └── components/
            ├── StoryInput.jsx       # Prompt + generation controls
            ├── SceneCard.jsx        # Narrative + image/audio render
            ├── ChoiceButtons.jsx    # Branching path controls
            └── TimelinePanel.jsx    # Session story history
```

---

## 🚀 Quick Start (Local Dev)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Cloud project with Vertex AI + Cloud Storage enabled
- Service account credentials or local `gcloud auth application-default login`

### Setup & Run

**1. Backend setup:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your project/config values
```

**2. Start backend (port 8000):**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**3. Frontend setup (new terminal):**
```bash
cd frontend
npm install
npm run dev
```

**4. Open in browser:**
```text
http://localhost:5173
```

---

## 🔌 API Reference

### POST `/api/generate-scene`
Send user prompt and story context to generate the next scene package.

**Request:**
```json
{
  "prompt": "A cyberpunk samurai enters a neon temple.",
  "history": [
    { "role": "user", "content": "Start a dark fantasy adventure." },
    { "role": "assistant", "content": "The moon cracked above the iron forest..." }
  ],
  "style": "cinematic"
}
```

**Response:**
```json
{
  "narrative": "Rain hissed against chrome armor as Kael stepped into the temple gate...",
  "image_url": "https://storage.googleapis.com/BUCKET/scenes/scene-12.png",
  "audio_url": "https://storage.googleapis.com/BUCKET/audio/scene-12.mp3",
  "choices": [
    "Investigate the altar",
    "Challenge the masked guardian",
    "Scan for hidden exits"
  ]
}
```

---

## 🎨 Features

### Story Loop State Machine
```text
IDLE -> GENERATING_TEXT -> GENERATING_MEDIA -> RENDERING_SCENE -> WAITING_FOR_CHOICE -> IDLE
```

### Frontend Components

| Component | Purpose |
|---|---|
| **StoryInput.jsx** | Prompt entry, tone selector, generate action |
| **SceneCard.jsx** | Displays scene text, artwork, and narration player |
| **ChoiceButtons.jsx** | Branching actions for next turn |
| **TimelinePanel.jsx** | Scrollable history of generated scenes |

### Content Package Per Turn
- **Narrative Segment**: 100-250 words scene text
- **Illustration**: Generated image from scene description
- **Voiceover**: Narration audio for accessibility/immersion
- **Choices**: 2-4 branching options to continue the story

---

## 🧠 Director Persona (System Prompt)

```text
You are the Interactive Mythos Director.
Create immersive, coherent story scenes based on user input.
For each turn, produce:
1) A vivid narrative segment
2) A precise visual description for image generation
3) A clean voiceover script for narration
4) 2-4 meaningful branching choices
Maintain continuity with prior events and avoid contradictions.
```

---

## 🐳 Docker & Cloud Run Deployment

### Local Docker Build
```bash
docker build -t mythos-director:latest .
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e GOOGLE_CLOUD_PROJECT=your_project_id \
  -e GCS_BUCKET=your_bucket \
  mythos-director:latest
```

### Deploy to Google Cloud Run

**1. Authenticate and configure project:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**2. Build container in Cloud Build:**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mythos-director
```

**3. Deploy to Cloud Run:**
```bash
gcloud run deploy mythos-director \
  --image gcr.io/YOUR_PROJECT_ID/mythos-director \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**4. Verify service URL:**
```bash
gcloud run services describe mythos-director --platform managed --region us-central1
```

---

## 📊 Architecture

```text
┌────────────────────┐
│ React Frontend     │
│ (Vite SPA)         │
│ StoryInput/SceneUI │
└─────────┬──────────┘
          │ HTTPS
          ▼
   /api/generate-scene
          │
┌─────────▼──────────┐
│ Python Backend     │
│ (FastAPI on        │
│ Cloud Run)         │
│ - GenAI Orchestrator
│ - Media Pipeline   │
└──────┬─────┬───────┘
       │     │
       │     └───────────────┐
       ▼                     ▼
┌───────────────┐      ┌───────────────┐
│ Vertex AI     │      │ Cloud Storage │
│ Gemini/Imagen │      │ Scene Assets  │
└───────────────┘      └───────────────┘
       │
       ▼
┌───────────────┐
│ Cloud TTS     │
│ Narration MP3 │
└───────────────┘
```

---

## 🔑 Environment Variables

```bash
# backend/.env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GCS_BUCKET=your-asset-bucket
PORT=8000
ENV=development
```

---

## ✅ Hackathon Checklist

- [ ] React frontend connected to backend API
- [ ] Python backend integrated with Google GenAI SDK
- [ ] Interleaved multimodal output (text + image + audio)
- [ ] Assets uploaded and served from GCS
- [ ] Dockerized backend running on Cloud Run
- [ ] Architecture diagram finalized
- [ ] Demo video recorded (<=4 minutes)
- [ ] Public repository and submission page ready

---

## 🐛 Troubleshooting

### "Backend cannot access Google services"
- Verify `gcloud auth application-default login` for local development
- Confirm Vertex AI, Cloud Storage, and Cloud Run APIs are enabled
- Check service account permissions for deployed Cloud Run service

### "Image or audio URL is empty"
- Ensure `GCS_BUCKET` is set correctly
- Validate bucket write permissions
- Inspect backend logs for failed upload operations

### Frontend cannot call backend
- Confirm backend is running on `http://localhost:8000`
- Check frontend API base URL configuration
- Verify CORS settings in FastAPI

---

## 📝 License

Open source for educational and hackathon use.

---

## 🙌 Credits

- **Frontend**: React + Vite
- **Backend**: Python + FastAPI
- **AI**: Google GenAI SDK (Gemini)
- **Media**: Imagen + Google Cloud Text-to-Speech
- **Cloud**: Google Cloud Run + Cloud Storage
