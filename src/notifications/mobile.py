import requests
from datetime import datetime

class MobileNotifier:
    def __init__(self, topic: str = "weatheralert_marco"):
        self.topic = topic
        print(f"📱 Mobile Notifier inicializado")
        print(f"📌 Topico: {topic}")
    
    def send_notification(self, title: str, message: str, priority: int = 3):
        """Envia notificacao usando o mesmo metodo que funcionou no teste"""
        try:
            # Usar o mesmo formato que funcionou no curl
            url = f"https://ntfy.sh/{self.topic}"
            
            print(f"📤 Enviando: {title}")
            
            response = requests.post(
                url,
                data=message.encode('utf-8'),
                headers={
                    "Title": title,
                    "Priority": str(priority),
                    "Tags": "cloud,thermometer"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Notificacao enviada com sucesso!")
                return True
            else:
                print(f"❌ Erro: Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def send_weather_alert(self, city: str, temp: float, alert_type: str):
        """Envia alerta climatico"""
        if alert_type == 'high_temp':
            title = f"🔥 ALERTA DE CALOR - {city}"
            message = f"🌡️ Temperatura extremamente alta: {temp}°C!\n\n⚠️ Mantenha-se hidratado, evite sol entre 10h-16h.\n📍 {city}\n🕐 {datetime.now().strftime('%H:%M')}"
            priority = 5
        elif alert_type == 'low_temp':
            title = f"❄️ ALERTA DE FRIO - {city}"
            message = f"🌡️ Temperatura muito baixa: {temp}°C!\n\n⚠️ Proteja-se do frio, agasalhe-se bem.\n📍 {city}\n🕐 {datetime.now().strftime('%H:%M')}"
            priority = 5
        else:
            title = f"⚠️ ALERTA CLIMATICO - {city}"
            message = f"⚠️ Condicao climatica severa detectada!\n📍 {city}"
            priority = 4
        
        return self.send_notification(title, message, priority)
    
    def send_daily_summary(self, city: str, weather_data: dict):
        """Envia resumo diario"""
        temp = weather_data.get('temp', 'N/A')
        description = weather_data.get('description', 'N/A')
        
        title = f"🌤️ RESUMO DO CLIMA - {city}"
        message = f"🌡️ Temperatura: {temp}°C\n📝 Condicao: {description}\n\n📅 {datetime.now().strftime('%d/%m/%Y')}"
        
        return self.send_notification(title, message, priority=3)
