import os
import platform
import subprocess
import shutil

def ensure_directories():
    """Cria diretórios necessários se não existirem"""
    print("Verificando diretórios necessários...")
    
    if not os.path.exists("templates"):
        print("Criando pasta templates...")
        os.makedirs("templates")
    
    if not os.path.exists("static"):
        print("Criando pasta static...")
        os.makedirs("static")
        # Criar subpastas comuns
        for subdir in ['css', 'js', 'img']:
            os.makedirs(os.path.join("static", subdir), exist_ok=True)

def clean_build():
    """Limpa diretórios de build anteriores"""
    print("Limpando diretórios de build anteriores...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    for item in os.listdir("."):
        if item.endswith(".spec"):
            os.remove(item)

def build_app():
    """Constrói o aplicativo usando PyInstaller"""
    print("Iniciando build com PyInstaller...")
    
    # Determina o separador correto para o sistema operacional
    separator = ";" if platform.system() == "Windows" else ":"
    
    # Lista de recursos para adicionar
    resources = []
    
    # Adicionar templates se existir
    if os.path.exists("templates"):
        resources.append(f"--add-data=templates{separator}templates")
    
    # Adicionar static se existir
    if os.path.exists("static"):
        resources.append(f"--add-data=static{separator}static")
    
    # Comando base
    cmd = [
        "pyinstaller",
        "--onefile",
        "--clean",
    ]
    
    # Adiciona recursos
    cmd.extend(resources)
    
    # Adiciona ícone se estiver no Windows ou Mac
    if platform.system() == "Windows":
        if os.path.exists("icon.ico"):
            cmd.append("--icon=icon.ico")
    elif platform.system() == "Darwin":  # macOS
        if os.path.exists("icon.icns"):
            cmd.append("--icon=icon.icns")
    
    # Adiciona o script principal
    cmd.append("run.py")
    
    # Executa o comando
    print(f"Executando comando: {' '.join(cmd)}")
    subprocess.run(cmd)

def verify_build():
    """Verifica se a build foi concluída com sucesso"""
    if os.path.exists("dist/run") or os.path.exists("dist/run.exe"):
        print("\n✅ Build concluída com sucesso!")
        if platform.system() == "Windows":
            print(f"O executável está em: {os.path.abspath('dist/run.exe')}")
        else:
            print(f"O executável está em: {os.path.abspath('dist/run')}")
    else:
        print("\n❌ Falha na build. Verifique os erros acima.")

if __name__ == "__main__":
    ensure_directories()
    clean_build()
    build_app()
    verify_build()