from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
from datetime import datetime
import uvicorn

app = FastAPI()
TOPICO = "weatheralert_marco"

def enviar(titulo, mensagem):
    """Usa o MESMO método que funcionou no teste"""
    cmd = f'curl.exe -X POST -H "Title: {titulo}" -H "Priority: 5" -d "{mensagem}" https://ntfy.sh/{TOPICO}'
    resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return resultado.returncode == 0

@app.get("/")
def root():
    return {"status": "online", "topic": TOPICO}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/testar")
def testar():
    """Teste rápido - deve enviar notificação"""
    sucesso = enviar(
        "🧪 WeatherAlert Teste",
        f"✅ Sistema conectado em {datetime.now().strftime('%H:%M:%S')}\n\nVocê receberá alertas climáticos!"
    )
    return {"sucesso": sucesso, "mensagem": "Teste enviado"}

@app.get("/alerta/calor/{cidade}")
def alerta_calor(cidade: str, temp: float = 38):
    sucesso = enviar(
        f"🔥 ALERTA DE CALOR - {cidade}",
        f"🌡️ Temperatura: {temp}°C\n\n⚠️ Mantenha-se hidratado!\nEvite sol entre 10h-16h.\n\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    return {"sucesso": sucesso}

@app.get("/alerta/frio/{cidade}")
def alerta_frio(cidade: str, temp: float = 5):
    sucesso = enviar(
        f"❄️ ALERTA DE FRIO - {cidade}",
        f"🌡️ Temperatura: {temp}°C\n\n⚠️ Proteja-se do frio!\nAgasalhe-se bem.\n\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    return {"sucesso": sucesso}

@app.get("/weather/now/{cidade}")
def weather(cidade: str):
    """Clima atual com alerta automático"""
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
    
    if alerta == "calor":
        enviar(
            f"🔥 ALERTA DE CALOR - {cidade}",
            f"🌡️ Temperatura atual: {temp}°C!\n\n⚠️ Mantenha-se hidratado!"
        )
    elif alerta == "frio":
        enviar(
            f"❄️ ALERTA DE FRIO - {cidade}",
            f"🌡️ Temperatura atual: {temp}°C!\n\n⚠️ Proteja-se do frio!"
        )
    
    return {"cidade": cidade, "temperatura": temp, "alerta": alerta}

if __name__ == "__main__":
    print("=" * 50)
    print("🌤️ WeatherAlert Server - Versão Funcional")
    print("=" * 50)
    print(f"📌 Tópico: {TOPICO}")
    print(f"🧪 Teste: http://127.0.0.1:8000/testar")
    print(f"🔥 Calor: http://127.0.0.1:8000/alerta/calor/SaoPaulo")
    print(f"❄️ Frio: http://127.0.0.1:8000/alerta/frio/PortoAlegre")
    print(f"🌡️ Clima: http://127.0.0.1:8000/weather/now/SaoPaulo")
    print(f"📊 Dashboard: http://127.0.0.1:8000/dashboard")
    print("=" * 50)
    print("✅ Servidor iniciando...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
