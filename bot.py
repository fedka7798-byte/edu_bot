import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    PollAnswerHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

QUESTIONS = [
    {
        "q": "Avtomobil 18 km masofani 30 minutda bosib o'tdi. O‘rtacha tezlik?",
        "options": ["36 m/s", "10 km/soat", "36 km/soat", "To‘g‘ri javob yo‘q"],
        "correct": 2
    },
    {
        "q": "1 soat nechta sekund?",
        "options": ["60", "3600", "600", "360"],
        "correct": 1
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["index"] = 0
    context.user_data["score"] = 0
    await send_poll(update, context)

async def send_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data["index"]

    if idx >= len(QUESTIONS):
        await update.message.reply_text(
            f"✅ Test tugadi!\nNatija: {context.user_data['score']} / {len(QUESTIONS)}"
        )
        return

    q = QUESTIONS[idx]
    await update.message.reply_poll(
        question=q["q"],
        options=q["options"],
        type="quiz",
        correct_option_id=q["correct"],
        is_anonymous=True,
    )

async def poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data["index"]
    correct = QUESTIONS[idx]["correct"]

    if update.poll_answer.option_ids[0] == correct:
        context.user_data["score"] += 1

    context.user_data["index"] += 1
    await send_poll(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(PollAnswerHandler(poll_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
