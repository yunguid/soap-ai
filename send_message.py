import subprocess

def send_imessage(phone_number, message):
    script = f'osascript send_message.applescript {phone_number} "{message}"'
    try:
        subprocess.run(script, shell=True, check=True)
        print(f"Sent AI-generated message to {phone_number}")
    except subprocess.CalledProcessError as e:
        print(f"Error sending message: {e}")