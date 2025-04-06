# Telegram Bot для получения баланса и цен
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from testr import get_balance_and_prices

import io
import sys

BOT_TOKEN = "7778594685:AAG3g5o0hMlYefMMiQBtCcm8m5zFkWrSp1I"

# ID чата, куда бот будет отправлять сообщения
user_chat_id = None

# Получение текста из функции
def capture_output():
    buffer = io.StringIO()
    sys.stdout = buffer
    get_balance_and_prices()
    sys.stdout = sys.__stdout__
    return buffer.getvalue()

# Планируемая задача — слать баланс каждые 10 минут
def send_auto_balance(app):
    if user_chat_id:
        text = capture_output()
        app.bot.send_message(chat_id=user_chat_id, text=text)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_chat_id
    user_chat_id = update.effective_chat.id
    await update.message.reply_text("🔔 Подписка включена! Буду слать тебе баланс каждые 10 минут.")

# Команда /balance вручную
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = capture_output()
    await update.message.reply_text(text or "Нет данных.")

# Запуск приложения
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))

# Планировщик
scheduler = BackgroundScheduler()
scheduler.add_job(send_auto_balance, 'interval', minutes=10, args=[app])
scheduler.start()

print("Бот запущен с автообновлением каждые 10 минут.")
app.run_polling()