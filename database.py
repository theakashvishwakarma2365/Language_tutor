import sqlite3
import streamlit as st

conn = sqlite3.connect("chat_data.db", check_same_thread=False)
cursor = conn.cursor()

def format_table_name(session_id):
    return f"chat_{session_id.replace('-', '_')}"

def create_new_chat_table(session_id):
    table_name = format_table_name(session_id)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            ai TEXT,
            correction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return table_name

def save_message(session_id, user_query, ai_response, corrections):
    table_name = format_table_name(session_id)
    cursor.execute(f'''
        INSERT INTO {table_name} (user, ai, correction)
        VALUES (?, ?, ?)
    ''', (user_query, ai_response, corrections))
    conn.commit()

def get_chat(session_id):
    table_name = format_table_name(session_id)
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY timestamp")
    return cursor.fetchall()

def get_all_sessions():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'chat_%'")
    tables = cursor.fetchall()
    result = []
    for t in tables:
        sid = t[0].replace("chat_", "")
        cursor.execute(f"SELECT COUNT(*) FROM {t[0]}")
        total_msgs = cursor.fetchone()[0]
        result.append((sid, f"{total_msgs} messages"))
    return result

def delete_all_chat_history():
    active_session = format_table_name(st.session_state.get("session_id", ""))
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """)
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        if table_name != active_session:
            cursor.execute(f"DROP TABLE IF EXISTS '{table_name}'")

    conn.commit()