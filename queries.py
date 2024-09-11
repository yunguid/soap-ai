import sqlite3
from datetime import datetime

DB_PATH = "/Users/dtts/Library/Messages/chat.db"

def get_latest_messages(last_check_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        message.ROWID,
        message.date,
        message.is_from_me,
        message.text,
        handle.id
    FROM message 
    LEFT JOIN handle ON message.handle_id = handle.ROWID
    WHERE message.date > ? AND message.is_from_me = 0
    ORDER BY message.date ASC
    """
    
    params = (int((last_check_time.timestamp() - 978307200) * 1000000000),)
    cursor.execute(query, params)
    
    results = cursor.fetchall()
    
    messages = []
    for row in results:
        message_date = datetime.fromtimestamp((row[1] / 1000000000) + 978307200)
        messages.append({
            'rowid': row[0],
            'is_from_me': row[2],
            'text': row[3] if row[3] is not None else "<No text>",
            'user_id': row[4] if row[4] is not None else "Unknown",
            'date_time': message_date
        })
    
    conn.close()
    return messages