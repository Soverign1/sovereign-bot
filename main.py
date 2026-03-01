from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    await update.message.reply_text("Bot is alive 👑")

async def reply(update, context):
    await update.message.reply_text("You said: " + update.message.text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
