#!/usr/bin/env python3
from app import create_app
from models import db
from models.user import User
from getpass import getpass

app = create_app()

with app.app_context():
    # Verificar se já existe algum usuário
    if User.query.count() == 0:
        try:
            # Solicitar informações do usuário admin
            print("Criando usuário administrador...")
            username = input("Username: ")
            email = input("Email: ")
            password = getpass("Password: ")  # Oculta a senha durante a digitação
            first_name = input("Nome: ")
            last_name = input("Sobrenome: ")
            municipality = input("Município: ")
            
            # Criar usuário admin
            admin = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                department="TI",
                position="Administrador",
                municipality=municipality,
                is_admin=True
            )
            admin.set_password(password)
            
            # Salvar no banco de dados
            db.session.add(admin)
            db.session.commit()
            
            print(f"Administrador {username} criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar usuário administrador: {e}")
    else:
        print("Já existem usuários cadastrados no sistema.")
        users = User.query.all()
        print("Usuários existentes:")
        for user in users:
            print(f"- {user.username} ({user.email})")