import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# הגדרת לוגים למעקב
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# נתיב לתיקיית התמונות במחשב שלך
IMAGE_FOLDER = r"C:\telgram dels"

# טוקן של הבוט שלך
BOT_TOKEN = "8036195196:AAEkOQC_tO0WmGxuc3WbBikFmfqFKMJwMPo"

# הפונקציה שמופעלת כשהבוט מקבל הודעה
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        filename = f"{text}.jpg"
        filepath = os.path.join(IMAGE_FOLDER, filename)

        logging.info(f"מחפש קובץ: {filepath}")

        if os.path.isfile(filepath):
            with open(filepath, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
                logging.info(f"נשלחה תמונה: {filename}")
        else:
            await update.message.reply_text("לא מצאתי תמונה מתאימה 😕")
            logging.warning("קובץ לא נמצא")
    except Exception as e:
        logging.error(f"שגיאה כללית: {e}")
        await update.message.reply_text("אירעה שגיאה בטיפול בבקשה 😢")

# הפעלת הבוט
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("הבוט פעיל ומחכה להודעות...")
    app.run_polling()
