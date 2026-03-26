import os
import telebot
from flask import Flask
from openai import OpenAI
from threading import Thread

# Initialize Telegram Bot
bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))

# Initialize Hugging Face Client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),
)

# Initialize Flask for Render (Keep-Alive)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "नमस्ते! मैं जार्विस हूँ। आप मुझसे चैट कर सकते हैं।")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Chat completion request using the requested model
        chat_completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1", # Note: Ensure you have access to this model
            messages=[
                {"role": "user", "content": message.text},
            ],
        )
        reply = chat_completion.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Oops! Error: {str(e)}")

# Function to run Flask server
def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Run both Flask and Bot
if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
