#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import venv
import shutil

class CyberSecurityAppSetup:
    def __init__(self):
        """
        Classe para configuração e execução do aplicativo de segurança
        """
        self.sistema_operacional = platform.system().lower()
        self.versao_python = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.caminho_base = os.path.dirname(os.path.abspath(__file__))
        
    def verificar_dependencias_sistema(self):
        """
        Verifica e instala dependências de sistema
        """
        print("🔍 Verificando dependências do sistema...")
        
        try:
            if self.sistema_operacional == 'linux':
                # Comandos para sistemas Linux
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 
                    'python3-venv', 'python3-pip', 'python3-dev', 'build-essential'], 
                    check=True)
            
            elif self.sistema_operacional == 'darwin':
                # Verificações para macOS
                # Verificar Homebrew
                try:
                    subprocess.run(['brew', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("🍺 Homebrew não encontrado. Sugerindo instalação manual de dependências.")
                    print("Por favor, instale as dependências manualmente:")
                    print("1. Instale Xcode Command Line Tools: xcode-select --install")
                    print("2. Instale Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            
            elif self.sistema_operacional == 'windows':
                print("⚠️ No Windows, certifique-se de ter Python e pip instalados.")

        except Exception as e:
            print(f"⚠️ Aviso: {e}")
        
    def criar_ambiente_virtual(self):
        """
        Cria ambiente virtual Python
        """
        caminho_venv = os.path.join(self.caminho_base, 'venv')
        
        print("🌐 Criando ambiente virtual...")
        
        if not os.path.exists(caminho_venv):
            venv.create(caminho_venv, with_pip=True)
            print("✅ Ambiente virtual criado com sucesso!")
        else:
            print("✔️ Ambiente virtual já existe.")
        
        return caminho_venv
    
    def instalar_dependencias(self, caminho_venv):
        """
        Instala dependências do projeto
        """
        print("📦 Instalando dependências...")
        
        # Definir caminho do pip baseado no sistema operacional
        if self.sistema_operacional == 'windows':
            pip_path = os.path.join(caminho_venv, 'Scripts', 'pip')
        else:
            pip_path = os.path.join(caminho_venv, 'bin', 'pip')
        
        try:
            # Atualizar pip
            subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
            
            # Instalar dependências
            subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
            
            print("✅ Dependências instaladas com sucesso!")
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            # Tentar instalar sem especificar caminho
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
                print("✅ Dependências instaladas com sucesso usando método alternativo.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro crítico ao instalar dependências: {e}")
                sys.exit(1)
    
    def criar_executavel(self):
        """
        Cria executável multiplataforma usando PyInstaller
        """
        print("🚀 Criando executável...")
        
        try:
            # Instalar PyInstaller
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
            
            # Criar diretório de distribuição
            dist_dir = os.path.join(self.caminho_base, 'dist')
            os.makedirs(dist_dir, exist_ok=True)
            
            # Opções de PyInstaller
            pyinstaller_opts = [
                'pyinstaller',
                '--onefile',               # Arquivo único
                '--windowed',              # Sem console no Windows
                '--name=CyberSecurity',    # Nome do executável
                '--add-data=templates:templates',  # Incluir templates
                '--add-data=modules:modules',      # Incluir módulos
                'app.py'                   # Arquivo principal
            ]
            
            # Executar PyInstaller
            subprocess.run(pyinstaller_opts, check=True)
            
            print("✅ Executável criado com sucesso!")
            print(f"📂 Localização: {os.path.join(dist_dir, 'CyberSecurity')}")
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar executável: {e}")
            sys.exit(1)
    
    def executar_aplicativo(self, caminho_venv):
        """
        Executa o aplicativo no ambiente virtual
        """
        print("🔐 Iniciando aplicativo de Cibersegurança...")
        
        # Definir caminho do Python baseado no sistema operacional
        if self.sistema_operacional == 'windows':
            python_path = os.path.join(caminho_venv, 'Scripts', 'python')
        else:
            python_path = os.path.join(caminho_venv, 'bin', 'python')
        
        try:
            # Verificar se o ambiente virtual está ativado
            if not os.path.exists(python_path):
                print("❌ Ambiente virtual não encontrado. Recriando...")
                caminho_venv = self.criar_ambiente_virtual()
                self.instalar_dependencias(caminho_venv)
                
                # Atualizar caminho do Python
                if self.sistema_operacional == 'windows':
                    python_path = os.path.join(caminho_venv, 'Scripts', 'python')
                else:
                    python_path = os.path.join(caminho_venv, 'bin', 'python')
            
            # Executar aplicativo
            subprocess.run([python_path, 'app.py'], check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar o aplicativo: {e}")
            
            # Tentar executar diretamente com Python do sistema
            try:
                subprocess.run([sys.executable, 'app.py'], check=True)
            except subprocess.CalledProcessError as fallback_error:
                print(f"❌ Erro crítico ao executar o aplicativo: {fallback_error}")
                sys.exit(1)
    
    def atualizar_projeto(self):
        """
        Atualiza o projeto e suas dependências
        """
        print("🔄 Atualizando projeto...")
        
        try:
            # Atualizar repositório Git (se existir)
            if os.path.exists('.git'):
                subprocess.run(['git', 'pull'], check=True)
            
            # Atualizar dependências
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'], check=True)
            
            print("✅ Projeto atualizado com sucesso!")
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao atualizar projeto: {e}")
    
    def diagnosticar_sistema(self):
        """
        Realiza diagnóstico do sistema e ambiente
        """
        print("🩺 Diagnóstico do Sistema")
        print(f"Sistema Operacional: {platform.platform()}")
        print(f"Python: {platform.python_version()}")
        
        try:
            # Verificar versão do pip
            pip_version = subprocess.check_output([sys.executable, '-m', 'pip', '--version']).decode().strip()
            print(f"Pip: {pip_version}")
            
            # Verificar pacotes instalados
            print("\nPacotes Instalados:")
            pacotes = subprocess.check_output([sys.executable, '-m', 'pip', 'list']).decode()
            print(pacotes)
        
        except Exception as e:
            print(f"❌ Erro durante diagnóstico: {e}")
    
    def main(self):
        """
        Método principal de execução
        """
        print(f"🖥️  Detectado: {self.sistema_operacional.upper()} - Python {self.versao_python}")
        
        # Verificar e instalar dependências do sistema
        self.verificar_dependencias_sistema()
        
        # Criar ambiente virtual
        caminho_venv = self.criar_ambiente_virtual()
        
        # Instalar dependências do projeto
        self.instalar_dependencias(caminho_venv)
        
        # Menu de opções
        while True:
            print("\n--- Menu CyberSecurity ---")
            print("1. Executar Aplicativo")
            print("2. Criar Executável")
            print("3. Atualizar Projeto")
            print("4. Diagnóstico do Sistema")
            print("5. Sair")
            
            try:
                escolha = input("Escolha uma opção (1-5): ")
                
                if escolha == '1':
                    self.executar_aplicativo(caminho_venv)
                elif escolha == '2':
                    self.criar_executavel()
                elif escolha == '3':
                    self.atualizar_projeto()
                elif escolha == '4':
                    self.diagnosticar_sistema()
                elif escolha == '5':
                    print("👋 Saindo...")
                    break
                else:
                    print("❌ Opção inválida!")
            
            except KeyboardInterrupt:
                print("\n👋 Operação interrompida pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")

# Ponto de entrada do script
if __name__ == '__main__':
    try:
        setup = CyberSecurityAppSetup()
        setup.main()
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)