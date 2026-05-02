from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
from datetime import datetime
import uvicorn

app = FastAPI()

TOPICO = "weatheralert_marco"

def enviar_notificacao(titulo, mensagem):
    """Usa curl.exe para enviar (mesmo metodo que funcionou)"""
    try:
        # Escapar aspas na mensagem
        mensagem_escapada = mensagem.replace('"', '\\"')
        
        # Comando curl
        cmd = f'curl.exe -X POST -H "Title: {titulo}" -H "Priority: 5" -d "{mensagem_escapada}" https://ntfy.sh/{TOPICO}'
        
        # Executar
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Notificacao enviada: {titulo}")
            return True
        else:
            print(f"❌ Erro: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Excecao: {e}")
        return False

@app.get("/")
def root():
    return {"status": "online", "topic": TOPICO, "message": "WeatherAlert API"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/testar")
def testar():
    """Teste simples - vai enviar notificacao"""
    sucesso = enviar_notificacao(
        "WeatherAlert Teste",
        f"Conexao estabelecida em {datetime.now().strftime('%H:%M:%S')}\n\nVoce recebera alertas climaticos!"
    )
    return {"sucesso": sucesso, "mensagem": "Notificacao enviada para o celular"}

@app.get("/alerta/calor/{cidade}")
def alerta_calor(cidade: str, temp: float = 38):
    """Alerta de calor"""
    sucesso = enviar_notificacao(
        f"ALERTA DE CALOR - {cidade}",
        f"Temperatura: {temp}C\n\n⚠️ Mantenha-se hidratado!\nEvite sol entre 10h e 16h."
    )
    return {"sucesso": sucesso, "cidade": cidade, "temperatura": temp}

@app.get("/alerta/frio/{cidade}")
def alerta_frio(cidade: str, temp: float = 5):
    """Alerta de frio"""
    sucesso = enviar_notificacao(
        f"ALERTA DE FRIO - {cidade}",
        f"Temperatura: {temp}C\n\n⚠️ Proteja-se do frio!\nAgasalhe-se bem."
    )
    return {"sucesso": sucesso, "cidade": cidade, "temperatura": temp}

@app.get("/weather/now/{cidade}")
def weather(cidade: str):
    """Clima atual com alerta automatico"""
    cidade_lower = cidade.lower()
    
    # Simular temperaturas
    if "paulo" in cidade_lower:
        temp = 38
        alerta = "calor"
    elif "porto" in cidade_lower or "alegre" in cidade_lower:
        temp = 5
        alerta = "frio"
    elif "rio" in cidade_lower:
        temp = 39
        alerta = "calor"
    else:
        temp = 25
        alerta = None
    
    # Enviar alerta se necessario
    if alerta == "calor":
        enviar_notificacao(
            f"ALERTA DE CALOR - {cidade}",
            f"Temperatura atual: {temp}C!\n\nMantenha-se hidratado e evite exposicao ao sol."
        )
    elif alerta == "frio":
        enviar_notificacao(
            f"ALERTA DE FRIO - {cidade}",
            f"Temperatura atual: {temp}C!\n\nProteja-se do frio e agasalhe-se bem."
        )
    
    return {
        "cidade": cidade,
        "temperatura": temp,
        "timestamp": datetime.now().isoformat(),
        "alerta_enviado": alerta is not None
    }

if __name__ == "__main__":
    print("=" * 50)
    print("🌤️ WeatherAlert Server - Versao Final")
    print("=" * 50)
    print(f"📌 Topico: {TOPICO}")
    print(f"🧪 Teste: http://127.0.0.1:8000/testar")
    print(f"🔥 Calor: http://127.0.0.1:8000/alerta/calor/SaoPaulo?temp=38")
    print(f"❄️ Frio: http://127.0.0.1:8000/alerta/frio/PortoAlegre?temp=5")
    print(f"🌡️ Clima: http://127.0.0.1:8000/weather/now/SaoPaulo")
    print(f"📊 Dashboard: http://127.0.0.1:8000/dashboard")
    print("=" * 50)
    print("✅ Servidor iniciando...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
