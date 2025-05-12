import logging
import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# הגדרת לוגים
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)  # תיקון: שימוש ב-name במקום name

# כתובת בסיס של קבצי התמונות בגיטהאב
GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/omrihazan97/emporium-bot/master/images"

# הטוקן של הבוט שלך
BOT_TOKEN = os.getenv("BOT_TOKEN")

# הפונקציה שמופעלת כששולחים לבוט טקסט
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    # ניקוי טקסט: המרת נקודה ל-underscore והשארת רק אותיות, מספרים ונקודות
    text = re.sub(r'[^\w.]', '', text).replace('.', '_')
    if not text:
        await update.message.reply_text("אנא שלח מספר או טקסט תקין")
        return
    image_url = f"{GITHUB_IMAGE_URL}/{text}.jpg"
    logger.info(f"Attempting to send image: {image_url}")
    
    try:
        await update.message.reply_photo(photo=image_url)
        logger.info("Image sent successfully")
    except Exception as e:
        logger.error(f"Error sending image: {e}")
        await update.message.reply_text("לא מצאתי תמונה מתאימה 😕")

# הפעלת הבוט
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
logger.info("Starting bot...")
app.run_polling()
