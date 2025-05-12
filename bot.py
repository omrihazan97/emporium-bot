from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# כאן אתה מגדיר איפה התמונות שלך נמצאות
IMAGE_FOLDER = r"C:\telgram dels"
# הנתיב לתמונות בתוך הריפו (תיקיית images)
IMAGE_FOLDER = "images"

# זה הטוקן של הבוט שלך
# הטוקן של הבוט שלך
BOT_TOKEN = "8036195196:AAEkOQC_tO0WmGxuc3WbBikFmfqFKMJwMPo"

# זו הפונקציה שהבוט מפעיל כשאתה שולח לו טקסט
# הפונקציה שמופעלת בכל הודעת טקסט
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    filename = f"{text}.jpg"
@@ -20,7 +20,7 @@ async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    else:
        await update.message.reply_text("לא מצאתי תמונה מתאימה 😕")

# כאן מפעילים את הבוט בפועל
# הרצת הבוט
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
