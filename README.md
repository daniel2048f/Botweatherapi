# Bot de Clima con Telegram y FastAPI

Este proyecto implementa un bot de Telegram que accede a la API de WeatherAPI para enviar reportes automáticos del clima en dos ciudades predeterminadas: Bogotá y Armenia (Colombia). El bot también responde de manera manual al mensaje "clima", devolviendo el reporte actual. Se ha desplegado en [Render](https://render.com/) y utiliza FastAPI como framework web para manejar el webhook de Telegram.

---

## 📌 Características Principales

- ✅ Reportes automáticos del clima a las **6:00 a.m., 12:00 p.m. y 11:48 p.m.**
- 📩 Respuesta inmediata al mensaje `"clima"` en el chat de Telegram.
- 🌐 Desplegado en **Render** con soporte para webhook.
- 🔁 Tareas programadas con `APScheduler`.
- 🧪 Mensaje de prueba automático cada 2 minutos para verificar funcionamiento.
- ⚙️ Integra `FastAPI`, `python-telegram-bot` y `uvicorn`.

---

## ⚙️ Tecnologías Usadas

- Python 3.11.8 (`runtime.txt`)
- FastAPI
- python-telegram-bot (v20.8)
- APScheduler
- requests
- pytz
- uvicorn

---

## 🗂️ Estructura del Proyecto

```
├── apiclima.py              # Código principal del bot y FastAPI
├── requirements.txt         # Dependencias del proyecto
├── Dockerfile               # Configuración para desplegar en contenedores
├── runtime.txt              # Versión de Python para Render
└── README.md                # Documentación del proyecto
```

---

## 🚀 Despliegue en Render

El proyecto está listo para desplegarse en [Render](https://render.com):

1. Crear un nuevo servicio de tipo **Web Service**.
2. Configurar la rama del repositorio de GitHub.
3. Usar la siguiente configuración:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python apiclima.py`
4. Asegurar que el puerto 8000 esté disponible y que la URL del webhook se actualice correctamente.

---

## 📲 Instrucciones de Uso

1. Envía el mensaje **"clima"** al bot para recibir el estado actual de Bogotá y Armenia.
2. El bot también enviará reportes **automáticamente tres veces al día**.
3. Los mensajes se formatean con Markdown para una mejor visualización.

---

## 📚 Recomendaciones

- Cambiar los valores de las siguientes variables en `apiclima.py` antes de subirlo a GitHub:
  ```python
  API_KEY = "TU_API_KEY"
  BOT_TOKEN = "TU_BOT_TOKEN"
  CHAT_ID = "TU_CHAT_ID"
  ```

---

## 📬 Créditos

- Autor: Daniel Cangrejo
- Basado en `python-telegram-bot` v20 y `FastAPI`

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` si deseas más detalles.
