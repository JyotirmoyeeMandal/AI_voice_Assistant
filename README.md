# AI Voice Assistant (Web-Based) using Gemini Pro

This is a web-based AI voice assistant built with **Flask**, **Gemini 2.5 Pro API**, and modern **JavaScript-based speech recognition**. It allows users to speak naturally to an AI agent via their browser and receive intelligent, spoken responses in real time.

---

## Features

- **Voice input** using Web Speech API
- **Conversational AI** via Google's Gemini 2.5 Pro
- Smart and natural responses under 150 words
- Real-time text and voice reply
- Web-based interface with interactive chat-style UI
- `/health` endpoint for service health checking

---

## How It Works

1. User clicks the mic button and speaks.
2. The browser uses **SpeechRecognition API** to convert voice to text.
3. Text is sent to a Flask backend via `/chat`.
4. Gemini 2.5 Pro generates a concise, conversational reply.
5. The reply is:
   - Shown in the chat box
   - Spoken aloud via **SpeechSynthesis API**

---

## Setup Instructions

### 1. Clone the Repo

```
git clone git@github.com:JyotirmoyeeMandal/AI_voice_Assistant.git
cd AI_voice_Assistant
```
2. Create & Activate Virtual Environment (Optional but Recommended)
  ```
   python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate        # On Windows
```
3. Install Dependencies
   ```
   pip install flask google-generativeai

4. Set up .env file 
```
GEMINI_API_KEY=your_api_key_here
```
5. Start the Flask Server
   ```
   python app.py

Open your browser and go to: http://localhost:5000

### API Endpoints
GET /
Renders the voice assistant UI in your browser.

### POST /chat
Request Body:
```
{
  "message": "What's the weather today?"
}
```
Response:
```
{
  "response": "The weather today is sunny and warm. Don’t forget your sunglasses!"
}
```
### GET /health

Simple health check endpoint. Returns JSON.

### Security Notes
1. .env is excluded via .gitignore to keep your API key safe.
2. Do not expose your backend without API rate limiting or auth if deployed publicly.

### Deployment Tips
1. You can deploy this app to Render, Fly.io, Heroku, or any cloud service that supports Flask.
2. Set your 'GEMINI_API_KEY' in environment variables during deployment.

### Future Improvements
1. Add authentication for multi-user support
2. Persistent chat history
3. Support for multiple languages
4. Progressive Web App (PWA) features




Let me know if you'd like this in a file (`README.md`) or want to add badges, a GIF demo, or a deployment button (like Render or Heroku)!
