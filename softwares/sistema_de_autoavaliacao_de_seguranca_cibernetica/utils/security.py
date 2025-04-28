from functools import wraps
from flask import abort, request, current_app
from flask_login import current_user
import jwt
from datetime import datetime, timedelta

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Acesso proibido
        return f(*args, **kwargs)
    return decorated_function

def require_same_user_or_admin(f):
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        if not current_user.is_authenticated or \
           (current_user.id != user_id and not current_user.is_admin):
            abort(403)  # Acesso proibido
        return f(user_id, *args, **kwargs)
    return decorated_function

def generate_confirmation_token(email):
    """Gera um token para confirmação de email"""
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def confirm_token(token):
    """Confirma um token de email e retorna o email se válido"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload['email']
    except:
        return None
