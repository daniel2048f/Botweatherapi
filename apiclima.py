import asyncio
import requests
import pytz
import nest_asyncio
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- Configuración ---
API_KEY = "95a0ff6d637e47d894801929252006"
BOT_TOKEN = "7728617352:AAHepi1NewR0s_yOwgnQw6wCPz0vHIvU1W8"
CHAT_ID = "1354921991"
ciudad1 = "Bogotá"
ciudad2 = "Armenia,Quindio"

# --- Funciones del clima ---
def obtener_clima(ciudad):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={ciudad}&lang=es"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        nombre = datos["location"]["name"]
        pais = datos["location"]["country"]
        temp = datos["current"]["temp_c"]
        condicion = datos["current"]["condition"]["text"]
        return f"Clima en {nombre}, {pais}: {condicion}, {temp}°C"
    else:
        return f"Error al obtener el clima de {ciudad}"

def generar_reporte():
    clima1 = obtener_clima(ciudad1)
    clima2 = obtener_clima(ciudad2)
    return f"""
🌤️ *Reporte del clima*

{clima1}
{clima2}
"""

# --- Función para enviar el reporte programado ---
async def enviar_reporte_programado(bot: Bot):
    mensaje = generar_reporte()
    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
    print(f"[{datetime.now()}] ✅ Enviado automáticamente")

# --- Función para responder a mensajes con "clima" ---
async def responder_clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "clima" in update.message.text.lower():
        mensaje = generar_reporte()
        await update.message.reply_text(mensaje, parse_mode="Markdown")
        print(f"[{datetime.now()}] ✅ Respuesta manual enviada")

# --- Función principal ---
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Configura respuestas a texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_clima))

    # Scheduler para envío automático
    colombia_tz = pytz.timezone("America/Bogota")
    scheduler = AsyncIOScheduler(timezone=colombia_tz)
    scheduler.add_job(enviar_reporte_programado, 'cron', hour=6, minute=0, args=[app.bot])
    scheduler.add_job(enviar_reporte_programado, 'cron', hour=12, minute=0, args=[app.bot])
    scheduler.add_job(enviar_reporte_programado, 'cron', hour=20, minute=32, args=[app.bot])

    scheduler.start()

    # Enviar uno al arrancar
    await enviar_reporte_programado(app.bot)

    print("🤖 Bot activo con programación y respuesta manual...")
    await app.run_polling()

# --- Ejecutar ---
nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())
