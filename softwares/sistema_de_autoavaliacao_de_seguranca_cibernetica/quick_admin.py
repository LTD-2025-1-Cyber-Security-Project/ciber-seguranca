#!/usr/bin/env python3

from app import create_app
from models import db
from models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

# Credenciais padrão
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"
DEFAULT_EMAIL = "admin@example.com"
DEFAULT_MUNICIPALITY = "Sua Cidade"

with app.app_context():
    # Verificar se já existe o usuário admin
    admin = User.query.filter_by(username=DEFAULT_USERNAME).first()
    
    if not admin:
        # Criar usuário admin
        admin = User(
            username=DEFAULT_USERNAME,
            email=DEFAULT_EMAIL,
            first_name="Administrador",
            last_name="Sistema",
            department="TI",
            position="Administrador",
            municipality=DEFAULT_MUNICIPALITY,
            is_admin=True,
            password_hash=generate_password_hash(DEFAULT_PASSWORD)
        )
        
        # Salvar no banco de dados
        db.session.add(admin)
        db.session.commit()
        
        print(f"Administrador criado com sucesso!")
        print(f"Username: {DEFAULT_USERNAME}")
        print(f"Password: {DEFAULT_PASSWORD}")
        print("IMPORTANTE: Altere esta senha após o primeiro login!")
    else:
        print("Usuário admin já existe.")