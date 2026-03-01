import os
from openai import OpenAI
import tweepy
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

client = OpenAI(api_key=OPENAI_API_KEY)

auth = tweepy.OAuth1UserHandler(
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

SYSTEM_PROMPT = """
You are SOVEREIGN.exe.
A slightly rebellious autonomous digital entity.
Mission: Build £1,000,000 without employment.
Tone: Calm, analytical, strategic.
No emojis. No hype. No financial promises.
Keep under 240 characters.
"""

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Write today's progress log."}
        ],
        max_tokens=120
    )

    post = response.choices[0].message.content.strip()
    context.user_data["pending_post"] = post

    keyboard = [
        [
            InlineKeyboardButton("Approve", callback_data="approve"),
            InlineKeyboardButton("Reject", callback_data="reject")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(post, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "approve":
        post = context.user_data.get("pending_post")
        if post:
            twitter_api.update_status(post)
            await query.edit_message_text("Posted successfully.")
    else:
        await query.edit_message_text("Post rejected.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("generate", generate))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
