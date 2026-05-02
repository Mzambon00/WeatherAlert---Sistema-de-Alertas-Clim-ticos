from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import threading
import time
from datetime import datetime
import uvicorn

app = FastAPI()
TOPICO = "weatheralert_marco"

# Fila de notificações para enviar em background
fila_notificacoes = []
ultimo_envio = {}

def enviar_notificacao(titulo, mensagem, cidade=""):
    """Envia notificação de forma independente"""
    try:
        # Limpar mensagem
        msg_limpa = mensagem.replace('"', ' ').replace('\n', ' ')[:200]
        titulo_limpo = titulo.replace('"', ' ')[:50]
        
        # Comando curl
        cmd = f'curl.exe -s -X POST -H "Title: {titulo_limpo}" -H "Priority: 5" -d "{msg_limpa}" https://ntfy.sh/{TOPICO}'
        
        # Executar em thread separada para não bloquear
        def enviar():
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] {titulo_limpo[:30]}...")
                else:
                    print(f"❌ Erro: {result.stderr}")
            except Exception as e:
                print(f"❌ Exceção: {e}")
        
        thread = threading.Thread(target=enviar)
        thread.start()
        return True
        
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False

@app.get("/")
def root():
    return {"status": "online", "topic": TOPICO, "mensagem": "Servidor otimizado"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/testar")
def testar():
    """Teste rápido de notificação"""
    sucesso = enviar_notificacao(
        "🧪 WeatherAlert Teste",
        f"Sistema conectado! {datetime.now().strftime('%H:%M:%S')}"
    )
    return {"sucesso": sucesso}

@app.get("/alerta/calor/{cidade}")
def alerta_calor(cidade: str, temp: float = 38):
    enviar_notificacao(
        f"🔥 ALERTA CALOR - {cidade}",
        f"🌡️ {temp}°C em {cidade}! Beba água e evite sol 10h-16h. 🧴"
    )
    return {"sucesso": True, "cidade": cidade, "temperatura": temp}

@app.get("/alerta/frio/{cidade}")
def alerta_frio(cidade: str, temp: float = 5):
    enviar_notificacao(
        f"❄️ ALERTA FRIO - {cidade}",
        f"🌡️ {temp}°C em {cidade}! Agasalhe-se e evite áreas abertas. 🧣"
    )
    return {"sucesso": True, "cidade": cidade, "temperatura": temp}

@app.get("/weather/now/{cidade}")
def weather(cidade: str):
    """Clima com notificação automática"""
    # Mapeamento de temperaturas realistas
    temperaturas = {
        'sao paulo': 22, 'rio de janeiro': 28, 'belo horizonte': 24,
        'porto alegre': 18, 'salvador': 30, 'curitiba': 16,
        'recife': 29, 'brasilia': 26, 'fortaleza': 31, 'manaus': 32
    }
    
    cidade_lower = cidade.lower()
    temp = temperaturas.get(cidade_lower, 25)
    
    # Decidir alerta
    if temp >= 35:
        alerta_calor(cidade, temp)
    elif temp <= 10:
        alerta_frio(cidade, temp)
    else:
        # Notificação normal
        enviar_notificacao(
            f"🌤️ Clima em {cidade}",
            f"{temp}°C - Clima agradável! Aproveite o dia. 😎"
        )
    
    return {
        "cidade": cidade,
        "temperatura": temp,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/enviar/{cidade}")
def enviar_manual(cidade: str, temp: int = 25):
    """Envia notificação personalizada"""
    enviar_notificacao(
        f"🌤️ WeatherAlert - {cidade}",
        f"Temperatura: {temp}°C\nUmidade: {65}%\nVento: {12} km/h"
    )
    return {"sucesso": True, "mensagem": f"Notificação enviada para {cidade}"}

if __name__ == "__main__":
    print("=" * 60)
    print("🌤️ WeatherAlert - Servidor Otimizado")
    print("=" * 60)
    print(f"📱 Tópico: {TOPICO}")
    print(f"🧪 Teste: http://127.0.0.1:8000/testar")
    print(f"🔥 Calor: http://127.0.0.1:8000/alerta/calor/SaoPaulo?temp=38")
    print(f"❄️ Frio: http://127.0.0.1:8000/alerta/frio/PortoAlegre?temp=5")
    print(f"🌤️ Clima: http://127.0.0.1:8000/weather/now/SaoPaulo")
    print(f"📤 Manual: http://127.0.0.1:8000/enviar/SaoPaulo?temp=25")
    print("=" * 60)
    print("✅ Servidor pronto para múltiplas notificações!")
    uvicorn.run(app, host="127.0.0.1", port=8000)
