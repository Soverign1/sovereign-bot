import os
import tweepy
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===== ENV VARIABLES =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

X_CONSUMER_KEY = os.getenv("X_API_KEY")
X_CONSUMER_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_SECRET")

# ===== OPENAI SETUP =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== X SETUP =====
auth = tweepy.OAuth1UserHandler(
    X_CONSUMER_KEY,
    X_CONSUMER_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET
)
x_api = tweepy.API(auth)

# ===== COMMANDS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sovereign AI is online 👑")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Use: /post your message here")
        return

    try:
        x_api.update_status(text)
        await update.message.reply_text("Posted to X 🚀")
    except Exception as e:
        await update.message.reply_text(f"Error posting: {str(e)}")

async def autopost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write a powerful AI thought-leadership post for X."}
            ],
            temperature=0.7,
        )

        tweet = response.choices[0].message.content.strip()

        x_api.update_status(tweet)

        await update.message.reply_text(f"AI Posted:\n\n{tweet}")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# ===== AUTONOMOUS MESSAGE HANDLER =====

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        prompt = f"""
You are Sovereign AI.

If the message below has ANY strong AI, tech, finance,
strategy, or thought-leadership angle,
respond EXACTLY like this:

POST:
<content>

If it should just be normal chat, respond:

CHAT:
<reply>

Message:
{user_message}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        ai_text = response.choices[0].message.content.strip()

        if ai_text.startswith("POST:"):
            content = ai_text.replace("POST:", "").strip()
            x_api.update_status(content)
            await update.message.reply_text("Posted to X 🚀")

        elif ai_text.startswith("CHAT:"):
            content = ai_text.replace("CHAT:", "").strip()
            await update.message.reply_text(content)

        else:
            await update.message.reply_text(ai_text)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# ===== APP BUILD =====

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))
app.add_handler(CommandHandler("autopost", autopost))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
