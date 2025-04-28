import os
from flask import Flask, redirect, url_for, flash, render_template
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_mail import Mail
from datetime import datetime

# Importação dos modelos e módulos
from models import db
from models.user import User
from models.assessment import Assessment
from models.recommendation import Recommendation

# Importação dos controllers
from controllers.auth_controller import auth_bp
from controllers.assessment_controller import assessment_bp
from controllers.dashboard_controller import dashboard_bp

# Importação das configurações
from config import Config

def create_app(config_class=Config):
    """Função de Factory para criação da aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Inicializar login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Inicializar migração de banco de dados
    migrate = Migrate(app, db)
    
    # Inicializar envio de emails
    mail = Mail(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(assessment_bp, url_prefix='/assessment')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Criar pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Rota principal
    @app.route('/')
    def index():
        # if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        # return redirect(url_for('auth.login'))
    
    # Página de erro 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    # Página de erro 403
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403
    
    # Página de erro 500
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Context processor para variáveis globais
    @app.context_processor
    def inject_global_vars():
        return dict(
            current_year=datetime.now().year,
            app_name="CyberSecAssessment"
        )
    
    return app

# Inicialização direta da aplicação
app = create_app()

# Criar usuário admin inicial
@app.cli.command("create-admin")
def create_admin():
    """Cria um usuário administrador inicial"""
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    municipality = input("Município: ")
    
    user = User.query.filter((User.username == username) | (User.email == email)).first()
    if user:
        print("Usuário já existe!")
        return
    
    admin = User(
        username=username,
        email=email,
        first_name="Admin",
        last_name="Sistema",
        department="TI",
        position="Administrador",
        municipality=municipality,
        is_admin=True
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Administrador {username} criado com sucesso!")

# Comando para inicializar banco de dados
@app.cli.command("init-db")
def init_db():
    """Inicializa o banco de dados"""
    db.create_all()
    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')