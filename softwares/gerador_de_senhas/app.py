from flask import Flask, render_template, request, jsonify
import random
import string
import re
import html
import secrets
import math

app = Flask(__name__)

# Configurações de segurança
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True


@app.route('/')
def index():
    """Renderiza a página principal do gerador de senhas."""
    return render_template('index.html')


@app.route('/generate-password', methods=['POST'])
def generate_password():
    """API para gerar senhas baseadas nos parâmetros do usuário."""
    try:
        # Sanitização e validação das entradas
        data = request.get_json()
        
        # Validar comprimento da senha
        length = data.get('length', 16)
        try:
            length = int(length)
            if length < 8 or length > 64:
                return jsonify({'error': 'Comprimento deve estar entre 8 e 64 caracteres'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Comprimento inválido'}), 400
            
        # Validar opções de caracteres
        use_uppercase = bool(data.get('uppercase', True))
        use_lowercase = bool(data.get('lowercase', True))
        use_numbers = bool(data.get('numbers', True))
        use_special = bool(data.get('special', True))
        exclude_similar = bool(data.get('excludeSimilar', False))
        exclude_ambiguous = bool(data.get('excludeAmbiguous', False))
        
        # Verificar se pelo menos uma opção foi selecionada
        if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
            return jsonify({'error': 'Selecione pelo menos um tipo de caractere'}), 400
            
        # Gerar a senha
        password = generate_secure_password(
            length, 
            use_uppercase, 
            use_lowercase, 
            use_numbers, 
            use_special,
            exclude_similar,
            exclude_ambiguous
        )
        
        # Verificar se a senha atende aos requisitos mínimos
        if not validate_password(password, use_uppercase, use_lowercase, use_numbers, use_special):
            # Tentar novamente se não atender aos requisitos
            password = generate_secure_password(
                length, 
                use_uppercase, 
                use_lowercase, 
                use_numbers, 
                use_special,
                exclude_similar,
                exclude_ambiguous
            )
            
        # Calcular entropia
        charset_size = 0
        if use_uppercase: charset_size += 26
        if use_lowercase: charset_size += 26
        if use_numbers: charset_size += 10
        if use_special: charset_size += 33
        
        # Ajustar com base nas exclusões
        if exclude_similar:
            # Caracteres similares: i, l, 1, I, O, 0
            charset_size = max(0, charset_size - 6)
        
        if exclude_ambiguous:
            # Caracteres ambíguos: {}, [], (), /\, etc.
            charset_size = max(0, charset_size - 10)
            
        entropy = math.log2(charset_size ** length) if charset_size > 0 else 0
            
        return jsonify({
            'password': password,
            'entropy': entropy
        })
    
    except Exception as e:
        app.logger.error(f"Erro ao gerar senha: {str(e)}")
        return jsonify({'error': 'Ocorreu um erro ao gerar a senha'}), 500


def generate_secure_password(length, use_uppercase=True, use_lowercase=True, 
                            use_numbers=True, use_special=True,
                            exclude_similar=False, exclude_ambiguous=False):
    """
    Gera uma senha segura com base nos parâmetros fornecidos.
    
    Args:
        length: Comprimento da senha (8-64)
        use_uppercase: Incluir letras maiúsculas
        use_lowercase: Incluir letras minúsculas
        use_numbers: Incluir números
        use_special: Incluir caracteres especiais
        exclude_similar: Excluir caracteres semelhantes (i, l, 1, I, O, 0)
        exclude_ambiguous: Excluir caracteres ambíguos ({}, [], (), /\)
        
    Returns:
        Uma senha aleatória que atende aos critérios especificados
    """
    # Definir conjuntos de caracteres
    chars = []
    required_chars = []
    
    # Caracteres similares a evitar
    similar_chars = 'il1IO0'
    
    # Caracteres ambíguos a evitar
    ambiguous_chars = '{}[]()/\\\'"`~,;:.<>'
    
    if use_uppercase:
        uppercase_chars = string.ascii_uppercase
        if exclude_similar:
            uppercase_chars = ''.join(c for c in uppercase_chars if c not in similar_chars)
        
        chars.extend(uppercase_chars)
        if uppercase_chars:
            required_chars.append(secrets.choice(uppercase_chars))
        
    if use_lowercase:
        lowercase_chars = string.ascii_lowercase
        if exclude_similar:
            lowercase_chars = ''.join(c for c in lowercase_chars if c not in similar_chars)
            
        chars.extend(lowercase_chars)
        if lowercase_chars:
            required_chars.append(secrets.choice(lowercase_chars))
        
    if use_numbers:
        number_chars = string.digits
        if exclude_similar:
            number_chars = ''.join(c for c in number_chars if c not in similar_chars)
            
        chars.extend(number_chars)
        if number_chars:
            required_chars.append(secrets.choice(number_chars))
        
    if use_special:
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
        if exclude_ambiguous:
            special_chars = ''.join(c for c in special_chars if c not in ambiguous_chars)
            
        chars.extend(special_chars)
        if special_chars:
            required_chars.append(secrets.choice(special_chars))
    
    # Se não temos caracteres suficientes após as filtragens
    if not chars:
        raise ValueError("As opções de caracteres são muito restritivas, não há caracteres disponíveis")
    
    # Garantir que temos pelo menos um caractere de cada tipo selecionado
    if len(required_chars) > length:
        required_chars = required_chars[:length]
    
    # Completar o restante da senha com caracteres aleatórios
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(chars) for _ in range(remaining_length)]
    
    # Embaralhar para aumentar a aleatoriedade usando o algoritmo de Fisher-Yates
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
    
    return ''.join(password_chars)


def validate_password(password, use_uppercase, use_lowercase, use_numbers, use_special):
    """
    Valida se a senha contém pelo menos um caractere de cada tipo selecionado.
    
    Args:
        password: A senha a ser validada
        use_uppercase: Se letras maiúsculas são obrigatórias
        use_lowercase: Se letras minúsculas são obrigatórias
        use_numbers: Se números são obrigatórios
        use_special: Se caracteres especiais são obrigatórios
        
    Returns:
        True se a senha atende a todos os requisitos, False caso contrário
    """
    has_uppercase = bool(re.search(r'[A-Z]', password)) if use_uppercase else True
    has_lowercase = bool(re.search(r'[a-z]', password)) if use_lowercase else True
    has_number = bool(re.search(r'[0-9]', password)) if use_numbers else True
    has_special = bool(re.search(r'[^A-Za-z0-9]', password)) if use_special else True
    
    return all([has_uppercase, has_lowercase, has_number, has_special])


@app.route('/passphrase', methods=['POST'])
def generate_passphrase():
    """Gera uma frase-senha baseada em palavras aleatórias."""
    try:
        data = request.get_json()
        num_words = min(max(int(data.get('numWords', 4)), 3), 10)
        include_number = bool(data.get('includeNumber', True))
        include_special = bool(data.get('includeSpecial', False))
        capitalize = bool(data.get('capitalize', True))
        
        # Lista de palavras comuns
        words = [
            "apple", "banana", "sunset", "mountain", "river", "ocean", "forest", "desert", 
            "castle", "dragon", "knight", "wizard", "magic", "science", "planet", "galaxy", 
            "star", "moon", "robot", "computer", "network", "system", "keyboard", "screen",
            "phone", "camera", "picture", "music", "guitar", "piano", "violin", "trumpet",
            "garden", "flower", "coffee", "cookie", "pizza", "burger", "chicken", "potato",
            "carrot", "broccoli", "cheese", "bread", "butter", "honey", "sugar", "pepper",
            "bottle", "glass", "table", "chair", "window", "door", "roof", "floor", "wall",
            "paper", "pencil", "notebook", "backpack", "jacket", "shirt", "pants", "shoes",
            "clock", "watch", "morning", "evening", "minute", "second", "weekend", "holiday"
        ]
        
        # Selecionar palavras aleatórias
        selected_words = [secrets.choice(words) for _ in range(num_words)]
        
        # Aplicar capitalização
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
            
        # Juntar com um separador
        passphrase = "-".join(selected_words)
        
        # Adicionar número se solicitado
        if include_number:
            passphrase += str(secrets.randbelow(1000))
            
        # Adicionar caractere especial se solicitado
        if include_special:
            special_chars = "!@#$%^&*"
            passphrase += secrets.choice(special_chars)
            
        return jsonify({'passphrase': passphrase})
            
    except Exception as e:
        app.logger.error(f"Erro ao gerar frase-senha: {str(e)}")
        return jsonify({'error': 'Ocorreu um erro ao gerar a frase-senha'}), 500


@app.after_request
def add_security_headers(response):
    """Adiciona cabeçalhos de segurança em todas as respostas."""
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' https://cdnjs.cloudflare.com; script-src 'self'; font-src 'self' https://cdnjs.cloudflare.com;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')