from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from testr import get_balance_and_prices  # Импорт функции из твоей программы

BOT_TOKEN = '7778594685:AAG3g5o0hMlYefMMiQBtCcm8m5zFkWrSp1I'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши /balance для просмотра баланса и цен.")

async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import io
    import sys


    buffer = io.StringIO()
    sys.stdout = buffer
    get_balance_and_prices()
    sys.stdout = sys.__stdout__
    result = buffer.getvalue()

    await update.message.reply_text(result or "Нет данных.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", show_balance))

print("Бот запущен...") 
app.run_polling()