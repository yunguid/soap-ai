import time
from datetime import datetime, timedelta
from ai import completion
from queries import get_latest_messages
from send_message import send_imessage
from json_operations import add_message

def process_messages(new_messages):
    for message in new_messages:
        if message['is_from_me'] == 0:
            # Store incoming message
            add_message(message['user_id'], "user", message['text'])
            
            # Generate AI response
            ai_response = completion([{"role": "user", "content": message['text']}])
            
            # Store AI response
            add_message(message['user_id'], "assistant", ai_response)
            
            # Send AI response
            send_imessage(message['user_id'], ai_response)

def main():
    last_check_time = datetime.now() - timedelta(seconds=10)
    
    while True:
        new_messages = get_latest_messages(last_check_time)
        
        if new_messages:
            print(f"Found {len(new_messages)} new message(s):")
            process_messages(new_messages)
            last_check_time = max(message['date_time'] for message in new_messages)
        else:
            print(f"No new messages since {last_check_time.strftime('%Y-%m-%d %H:%M:%S')}", end="\r", flush=True)
        
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()