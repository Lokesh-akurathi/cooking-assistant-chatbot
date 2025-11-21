# Cooking Assistant Chatbot

## Project overview
This project is a Cooking Assistant chatbot backend (Django) with a decent frontend(HTML&CSS). It stores conversation context (per-session) in the database so the assistant remembers ingredients across messages, and it integrates with an LLM (Gemini) to generate meal ideas and recipes.

---

## Key features
- Session-scoped conversation storage  
- Persistent Conversation & Message models  
- Initial structured prompt flow  
- Simple REST endpoints  
- Swappable LLM backend  

---

## Important Files
- llm.py — LLM integration  
- models.py — Conversation & Message models  
- urls.py — API routes  
- utils.py — session & conversation helper  
- views.py — main logic  

---

## Requirements
- Python 3.10+  
- Django  
- google-generativeai  
- Environment variable: `GEMINI_API_KEY`  

---

## Setup & Run

clone repository

```bash
cd cooking-assistant-chatbot
python3 -m venv venv
source venv/bin/activate

python3 manage.py makemigrations
python3 manage.py migrate

python3 -m pip install -r requirements.txt
cat > .env <<'EOF'
GEMINI_API_KEY=your_real_gemini_api_key
EOF

python3 manage.py runserver
```

Open: http://127.0.0.1:8000/

---

## Session & persistence
-The project uses the Django session key to tie a Conversation record to a browser session, utils.get_or_create_conversation(request) handles that flow.


## User Flow
- First message → Generate 3–5 meal ideas + ask for more ingredients + ask if recipe needed.  
- Later messages → Use full conversation context.
- Avoid giving recipes unless the user explicitly requests one; when a recipe is requested, return concise numbered steps
- Remember and accumulate ingredient context unless the user explicitly removes/replaces items
- This design enforces consistent UX and predictable LLM behavior for ingredient accumulation and recipe delivery.

## 🎥 Demo Video
<video src="demo/cooking_assistant_chatbot_demo.mp4" controls width="600">
  Your browser does not support the video tag.
</video>

 - You can check demo video in demo folder of this project.

