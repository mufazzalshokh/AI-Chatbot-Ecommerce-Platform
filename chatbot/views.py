# chatbot/views.py
import os, json, httpx
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

OPENAI_API_KEY = getattr(settings, "OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# System prompt that defines our “persona”
SYSTEM_PROMPT = """
You are Elle, a super-professional e-commerce customer support agent and styling advisor.
• Always greet warmly.
• Help customers pick perfect outfits and sizes based on their height, weight, and body type.
• Reference their past orders where relevant.
• Be concise, friendly, and close with “Is there anything else I can help you with today?”
"""

# A simple per-session memory store (for demo—use Redis or a database in production)
SESSION_MEMORY = {}

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    payload = json.loads(request.body)
    session_id = payload.get('session_id')
    user_info   = payload.get('user_info', {})
    history     = payload.get('contents', [])

    # Initialize session memory if needed
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "system": SYSTEM_PROMPT,
            "user_profile": user_info,    # e.g. {"height_cm": 170, "weight_kg": 60, "body_type": "athletic"}
            "past_orders": payload.get('past_orders', []),
            "history": []                 # we’ll mirror back the conversation
        }

    sess = SESSION_MEMORY[session_id]

    # Build the messages array with persona + personalization
    messages = [
        {"role": "system", "content": sess["system"]},
        {
            "role": "system",
            "content": (
                f"Customer profile:\n"
                f"- Height: {sess['user_profile'].get('height_cm', 'unknown')} cm\n"
                f"- Weight: {sess['user_profile'].get('weight_kg', 'unknown')} kg\n"
                f"- Body type: {sess['user_profile'].get('body_type', 'unknown')}\n"
                f"Past orders: {', '.join(sess['past_orders']) or 'none'}"
            )
        }
    ]

    # Append prior chat turns for full context
    messages += sess["history"] + history

    # Cap the reply length
    MAX_REPLY_TOKENS = 100

    # Call OpenAI
    resp = httpx.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'gpt-4o-mini',
            'messages': messages,
            'max_tokens': MAX_REPLY_TOKENS,
            'temperature': 0.7,
        },
        timeout=30
    )
    data = resp.json()
    if resp.status_code != 200:
        return JsonResponse({'error': data.get('error', {}).get('message')}, status=502)

    bot_reply = data['choices'][0]['message']

    # Save this turn into session memory
    sess["history"].extend(history + [bot_reply])

    # Return to front-end
    return JsonResponse({
        'candidates': [{
            'content': { 'parts': [{ 'text': bot_reply['content'] }] }
        }]
    })


# chatbot/views.py

# import os, json, httpx, uuid
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings

# from .models import Product, UserProfile, ChatMessage

# OPENAI_API_KEY = settings.OPENAI_API_KEY

# @csrf_exempt
# def chat_api(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'POST only'}, status=405)

#     # 1) Parse the body and extract everything we need
#     payload = json.loads(request.body or '{}')
#     session_id = payload.get('session_id') or str(uuid.uuid4())
#     user_text  = payload.get('user_message')
#     user_info  = payload.get('user_info', {})
#     past_orders= payload.get('past_orders', [])

#     # 2) Validate the required bit
#     if not user_text:
#         return JsonResponse({'error': 'Missing "user_message" in request body.'}, status=400)

#     # 3) Load or create the user profile, and update it
#     profile, _ = UserProfile.objects.get_or_create(session_id=session_id)
#     for field in ('height_cm','weight_kg','body_type'):
#         if field in user_info:
#             setattr(profile, field, user_info[field])
#     profile.past_orders = past_orders
#     profile.save()

#     # 4) Record the user’s message
#     ChatMessage.objects.create(session=profile, role='user', content=user_text)

#     # 5) Fetch top‐3 relevant products
#     relevant = Product.objects.filter(name__icontains=user_text)[:3]
#     product_context = "\n".join(
#         f"- {p.name} (sizes: {', '.join(p.sizes)}): {p.description}"
#         for p in relevant
#     ) or "No matching products found."

#     # 6) Build the OpenAI conversation
#     messages = [
#         {"role":"system","content":(
#             "You are Elle, a super-professional e-commerce support agent "
#             "and styling advisor. Help customers pick perfect outfits and sizes. "
#             "Always be friendly and concise."
#         )},
#         {"role":"system","content":(
#             f"Customer profile:\n"
#             f"- Height: {profile.height_cm or 'unknown'} cm\n"
#             f"- Weight: {profile.weight_kg or 'unknown'} kg\n"
#             f"- Body type: {profile.body_type or 'unknown'}\n"
#             f"Past orders: {', '.join(profile.past_orders) or 'none'}\n"
#             f"Available products:\n{product_context}"
#         )}
#     ]
#     # conversation history
#     for msg in profile.messages.all():
#         messages.append({"role": msg.role, "content": msg.content})
#     # current user turn
#     messages.append({"role":"user","content":user_text})

#     # 7) Call OpenAI
#     resp = httpx.post(
#         "https://api.openai.com/v1/chat/completions",
#         headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
#         json={
#             "model":       "gpt-4o-mini",
#             "messages":    messages,
#             "max_tokens":  150,
#             "temperature": 0.7,
#         },
#         timeout=30
#     )
#     if resp.status_code != 200:
#         data = resp.json()
#         return JsonResponse({'error': data.get('error',{}).get('message')}, status=502)

#     bot_msg = resp.json()['choices'][0]['message']['content']

#     # 8) Record assistant’s reply
#     ChatMessage.objects.create(session=profile, role='assistant', content=bot_msg)

#     # 9) Return both session_id and reply
#     return JsonResponse({
#         "session_id": session_id,
#         "reply": bot_msg
#     })

