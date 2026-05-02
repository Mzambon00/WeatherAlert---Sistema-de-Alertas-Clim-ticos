from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import random
from src.notifications.mobile import MobileNotifier

app = FastAPI(title="WeatherAlert API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar notificador
mobile = MobileNotifier(topic="weatheralert_marco")

@app.get("/")
async def root():
    return {
        "message": "WeatherAlert API",
        "status": "online",
        "topic": "weatheralert_marco",
        "dashboard": "/dashboard"
    }

@app.get("/dashboard")
async def dashboard():
    return FileResponse("index.html")

@app.get("/notifications/test")
async def test_notification():
    """Teste simples de notificacao"""
    success = mobile.send_notification(
        "🧪 WeatherAlert Teste",
        "✅ Sistema funcionando!\n\nVocê receberá alertas climáticos em tempo real.\n\n📱 App conectado com sucesso!",
        priority=5
    )
    return {"success": success, "message": "Teste enviado"}

@app.get("/notifications/alert/{city}/{alert_type}")
async def send_alert(city: str, alert_type: str, temp: float = 0):
    """Enviar alerta climatico"""
    success = mobile.send_weather_alert(city, temp, alert_type)
    return {"success": success, "alert_type": alert_type, "city": city}

@app.get("/weather/now/{city}")
async def get_weather(city: str):
    """Clima atual com alertas automáticos para teste"""
    
    # Dados para teste com alertas
    weather_db = {
        "saopaulo": {"temp": 38, "desc": "Muito quente", "alert": "high_temp"},
        "riodejaneiro": {"temp": 39, "desc": "Calor extremo", "alert": "high_temp"},
        "portoalegre": {"temp": 5, "desc": "Muito frio", "alert": "low_temp"},
        "default": {"temp": 25, "desc": "Clima agradavel", "alert": None}
    }
    
    city_key = city.lower().replace(" ", "")
    data = weather_db.get(city_key, weather_db["default"])
    
    result = {
        "city": city.title(),
        "temp": data["temp"],
        "description": data["desc"],
        "timestamp": datetime.now()
    }
    
    # Enviar alerta se houver condicao severa
    if data["alert"]:
        mobile.send_weather_alert(city, data["temp"], data["alert"])
    
    return result

@app.get("/weather/forecast/{city}")
async def get_forecast(city: str, days: int = 5):
    """Previsao estendida"""
    forecast = []
    conditions = ['Ceu claro', 'Parcialmente nublado', 'Sol', 'Chuva fraca']
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        forecast.append({
            'date': date.strftime('%d/%m/%Y'),
            'temp_min': round(18 + random.uniform(-5, 5), 1),
            'temp_max': round(25 + random.uniform(-3, 8), 1),
            'description': random.choice(conditions),
            'humidity': random.randint(55, 85)
        })
    
    return forecast

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🌤️ WeatherAlert - Sistema Ativo")
    print("=" * 50)
    print("📱 App ntfy: weatheralert_marco")
    print("🧪 Teste: http://127.0.0.1:8000/notifications/test")
    print("🌡️ Alerta calor: http://127.0.0.1:8000/notifications/alert/SaoPaulo/high_temp?temp=38")
    print("📊 Dashboard: http://127.0.0.1:8000/dashboard")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)
