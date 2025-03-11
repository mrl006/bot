import json

USER_MEMORY_FILE = "user_memory.json"

def load_user_memory():
    """Load user preferences from a JSON file."""
    try:
        with open(USER_MEMORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_memory(memory):
    """Save user preferences to a JSON file."""
    with open(USER_MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)

user_memory = load_user_memory()

def remember_user_preference(user_id, preference):
    """Save a user's preferred design style or service."""
    user_memory[user_id] = preference
    save_user_memory(user_memory)
