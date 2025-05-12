import logging
import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# הגדרת לוגים מפורטים
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# כתובת בסיס של קבצי התמונות בגיטהאב
GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/omrihazan97/emporium-bot/master/images"

# הטוקן של הבוט שלך
logger.debug("Loading BOT_TOKEN from environment...")
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set! Please set it in environment variables.")
    raise ValueError("BOT_TOKEN is not set")

# הפונקציה שמופעלת כששולחים לבוט טקסט
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message: {update.message.text}")
    await update.message.reply_text("קיבלתי את ההודעה שלך! מנסה לשלוח תמונה...")
    
    text = update.message.text.strip()
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
try:
    logger.debug("Building application...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    logger.debug("Adding message handler...")
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Starting bot with polling...")
    app.run_polling()
except Exception as e:
    logger.error(f"Failed to start bot: {e}")
    raise