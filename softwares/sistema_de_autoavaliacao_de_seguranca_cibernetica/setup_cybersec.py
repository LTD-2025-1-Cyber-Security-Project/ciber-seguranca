#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para criar um pacote distribuível do Sistema de Autoavaliação de Segurança Cibernética
Este script gera um pacote completo que pode ser executado em sistemas Windows e macOS.
"""

import os
import sys
import shutil
import subprocess
import platform
import zipfile
from pathlib import Path

# Verificar sistema operacional
SYSTEM = platform.system()
print(f"Sistema operacional detectado: {SYSTEM}")

# Diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

# Diretório de saída
OUTPUT_DIR = os.path.join(ROOT_DIR, "dist")
PACKAGE_DIR = os.path.join(OUTPUT_DIR, "CybersecPrefeitura")

# Limpar diretório de saída se existir
if os.path.exists(PACKAGE_DIR):
    print(f"Removendo diretório de saída existente: {PACKAGE_DIR}")
    shutil.rmtree(PACKAGE_DIR)

# Criar estrutura de diretórios
print("Criando estrutura de diretórios...")
os.makedirs(PACKAGE_DIR, exist_ok=True)

# Diretórios a serem copiados
directories = [
    "templates",
    "static",
    "models",
    "controllers",
    "utils"
]

# Copiar diretórios
for directory in directories:
    src_dir = os.path.join(ROOT_DIR, directory)
    dst_dir = os.path.join(PACKAGE_DIR, directory)
    if os.path.exists(src_dir):
        print(f"Copiando diretório: {directory}")
        shutil.copytree(src_dir, dst_dir)
    else:
        print(f"Atenção: Diretório {directory} não encontrado.")
        os.makedirs(dst_dir, exist_ok=True)

# Arquivos a serem copiados
files = [
    "app.py",
    "config.py",
    "run.py",
    "requirements.txt"
]

# Copiar arquivos
for file in files:
    src_file = os.path.join(ROOT_DIR, file)
    dst_file = os.path.join(PACKAGE_DIR, file)
    if os.path.exists(src_file):
        print(f"Copiando arquivo: {file}")
        shutil.copy2(src_file, dst_file)
    else:
        print(f"Atenção: Arquivo {file} não encontrado.")

# Criar script de inicialização para Windows
if SYSTEM == "Windows" or True:  # Criar scripts para ambos sistemas
    win_script = os.path.join(PACKAGE_DIR, "iniciar_sistema.bat")
    with open(win_script, "w") as f:
        f.write('''@echo off
TITLE Sistema de Autoavaliacao de Seguranca Cibernetica
ECHO ==================================================
ECHO Sistema de Autoavaliacao de Seguranca Cibernetica
ECHO Inicializando...
ECHO ==================================================

REM Verificar se Python está instalado
python --version >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro: Python nao encontrado.
    ECHO Por favor, instale Python 3.8 ou superior e reinicie este script.
    PAUSE
    EXIT /B 1
)

REM Verificar se as dependências estão instaladas
ECHO Verificando dependencias...
pip install -r requirements.txt

REM Inicializar banco de dados
ECHO Inicializando banco de dados...
python -c "from app import create_app; from models import db; from models.user import User; app = create_app(); with app.app_context(): db.create_all(); admin = User.query.filter_by(username='estevam5s').first(); if not admin: admin = User(username='estevam5s', email='contato@estevamsouza.com.br', first_name='Estevam Souza', last_name='Laureth', department='TI', position='Administrador', municipality='Floripa', is_admin=True); admin.set_password('estevam5s'); db.session.add(admin); db.session.commit(); print('Usuario administrador criado com sucesso!');"

ECHO Iniciando sistema...
START python run.py
TIMEOUT /T 2 >NUL
START http://127.0.0.1:5000

ECHO Sistema iniciado! Acesse no navegador: http://127.0.0.1:5000
ECHO Use as credenciais:
ECHO   Usuario: estevam5s
ECHO   Senha: estevam5s
ECHO.
ECHO Para encerrar, feche esta janela ou pressione Ctrl+C.
PAUSE
''')

# Criar script de inicialização para macOS/Linux
mac_script = os.path.join(PACKAGE_DIR, "iniciar_sistema.sh")
with open(mac_script, "w") as f:
    f.write('''#!/bin/bash

echo "=================================================="
echo "Sistema de Autoavaliação de Segurança Cibernética"
echo "Inicializando..."
echo "=================================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado."
    echo "Por favor, instale Python 3.8 ou superior e reinicie este script."
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
python3 -m pip install -r requirements.txt

# Inicializar banco de dados
echo "Inicializando banco de dados..."
python3 -c "from app import create_app; from models import db; from models.user import User; app = create_app(); with app.app_context(): db.create_all(); admin = User.query.filter_by(username='estevam5s').first(); if not admin: admin = User(username='estevam5s', email='contato@estevamsouza.com.br', first_name='Estevam Souza', last_name='Laureth', department='TI', position='Administrador', municipality='Floripa', is_admin=True); admin.set_password('estevam5s'); db.session.add(admin); db.session.commit(); print('Usuário administrador criado com sucesso!');"

echo "Iniciando sistema..."
python3 run.py &
PID=$!
sleep 2

# Abrir navegador
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://127.0.0.1:5000
else
    # Linux
    xdg-open http://127.0.0.1:5000 &> /dev/null || sensible-browser http://127.0.0.1:5000 &> /dev/null || x-www-browser http://127.0.0.1:5000 &> /dev/null
fi

echo "Sistema iniciado! Acesse no navegador: http://127.0.0.1:5000"
echo "Use as credenciais:"
echo "  Usuário: estevam5s"
echo "  Senha: estevam5s"
echo ""
echo "Para encerrar, pressione Ctrl+C."

# Aguardar término do processo
wait $PID
''')

# Tornar script do macOS/Linux executável
if SYSTEM != "Windows":
    os.chmod(mac_script, 0o755)

# Criar README
readme_file = os.path.join(PACKAGE_DIR, "README.txt")
with open(readme_file, "w") as f:
    f.write('''======================================================
Sistema de Autoavaliação de Segurança Cibernética para Prefeituras
======================================================

## Requisitos
- Python 3.8 ou superior
- Conexão com a internet (para download de dependências)

## Instruções de Uso

### No Windows:
1. Execute o arquivo "iniciar_sistema.bat" clicando duas vezes
2. O sistema irá instalar as dependências, inicializar o banco de dados e abrir automaticamente no seu navegador

### No macOS/Linux:
1. Abra o Terminal na pasta do sistema
2. Execute o comando: chmod +x iniciar_sistema.sh
3. Execute o comando: ./iniciar_sistema.sh
4. O sistema irá instalar as dependências, inicializar o banco de dados e abrir automaticamente no seu navegador

## Credenciais de Acesso
- Usuário: estevam5s
- Senha: estevam5s

## Observações Importantes
- Após o primeiro login, recomenda-se alterar a senha no menu de Perfil
- O banco de dados é armazenado localmente no arquivo "cybersec_assessment.db"
- Para encerrar o sistema, feche a janela do prompt/terminal ou pressione Ctrl+C

Para qualquer problema ou suporte, consulte a documentação ou entre em contato com a equipe de desenvolvimento.
''')

# Criar arquivo ZIP para distribuição fácil
zip_file = os.path.join(OUTPUT_DIR, "CybersecPrefeitura.zip")
print(f"Criando arquivo ZIP: {zip_file}")

with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PACKAGE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, OUTPUT_DIR)
            zipf.write(file_path, arcname)

print("\n" + "=" * 60)
print("Pacote criado com sucesso!")
print(f"Localização: {zip_file}")
print("\nPara usar o sistema:")
print("1. Extraia o arquivo ZIP")
print("2. Execute o script de inicialização apropriado para seu sistema:")
print("   - Windows: iniciar_sistema.bat")
print("   - macOS/Linux: ./iniciar_sistema.sh")
print("\nCredenciais de acesso:")
print("Usuário: estevam5s")
print("Senha: estevam5s")
print("=" * 60)