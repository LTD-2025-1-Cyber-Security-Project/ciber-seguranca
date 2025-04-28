#!/usr/bin/env python3
from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Banco de dados inicializado com sucesso!")