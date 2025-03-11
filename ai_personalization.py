# ai_personalization.py (Learns from Admin Messages & Auto-Replies Like Admin)
import sqlite3
from config import DB_PATH

def save_admin_response(trigger, response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admin_responses (trigger, response) VALUES (?, ?)", (trigger, response))
    conn.commit()
    conn.close()

def get_admin_response(trigger):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM admin_responses WHERE trigger = ?", (trigger,))
    response = cursor.fetchone()
    conn.close()
    return response[0] if response else None
