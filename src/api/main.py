from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from src.scraper.weather_api import WeatherService
from src.notifications.desktop import DesktopNotifier
from src.notifications.email import EmailNotifier

# Configuracoes
API_KEY = os.getenv('OPENWEATHER_API_KEY')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
DEFAULT_CITIES = os.getenv('DEFAULT_CITIES', 'Sao Paulo,Rio de Janeiro,Belo Horizonte').split(',')

# Inicializar servicos
weather_service = WeatherService(API_KEY) if API_KEY else None
desktop_notifier = DesktopNotifier()
email_notifier = EmailNotifier(EMAIL_USER, EMAIL_PASSWORD) if EMAIL_USER and EMAIL_PASSWORD else None

app = FastAPI(
    title="WeatherAlert API",
    description="Sistema de monitoramento climatico com alertas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivo HTML
@app.get("/dashboard")
async def dashboard():
    return FileResponse("index.html")

@app.get("/")
async def root():
    return {
        "message": "WeatherAlert API",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "dashboard": "/dashboard",
        "docs": "/docs"
    }

@app.get("/weather/now/{city}")
async def get_current_weather(city: str):
    if not weather_service:
        raise HTTPException(status_code=503, detail="Weather service not configured")
    
    weather = weather_service.get_current_weather(city)
    if not weather:
        raise HTTPException(status_code=404, detail=f"City {city} not found")
    
    desktop_notifier.send_daily_summary(city, weather)
    return weather

@app.get("/weather/forecast/{city}")
async def get_weather_forecast(city: str, days: int = 5):
    if not weather_service:
        raise HTTPException(status_code=503, detail="Weather service not configured")
    
    forecast = weather_service.get_forecast(city, days)
    if not forecast:
        raise HTTPException(status_code=404, detail=f"Forecast for {city} not found")
    
    return forecast

@app.post("/notifications/test-desktop")
async def test_desktop_notification():
    success = desktop_notifier.send_weather_alert(
        "WeatherAlert Teste",
        "Sistema de notificacoes funcionando!"
    )
    return {"success": success}

@app.post("/notifications/test-email")
async def test_email_notification():
    if not email_notifier:
        raise HTTPException(status_code=503, detail="Email service not configured")
    
    test_weather = {
        'temp': 25.5,
        'description': 'Ceu claro',
        'humidity': 65,
        'pressure': 1012,
        'wind_speed': 10
    }
    
    success = email_notifier.send_weather_report("marcoszambon18@gmail.com", "Sao Paulo", test_weather)
    return {"success": success, "message": "Email de teste enviado para marcoszambon18@gmail.com"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
