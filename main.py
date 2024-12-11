import os
import speech_recognition as sr
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from pydub import AudioSegment
import ollama

load_dotenv()

TG_API_KEY = os.getenv("TG_API_KEY")

model_name = "moondream"

def convert_ogg_to_wav(input_file: str, output_file: str):
    audio = AudioSegment.from_ogg(input_file)
    audio.export(output_file, format="wav")

async def handle_voice(update: Update, context: CallbackContext) -> None:
    voice = update.message.voice
    file = await voice.get_file()

    file_path = "voice.ogg"
    await file.download_to_drive(file_path)

    wav_file_path = "voice.wav"
    convert_ogg_to_wav(file_path, wav_file_path)

    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        print(f"Recognized text: {text}")

        response = ollama.generate(model_name, text)
        bot_reply = response.response.strip()
        await update.message.reply_text(bot_reply)
        
    except sr.UnknownValueError:
        await update.message.reply_text("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        await update.message.reply_text(f"Could not request results; {e}")

async def handle_audio(update: Update, context: CallbackContext) -> None:
    audio = update.message.audio
    file = await audio.get_file()

    file_path = "audio_file.mp3"
    await file.download_to_drive(file_path)

    wav_file_path = "audio_file.wav"
    audio = AudioSegment.from_mp3(file_path)
    audio.export(wav_file_path, format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        print(f"Recognized text: {text}")

        response = ollama.generate(model_name, text)
        bot_reply = response.response.strip()
        await update.message.reply_text(bot_reply)
        
    except sr.UnknownValueError:
        await update.message.reply_text("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        await update.message.reply_text(f"Could not request results; {e}")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I'm your Moondream chatbot. You can send me both text and audio messages!")

def main():
    if not TG_API_KEY:
        print("Error: TG_API_KEY not found in .env file.")
        return

    application = Application.builder().token(TG_API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Handle voice messages
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))  # Handle audio files

    application.run_polling()

if __name__ == '__main__':
    main()
