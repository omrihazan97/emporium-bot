import logging
import re
import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/omrihazan97/emporium-bot/master/images"

logger.debug("Loading BOT_TOKEN from environment...")
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set! Please set it in environment variables.")
    raise ValueError("BOT_TOKEN is not set")

application = Application.builder().token(BOT_TOKEN).build()

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

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post(f"/{BOT_TOKEN}")
async def webhook(request: Request):
    update = await request.json()
    await application.process_update(Update.de_json(update, application.bot))
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    logger.info("Starting bot...")
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
    logger.info(f"Setting webhook to: {webhook_url}")
    await application.bot.set_webhook(url=webhook_url)
    logger.info("Webhook set successfully")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down bot...")
    await application.bot.delete_webhook()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)