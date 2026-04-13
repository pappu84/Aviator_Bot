import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# প্রতিটি chat এর জন্য running task রাখবে
running_tasks = {}

def generate_signal():
    # RNG based fake signal (custom logic)
    return round(random.uniform(1.2, 3.5), 2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = generate_signal()
    await update.message.reply_text(f"🚀 Signal: Cashout at {value}x")

async def autosignal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # যদি আগে থেকেই running থাকে
    if chat_id in running_tasks:
        await update.message.reply_text("⚠️ Auto signal already running!")
        return

    await update.message.reply_text("▶️ Auto signal started (RNG mode)")

    async def loop():
        while True:
            await asyncio.sleep(15)
            value = generate_signal()
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"📡 Auto Signal (RNG): {value}x"
            )

    task = asyncio.create_task(loop())
    running_tasks[chat_id] = task

async def stopsignal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    task = running_tasks.get(chat_id)

    if task:
        task.cancel()
        del running_tasks[chat_id]
        await update.message.reply_text("⛔ Auto signal stopped successfully!")
    else:
        await update.message.reply_text("ℹ️ No running auto signal found.")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("autosignal", autosignal))
    app.add_handler(CommandHandler("stopsignal", stopsignal))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()