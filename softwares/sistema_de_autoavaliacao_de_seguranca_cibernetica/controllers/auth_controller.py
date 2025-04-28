from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from models import db
from models.user import User
from utils.security import require_admin, generate_confirmation_token, confirm_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
@require_admin
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        department = request.form.get('department')
        position = request.form.get('position')
        municipality = request.form.get('municipality')
        is_admin = 'is_admin' in request.form
        
        # Verificar se username ou email já existem
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já está em uso.', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email já está em uso.', 'danger')
            return render_template('auth/register.html')
        
        # Criar novo usuário
        new_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            department=department,
            position=position,
            municipality=municipality,
            is_admin=is_admin
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'Usuário {username} criado com sucesso!', 'success')
        return redirect(url_for('auth.manage_users'))
    
    return render_template('auth/register.html')

@auth_bp.route('/users')
@login_required
@require_admin
def manage_users():
    users = User.query.all()
    return render_template('auth/users.html', users=users)

@auth_bp.route('/users//edit', methods=['GET', 'POST'])
@login_required
@require_admin
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')
        user.department = request.form.get('department')
        user.position = request.form.get('position')
        user.municipality = request.form.get('municipality')
        user.is_admin = 'is_admin' in request.form
        
        # Atualizar senha se fornecida
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('auth.manage_users'))
    
    return render_template('auth/edit_user.html', user=user)

@auth_bp.route('/users//delete', methods=['POST'])
@login_required
@require_admin
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Proibir exclusão do próprio usuário
    if user.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário.', 'danger')
        return redirect(url_for('auth.manage_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('auth.manage_users'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.email = request.form.get('email')
        current_user.department = request.form.get('department')
        current_user.position = request.form.get('position')
        
        # Atualizar senha se fornecida
        if request.form.get('password'):
            current_user.set_password(request.form.get('password'))
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html')