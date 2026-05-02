# Criar README.md atualizado
@'
# 🌤️ WeatherAlert - Sistema de Alertas Climáticos

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**API REST** que monitora condições climáticas em cidades brasileiras e envia **alertas automáticos** para o celular em tempo real.

## ✨ Funcionalidades

- 🌡️ **Clima em Tempo Real** - Temperatura, umidade e sensação térmica
- 📱 **Notificações Push** - Alertas instantâneos no celular via ntfy.sh
- 🔥 **Alertas de Calor** - Notificação automática quando >35°C
- ❄️ **Alertas de Frio** - Notificação automática quando <12°C
- 🌐 **Dashboard Web** - Interface responsiva e intuitiva
- 🔍 **Pesquisa Rápida** - Sugestões de cidades brasileiras

## 🚀 Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/Mzambon00/WeatherAlert---Sistema-de-Alertas-Clim-ticos.git
cd WeatherAlert---Sistema-de-Alertas-Clim-ticos

# 2. Instale as dependências
pip install fastapi uvicorn

# 3. Execute o servidor
python server_completo.py

# 4. Acesse o dashboard
# Abra o navegador em: http://127.0.0.1:8000/dashboard
