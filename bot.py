from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# כתובת בסיס של קבצי התמונות בגיטהאב
GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/omrihazan97/emporium-bot/master/images"

# הטוקן של הבוט שלך
BOT_TOKEN = "8036195196:AAEkOQC_tO0WmGxuc3WbBikFmfqFKMJwMPo"

# הפונקציה שמופעלת כששולחים לבוט טקסט
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    image_url = f"{GITHUB_IMAGE_URL}/{text}.jpg"
    
    try:
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        await update.message.reply_text("לא מצאתי תמונה מתאימה 😕")

# הפעלת הבוט
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
