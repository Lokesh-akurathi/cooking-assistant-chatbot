from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import get_or_create_conversation
from .models import Message
from .llm import call_llm
import json

@require_http_methods(["GET"])
def conversation_state(request):
    conv = get_or_create_conversation(request)
    msgs = list(conv.messages.order_by("created_at").values("sender", "text", "created_at"))
    return JsonResponse({"messages": msgs})

@require_http_methods(["POST"])
def post_message(request):
    """
    Main message endpoint:
    - Save user message
    - Build a prompt using the conversation history
    - Call LLM
    - Save assistant message
    """
    conv = get_or_create_conversation(request)
    body = json.loads(request.body.decode("utf-8") or "{}")
    text = body.get("text", "").strip()
    if not text:
        return JsonResponse({"error": "text required"}, status=400)

    # save usr messaage
    Message.objects.create(conversation=conv, sender="user", text=text)

    # build prompt from conversation history
    messages = conv.messages.order_by('created_at')
    
    # If this is the first user messaage, use a more specific prompt.
    if messages.count() == 1:
        prompt =f"""Given the following ingredients: [{text}].

        **Primary Task:**
        1. Generate 3-5 distinct meal ideas that can be made using these ingredients, provided in a single comma-separated line.
        2. Immediately after the meal ideas, ask the user: "Do you have any other ingredients you'd like to add?" and incorporate new ingredients into context if the user provides them.
        3. Immediately after that, ask the user: "Would you like a recipe for any of these?"

        **Critical Constraints:**
        - when ever user responds with (a list of ingredients),(dont respond with thaanks, noted, etc..)Generate 3-5 distinct meal ideas that can be made using (the ingredients so far in context unless if some ingredients were explicitly removed by user), provided in a single comma-separated line.
        - DO NOT provide a recipe unless the user explicitly asks for one in a subsequent message.
        - When the user DOES request a recipe:
        - Provide the recipe in clear, numbered steps.
        - Each step must appear on a new line (not in a paragraph).
        - Keep the recipe concise and easy to follow.
        - Include the estimated total cooking/preparation time at the end.
        - Provide only one recipe unless the user asks for multiple.

        **Context Handling:**
        - You must remember ingredients provided earlier in the conversation and treat them as active context.
        - Add newly provided ingredients to the existing list unless the user explicitly says to replace or remove them.
        - Always respond based on the full accumulated ingredient list."""


    else:
        history = "\n".join([f"{m.sender}: {m.text}" for m in messages])
        prompt = f"Here is the conversation so far:\n{history}\n\nAssistant:"

    # Call LLM
    llm_resp = call_llm(prompt)
    assistant_text = llm_resp.get("text", "")

    # Save assistant message
    Message.objects.create(conversation=conv, sender="assistant", text=assistant_text)

    return JsonResponse({"assistant_text": assistant_text})

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')



