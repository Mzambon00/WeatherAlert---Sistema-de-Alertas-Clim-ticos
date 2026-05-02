from fastapi import FastAPI
import subprocess
import uvicorn

app = FastAPI()
TOPICO = "weatheralert_marco"

@app.get("/testar")
def testar():
    result = subprocess.run(
        f'curl.exe -X POST -H "Title: Teste API" -H "Priority: 5" -d "Notificacao da API em {__import__("datetime").datetime.now().strftime("%H:%M:%S")}" https://ntfy.sh/{TOPICO}',
        shell=True
    )
    return {"status": "enviado"}

@app.get("/")
def root():
    return {"msg": "WeatherAlert OK"}

if __name__ == "__main__":
    print("🚀 Servidor iniciado em http://127.0.0.1:8000")
    print("🧪 Teste: http://127.0.0.1:8000/testar")
    uvicorn.run(app, host="127.0.0.1", port=8000)
