import os
import sys
import webbrowser
import threading
import time
import sqlite3
from app import app, db, User

def resource_path(relative_path):
    """Obtém caminho absoluto para recursos, funciona para dev e para PyInstaller"""
    try:
        # PyInstaller cria um dir temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def check_directory(path, name):
    """Verifica se o diretório existe e registra seu conteúdo"""
    if os.path.exists(path):
        print(f"Pasta {name} existe: {path}")
        try:
            print(f"Conteúdo da pasta {name}: {os.listdir(path)}")
        except:
            print(f"Não foi possível listar o conteúdo da pasta {name}")
    else:
        print(f"AVISO: Pasta {name} não existe: {path}")

def initialize_database():
    """Inicializa o banco de dados se não existir"""
    # Verificar onde estamos executando
    if hasattr(sys, '_MEIPASS'):
        # Se estamos em modo PyInstaller, o banco de dados deve ficar no diretório do usuário
        db_dir = os.path.join(os.path.expanduser("~"), ".simulador_phishing")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "database.db")
    else:
        # Em modo de desenvolvimento, o banco de dados fica no diretório atual
        db_path = os.path.join(os.path.abspath("."), "database.db")
    
    print(f"Caminho do banco de dados: {db_path}")
    
    # Configurar caminho do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    # Criar tabelas se não existirem
    with app.app_context():
        db.create_all()
        print("Tabelas criadas/verificadas com sucesso!")
        
        # Verificar se existe pelo menos um admin
        if not User.query.filter_by(is_admin=True).first():
            print("Nenhum administrador encontrado. Criando usuário admin padrão...")
            admin = User(username="admin", email="admin@example.com", is_admin=True)
            admin.set_password("admin123")  # Senha padrão - deve ser alterada
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")

def open_browser():
    # Aguarda 1.5 segundos para garantir que o servidor iniciou
    time.sleep(1.5)
    # Abre o navegador padrão
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Verificar se estamos em modo PyInstaller
    if hasattr(sys, '_MEIPASS'):
        print(f"Executando a partir do PyInstaller")
        # Definir caminhos das pastas para o Flask
        template_path = resource_path('templates')
        static_path = resource_path('static')
        
        app.template_folder = template_path
        app.static_folder = static_path
        
        # Verificar diretórios
        check_directory(template_path, "templates")
        check_directory(static_path, "static")
    else:
        print("Executando em modo de desenvolvimento")
    
    # Inicializar banco de dados
    initialize_database()
    
    # Inicia um thread para abrir o navegador
    threading.Thread(target=open_browser).start()
    
    # Inicia o servidor Flask
    app.run(debug=False, host='127.0.0.1', port=5000)