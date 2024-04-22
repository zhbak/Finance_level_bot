from dotenv import load_dotenv
import telebot.async_telebot as telebot
import os

load_dotenv()
bot_token = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.AsyncTeleBot(bot_token)