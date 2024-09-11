import json
import os
from datetime import datetime

def ensure_conversations_dir():
    os.makedirs("conversations", exist_ok=True)

def get_conversation_file(phone_number):
    ensure_conversations_dir()
    return f"conversations/{phone_number}.json"

def load_conversation(phone_number):
    filename = get_conversation_file(phone_number)
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"messages": []}

def save_conversation(phone_number, data):
    filename = get_conversation_file(phone_number)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)

def add_message(phone_number, role, content):
    data = load_conversation(phone_number)
    data["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    save_conversation(phone_number, data)