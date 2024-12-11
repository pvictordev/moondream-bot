from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import ollama

load_dotenv()

TG_API_KEY = os.getenv("TG_API_KEY")

model_name = "moondream"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your Moondream chatbot. Ask me anything.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    try:
        response = ollama.generate(model_name, user_message)
        bot_reply = response.response.strip()
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text("Sorry, something went wrong!")
        print(f"Error: {e}")

def main():
    if not TG_API_KEY:
        print("Error: TG_API_KEY not found in .env file.")
        return
    
    application = Application.builder().token(TG_API_KEY).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    application.run_polling()

if __name__ == '__main__':
    main()
