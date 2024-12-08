import openai
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def chat_with_openai(user_input):
    try:
        response = await openai.ChatCompletion.acreate(
            model="GPT-3.5", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"An error occurred: {e}"

async def start_chatbot():
    print("👋 Welcome! I'm your chatbot. Type 'exit' to end the chat.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        response = await chat_with_openai(user_input)  
        print(f"Bot: {response}\n")

# Entry point for the chatbot
if __name__ == "__main__":
    asyncio.run(start_chatbot())  
