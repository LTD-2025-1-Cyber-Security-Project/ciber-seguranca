@echo off
setlocal enabledelayedexpansion

:: Cores para output
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "NC=[0m"

:: Função de log
set "log=echo %GREEN%[✓]%NC% "
set "error=echo %RED%[✗]%NC% "

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    %error% Python não está instalado!
    pause
    exit /b 1
)

:: Verificar pip
pip --version >nul 2>&1
if errorlevel 1 (
    %error% pip não está instalado!
    pause
    exit /b 1
)

:: Preparar ambiente
%log% Preparando ambiente de instalação

:: Criar ambiente virtual
python -m venv venv
if errorlevel 1 (
    %error% Falha ao criar ambiente virtual
    pause
    exit /b 1
)
%log% Ambiente virtual criado

:: Ativar ambiente virtual
call venv\Scripts\activate
if errorlevel 1 (
    %error% Falha ao ativar ambiente virtual
    pause
    exit /b 1
)

:: Atualizar pip
pip install --upgrade pip
if errorlevel 1 (
    %error% Falha ao atualizar pip
    pause
    exit /b 1
)

:: Instalar dependências
pip install -r requirements.txt
if errorlevel 1 (
    %error% Falha ao instalar dependências
    pause
    exit /b 1
)

%log% Instalação concluída com sucesso!

:menu
echo.
echo === CyberSecurity App ===
echo 1. Executar Aplicativo
echo 2. Criar Executável
echo 3. Sair

set /p choice="Escolha uma opção (1-3): "

if "%choice%"=="1" (
    python app.py
    goto menu
)

if "%choice%"=="2" (
    pip install pyinstaller
    pyinstaller --onefile --windowed --name=CyberSecurity --add-data "templates;templates" --add-data "modules;modules" app.py
    %log% Executável criado em dist\CyberSecurity.exe
    goto menu
)

if "%choice%"=="3" (
    echo Saindo...
    exit /b 0
)

echo Opção inválida!
goto menu