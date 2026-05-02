from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import threading
from datetime import datetime
import uvicorn

app = FastAPI()
TOPICO = "weatheralert_marco"

# Banco de temperaturas para várias cidades
TEMPERATURAS = {
    'sao paulo': 22, 'rio de janeiro': 28, 'belo horizonte': 24,
    'porto alegre': 18, 'salvador': 30, 'curitiba': 16,
    'recife': 29, 'brasilia': 26, 'fortaleza': 31, 'manaus': 32,
    'belem': 33, 'goiania': 27, 'campinas': 23, 'santos': 25,
}

def enviar_notificacao(titulo, mensagem, prioridade=5):
    """Envia notificação para o celular"""
    try:
        msg_limpa = mensagem.replace('"', '').replace('\n', ' ')[:200]
        titulo_limpo = titulo.replace('"', '')[:50]
        
        cmd = f'curl.exe -s -X POST -H "Title: {titulo_limpo}" -H "Priority: {prioridade}" -d "{msg_limpa}" https://ntfy.sh/{TOPICO}'
        
        print(f"📤 [{datetime.now().strftime('%H:%M:%S')}] {titulo_limpo}")
        
        def enviar():
            try:
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
                print(f"✅ Notificação enviada!")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        threading.Thread(target=enviar).start()
        return True
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False

@app.get("/")
def root():
    return {"status": "online", "topic": TOPICO, "mensagem": "WeatherAlert Ativo"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/pesquisar/{cidade}")
def pesquisar_cidade(cidade: str):
    """Endpoint principal - pesquisar qualquer cidade e enviar notificação"""
    
    cidade_normalizada = cidade.lower().strip()
    
    # Buscar temperatura
    if cidade_normalizada in TEMPERATURAS:
        temp_base = TEMPERATURAS[cidade_normalizada]
        variacao = (hash(cidade) % 9) - 4
        temp = temp_base + variacao
    else:
        temp = 22 + (hash(cidade) % 15)
    
    # Ajustar temperatura
    temp = max(5, min(45, temp))
    
    # Decidir tipo de alerta
    if temp >= 35:
        tipo_clima = "calor"
        descricao = f"🔥 CALOR INTENSO! {temp}°C"
        recomendacao = "💧 Beba água, use protetor solar e evite sol 10h-16h!"
        emoji = "🔥"
    elif temp <= 12:
        tipo_clima = "frio"
        descricao = f"❄️ FRIO INTENSO! {temp}°C"
        recomendacao = "🧣 Agasalhe-se bem e mantenha-se aquecido!"
        emoji = "❄️"
    else:
        tipo_clima = "normal"
        descricao = f"🌤️ Clima agradável com {temp}°C"
        recomendacao = "😎 Aproveite o dia!"
        emoji = "🌤️"
    
    # Montar notificação
    titulo = f"{emoji} WeatherAlert - {cidade.title()}"
    mensagem = f"""📍 LOCAL: {cidade.title()}
🌡️ TEMPERATURA: {temp}°C
📝 CONDIÇÃO: {descricao}

💡 RECOMENDAÇÃO: {recomendacao}

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🔔 WeatherAlert - Monitoramento Ativo"""
    
    # Enviar notificação
    enviar_notificacao(titulo, mensagem)
    
    return {
        "sucesso": True,
        "cidade": cidade,
        "temperatura": temp,
        "descricao": descricao,
        "recomendacao": recomendacao,
        "alerta": tipo_clima,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/weather/now/{cidade}")
def weather(cidade: str):
    """Alias para /pesquisar/"""
    return pesquisar_cidade(cidade)

@app.get("/notificar/{cidade}")
def notificar(cidade: str):
    """Alias para /pesquisar/"""
    return pesquisar_cidade(cidade)

if __name__ == "__main__":
    print("=" * 60)
    print("🌤️ WeatherAlert - Sistema Completo")
    print("=" * 60)
    print(f"📱 Tópico: {TOPICO}")
    print(f"📊 Dashboard: http://127.0.0.1:8000/dashboard")
    print(f"🔍 Exemplo: http://127.0.0.1:8000/pesquisar/Sao%20Paulo")
    print("=" * 60)
    print("✅ Servidor iniciando...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
