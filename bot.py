from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from parser_partiti import estrai_risultati

TOKEN = "7993221949:AAEiFnyfHfcBQANiKhg91KjkIROG1Tcr2z8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Scrivi /partiti per generare il risultato.")

async def partiti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ Elaboro...")
    risultato = estrai_risultati()   # ← ottieni la stringa

    await msg.edit_text(risultato) 

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("partiti", partiti))

app.run_polling()
