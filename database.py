import sqlite3
from datetime import datetime

def init_db():
    """Initialize database with logs table"""
    conn = sqlite3.connect('chat_logs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            bot_response TEXT,
            timestamp TEXT,
            session_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(user_input, bot_response, session_id=None):
    """Log user-bot interaction to database"""
    conn = sqlite3.connect('chat_logs.db')
    c = conn.cursor()
    c.execute('INSERT INTO logs (user_input, bot_response, timestamp, session_id) VALUES (?, ?, ?, ?)',
              (user_input, bot_response, datetime.utcnow().isoformat(), session_id))
    conn.commit()
    conn.close()

def get_chat_history(session_id=None, limit=10):
    """Retrieve chat history from database"""
    conn = sqlite3.connect('chat_logs.db')
    c = conn.cursor()
    
    if session_id:
        c.execute('SELECT user_input, bot_response, timestamp FROM logs WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
                  (session_id, limit))
    else:
        c.execute('SELECT user_input, bot_response, timestamp FROM logs ORDER BY timestamp DESC LIMIT ?', (limit,))
    
    history = c.fetchall()
    conn.close()
    return history