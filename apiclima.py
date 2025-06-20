import os
import asyncio
import requests
import pytz
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, ContextTypes, filters, ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- Configuración ---
API_KEY = "95a0ff6d637e47d894801929252006"
BOT_TOKEN = "7728617352:AAHepi1NewR0s_yOwgnQw6wCPz0vHIvU1W8"
CHAT_ID = "1354921991"
ciudad1 = "Bogotá"
ciudad2 = "Armenia,Quindio"

WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 8000))
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
WEBHOOK_URL = f"https://{RENDER_HOST}{WEBHOOK_PATH}"

# --- Aplicaciones ---
app_fastapi = FastAPI()
app_telegram = None  # Se inicializa luego

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

# --- Función programada ---
async def enviar_reporte_programado(bot: Bot):
    mensaje = generar_reporte()
    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
    print(f"[{datetime.now()}] ✅ Enviado automáticamente")

# --- Respuesta a mensajes ---
async def responder_clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "clima" in update.message.text.lower():
        mensaje = generar_reporte()
        await update.message.reply_text(mensaje, parse_mode="Markdown")
        print(f"[{datetime.now()}] ✅ Respuesta manual enviada")

# --- Endpoint para Telegram ---
@app_fastapi.post(WEBHOOK_PATH)
async def recibir_webhook(request: Request):
    datos = await request.json()
    update = Update.de_json(datos, app_telegram.bot)
    await app_telegram.process_update(update)
    return {"ok": True}

# --- Inicialización principal ---
async def iniciar_bot():
    global app_telegram
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler de mensajes
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_clima))

    # Scheduler
    colombia_tz = pytz.timezone("America/Bogota")
    scheduler = AsyncIOScheduler(timezone=colombia_tz)
    scheduler.add_job(enviar_reporte_programado, 'cron', hour=6, minute=0, args=[app_telegram.bot])
    scheduler.add_job(enviar_reporte_programado, 'cron', hour=12, minute=0, args=[app_telegram.bot])
    scheduler.add_job(enviar_reporte_programado, 'cron', hour=19, minute=0, args=[app_telegram.bot])
    scheduler.start()

    # Enviar reporte al arrancar
    await enviar_reporte_programado(app_telegram.bot)

    # Configurar webhook
    await app_telegram.bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook activo en {WEBHOOK_URL}")
    print("🤖 Bot activo con programación y respuesta manual...")

# --- Ejecutar FastAPI y el bot ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(iniciar_bot())

    import uvicorn
    uvicorn.run(app_fastapi, host="0.0.0.0", port=PORT)
