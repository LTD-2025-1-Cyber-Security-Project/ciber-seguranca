#!/bin/bash

# Diretório de instalação
INSTALL_DIR="$HOME/CybersecPrefeitura"

# Criar diretório de instalação
mkdir -p "$INSTALL_DIR"

echo "Criando estrutura de diretórios..."
# Copiar arquivos do projeto
cp -R templates/ "$INSTALL_DIR/"
cp -R static/ "$INSTALL_DIR/"
cp -R models/ "$INSTALL_DIR/"
cp -R controllers/ "$INSTALL_DIR/"
cp -R utils/ "$INSTALL_DIR/"
cp app.py config.py run.py requirements.txt "$INSTALL_DIR/"

# Criar ambiente virtual e instalar dependências
echo "Instalando Python e dependências..."
cd "$INSTALL_DIR"

# Verificar se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não está instalado. Por favor, instale Python 3 e execute este script novamente."
    exit 1
fi

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo de execução
echo "Criando arquivo de execução..."
cat > "$INSTALL_DIR/start_cybersec.sh" << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python run.py
EOL

chmod +x "$INSTALL_DIR/start_cybersec.sh"

# Criar atalho no desktop
echo "Criando atalho no desktop..."
cat > "$HOME/Desktop/CybersecPrefeitura.sh" << EOL
#!/bin/bash
"$INSTALL_DIR/start_cybersec.sh"
EOL

chmod +x "$HOME/Desktop/CybersecPrefeitura.sh"

echo "Instalação concluída!"
echo "Para iniciar o Sistema de Autoavaliação de Segurança Cibernética, clique no atalho no Desktop ou execute:"
echo "$INSTALL_DIR/start_cybersec.sh"