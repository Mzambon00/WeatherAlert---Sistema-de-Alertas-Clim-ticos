import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailNotifier:
    """Gerenciador de envio de emails"""
    
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password
        print("Email notifier inicializado")
    
    def send_weather_report(self, to_email: str, city: str, weather_data: dict):
        """Envia relatorio climatico por email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = to_email
            msg['Subject'] = f"WeatherAlert - Clima em {city}"
            
            body = f"""
WeatherAlert - Relatorio do Clima

Cidade: {city}
Temperatura: {weather_data.get('temp', 'N/A')}C
Condicao: {weather_data.get('description', 'N/A')}
Umidade: {weather_data.get('humidity', 'N/A')}%
Vento: {weather_data.get('wind_speed', 'N/A')} km/h

Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

---
WeatherAlert - Seu monitor climatico pessoal
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email enviado para {to_email}")
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
