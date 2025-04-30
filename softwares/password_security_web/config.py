import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """
    Configurações centralizadas da aplicação
    """
    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    
    # Configurações de segurança
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Configurações de debug
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # Configurações de log
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configurações de banco de dados (opcional)
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///security_app.db')
    
    # Configurações de APIs externas
    HAVEIBEENPWNED_API_KEY = os.getenv('HAVEIBEENPWNED_API_KEY')
    
    # Limites de segurança
    MAX_PASSWORD_ATTEMPTS = 5
    BLOCK_DURATION_MINUTES = 15

class DevelopmentConfig(Config):
    """
    Configurações para ambiente de desenvolvimento
    """
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """
    Configurações para ambiente de produção
    """
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """
    Configurações para testes
    """
    TESTING = True
    DATABASE_URI = 'sqlite:///:memory:'

# Seletor de configuração
def get_config():
    """
    Seleciona a configuração baseada no ambiente
    """
    env = os.getenv('FLASK_ENV', 'development')
    
    config_selector = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_selector.get(env, DevelopmentConfig)