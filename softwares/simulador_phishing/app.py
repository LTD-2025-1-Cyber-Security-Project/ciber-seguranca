"""
Simulador de Phishing Educacional

Uma aplicação web Flask para criar e gerenciar campanhas de phishing educacional,
ajudando organizações a treinar seus funcionários na identificação e prevenção de ataques de phishing.

Versão: 1.0.0
"""

import os
import re
import uuid
import secrets
import logging
from datetime import datetime
from functools import wraps

# Flask e extensões
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import ssl

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Inicialização do banco de dados e login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

# Modelos - Compatíveis com o banco existente
class User(UserMixin, db.Model):
    """Modelo de usuário para autenticação e gerenciamento de campanhas"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    campaigns = db.relationship('Campaign', backref='creator', lazy=True)
    
    def set_password(self, password):
        """Gera hash da senha para armazenamento seguro"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'

class Campaign(db.Model):
    """Modelo de campanha de phishing"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    templates = db.relationship('EmailTemplate', backref='campaign', lazy=True, cascade="all, delete-orphan")
    targets = db.relationship('Target', backref='campaign', lazy=True, cascade="all, delete-orphan")
    emails = db.relationship('Email', backref='campaign', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Campaign {self.name}>'
    
    def get_stats(self):
        """Calcula estatísticas da campanha"""
        total_emails = len(self.emails)
        opened_emails = sum(1 for email in self.emails if email.opened)
        clicked_emails = sum(1 for email in self.emails if email.clicked)
        reported_emails = sum(1 for email in self.emails if email.reported)
        
        # Taxas
        open_rate = (opened_emails / total_emails) * 100 if total_emails > 0 else 0
        click_rate = (clicked_emails / total_emails) * 100 if total_emails > 0 else 0
        report_rate = (reported_emails / total_emails) * 100 if total_emails > 0 else 0
        
        return {
            'total': total_emails,
            'opened': opened_emails,
            'clicked': clicked_emails,
            'reported': reported_emails,
            'open_rate': open_rate,
            'click_rate': click_rate,
            'report_rate': report_rate
        }
    
class EmailTemplate(db.Model):
    """Modelo de template de e-mail de phishing"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    phishing_indicators = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    emails = db.relationship('Email', backref='template', lazy=True)
    
    def __repr__(self):
        return f'<EmailTemplate {self.name}>'
    
class Target(db.Model):
    """Modelo para alvos das campanhas"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    emails_received = db.relationship('Email', backref='target', lazy=True)
    
    def __repr__(self):
        return f'<Target {self.name} ({self.email})>'
    
class Email(db.Model):
    """Modelo para e-mails enviados nas campanhas"""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened = db.Column(db.Boolean, default=False)
    opened_at = db.Column(db.DateTime)
    clicked = db.Column(db.Boolean, default=False)
    clicked_at = db.Column(db.DateTime)
    reported = db.Column(db.Boolean, default=False)
    reported_at = db.Column(db.DateTime)
    template_id = db.Column(db.Integer, db.ForeignKey('email_template.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    
    def __repr__(self):
        return f'<Email {self.uuid}>'

# Configuração do Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário a partir do ID para o Flask-Login"""
    return User.query.get(int(user_id))

# Decorador personalizado para verificar permissões de administrador
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Você precisa de privilégios de administrador para acessar esta página.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar propriedade de campanha
def campaign_owner_required(f):
    @wraps(f)
    @login_required
    def decorated_function(campaign_id, *args, **kwargs):
        campaign = Campaign.query.get_or_404(campaign_id)
        if campaign.creator_id != current_user.id and not current_user.is_admin:
            flash('Você não tem permissão para acessar esta campanha', 'danger')
            return redirect(url_for('dashboard'))
        return f(campaign_id, *args, **kwargs)
    return decorated_function

