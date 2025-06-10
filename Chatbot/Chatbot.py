import re
from datetime import datetime

def get_response(user_input):
    user_input = user_input.lower()

    if re.search(r'\b(hi|hello|hey|good morning|good evening)\b', user_input):
        return "Hello! How can I assist you today?"

    elif re.search(r'\b(who are you|what are you|are you a bot)\b', user_input):
        return "I'm a simple rule-based chatbot built using Python!"

    elif re.search(r'\b(help|support|assist|need help)\b', user_input):
        return "Sure, I'm here to help. Please tell me what you need assistance with."

    elif re.search(r'\b(time|current time|what time)\b', user_input):
        return "The current time is " + datetime.now().strftime("%H:%M:%S")

    elif re.search(r'\b(bye|goodbye|see you|exit|quit)\b', user_input):
        return "Goodbye! Have a great day 😊"

    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

if __name__ == "__main__":
    print("🤖 Chatbot: Hello! I am your assistant. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ['bye', 'exit', 'quit']:
            print("🤖 Chatbot:", get_response(user_input))
            break
        else:
            response = get_response(user_input)
            print("🤖 Chatbot:", response)

