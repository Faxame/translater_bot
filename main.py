import json
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import http.client




# print(data.decode("utf-8"))

# Asinxron tarjima qilish funksiyasi
async def tarjima_matni(matn, manba_tili='auto', maqsad_tili='uz'):

    conn = http.client.HTTPSConnection("text-translator2.p.rapidapi.com")

    payload = "source_language=en&target_language=uz&text=" + matn

    headers = {
        'x-rapidapi-key': "04e4dbd979msh0af4a64dc93556dp139225jsndb7632f574c7",
        'x-rapidapi-host': "text-translator2.p.rapidapi.com",
        'Content-Type': "application/x-www-form-urlencoded"
    }

        
        
    try:
        conn.request("POST", "/translate", payload, headers)

        res = conn.getresponse()
        data = res.read()
        print(data)

        
        response_dict = json.loads(data.decode("utf-8"))

        # Extract the translated text
        
        translated_text = response_dict['data']['translatedText']
        return translated_text
        
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"

# Start komandasini ishlovchi handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men tarjimon botiman. Tarjima qilish uchun matn yuboring.")

# Foydalanuvchi xabariga javob beruvchi handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    tarjima = await tarjima_matni(matn)
    await update.message.reply_text(tarjima)

def main():
    # Telegram botni ishga tushirish
    application = Application.builder().token('7653297912:AAHFb5nvvLpaGsGMbF2jcOeiMfs1vy9dqEs').build()

    # Handlerlar qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
