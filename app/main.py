import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from fastapi import FastAPI, Request

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger(__name__)


app = FastAPI()

ptb_app = Application.builder().token(os.getenv('BOT_TOKEN')).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Hi, {user.mention_html()}", parse_mode="HTML")

ptb_app.add_handler(CommandHandler("start", start))

@app.on_event("startup")
async def on_startup():
    await ptb_app.initialize()
    await ptb_app.start()
    asyncio.create_task(ptb_app.updater.start_polling())
    logger.info("BOT STARTED WITH POLLING")

@app.on_event("shutdown")
async def on_shutdown():
    await ptb_app.stop()
    await ptb_app.shutdown()

@app.get("/")
async def root():
    return {"status": "Bot is running"}

@app.get("/health")
async def health():
    return {"status" : "ok"}