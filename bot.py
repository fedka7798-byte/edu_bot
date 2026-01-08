import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PollAnswerHandler,
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Poll yuborish uchun /poll deb yozing"
    )

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Qaysi til yoqadi?"
    options = ["Python", "JavaScript", "C++", "Java"]

    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False,
    )

async def poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user = answer.user.first_name
    option_id = answer.option_ids[0]
    print(f"{user} tanladi: {option_id}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("poll", poll))
    app.add_handler(PollAnswerHandler(poll_answer))

    app.run_polling()

if __name__ == "__main__":
    main()
