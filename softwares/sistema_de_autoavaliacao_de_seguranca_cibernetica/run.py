#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Execução para o Sistema de Autoavaliação de Segurança Cibernética
Este script inicializa o banco de dados, cria estruturas de diretórios necessárias,
cria um usuário administrador se necessário e inicia a aplicação.
"""

import os
import sys
import webbrowser
import threading
import time
import getpass
from pathlib import Path

# Criar estrutura de diretórios necessária
def create_directories():
    print("Criando estrutura de diretórios necessária...")
    dirs = [
        'static/css',
        'static/js',
        'static/images',
        'templates/auth',
        'templates/assessment',
        'templates/dashboard',
        'templates/errors'
    ]
    
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("Estrutura de diretórios criada com sucesso.")

# Inicializar o banco de dados
def init_database():
    try:
        print("Inicializando banco de dados...")
        from app import create_app
        from models import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
            print("Banco de dados inicializado com sucesso!")
        return app
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        sys.exit(1)

# Criar usuário administrador
def create_admin_user(app):
    from models import db
    from models.user import User
    
    with app.app_context():
        # Verificar se já existe algum usuário
        if User.query.count() == 0:
            try:
                print("Criando usuário administrador...")
                username = "vagnercordeiro"
                email = "contato@estevamsouza.com.br"
                # password = getpass.getpass("Password: ")
                password = "Vagnercordeiro@123-2025"
                first_name = "Estevam Souza"
                last_name = "Laureth"
                municipality = "Floripa"
                
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
                sys.exit(1)
        else:
            print("Usuário administrador já existe. Pulando criação.")

# Abrir navegador após o servidor iniciar
def open_browser():
    # Aguarda 1.5 segundos para garantir que o servidor iniciou
    time.sleep(1.5)
    # Abre o navegador padrão
    webbrowser.open('http://127.0.0.1:5000/')
    print("Navegador aberto em http://127.0.0.1:5000/")

# Verificar se os arquivos de template existem, caso contrário criar templates vazios
def check_templates():
    print("Verificando templates necessários...")
    templates = {
        # Templates de erro
        'templates/errors/404.html': '''{% extends 'base.html' %}
{% block title %}Página Não Encontrada - CyberSecAssessment{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-8 text-center">
        <div class="error-container py-5">
            <h1 class="display-1 text-primary">404</h1>
            <h2 class="mb-4">Página Não Encontrada</h2>
            <p class="lead mb-4">A página que você está procurando não existe ou foi movida.</p>
            <div class="mt-4">
                <a href="{{ url_for('index') }}" class="btn btn-primary btn-lg">
                    <i class="fas fa-home me-2"></i>Voltar para a Página Inicial
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        'templates/errors/403.html': '''{% extends 'base.html' %}
{% block title %}Acesso Negado - CyberSecAssessment{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-8 text-center">
        <div class="error-container py-5">
            <h1 class="display-1 text-danger">403</h1>
            <h2 class="mb-4">Acesso Negado</h2>
            <p class="lead mb-4">Você não tem permissão para acessar este recurso.</p>
            <div class="mt-4">
                <a href="{{ url_for('index') }}" class="btn btn-primary btn-lg">
                    <i class="fas fa-home me-2"></i>Voltar para a Página Inicial
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        'templates/errors/500.html': '''{% extends 'base.html' %}
{% block title %}Erro Interno - CyberSecAssessment{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-8 text-center">
        <div class="error-container py-5">
            <h1 class="display-1 text-danger">500</h1>
            <h2 class="mb-4">Erro Interno do Servidor</h2>
            <p class="lead mb-4">Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde ou entre em contato com o suporte.</p>
            <div class="mt-4">
                <a href="{{ url_for('index') }}" class="btn btn-primary btn-lg">
                    <i class="fas fa-home me-2"></i>Voltar para a Página Inicial
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        
        # Templates de autenticação
        'templates/auth/users.html': '''{% extends 'base.html' %}

{% block title %}Gerenciamento de Usuários - CyberSecAssessment{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <h1 class="display-5 fw-bold">
            <i class="fas fa-users-cog text-primary me-2"></i> Gerenciamento de Usuários
        </h1>
        <p class="lead">Gerencie os usuários do sistema de avaliação de segurança cibernética.</p>
    </div>
</div>

<div class="row mb-4">
    <div class="col">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Usuários Cadastrados</h5>
            <a href="{{ url_for('auth.register') }}" class="btn btn-primary">
                <i class="fas fa-user-plus me-1"></i> Novo Usuário
            </a>
        </div>
    </div>
</div>

{% if users %}
<div class="card shadow-sm">
    <div class="table-responsive">
        <table class="table table-hover mb-0">
            <thead class="table-light">
                <tr>
                    <th>Nome</th>
                    <th>Usuário</th>
                    <th>Email</th>
                    <th>Departamento</th>
                    <th>Município</th>
                    <th>Tipo</th>
                    <th>Último Acesso</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ user.first_name }} {{ user.last_name }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.department }}</td>
                    <td>{{ user.municipality }}</td>
                    <td>
                        {% if user.is_admin %}
                        <span class="badge bg-danger">Administrador</span>
                        {% else %}
                        <span class="badge bg-secondary">Usuário</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if user.last_login %}
                        {{ user.last_login.strftime('%d/%m/%Y %H:%M') }}
                        {% else %}
                        <span class="text-muted">Nunca acessou</span>
                        {% endif %}
                    </td>
                    <td>
                        <div class="btn-group" role="group">
                            <a href="{{ url_for('auth.edit_user', user_id=user.id) }}" class="btn btn-sm btn-outline-primary">
                                <i class="fas fa-edit"></i>
                            </a>
                            {% if user.id != current_user.id %}
                            <button type="button" class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{ user.id }}">
                                <i class="fas fa-trash"></i>
                            </button>
                            {% endif %}
                        </div>
                        
                        <!-- Modal de Confirmação de Exclusão -->
                        {% if user.id != current_user.id %}
                        <div class="modal fade" id="deleteModal{{ user.id }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ user.id }}" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="deleteModalLabel{{ user.id }}">Confirmar Exclusão</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                                    </div>
                                    <div class="modal-body">
                                        <p>Tem certeza que deseja excluir o usuário <strong>"{{ user.username }}"</strong>?</p>
                                        <p class="text-danger">Esta ação não pode ser desfeita e removerá todas as avaliações associadas a este usuário.</p>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                        <form action="{{ url_for('auth.delete_user', user_id=user.id) }}" method="post">
                                            <button type="submit" class="btn btn-danger">Excluir</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% else %}
<div class="card shadow-sm">
    <div class="card-body text-center py-5">
        <div class="mb-4">
            <i class="fas fa-users fa-4x text-muted"></i>
        </div>
        <h4>Nenhum usuário encontrado</h4>
        <p class="text-muted">Não há usuários cadastrados no sistema além de você.</p>
        <a href="{{ url_for('auth.register') }}" class="btn btn-primary">
            <i class="fas fa-user-plus me-2"></i> Cadastrar Novo Usuário
        </a>
    </div>
</div>
{% endif %}
{% endblock %}''',
        
        'templates/auth/register.html': '''{% extends 'base.html' %}

{% block title %}Novo Usuário - CyberSecAssessment{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{{ url_for('dashboard.index') }}">Dashboard</a></li>
                <li class="breadcrumb-item"><a href="{{ url_for('auth.manage_users') }}">Usuários</a></li>
                <li class="breadcrumb-item active">Novo Usuário</li>
            </ol>
        </nav>
        
        <h1 class="display-5 fw-bold">
            <i class="fas fa-user-plus text-primary me-2"></i> Novo Usuário
        </h1>
        <p class="lead">Cadastre um novo usuário no sistema de avaliação de segurança cibernética.</p>
    </div>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card shadow-sm">
            <div class="card-body p-4">
                <form method="post">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="first_name" class="form-label">Nome</label>
                            <input type="text" class="form-control" id="first_name" name="first_name" required>
                        </div>
                        <div class="col-md-6">
                            <label for="last_name" class="form-label">Sobrenome</label>
                            <input type="text" class="form-control" id="last_name" name="last_name" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="username" class="form-label">Nome de Usuário</label>
                            <input type="text" class="form-control" id="username" name="username" required>
                            <div class="form-text">Deve ser único no sistema.</div>
                        </div>
                        <div class="col-md-6">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="password" class="form-label">Senha</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                            <div class="form-text">Mínimo de 8 caracteres, incluindo letras e números.</div>
                        </div>
                        <div class="col-md-6">
                            <label for="password_confirm" class="form-label">Confirmar Senha</label>
                            <input type="password" class="form-control" id="password_confirm" name="password_confirm" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="department" class="form-label">Departamento</label>
                            <input type="text" class="form-control" id="department" name="department" required>
                        </div>
                        <div class="col-md-6">
                            <label for="position" class="form-label">Cargo</label>
                            <input type="text" class="form-control" id="position" name="position" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="municipality" class="form-label">Município</label>
                        <input type="text" class="form-control" id="municipality" name="municipality" required>
                    </div>
                    
                    <div class="mb-4 form-check">
                        <input type="checkbox" class="form-check-input" id="is_admin" name="is_admin">
                        <label class="form-check-label" for="is_admin">Conceder privilégios de administrador</label>
                        <div class="form-text">Administradores podem gerenciar usuários e ter acesso a todas as avaliações.</div>
                    </div>
                    
                    <div class="d-flex justify-content-between">
                        <a href="{{ url_for('auth.manage_users') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-1"></i> Voltar
                        </a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-1"></i> Salvar Usuário
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        
        'templates/auth/edit_user.html': '''{% extends 'base.html' %}

{% block title %}Editar Usuário - CyberSecAssessment{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{{ url_for('dashboard.index') }}">Dashboard</a></li>
                <li class="breadcrumb-item"><a href="{{ url_for('auth.manage_users') }}">Usuários</a></li>
                <li class="breadcrumb-item active">Editar Usuário</li>
            </ol>
        </nav>
        
        <h1 class="display-5 fw-bold">
            <i class="fas fa-user-edit text-primary me-2"></i> Editar Usuário
        </h1>
        <p class="lead">Atualize as informações do usuário no sistema.</p>
    </div>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card shadow-sm">
            <div class="card-body p-4">
                <form method="post">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="first_name" class="form-label">Nome</label>
                            <input type="text" class="form-control" id="first_name" name="first_name" value="{{ user.first_name }}" required>
                        </div>
                        <div class="col-md-6">
                            <label for="last_name" class="form-label">Sobrenome</label>
                            <input type="text" class="form-control" id="last_name" name="last_name" value="{{ user.last_name }}" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="username" class="form-label">Nome de Usuário</label>
                            <input type="text" class="form-control" id="username" value="{{ user.username }}" readonly disabled>
                            <div class="form-text">O nome de usuário não pode ser alterado.</div>
                        </div>
                        <div class="col-md-6">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="password" class="form-label">Nova Senha (opcional)</label>
                            <input type="password" class="form-control" id="password" name="password">
                            <div class="form-text">Deixe em branco para manter a senha atual.</div>
                        </div>
                        <div class="col-md-6">
                            <label for="password_confirm" class="form-label">Confirmar Nova Senha</label>
                            <input type="password" class="form-control" id="password_confirm" name="password_confirm">
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="department" class="form-label">Departamento</label>
                            <input type="text" class="form-control" id="department" name="department" value="{{ user.department }}" required>
                        </div>
                        <div class="col-md-6">
                            <label for="position" class="form-label">Cargo</label>
                            <input type="text" class="form-control" id="position" name="position" value="{{ user.position }}" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="municipality" class="form-label">Município</label>
                        <input type="text" class="form-control" id="municipality" name="municipality" value="{{ user.municipality }}" required>
                    </div>
                    
                    <div class="mb-4 form-check">
                        <input type="checkbox" class="form-check-input" id="is_admin" name="is_admin" {% if user.is_admin %}checked{% endif %}>
                        <label class="form-check-label" for="is_admin">Conceder privilégios de administrador</label>
                        <div class="form-text">Administradores podem gerenciar usuários e ter acesso a todas as avaliações.</div>
                    </div>
                    
                    <div class="d-flex justify-content-between">
                        <a href="{{ url_for('auth.manage_users') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-1"></i> Voltar
                        </a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-1"></i> Salvar Alterações
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

'templates/auth/profile.html': '''{% extends 'base.html' %}

{% block title %}Meu Perfil - CyberSecAssessment{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <h1 class="display-5 fw-bold">
            <i class="fas fa-user-circle text-primary me-2"></i> Meu Perfil
        </h1>
        <p class="lead">Gerencie suas informações pessoais e credenciais de acesso.</p>
    </div>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card shadow-sm">
            <div class="card-body p-4">
                <form method="post">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="first_name" class="form-label">Nome</label>
                            <input type="text" class="form-control" id="first_name" name="first_name" value="{{ current_user.first_name }}" required>
                        </div>
                        <div class="col-md-6">
                            <label for="last_name" class="form-label">Sobrenome</label>
                            <input type="text" class="form-control" id="last_name" name="last_name" value="{{ current_user.last_name }}" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="username" class="form-label">Nome de Usuário</label>
                            <input type="text" class="form-control" id="username" value="{{ current_user.username }}" readonly disabled>
                            <div class="form-text">O nome de usuário não pode ser alterado.</div>
                        </div>
                        <div class="col-md-6">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" value="{{ current_user.email }}" required>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="password" class="form-label">Nova Senha (opcional)</label>
                            <input type="password" class="form-control" id="password" name="password">
                            <div class="form-text">Deixe em branco para manter a senha atual.</div>
                        </div>
                        <div class="col-md-6">
                            <label for="password_confirm" class="form-label">Confirmar Nova Senha</label>
                            <input type="password" class="form-control" id="password_confirm" name="password_confirm">
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="department" class="form-label">Departamento</label>
                            <input type="text" class="form-control" id="department" name="department" value="{{ current_user.department }}" required>
                        </div>
                        <div class="col-md-6">
                            <label for="position" class="form-label">Cargo</label>
                            <input type="text" class="form-control" id="position" name="position" value="{{ current_user.position }}" required>
                        </div>
                    </div>
                    
                    <div class="mb-4">
                        <label for="municipality" class="form-label">Município</label>
                        <input type="text" class="form-control" id="municipality" value="{{ current_user.municipality }}" readonly disabled>
                        <div class="form-text">O município não pode ser alterado. Entre em contato com um administrador se precisar modificar este campo.</div>
                    </div>
                    
                    <div class="d-flex justify-content-between">
                        <a href="{{ url_for('dashboard.index') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-1"></i> Voltar para Dashboard
                        </a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-1"></i> Salvar Alterações
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        
        # Templates de avaliações
        'templates/assessment/list.html': '''{% extends 'base.html' %}

{% block title %}Avaliações - CyberSecAssessment{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <h1 class="display-5 fw-bold">
            <i class="fas fa-clipboard-check text-primary me-2"></i> Avaliações
        </h1>
        <p class="lead">Gerencie suas avaliações de segurança cibernética.</p>
    </div>
</div>

<div class="row mb-4">
    <div class="col">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Suas Avaliações</h5>
            <a href="{{ url_for('assessment.new_assessment') }}" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i> Nova Avaliação
            </a>
        </div>
    </div>
</div>

{% if assessments %}
<div class="card shadow-sm">
    <div class="table-responsive">
        <table class="table table-hover mb-0">
            <thead class="table-light">
                <tr>
                    <th>Título</th>
                    <th>Data</th>
                    <th>Status</th>
                    <th>Pontuação</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for assessment in assessments %}
                <tr>
                    <td>
                        <strong>{{ assessment.title }}</strong>
                        {% if assessment.description %}
                        <br>
                        <small class="text-muted">{{ assessment.description|truncate(60) }}</small>
                        {% endif %}
                    </td>
                    <td>{{ assessment.created_at.strftime('%d/%m/%Y') }}</td>
                    <td>
                        {% if assessment.status == 'completed' %}
                        <span class="badge bg-success">Concluída</span>
                        {% else %}
                        <span class="badge bg-warning text-dark">Em Progresso</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if assessment.status == 'completed' %}
                        <div class="d-flex align-items-center">
                            <div class="progress flex-grow-1 me-2" style="height: 8px">
                                <div class="progress-bar 
                                    {% if assessment.total_score >= 80 %}bg-success
                                    {% elif assessment.total_score >= 60 %}bg-warning
                                    {% else %}bg-danger{% endif %}"
                                    role="progressbar" 
                                    style="width: {{ assessment.total_score }}%" 
                                    aria-valuenow="{{ assessment.total_score }}" 
                                    aria-valuemin="0" 
                                    aria-valuemax="100">
                                </div>
                            </div>
                            <span class="small fw-bold">{{ assessment.total_score|round|int }}%</span>
                        </div>
                        {% else %}
                        <span class="text-muted">--</span>
                        {% endif %}
                    </td>
                    <td>
                        <div class="btn-group" role="group">
                            {% if assessment.status == 'completed' %}
                            <a href="{{ url_for('assessment.view_assessment', assessment_id=assessment.id) }}" class="btn btn-sm btn-outline-primary">
                                <i class="fas fa-eye"></i>
                            </a>
                            {% else %}
                            <a href="{{ url_for('assessment.edit_assessment', assessment_id=assessment.id) }}" class="btn btn-sm btn-outline-primary">
                                <i class="fas fa-edit"></i>
                            </a>
                            {% endif %}
                            <button type="button" class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{ assessment.id }}">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                        
                        <!-- Modal de Confirmação de Exclusão -->
                        <div class="modal fade" id="deleteModal{{ assessment.id }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ assessment.id }}" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="deleteModalLabel{{ assessment.id }}">Confirmar Exclusão</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                                    </div>
                                    <div class="modal-body">
                                        <p>Tem certeza que deseja excluir a avaliação <strong>"{{ assessment.title }}"</strong>?</p>
                                        <p class="text-danger">Esta ação não pode ser desfeita.</p>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                        <form action="{{ url_for('assessment.delete_assessment', assessment_id=assessment.id) }}" method="post">
                                            <button type="submit" class="btn btn-danger">Excluir</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% else %}
<div class="card shadow-sm">
    <div class="card-body text-center py-5">
        <div class="mb-4">
            <i class="fas fa-clipboard-list fa-4x text-muted"></i>
        </div>
        <h4>Nenhuma avaliação encontrada</h4>
        <p class="text-muted">Você ainda não realizou nenhuma avaliação de segurança cibernética.</p>
        <a href="{{ url_for('assessment.new_assessment') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i> Iniciar Primeira Avaliação
        </a>
    </div>
</div>
{% endif %}
{% endblock %}'''
    }
    
    for template_path, content in templates.items():
        path = Path(template_path)
        if not path.exists():
            print(f"Criando template: {template_path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("Verificação de templates concluída.")

# Função principal
def main():
    print("=" * 50)
    print("Sistema de Autoavaliação de Segurança Cibernética")
    print("Inicializando...")
    print("=" * 50)
    
    # Criar estrutura de diretórios
    create_directories()
    
    # Verificar templates necessários
    check_templates()
    
    # Inicializar banco de dados
    app = init_database()
    
    # Criar usuário administrador
    create_admin_user(app)
    
    print("\nTudo pronto! Iniciando o sistema...")
    print("=" * 50)
    
    # Inicia um thread para abrir o navegador
    threading.Thread(target=open_browser).start()
    
    # Inicia o servidor Flask
    app.run(debug=False, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()