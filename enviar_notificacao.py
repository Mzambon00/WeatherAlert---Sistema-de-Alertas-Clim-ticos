import requests
from datetime import datetime

# Configuração
TOPICO = "weatheralert_marco"
URL = f"https://ntfy.sh/{TOPICO}"

def enviar_notificacao(titulo, mensagem, prioridade=3):
    """Função que envia notificação sem caracteres especiais"""
    headers = {
        "Title": titulo,
        "Priority": str(prioridade),
        "Tags": "cloud"
    }
    
    print(f"\nEnviando: {titulo}")
    
    # Remover caracteres especiais da mensagem
    mensagem_limpa = mensagem.encode('utf-8', errors='ignore').decode('utf-8')
    
    response = requests.post(
        URL,
        data=mensagem_limpa.encode('utf-8'),
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        print("NOTIFICACAO ENVIADA COM SUCESSO!")
        return True
    else:
        print(f"Erro: {response.status_code}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("WeatherAlert - Teste de Notificacao")
    print("=" * 50)
    print(f"Topico: {TOPICO}")
    print()
    
    # Teste 1
    enviar_notificacao(
        "WeatherAlert Conectado",
        f"Sistema iniciado em {datetime.now().strftime('%H:%M:%S')}\n\nVoce recebera alertas climaticos!",
        prioridade=5
    )
    
    # Teste 2 - Alerta de calor
    enviar_notificacao(
        "ALERTA DE CALOR - Sao Paulo",
        "Temperatura: 38C\n\nMantenha-se hidratado!\nEvite sol entre 10h-16h.",
        prioridade=5
    )
    
    # Teste 3 - Alerta de frio
    enviar_notificacao(
        "ALERTA DE FRIO - Porto Alegre",
        "Temperatura: 5C\n\nProteja-se do frio!\nAgasalhe-se bem.",
        prioridade=5
    )
    
    print("\n" + "=" * 50)
    print("Testes concluidos!")
    print("Verifique as notificacoes no seu celular!")
    print("=" * 50)
