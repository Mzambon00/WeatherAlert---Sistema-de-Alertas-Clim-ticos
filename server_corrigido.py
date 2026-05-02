from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import os
from datetime import datetime
import uvicorn

app = FastAPI()
TOPICO = "weatheralert_marco"

# Localizar curl.exe
CURL_PATH = "C:\\Windows\\System32\\curl.exe"

def enviar(titulo, mensagem):
    """Envia notificacao usando curl.exe com caminho completo"""
    try:
        # Limpar mensagem para evitar problemas com caracteres especiais
        mensagem_limpa = mensagem.replace('"', '\\"').replace('\n', '\\n')
        
        # Comando completo
        cmd = f'"{CURL_PATH}" -X POST -H "Title: {titulo}" -H "Priority: 5" -d "{mensagem_limpa}" https://ntfy.sh/{TOPICO}'
        
        print(f"📤 Enviando: {titulo}")
        print(f"🔧 Comando: {cmd[:100]}...")
        
        # Executar
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ Notificacao enviada: {titulo}")
            print(f"📡 Resposta: {result.stdout[:100]}")
            return True
        else:
            print(f"❌ Erro: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Excecao: {e}")
        return False

@app.get("/")
def root():
    return {"status": "online", "topic": TOPICO}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/testar")
def testar():
    """Teste rápido - deve enviar notificacao"""
    sucesso = enviar(
        "WeatherAlert Teste",
        f"Conexao estabelecida em {datetime.now().strftime('%H:%M:%S')}\n\nSistema funcionando!"
    )
    return {"sucesso": sucesso, "mensagem": "Teste enviado"}

@app.get("/alerta/calor/{cidade}")
def alerta_calor(cidade: str, temp: float = 38):
    sucesso = enviar(
        f"ALERTA DE CALOR - {cidade}",
        f"Temperatura: {temp}C\n\nMantenha-se hidratado!"
    )
    return {"sucesso": sucesso}

@app.get("/alerta/frio/{cidade}")
def alerta_frio(cidade: str, temp: float = 5):
    sucesso = enviar(
        f"ALERTA DE FRIO - {cidade}",
        f"Temperatura: {temp}C\n\nProteja-se do frio!"
    )
    return {"sucesso": sucesso}

@app.get("/weather/now/{cidade}")
def weather(cidade: str):
    cidade_lower = cidade.lower()
    
    if "paulo" in cidade_lower:
        temp = 38
        alerta = "calor"
    elif "porto" in cidade_lower:
        temp = 5
        alerta = "frio"
    else:
        temp = 25
        alerta = None
    
    if alerta == "calor":
        enviar(f"ALERTA DE CALOR - {cidade}", f"Temperatura: {temp}C!")
    elif alerta == "frio":
        enviar(f"ALERTA DE FRIO - {cidade}", f"Temperatura: {temp}C!")
    
    return {"cidade": cidade, "temperatura": temp}

if __name__ == "__main__":
    # Verificar se curl.exe existe
    if os.path.exists(CURL_PATH):
        print("✅ curl.exe encontrado!")
    else:
        print(f"❌ curl.exe nao encontrado em {CURL_PATH}")
        print("Tentando usar 'curl' sem caminho...")
        CURL_PATH = "curl"
    
    print("=" * 50)
    print("WeatherAlert Server - Versao Corrigida")
    print("=" * 50)
    print(f"Topico: {TOPICO}")
    print(f"Teste: http://127.0.0.1:8000/testar")
    print("=" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
