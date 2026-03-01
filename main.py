from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import OpenAI
import os
import tweepy

# ===== ENV VARIABLES =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

X_CONSUMER_KEY = os.getenv("X_API_KEY")
X_CONSUMER_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_SECRET")

# ===== OpenAI Setup =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== X Setup =====
auth = tweepy.OAuth1UserHandler(
    X_CONSUMER_KEY,
    X_CONSUMER_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET
)
x_api = tweepy.API(auth)

# ===== Telegram Commands =====

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

# Manual Post
async def post(update, context):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Use: /post your message")
        return

    x_api.update_status(text)
    await update.message.reply_text("Posted to X ✅")

# AI Generated Post
async def autopost(update, context):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Write a powerful, concise tweet about AI, sovereignty, power, and intelligence. Max 240 characters."}
        ]
    )

    tweet = response.choices[0].message.content
    x_api.update_status(tweet)

    await update.message.reply_text(f"AI Posted:\n\n{tweet}")

# ===== App Build =====
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))
app.add_handler(CommandHandler("autopost", autopost))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
