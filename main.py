import ollama

model_name = "moondream"

print("Chatbot is ready! Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = ollama.generate(model_name, user_input)
    
    bot_response = response.response.strip()
    print(f"Bot: {bot_response}")
