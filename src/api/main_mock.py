from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import random

app = FastAPI(
    title="WeatherAlert API",
    description="Sistema de monitoramento climatico com alertas (Modo Demonstracao)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard")
async def dashboard():
    return FileResponse("index.html")

@app.get("/")
async def root():
    return {
        "message": "WeatherAlert API (Modo Demonstracao)",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "dashboard": "/dashboard",
        "docs": "/docs"
    }

@app.get("/weather/now/{city}")
async def get_current_weather(city: str):
    """Versao de demonstracao com dados simulados"""
    
    # Dados simulados para diferentes cidades
    weather_data = {
        "sao paulo": {"temp": 22, "feels_like": 21, "humidity": 65, "description": "Ceu parcialmente nublado", "wind_speed": 12, "pressure": 1015},
        "rio de janeiro": {"temp": 28, "feels_like": 29, "humidity": 70, "description": "Sol com algumas nuvens", "wind_speed": 8, "pressure": 1012},
        "belo horizonte": {"temp": 24, "feels_like": 23, "humidity": 60, "description": "Ceu claro", "wind_speed": 10, "pressure": 1018},
        "porto alegre": {"temp": 18, "feels_like": 17, "humidity": 75, "description": "Chuvoso", "wind_speed": 15, "pressure": 1010},
        "salvador": {"temp": 30, "feels_like": 32, "humidity": 80, "description": "Sol forte", "wind_speed": 5, "pressure": 1013},
        "curitiba": {"temp": 16, "feels_like": 15, "humidity": 82, "description": "Nublado", "wind_speed": 14, "pressure": 1020},
        "brasilia": {"temp": 26, "feels_like": 25, "humidity": 55, "description": "Ceu limpo", "wind_speed": 9, "pressure": 1016},
        "recife": {"temp": 29, "feels_like": 31, "humidity": 78, "description": "Sol com nuvens", "wind_speed": 11, "pressure": 1014},
        "fortaleza": {"temp": 31, "feels_like": 33, "humidity": 75, "description": "Sol", "wind_speed": 13, "pressure": 1012},
        "manaus": {"temp": 32, "feels_like": 34, "humidity": 85, "description": "Calor intenso", "wind_speed": 6, "pressure": 1009},
    }
    
    # Normalizar nome da cidade
    city_normalized = city.lower().strip()
    
    # Buscar dados
    for key in weather_data:
        if key in city_normalized or city_normalized in key:
            data = weather_data[key]
            return {
                'city': key.title(),
                'temp': data['temp'],
                'feels_like': data['feels_like'],
                'humidity': data['humidity'],
                'pressure': data['pressure'],
                'description': data['description'],
                'icon': '01d',
                'wind_speed': data['wind_speed'],
                'timestamp': datetime.now()
            }
    
    # Se não encontrou, retorna dados genéricos
    return {
        'city': city.title(),
        'temp': random.randint(18, 32),
        'feels_like': random.randint(17, 33),
        'humidity': random.randint(50, 90),
        'pressure': random.randint(1005, 1025),
        'description': random.choice(['Ceu claro', 'Parcialmente nublado', 'Nublado', 'Chuva fraca']),
        'icon': '01d',
        'wind_speed': random.randint(5, 20),
        'timestamp': datetime.now()
    }

@app.get("/weather/forecast/{city}")
async def get_weather_forecast(city: str, days: int = 5):
    """Versao de demonstracao com previsao simulada"""
    forecast = []
    conditions = ['Ceu claro', 'Parcialmente nublado', 'Nublado', 'Chuva fraca', 'Sol', 'Chuvoso']
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        forecast.append({
            'date': date.strftime('%d/%m/%Y'),
            'temp_min': round(18 + random.uniform(-8, 5), 1),
            'temp_max': round(25 + random.uniform(-5, 8), 1),
            'description': random.choice(conditions),
            'humidity': random.randint(50, 85)
        })
    return forecast

@app.post("/notifications/test-desktop")
async def test_desktop_notification():
    try:
        from plyer import notification
        notification.notify(
            title="WeatherAlert",
            message="Sistema de notificacoes funcionando!",
            timeout=5
        )
        return {"success": True, "message": "Notificacao desktop enviada"}
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🌤️ WeatherAlert - Modo Demonstracao")
    print("=" * 50)
    print("📊 Usando dados simulados (sem API key)")
    print("📖 Dashboard: http://127.0.0.1:8000/dashboard")
    print("📖 Documentacao: http://127.0.0.1:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)
