from plyer import notification
from datetime import datetime
import platform

class DesktopNotifier:
    """Gerenciador de notificacoes desktop"""
    
    def __init__(self):
        self.app_name = "WeatherAlert"
        self.system = platform.system()
        print(f"Desktop notifier inicializado para {self.system}")
    
    def send_weather_alert(self, title: str, message: str, timeout: int = 10):
        """Envia notificacao desktop"""
        try:
            notification.notify(
                title=title[:64],
                message=message[:256],
                app_name=self.app_name,
                timeout=timeout,
                ticker="WeatherAlert"
            )
            print(f"Notificacao desktop enviada: {title}")
            return True
        except Exception as e:
            print(f"Erro ao enviar notificacao desktop: {e}")
            return False
    
    def send_daily_summary(self, city: str, weather_data: dict):
        """Envia resumo diario do clima"""
        temp = weather_data.get('temp', 'N/A')
        description = weather_data.get('description', 'N/A')
        humidity = weather_data.get('humidity', 'N/A')
        
        title = f"Resumo do Clima - {city}"
        message = f"Temperatura: {temp}C\nCondicao: {description}\nUmidade: {humidity}%\nData: {datetime.now().strftime('%d/%m/%Y')}"
        return self.send_weather_alert(title, message)
    
    def send_alert(self, city: str, alert_type: str, value: float):
        """Envia alerta climatico"""
        icons = {
            'high_temp': 'Fogo',
            'low_temp': 'Frio',
            'rain': 'Chuva',
            'storm': 'Tempestade'
        }
        
        icon = icons.get(alert_type, 'Alerta')
        title = f"{icon} - {city}"
        
        messages = {
            'high_temp': f"Temperatura muito alta! {value}C",
            'low_temp': f"Frio intenso! {value}C",
            'rain': f"Chuva forte prevista!",
            'storm': f"Tempestade iminente!"
        }
        
        message = messages.get(alert_type, f"Alerta climatico: {value}")
        return self.send_weather_alert(title, message, timeout=15)
