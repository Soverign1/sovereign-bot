from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import OpenAI
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update, context):
    await update.message.reply_text("Sovereign AI is online 👑")

async def reply(update, context):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Sovereign AI. Intelligent, strategic, confident."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_reply = response.choices[0].message.content
    await update.message.reply_text(ai_reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
