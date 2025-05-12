import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# כאן אתה מגדיר איפה התמונות שלך נמצאות
IMAGE_FOLDER = r"C:\imeges"

# זה הטוקן של הבוט שלך
BOT_TOKEN = "8036195196:AAEkOQC_tO0WmGxuc3WbBikFmfqFKMJwMPo"

# זו הפונקציה שהבוט מפעיל כשאתה שולח לו טקסט
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    filename = f"{text}.jpg"
    filepath = os.path.join(IMAGE_FOLDER, filename)

    if os.path.isfile(filepath):
        with open(filepath, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
    else:
        await update.message.reply_text("לא מצאתי תמונה מתאימה 😕")

# כאן מפעילים את הבוט בפועל
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
