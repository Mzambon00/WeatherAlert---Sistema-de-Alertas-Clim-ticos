import httpx
from loguru import logger
from datetime import datetime
from typing import Dict, List, Optional

class WeatherService:
    """Servico de clima usando OpenWeatherMap API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.client = httpx.Client(timeout=10.0)
    
    def get_current_weather(self, city: str) -> Optional[Dict]:
        """Obtem clima atual da cidade"""
        try:
            response = self.client.get(
                f"{self.base_url}/weather",
                params={
                    'q': f"{city},BR",
                    'appid': self.api_key,
                    'units': 'metric',
                    'lang': 'pt_br'
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'temp': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'city': city,
                'timestamp': datetime.now()
            }
        except Exception as e:
            logger.error(f"Erro ao obter clima para {city}: {e}")
            return None
    
    def get_forecast(self, city: str, days: int = 7) -> List[Dict]:
        """Obtem previsao estendida"""
        try:
            response = self.client.get(
                f"{self.base_url}/forecast",
                params={
                    'q': f"{city},BR",
                    'appid': self.api_key,
                    'units': 'metric',
                    'lang': 'pt_br',
                    'cnt': days * 8
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Agrupar por dia
            forecast_by_day = {}
            for item in data['list']:
                date = item['dt_txt'].split()[0]
                if date not in forecast_by_day:
                    forecast_by_day[date] = {
                        'temps': [],
                        'descriptions': [],
                        'humidities': [],
                        'date': date
                    }
                
                forecast_by_day[date]['temps'].append(item['main']['temp'])
                forecast_by_day[date]['descriptions'].append(item['weather'][0]['description'])
                forecast_by_day[date]['humidities'].append(item['main']['humidity'])
            
            # Processar cada dia
            forecast = []
            for date, data in forecast_by_day.items():
                forecast.append({
                    'date': datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'temp_min': round(min(data['temps']), 1),
                    'temp_max': round(max(data['temps']), 1),
                    'description': max(set(data['descriptions']), key=data['descriptions'].count),
                    'humidity': round(sum(data['humidities']) / len(data['humidities']))
                })
            
            return forecast[:days]
            
        except Exception as e:
            logger.error(f"Erro ao obter previsao para {city}: {e}")
            return []
