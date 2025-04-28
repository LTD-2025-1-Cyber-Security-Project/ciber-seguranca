@echo off
echo Sistema de Autoavaliacao de Seguranca Cibernetica para Prefeituras
echo Instalador Automatico
echo.

set INSTALL_DIR=%USERPROFILE%\CybersecPrefeitura

echo Criando estrutura de diretorios...
mkdir "%INSTALL_DIR%"
xcopy /E /I templates "%INSTALL_DIR%\templates"
xcopy /E /I static "%INSTALL_DIR%\static"
xcopy /E /I models "%INSTALL_DIR%\models"
xcopy /E /I controllers "%INSTALL_DIR%\controllers"
xcopy /E /I utils "%INSTALL_DIR%\utils"
copy app.py "%INSTALL_DIR%"
copy config.py "%INSTALL_DIR%"
copy run.py "%INSTALL_DIR%"
copy requirements.txt "%INSTALL_DIR%"

echo Instalando Python e dependencias...
cd "%INSTALL_DIR%"

:: Verificar se Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python nao foi encontrado. Baixando e instalando Python...
    :: Baixar Python
    curl -L -o python_installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    :: Instalar Python
    python_installer.exe /quiet InstallAllUsers=0 PrependPath=1
    del python_installer.exe
)

:: Criar ambiente virtual
python -m venv venv
call venv\Scripts\activate.bat

:: Instalar dependências
pip install -r requirements.txt

:: Criar arquivo de execução
echo @echo off > "%INSTALL_DIR%\start_cybersec.bat"
echo cd "%INSTALL_DIR%" >> "%INSTALL_DIR%\start_cybersec.bat"
echo call venv\Scripts\activate.bat >> "%INSTALL_DIR%\start_cybersec.bat"
echo python run.py >> "%INSTALL_DIR%\start_cybersec.bat"

:: Criar atalho no Desktop
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%USERPROFILE%\Desktop\CybersecPrefeitura.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\start_cybersec.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Sistema de Autoavaliacao de Seguranca Cibernetica" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"
cscript /nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

echo.
echo Instalacao concluida!
echo Para iniciar o Sistema de Autoavaliacao de Seguranca Cibernetica, clique no atalho no Desktop ou execute:
echo %INSTALL_DIR%\start_cybersec.bat
pause