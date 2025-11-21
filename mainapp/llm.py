from django.conf import settings
import google.generativeai as genai
import os


API_KEY = os.environ.get("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", None)

if not API_KEY or API_KEY == "API_KEY":
    genai_configured = False
    print("Warning: Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
    model = None
else:
    genai.configure(api_key=API_KEY)
    genai_configured = True
    system_instruction = "You are a concise and helpful culinary assistant. You prioritize clarity and strict adherence to the requested output format and conversational flow."
    generation_config = {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1000,
    }
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=system_instruction,
        generation_config=generation_config,
    )

def call_llm(prompt):
    if not genai_configured or model is None:
        print("LLM call attempted but GEMINI_API_KEY is not configured.")
        return {"text": "LLM API key not configured. Please set the GEMINI_API_KEY environment variable and restart the server."}

    try:
        chat_session = model.start_chat(history=[]) 
        response = chat_session.send_message(prompt)
        return {"text": response.text.strip()}

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {"text": "Sorry, I'm having trouble connecting to my brain right now. Please try again later."}