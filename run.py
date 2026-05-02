#!/usr/bin/env python
"""
Script de inicializacao do WeatherAlert
"""
import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Instala dependencias necessarias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao instalar dependencias: {e}")
        return False
    return True

def check_env():
    """Verifica se o arquivo .env existe"""
    if not os.path.exists('.env'):
        print("⚠️ Arquivo .env nao encontrado!")
        print("📝 Criando .env a partir do .env.example...")
        try:
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✅ Arquivo .env criado!")
            print("⚠️ Configure sua OPENWEATHER_API_KEY no arquivo .env")
            print("🔑 Obtenha sua chave em: https://openweathermap.org/api")
            return False
        except Exception as e:
            print(f"❌ Erro ao criar .env: {e}")
            return False
    return True

def create_directories():
    """Cria diretorios necessarios"""
    directories = ['logs', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Diretorios criados!")

def main():
    print("=" * 60)
    print("🌤️ WeatherAlert - Sistema de Alertas Climaticos")
    print("=" * 60)
    
    # Criar diretorios
    create_directories()
    
    # Verificar/instalar dependencias
    if not install_dependencies():
        return
    
    # Verificar configuracao
    if not check_env():
        print("\n⚠️ Configure o arquivo .env e execute novamente!")
        return
    
    print("\n🚀 Iniciando WeatherAlert API...")
    print("📖 Documentacao: http://localhost:8000/docs")
    print("📧 Enviando notificacoes para: marcoszambon18@gmail.com")
    print("\n⚠️ Pressione CTRL+C para parar o servidor\n")
    
    # Executar API
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.api.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 WeatherAlert encerrado!")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar API: {e}")

if __name__ == "__main__":
    main()
