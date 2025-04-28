#!/bin/bash

echo "=================================================="
echo "Sistema de Autoavaliação de Segurança Cibernética"
echo "Inicializando..."
echo "=================================================="

# Configurar variáveis
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

# Criar estrutura de diretórios
echo "Criando estrutura de diretórios necessária..."
mkdir -p static/css static/js static/images
mkdir -p templates/auth templates/assessment templates/dashboard templates/errors
echo "Estrutura de diretórios criada com sucesso."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Inicializar banco de dados e criar usuário admin
DB_PATH="$BASE_DIR/cybersec_assessment.db"
echo "Configurando banco de dados em: $DB_PATH"

python3 -c "from app import create_app; from models import db; from models.user import User; app = create_app(); with app.app_context(): db.create_all(); admin = User.query.filter_by(username='estevam5s').first(); if not admin: admin = User(username='estevam5s', email='contato@estevamsouza.com.br', first_name='Estevam Souza', last_name='Laureth', department='TI', position='Administrador', municipality='Floripa', is_admin=True); admin.set_password('senha123'); db.session.add(admin); db.session.commit(); print('Usuário administrador criado com sucesso!')"

if [ $? -ne 0 ]; then
    echo "Erro ao inicializar banco de dados. Verifique as permissões de escrita na pasta."
    exit 1
fi

echo "Banco de dados inicializado com sucesso!"
echo "Iniciando o servidor..."

# Iniciar servidor e abrir navegador
python3 run.py &
sleep 2

# Detectar sistema operacional e abrir navegador
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://127.0.0.1:5000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://127.0.0.1:5000 &> /dev/null || sensible-browser http://127.0.0.1:5000 &> /dev/null || x-www-browser http://127.0.0.1:5000 &> /dev/null
fi

echo "Sistema iniciado! Para encerrar, pressione Ctrl+C."
wait