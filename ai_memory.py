# ai_memory.py (Stores Chat History & Remembers Past Interactions)
import sqlite3
from config import DB_PATH

def save_chat(user_id, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, message) VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM chat_history WHERE user_id = ?", (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history if history else ["No previous messages found."]
