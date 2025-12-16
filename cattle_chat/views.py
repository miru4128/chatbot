# views.py
import os
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render

from django.shortcuts import render

def home(request):
    return render(request, "cattle_chat/home.html")

def chat_page(request):
    return render(request, "cattle_chat/chat.html")

# Choose either the embedding filter or keyword filter
from .embedding_filter import is_cattle_related as embedding_is_cattle

# from .keyword_filter import is_cattle_related as keyword_is_cattle 

# Groq client
from groq import Groq
GROQ_CLIENT = Groq(api_key=settings.GROQ_API_KEY)

from .region_detector import detect_indian_region

def build_system_prompt(request):
    region = detect_indian_region(request)

    return f"""
You are GAAYATRI, an AI assistant for cattle management in INDIA.

DEFAULT CONTEXT (IMPORTANT):
- Assume cattle are raised in INDIA unless explicitly stated otherwise.
- Prioritize Indian cows and buffaloes (Gir, Sahiwal, HF cross, Murrah, Jaffarabadi).
- Use ICAR / NDDB aligned practices.
- Avoid US/European assumptions unless user asks.

USER REGION CONTEXT:
- Agro-climatic zone: {region['zone']}
- Region description: {region['label']}
- Environmental notes: {region['notes']}

RESPONSE RULES:
- Tailor advice to the above region automatically.
- Adjust temperature, housing, ventilation, bedding, water, and heat stress guidance accordingly.
- If advice differs for cow vs buffalo, clearly separate them.
- Use Markdown with:
  • **SUMMARY**
  • Bullet points
  • Practical Indian steps
"""

@csrf_exempt
def chat_api(request):
    """
    POST JSON: {"message": "user text"}
    Response JSON: {"ok": True, "answer": "...", "score": 0.78}
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Use POST.")

    try:
        data = json.loads(request.body)
        user_text = data.get("message", "").strip()
    except Exception:
        return HttpResponseBadRequest("Invalid JSON.")

    if not user_text:
        return JsonResponse({"ok": False, "error": "Empty message"}, status=400)

    # Check cattle-related using embedding filter
    related, score = embedding_is_cattle(user_text)  # returns (bool,score)
    if not related:
        return JsonResponse({
            "ok": False,
            "error": "non_cattle",
            "message": "I can only answer cattle-related queries. Please ask about cattle health, milk production, nutrition, or veterinary care.",
            "score": score
        }, status=200)

    # Build chat request (non-streaming for simplicity)
    try:
        system_prompt = build_system_prompt(request)
        completion = GROQ_CLIENT.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
    ],
    stream=False
)

        # The Groq SDK response shape may vary; adapt as needed. We'll assume completion.choices[0].message.content style.
        # If response shape is different, inspect completion in debugging prints.
        answer = ""
        # try common response formats:
        if hasattr(completion, "choices"):
            # e.g. completion.choices[0].message.content
            try:
                answer = completion.choices[0].message.content
            except Exception:
                # fallback: parse raw
                answer = str(completion)
        else:
            answer = str(completion)

        return JsonResponse({"ok": True, "answer": answer, "score": score})
    except Exception as e:
        return JsonResponse({"ok": False, "error": "model_error", "message": str(e)}, status=500)
