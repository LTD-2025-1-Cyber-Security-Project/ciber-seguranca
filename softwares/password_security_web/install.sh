#!/bin/bash

# Script de Instalação do CyberSecurity App

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem cor

# Função de log
log() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Função de erro
error() {
    echo -e "${RED}[✗]${NC} $1"
    exit 1
}

# Verificar sistema operacional
OS=$(uname -s)

# Verificar Python
if ! command -v python3 &> /dev/null; then
    error "Python 3 não está instalado!"
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    error "pip3 não está instalado!"
fi

# Preparar ambiente
log "Preparando ambiente de instalação"

# Criar ambiente virtual
python3 -m venv venv || error "Falha ao criar ambiente virtual"
log "Ambiente virtual criado"

# Ativar ambiente virtual
source venv/bin/activate || error "Falha ao ativar ambiente virtual"

# Atualizar pip
pip install --upgrade pip || error "Falha ao atualizar pip"

# Instalar dependências
pip install -r requirements.txt || error "Falha ao instalar dependências"

log "Instalação concluída com sucesso!"

# Menu de opções
while true; do
    echo -e "\n${YELLOW}=== CyberSecurity App ===${NC}"
    echo "1. Executar Aplicativo"
    echo "2. Criar Executável"
    echo "3. Sair"
    
    read -p "Escolha uma opção (1-3): " choice
    
    case $choice in
        1)
            python3 app.py
            ;;
        2)
            pip install pyinstaller
            pyinstaller --onefile --windowed --name=CyberSecurity --add-data "templates:templates" --add-data "modules:modules" app.py
            log "Executável criado em dist/CyberSecurity"
            ;;
        3)
            echo "Saindo..."
            break
            ;;
        *)
            error "Opção inválida!"
            ;;
    esac
done