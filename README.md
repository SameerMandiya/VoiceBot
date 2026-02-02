# Sem Voice Chatbot

A voice chatbot for hiring assessment. Users press mic, speak questions, and receive voice replies.

## Folder Structure

```
ChatBot/
├── app.py
├── index.html
├── requirements.txt
└── README.md
```

## Run Locally (Windows)

1. **Create virtual environment**
   ```powershell
   cd C:\Users\ASUS\Desktop\ChatBot
   python -m venv venv
   .\venv\Scripts\Activate
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Get a free Gemini API key**
   - Go to https://aistudio.google.com/app/apikey
   - Sign in with Google
   - Create an API key
   - Put it in `.env`: `AIzaSyCxoyPf3ZJwDAaVS9zI-SNk8yugTxdIJAY`

4. **Start server**
   ```powershell
   py -3 -m uvicorn app:app --reload
   ```

5. **Open browser** → http://127.0.0.1:8000

## Deploy to Render

**You need Git installed** (download from https://git-scm.com if not installed).

### Step 1: Push to GitHub

1. Install Git from https://git-scm.com (if needed)
2. Create a new repo on https://github.com/new
3. In PowerShell from your project folder:
   ```powershell
   cd C:\Users\ASUS\Desktop\ChatBot
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Create Render Web Service

1. Go to https://render.com and sign in (or create account)
2. Click **New** → **Web Service**
3. Connect your GitHub account and select your repository
4. Render will auto-detect `render.yaml` or configure manually:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variable (required)

1. In Render dashboard → your service → **Environment**
2. Add: `GEMINI_API_KEY` = your Gemini API key (get free at https://aistudio.google.com/app/apikey)
3. Click **Save Changes**

### Step 4: Deploy

1. Click **Deploy** (Render auto-deploys on save)
2. Wait 2–3 minutes for build
3. Your public URL: `https://YOUR_SERVICE_NAME.onrender.com`

## Usage

- **Start Recording**: Click to begin recording your question
- **Stop**: Click to stop and send to backend
- **Play Reply**: Click after processing to hear the response

No API keys needed for end users; only the server needs `OPENAI_API_KEY`.
