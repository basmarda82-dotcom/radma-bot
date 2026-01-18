import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import openai
import os

# ===== الإعدادات =====
BOT_TOKEN = "8504081684:AAFsrsfHQOQ_piIRmbMTURb-VQ3IU-ukYuo"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===== رسالة البداية =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً {name} 👋\n"
        "أنا بوت 𓆩𝕽𝖆𝖉𝖒𝖆𓆪 🤖\n"
        "اسألني أي سؤال وأنا أرد عليك بالذكاء الاصطناعي 💙"
    )

# ===== الرد بالذكاء الاصطناعي =====
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وترد بالعربية"},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("حصل خطأ 😢 حاول مرة تانية")

# ===== تشغيل البوت =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
