"""Vapi par assistant banata hai. Ek baar chalao, ID .env mein daal do."""
import os, requests
from dotenv import load_dotenv
from build_prompt import build_system_prompt

load_dotenv()
KEY = os.environ["VAPI_API_KEY"]
SERVER_URL = os.environ["SERVER_URL"]  # e.g. https://xxxx.ngrok-free.app/vapi

tools = [
    {
        "type": "function",
        "function": {
            "name": "save_lead",
            "description": "Client ki details save karo jab naam, need, budget mil jaye.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "need": {"type": "string"},
                    "budget": {"type": "string"},
                    "callback_time": {"type": "string"},
                    "status": {"type": "string", "enum": ["interested", "callback", "human_callback"]},
                },
                "required": ["name", "need"],
            },
        },
        "server": {"url": SERVER_URL},
    },
    {
        "type": "function",
        "function": {
            "name": "mark_do_not_call",
            "description": "Client ne dobara call na karne ko bola.",
            "parameters": {"type": "object", "properties": {"reason": {"type": "string"}}},
        },
        "server": {"url": SERVER_URL},
    },
]

body = {
    "name": "XYZ Sales Agent",
    "firstMessage": "Namaste! Main Riya bol rahi hoon, XYZ Company ki AI assistant. Kya aapke paas 2 minute hain?",
    "model": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": build_system_prompt()}],
        "tools": tools,
    },
    "transcriber": {"provider": "deepgram", "model": "nova-2", "language": "hi"},
    "voice": {"provider": "azure", "voiceId": "hi-IN-SwaraNeural"},
    "serverUrl": SERVER_URL,
    "endCallFunctionEnabled": True,
    "maxDurationSeconds": 300,
}

r = requests.post("https://api.vapi.ai/assistant",
                  headers={"Authorization": f"Bearer {KEY}"}, json=body, timeout=30)
print(r.status_code, r.json())
print("\n>>> 'id' ko .env mein VAPI_ASSISTANT_ID mein daalo")
