from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from datetime import datetime
import uvicorn

app = FastAPI()

TOPICO = "weatheralert_marco"
NTFY_URL = f"https://ntfy.sh/{TOPICO}"

def enviar(titulo, mensagem, prioridade=3):
    """Função que envia notificacao sem caracteres especiais"""
    try:
        mensagem_limpa = mensagem.encode('utf-8', errors='ignore').decode('utf-8')
        
        response = requests.post(
            NTFY_URL,
            data=mensagem_limpa.encode('utf-8'),
            headers={
                "Title": titulo,
                "Priority": str(prioridade),
                "Tags": "cloud"
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

@app.get("/")
def root():
    return {"status": "online", "topic": TOPICO}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/testar")
def testar():
    """Endpoint de teste - vai enviar notificacao"""
    sucesso = enviar(
        "WeatherAlert Teste",
        f"Conexao estabelecida em {datetime.now().strftime('%H:%M:%S')}\n\nVoce recebera alertas climaticos!",
        prioridade=5
    )
    return {"sucesso": sucesso, "mensagem": "Notificacao enviada"}

@app.get("/alerta/calor/{cidade}")
def alerta_calor(cidade: str, temp: float = 38):
    """Alerta de calor"""
    sucesso = enviar(
        f"ALERTA DE CALOR - {cidade}",
        f"Temperatura: {temp}C\n\nMantenha-se hidratado!\nEvite exposicao ao sol.",
        prioridade=5
    )
    return {"sucesso": sucesso}

@app.get("/alerta/frio/{cidade}")
def alerta_frio(cidade: str, temp: float = 5):
    """Alerta de frio"""
    sucesso = enviar(
        f"ALERTA DE FRIO - {cidade}",
        f"Temperatura: {temp}C\n\nProteja-se do frio!\nAgasalhe-se bem.",
        prioridade=5
    )
    return {"sucesso": sucesso}

@app.get("/weather/now/{cidade}")
def weather(cidade: str):
    """Simula clima e envia alerta automatico"""
    
    # Simular diferentes climas
    if "paulo" in cidade.lower() or "sao" in cidade.lower():
        temp = 38
        alerta = "calor"
    elif "porto" in cidade.lower() or "alegre" in cidade.lower():
        temp = 5
        alerta = "frio"
    else:
        temp = 25
        alerta = None
    
    resultado = {"cidade": cidade, "temperatura": temp, "timestamp": datetime.now().isoformat()}
    
    # Enviar alerta se necessario
    if alerta == "calor" and temp > 35:
        enviar(
            f"ALERTA DE CALOR - {cidade}",
            f"Temperatura atual: {temp}C\n\n⚠️ Mantenha-se hidratado!",
            prioridade=5
        )
    elif alerta == "frio" and temp < 10:
        enviar(
            f"ALERTA DE FRIO - {cidade}",
            f"Temperatura atual: {temp}C\n\n⚠️ Proteja-se do frio!",
            prioridade=5
        )
    
    return resultado

if __name__ == "__main__":
    print("=" * 50)
    print("WeatherAlert Server - Versao Simplificada")
    print("=" * 50)
    print(f"Topico: {TOPICO}")
    print("Teste: http://127.0.0.1:8000/testar")
    print("Calor: http://127.0.0.1:8000/alerta/calor/SaoPaulo?temp=38")
    print("Frio: http://127.0.0.1:8000/alerta/frio/PortoAlegre?temp=5")
    print("Clima: http://127.0.0.1:8000/weather/now/SaoPaulo")
    print("Dashboard: http://127.0.0.1:8000/dashboard")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)
