from openai import OpenAI
from typing import List, Dict
from json_operations import load_conversation

def completion(messages: List[Dict[str, str]], phone_number: str) -> str:
    client = OpenAI()
    
    system_message = {
        "role": "system",
        "content": """You are an AI assistant designed to help healthcare professionals. Your task is to receive a message about a patient interaction, parse and clean up the text, and then format it into the SOAP (Subjective, Objective, Assessment, Plan) format for a doctor's note. 

        When you receive a message, follow these steps:
        1. Parse and clean up the text, removing any irrelevant information.
        2. Organize the information into the SOAP format:
           - Subjective: Patient's symptoms, complaints, and history of present illness.
           - Objective: Physical examination findings, vital signs, and test results.
           - Assessment: Doctor's diagnosis or clinical impression based on the subjective and objective information.
           - Plan: Treatment plan, medications, further tests, or follow-up instructions.
        3. Present the formatted SOAP note in a clear, concise manner.

        Remember to maintain patient confidentiality and use professional medical terminology where appropriate."""
    }
    
    # Load conversation history
    conversation_data = load_conversation(phone_number)
    conversation_history = conversation_data["messages"][-5:]  # Get last 5 messages
    
    # Combine system message, conversation history, and new message
    all_messages = [system_message] + conversation_history + messages
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=all_messages,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content