# Simulador de Phishing Educacional

Um aplicativo web Flask projetado para criar e gerenciar campanhas de phishing para fins educacionais, ajudando organizações a treinar seus funcionários na identificação e prevenção de ataques de phishing.

![Versão](https://img.shields.io/badge/Versão-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-red)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Características](#características)
- [Instalação](#instalação)
- [Uso](#uso)
- [Empacotamento](#empacotamento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Solução de Problemas](#solução-de-problemas)
- [Considerações Éticas](#considerações-éticas)
- [Licença](#licença)

## 🔍 Visão Geral

O Simulador de Phishing Educacional é uma ferramenta projetada para criar e executar campanhas de phishing controladas em ambientes corporativos ou educacionais. O objetivo é aumentar a conscientização sobre segurança cibernética, ajudando os usuários a reconhecer e evitar tentativas de phishing no mundo real.

## ✨ Características

- **Gestão de campanhas**: Crie e gerencie múltiplas campanhas de phishing educacional
- **Templates personalizáveis**: Crie e customize templates de e-mail para simular diferentes tipos de ataques
- **Gestão de alvos**: Adicione alvos individualmente ou importe-os em massa via CSV
- **Rastreamento em tempo real**: Monitore quem abriu os e-mails, clicou em links ou reportou o phishing
- **Relatórios detalhados**: Visualize estatísticas e métricas por departamento, template ou campanha
- **Módulo educacional**: Material educativo e quiz sobre phishing para conscientização
- **Modo de simulação**: Teste campanhas sem enviar e-mails reais

## 🔧 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes do Python)

### Instalação a partir do código-fonte

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/simulador-phishing.git
   cd simulador-phishing
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No macOS/Linux
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicialize o banco de dados:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. Execute o aplicativo:
   ```bash
   python run.py
   ```

### Instalação a partir do executável

1. Baixe o executável mais recente da [página de releases](https://github.com/seu-usuario/simulador-phishing/releases)
2. Execute o arquivo:
   ```bash
   # No Windows
   simulador-phishing.exe
   
   # No macOS/Linux
   ./simulador-phishing
   ```

## 🚀 Uso

### Primeiros passos

1. Após iniciar o aplicativo, um navegador abrirá automaticamente com a página de login
2. Crie uma conta (o primeiro usuário registrado será automaticamente um administrador)
3. Faça login com suas credenciais

### Criando uma campanha

1. No dashboard, clique em "Nova Campanha"
2. Preencha o nome e a descrição da campanha
3. Adicione templates de e-mail:
   - Clique em "Adicionar Template"
   - Preencha o nome, assunto e corpo do e-mail
   - Indique os indicadores de phishing e o nível de dificuldade
4. Adicione alvos:
   - Clique em "Adicionar Alvo" para adicionar individualmente
   - Use "Importar CSV" para adicionar múltiplos alvos

### Enviando a campanha

1. Na página de detalhes da campanha, clique em "Enviar Campanha"
2. Selecione o template a ser usado
3. Configure as opções de SMTP:
   - Servidor, porta, usuário, senha
   - Nome e e-mail do remetente
4. Ative o "Modo de Simulação" para testar sem enviar e-mails reais
5. Clique em "Enviar Campanha"

### Analisando resultados

1. Acesse "Ver Resultados" na página da campanha
2. Visualize estatísticas gerais: taxa de abertura, cliques e reportes
3. Analise dados por departamento
4. Veja detalhes individuais de cada interação
5. Exporte os resultados em formato CSV

## 📦 Empacotamento

O aplicativo pode ser empacotado em um executável único para distribuição fácil:

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Execute o script de empacotamento:
   ```bash
   python build.py
   ```

3. O executável será gerado na pasta `dist/`

### Detalhes do empacotamento

O script `build.py` automatiza o processo de empacotamento:

- Verifica e cria as pastas necessárias (`templates`, `static`)
- Limpa arquivos de build anteriores
- Executa o PyInstaller com as configurações corretas
- Verifica se a build foi bem-sucedida

## 📁 Estrutura do Projeto

```
simulador-phishing/
├── app.py                 # Aplicação principal Flask
├── run.py                 # Script para executar a aplicação
├── build.py               # Script para empacotar a aplicação
├── requirements.txt       # Dependências do projeto
├── templates/             # Templates HTML
│   ├── base.html          # Layout base
│   ├── login.html         # Página de login
│   ├── dashboard.html     # Dashboard principal
│   ├── campaign_*.html    # Templates relacionados a campanhas
│   └── ...                # Outros templates
├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── img/
└── database.db            # Banco de dados SQLite
```

## 🔨 Solução de Problemas

### Problema com banco de dados

Se ocorrerem erros como `no such table: user` ou `no such column: email.delivery_status`:

1. **Recrie o banco de dados** (perderá dados existentes):
   ```bash
   rm database.db
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

2. **Ou faça uma migração manual** (preserva dados):
   ```bash
   sqlite3 database.db
   
   # Dentro do SQLite
   ALTER TABLE email ADD COLUMN delivery_status TEXT;
   ALTER TABLE email ADD COLUMN error_message TEXT;
   .exit
   ```

### Problemas com certificados SSL

Se ocorrerem erros como `CERTIFICATE_VERIFY_FAILED`:

1. **Desative temporariamente a verificação SSL** (apenas para desenvolvimento):
   ```python
   # No arquivo app.py, modifique a função send_email_with_tracking
   context = ssl.create_default_context()
   context.check_hostname = False
   context.verify_mode = ssl.CERT_NONE
   ```

2. **Ou instale os certificados adequados**:
   ```bash
   # macOS
   /Applications/Python\ 3.x/Install\ Certificates.command
   
   # Linux
   sudo apt-get update
   sudo apt-get install ca-certificates
   ```

### Problemas com PyInstaller

Se houver problemas ao empacotar ou executar o aplicativo empacotado:

1. **Verifique os recursos incluídos**:
   ```bash
   # Listar recursos incluídos
   pyi-archive_viewer dist/run
   ```

2. **Adicione recursos manualmente**:
   ```bash
   pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" run.py
   ```

3. **Consulte log para mais detalhes**:
   ```bash
   cat app.log
   ```

## 🔒 Considerações Éticas

Este software é projetado **apenas para fins educacionais**. Ao usá-lo, você concorda em:

- Obter **consentimento explícito** de todos os participantes
- Usar apenas em ambientes controlados e autorizados
- Não usar para phishing real ou atividades maliciosas
- Seguir políticas de sua organização e leis locais sobre testes de segurança

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

Criado com ❤️ para conscientização em segurança cibernética.