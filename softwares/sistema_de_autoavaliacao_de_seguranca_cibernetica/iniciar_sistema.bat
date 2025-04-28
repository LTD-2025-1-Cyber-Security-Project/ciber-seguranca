@echo off
cls
TITLE Sistema de Autoavaliação de Segurança Cibernética
ECHO =======================================================
ECHO Sistema de Autoavaliação de Segurança Cibernética
ECHO Inicializando...
ECHO =======================================================

REM Criar estrutura de diretórios
mkdir static\css static\js static\images static\uploads 2>nul
mkdir templates\auth templates\assessment templates\dashboard templates\errors 2>nul

REM Verificar se o banco de dados existe
IF NOT EXIST cybersec_assessment.db (
    ECHO Criando banco de dados e usuário administrador...
    
    REM Criar script Python temporário
    ECHO from app import create_app > init_db.py
    ECHO from models import db >> init_db.py
    ECHO from models.user import User >> init_db.py
    ECHO. >> init_db.py
    ECHO app = create_app() >> init_db.py
    ECHO. >> init_db.py
    ECHO with app.app_context(): >> init_db.py
    ECHO     db.create_all() >> init_db.py
    ECHO. >> init_db.py
    ECHO     admin = User.query.filter_by(username='estevam5s').first() >> init_db.py
    ECHO. >> init_db.py
    ECHO     if not admin: >> init_db.py
    ECHO         admin = User( >> init_db.py
    ECHO             username='estevam5s', >> init_db.py
    ECHO             email='contato@estevamsouza.com.br', >> init_db.py
    ECHO             first_name='Estevam Souza', >> init_db.py
    ECHO             last_name='Laureth', >> init_db.py
    ECHO             department='TI', >> init_db.py
    ECHO             position='Administrador', >> init_db.py
    ECHO             municipality='Floripa', >> init_db.py
    ECHO             is_admin=True >> init_db.py
    ECHO         ) >> init_db.py
    ECHO         admin.set_password('estevam5s') >> init_db.py
    ECHO. >> init_db.py
    ECHO         db.session.add(admin) >> init_db.py
    ECHO         db.session.commit() >> init_db.py
    ECHO. >> init_db.py
    ECHO         print('Usuário administrador criado com sucesso!') >> init_db.py
    ECHO     else: >> init_db.py
    ECHO         print('Usuário administrador já existe.') >> init_db.py
    
    REM Executar o script
    python init_db.py
    
    REM Remover o script temporário
    del init_db.py
) ELSE (
    ECHO Banco de dados já existe.
)

REM Iniciar o servidor e abrir o navegador
ECHO Iniciando o servidor...
start http://127.0.0.1:5000
python run.py