# Funções auxiliares
def send_email_with_tracking(email_record, smtp_config):
    """
    Envia um e-mail com pixel de rastreamento e links modificados
    
    Args:
        email_record (Email): Registro do e-mail a ser enviado
        smtp_config (dict): Configurações SMTP para envio
        
    Returns:
        bool: True se o e-mail foi enviado com sucesso, False caso contrário
    """
    try:
        target = email_record.target
        template = email_record.template
        
        # Configurar conexão SMTP com configuração de SSL modificada
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE  # Desabilita verificação de certificado
        
        server = smtplib.SMTP(smtp_config['server'], int(smtp_config['port']))
        server.starttls(context=context)
        server.login(smtp_config['user'], smtp_config['password'])
        
        # Preparar mensagem
        msg = MIMEMultipart('alternative')
        msg['Subject'] = template.subject
        msg['From'] = formataddr((smtp_config['sender_name'], smtp_config['sender_email']))
        msg['To'] = formataddr((target.name, target.email))
        msg['Message-ID'] = f"<{email_record.uuid}@phishingsimulator.local>"
        
        # Personalizar o corpo do e-mail com os dados do alvo
        body_html = template.body
        body_html = body_html.replace('{nome}', target.name)
        body_html = body_html.replace('{email}', target.email)
        body_html = body_html.replace('{departamento}', target.department or '')
        
        # Adicionar pixel de rastreamento
        tracking_pixel = f'<img src="{request.url_root}track/{email_record.uuid}/open" width="1" height="1" alt="" />'
        body_html += tracking_pixel
        
        # Substituir links com links de rastreamento
        def replace_links(match):
            original_url = match.group(1)
            tracking_url = f"{request.url_root}track/{email_record.uuid}/click?url={original_url}"
            return f'href="{tracking_url}"'
        
        body_html = re.sub(r'href="([^"]+)"', replace_links, body_html)
        
        # Adicionar botão de reporte de phishing
        report_button = f'''
        <div style="margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
            <p style="margin-bottom: 10px; font-size: 12px;">Se você acredita que este é um e-mail de phishing:</p>
            <a href="{request.url_root}report/{email_record.uuid}" 
               style="display: inline-block; padding: 5px 10px; background-color: #28a745; color: white; 
                      text-decoration: none; border-radius: 3px; font-size: 12px;">
                Reportar como Phishing
            </a>
        </div>
        '''
        body_html += report_button
        
        # Adicionar parte HTML
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        
        # Enviar e-mail
        server.sendmail(smtp_config['sender_email'], target.email, msg.as_string())
        server.quit()
        
        logger.info(f"E-mail enviado com sucesso para {target.email}")
        return True
        
    except Exception as e:
        # Registrar erro
        error_message = str(e)
        logger.error(f"Erro ao enviar e-mail para {target.email}: {error_message}")
        return False

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login de usuários"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Rota para logout de usuários"""
    logout_user()
    flash('Você saiu do sistema com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Rota para registro de novos usuários"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe', 'danger')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email já está em uso', 'danger')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Torna o primeiro usuário admin
        if User.query.count() == 0:
            user.is_admin = True
            
        db.session.add(user)
        db.session.commit()
        
        flash('Registro concluído com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

# Rotas principais
@app.route('/')
def index():
    """Rota principal - redireciona para login ou dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do usuário"""
    user_campaigns = Campaign.query.filter_by(creator_id=current_user.id).all()
    return render_template('dashboard.html', campaigns=user_campaigns)

# Rotas para campanhas
@app.route('/campaigns/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    """Rota para criar uma nova campanha"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        campaign = Campaign(
            name=name,
            description=description,
            creator_id=current_user.id
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        flash('Campanha criada com sucesso!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign.id))
        
    return render_template('campaign_new.html')

@app.route('/campaigns/<int:campaign_id>')
@login_required
@campaign_owner_required
def campaign_detail(campaign_id):
    """Rota para visualizar detalhes de uma campanha"""
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign_detail.html', campaign=campaign)

@app.route('/campaigns/<int:campaign_id>/edit', methods=['GET', 'POST'])
@login_required
@campaign_owner_required
def edit_campaign(campaign_id):
    """Rota para editar uma campanha existente"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if request.method == 'POST':
        campaign.name = request.form.get('name')
        campaign.description = request.form.get('description')
        campaign.active = 'active' in request.form
        
        db.session.commit()
        flash('Campanha atualizada com sucesso!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign.id))
        
    return render_template('campaign_edit.html', campaign=campaign)

@app.route('/campaigns/<int:campaign_id>/delete', methods=['POST'])
@login_required
@campaign_owner_required
def delete_campaign(campaign_id):
    """Rota para excluir uma campanha"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    db.session.delete(campaign)
    db.session.commit()
    
    flash('Campanha excluída com sucesso!', 'success')
    return redirect(url_for('dashboard'))

# Rotas para templates de e-mail
@app.route('/campaigns/<int:campaign_id>/templates/new', methods=['GET', 'POST'])
@login_required
@campaign_owner_required
def new_template(campaign_id):
    """Rota para criar um novo template de e-mail"""
    campaign = Campaign.query.get_or_404(campaign_id)
        
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        body = request.form.get('body')
        phishing_indicators = request.form.get('phishing_indicators')
        difficulty = request.form.get('difficulty')
        
        template = EmailTemplate(
            name=name,
            subject=subject,
            body=body,
            phishing_indicators=phishing_indicators,
            difficulty=difficulty,
            campaign_id=campaign_id
        )
        
        db.session.add(template)
        db.session.commit()
        
        flash('Template de e-mail adicionado com sucesso!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
        
    return render_template('template_new.html', campaign=campaign)

@app.route('/campaigns/<int:campaign_id>/templates/<int:template_id>/edit', methods=['GET', 'POST'])
@login_required
@campaign_owner_required
def edit_template(campaign_id, template_id):
    """Rota para editar um template de e-mail existente"""
    campaign = Campaign.query.get_or_404(campaign_id)
    template = EmailTemplate.query.get_or_404(template_id)
    
    if template.campaign_id != campaign.id:
        flash('Este template não pertence a esta campanha', 'danger')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
    
    if request.method == 'POST':
        template.name = request.form.get('name')
        template.subject = request.form.get('subject')
        template.body = request.form.get('body')
        template.phishing_indicators = request.form.get('phishing_indicators')
        template.difficulty = request.form.get('difficulty')
        
        db.session.commit()
        flash('Template atualizado com sucesso!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
        
    return render_template('template_edit.html', campaign=campaign, template=template)

@app.route('/campaigns/<int:campaign_id>/templates/<int:template_id>/delete', methods=['POST'])
@login_required
@campaign_owner_required
def delete_template(campaign_id, template_id):
    """Rota para excluir um template de e-mail"""
    template = EmailTemplate.query.get_or_404(template_id)
    
    if template.campaign_id != campaign_id:
        flash('Este template não pertence a esta campanha', 'danger')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
    
    db.session.delete(template)
    db.session.commit()
    
    flash('Template excluído com sucesso!', 'success')
    return redirect(url_for('campaign_detail', campaign_id=campaign_id))

# Rotas para alvos
@app.route('/campaigns/<int:campaign_id>/targets/new', methods=['GET', 'POST'])
@login_required
@campaign_owner_required
def new_target(campaign_id):
    """Rota para adicionar um novo alvo"""
    campaign = Campaign.query.get_or_404(campaign_id)
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        
        target = Target(
            name=name,
            email=email,
            department=department,
            campaign_id=campaign_id
        )
        
        db.session.add(target)
        db.session.commit()
        
        flash('Alvo adicionado com sucesso!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
        
    return render_template('target_new.html', campaign=campaign)

@app.route('/campaigns/<int:campaign_id>/targets/bulk', methods=['GET', 'POST'])
@login_required
@campaign_owner_required
def bulk_targets(campaign_id):
    """Rota para importação em massa de alvos"""
    campaign = Campaign.query.get_or_404(campaign_id)
        
    if request.method == 'POST':
        csv_data = request.form.get('csv_data')
        lines = csv_data.strip().split('\n')
        added_count = 0
        
        for line in lines:
            parts = line.split(',')
            if len(parts) >= 2:
                name = parts[0].strip()
                email = parts[1].strip()
                department = parts[2].strip() if len(parts) > 2 else ''
                
                # Verificar se o e-mail já existe nesta campanha
                if not Target.query.filter_by(email=email, campaign_id=campaign_id).first():
                    target = Target(
                        name=name,
                        email=email,
                        department=department,
                        campaign_id=campaign_id
                    )
                    
                    db.session.add(target)
                    added_count += 1
        
        db.session.commit()
        flash(f'{added_count} alvos adicionados com sucesso!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
        
    return render_template('targets_bulk.html', campaign=campaign)

@app.route('/campaigns/<int:campaign_id>/targets/<int:target_id>/delete', methods=['POST'])
@login_required
@campaign_owner_required
def delete_target(campaign_id, target_id):
    """Rota para excluir um alvo"""
    target = Target.query.get_or_404(target_id)
    
    if target.campaign_id != campaign_id:
        flash('Este alvo não pertence a esta campanha', 'danger')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
    
    db.session.delete(target)
    db.session.commit()
    
    flash('Alvo excluído com sucesso!', 'success')
    return redirect(url_for('campaign_detail', campaign_id=campaign_id))

# Rotas para envio de e-mails
@app.route('/campaigns/<int:campaign_id>/send', methods=['GET', 'POST'])
@login_required
@campaign_owner_required
def send_campaign(campaign_id):
    """Rota para enviar uma campanha de phishing"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if not campaign.templates:
        flash('Adicione pelo menos um template de e-mail antes de enviar a campanha', 'warning')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
    
    if not campaign.targets:
        flash('Adicione pelo menos um alvo antes de enviar a campanha', 'warning')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))
        
    if request.method == 'POST':
        template_id = request.form.get('template_id')
        template = EmailTemplate.query.get_or_404(template_id)
        
        # Configurações de e-mail
        smtp_config = {
            'server': request.form.get('smtp_server'),
            'port': request.form.get('smtp_port'),
            'user': request.form.get('smtp_user'),
            'password': request.form.get('smtp_password'),
            'sender_email': request.form.get('sender_email'),
            'sender_name': request.form.get('sender_name')
        }
        
        # Modo de simulação (não envia e-mails reais)
        simulation_mode = 'simulation_mode' in request.form
        
        # Criar registros de e-mail e enviar
        success_count = 0
        failure_count = 0
        
        for target in campaign.targets:
            # Criar registro de e-mail
            email = Email(
                template_id=template.id,
                target_id=target.id,
                campaign_id=campaign_id
            )
            db.session.add(email)
            db.session.commit()
            
            if simulation_mode:
                # Modo de simulação - apenas registra
                success_count += 1
            else:
                # Envio real
                if send_email_with_tracking(email, smtp_config):
                    success_count += 1
                else:
                    failure_count += 1
            
        if simulation_mode:
            flash(f'Simulação concluída! {success_count} e-mails foram registrados (mas não enviados realmente).', 'info')
        else:
            if failure_count == 0:
                flash(f'Campanha enviada com sucesso! {success_count} e-mails enviados.', 'success')
            else:
                flash(f'Campanha enviada com {failure_count} falhas. {success_count} e-mails foram enviados com sucesso.', 'warning')
        
        return redirect(url_for('campaign_results', campaign_id=campaign_id))
        
    return render_template('send_campaign.html', campaign=campaign)

# Rotas de rastreamento
@app.route('/track/<uuid>/open')
def track_open(uuid):
    """Rastreia a abertura de um e-mail através de um pixel invisível"""
    email = Email.query.filter_by(uuid=uuid).first()
    
    if email and not email.opened:
        email.opened = True
        email.opened_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"E-mail {uuid} aberto por {email.target.email}")
    
    # Retorna um pixel transparente de 1x1
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return pixel, 200, {'Content-Type': 'image/gif', 'Cache-Control': 'no-cache, no-store, must-revalidate'}

@app.route('/track/<uuid>/click')
def track_click(uuid):
    """Rastreia cliques em links no e-mail"""
    email = Email.query.filter_by(uuid=uuid).first()
    redirect_url = request.args.get('url', '')
    
    if email and not email.clicked:
        email.clicked = True
        email.clicked_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Link clicado no e-mail {uuid} por {email.target.email}")
    
    # Validação básica de URL para evitar redirecionamentos perigosos
    if not redirect_url.startswith(('http://', 'https://')):
        redirect_url = 'https://' + redirect_url
    
    # Redireciona para o URL original
    return redirect(redirect_url)

@app.route('/report/<uuid>')
def report_phishing(uuid):
    """Rota para reportar um e-mail como phishing"""
    email = Email.query.filter_by(uuid=uuid).first()
    
    if email and not email.reported:
        email.reported = True
        email.reported_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"E-mail {uuid} reportado como phishing por {email.target.email}")
        
    return render_template('phishing_reported.html')

# Rotas para resultados e análises
@app.route('/campaigns/<int:campaign_id>/results')
@login_required
@campaign_owner_required
def campaign_results(campaign_id):
    """Rota para visualizar resultados de uma campanha"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Calcular estatísticas
    stats = campaign.get_stats()
    
    # Dados por departamento (se houver)
    departments = {}
    for target in campaign.targets:
        dept = target.department or 'Sem departamento'
        if dept not in departments:
            departments[dept] = {'total': 0, 'opened': 0, 'clicked': 0, 'reported': 0}
        
        departments[dept]['total'] += 1
        for email in target.emails_received:
            if email.campaign_id == campaign.id:
                if email.opened:
                    departments[dept]['opened'] += 1
                if email.clicked:
                    departments[dept]['clicked'] += 1
                if email.reported:
                    departments[dept]['reported'] += 1
    
    # Calcular taxas por departamento
    for dept in departments:
        total = departments[dept]['total']
        if total > 0:
            departments[dept]['open_rate'] = (departments[dept]['opened'] / total) * 100
            departments[dept]['click_rate'] = (departments[dept]['clicked'] / total) * 100
            departments[dept]['report_rate'] = (departments[dept]['reported'] / total) * 100
    
    return render_template('campaign_results.html', campaign=campaign, stats=stats, departments=departments)

@app.route('/campaigns/<int:campaign_id>/export')
@login_required
@campaign_owner_required
def export_results(campaign_id):
    """Exporta os resultados de uma campanha em formato CSV"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Criar CSV
    csv_data = "Nome,Email,Departamento,Enviado,Aberto,Horário de Abertura,Clicado,Horário de Clique,Reportado,Horário de Reporte\n"
    
    for email in campaign.emails:
        target = email.target
        
        row = [
            target.name,
            target.email,
            target.department or '',
            email.sent_at.strftime('%d/%m/%Y %H:%M') if email.sent_at else '',
            'Sim' if email.opened else 'Não',
            email.opened_at.strftime('%d/%m/%Y %H:%M') if email.opened_at else '',
            'Sim' if email.clicked else 'Não',
            email.clicked_at.strftime('%d/%m/%Y %H:%M') if email.clicked_at else '',
            'Sim' if email.reported else 'Não',
            email.reported_at.strftime('%d/%m/%Y %H:%M') if email.reported_at else ''
        ]
        
        csv_data += ','.join([f'"{item}"' for item in row]) + "\n"
    
    # Criar arquivo temporário
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp:
        temp.write(csv_data)
        temp_path = temp.name
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=f'campanha_{campaign.name}_{datetime.now().strftime("%Y%m%d")}.csv',
        mimetype='text/csv'
    )

# Módulo educacional
@app.route('/learn')
@login_required
def learn():
    """Página com material educacional sobre phishing"""
    return render_template('learn.html')

@app.route('/learn/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    """Quiz sobre phishing"""
    if request.method == 'POST':
        # Processar respostas do quiz
        score = 0
        total_questions = 10
        
        for i in range(1, total_questions + 1):
            user_answer = request.form.get(f'q{i}')
            correct_answer = request.form.get(f'correct_q{i}')
            
            if user_answer == correct_answer:
                score += 1
        
        percentage = (score / total_questions) * 100
        
        return render_template('quiz_results.html', score=score, total=total_questions, percentage=percentage)
        
    return render_template('quiz.html')

# Rotas de administração
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Dashboard de administração para usuários admin"""
    users = User.query.all()
    campaigns = Campaign.query.all()
    
    total_users = len(users)
    total_campaigns = len(campaigns)
    total_templates = EmailTemplate.query.count()
    total_targets = Target.query.count()
    total_emails = Email.query.count()
    
    stats = {
        'total_users': total_users,
        'total_campaigns': total_campaigns,
        'total_templates': total_templates,
        'total_targets': total_targets,
        'total_emails': total_emails
    }
    
    return render_template('admin_dashboard.html', users=users, campaigns=campaigns, stats=stats)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Gerenciamento de usuários (apenas admin)"""
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Alterna o status de administrador de um usuário"""
    user = User.query.get_or_404(user_id)
    
    # Impedir que o admin remova seus próprios privilégios
    if user.id == current_user.id:
        flash('Você não pode remover seus próprios privilégios de administrador', 'danger')
        return redirect(url_for('admin_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    flash(f'Privilégios de administrador {"concedidos" if user.is_admin else "removidos"} para {user.username}', 'success')
    return redirect(url_for('admin_users'))

# Manipulação de erros
@app.errorhandler(404)
def page_not_found(e):
    """Manipulador para erro 404"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Manipulador para erro 500"""
    return render_template('errors/500.html'), 500

# Criação de templates - Função utilitária
def ensure_templates_exist():
    """Verifica se todas as pastas de templates existem"""
    template_dirs = [
        'templates',
        'templates/errors'
    ]
    
    for directory in template_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Criado diretório: {directory}")

if __name__ == '__main__':
    # Garantir que o diretório de templates existe
    ensure_templates_exist()
    
    # Criar tabelas no banco de dados antes de iniciar a aplicação
    with app.app_context():
        db.create_all()
        logger.info("Tabelas criadas/verificadas com sucesso!")
        
        # Verificar se existe pelo menos um admin
        if not User.query.filter_by(is_admin=True).first():
            logger.info("Nenhum administrador encontrado. O primeiro usuário registrado será um administrador.")
    
    # Iniciar a aplicação
    logger.info("Iniciando aplicação Simulador de Phishing Educacional...")
    app.run(debug=True, host='0.0.0.0', port=5000)