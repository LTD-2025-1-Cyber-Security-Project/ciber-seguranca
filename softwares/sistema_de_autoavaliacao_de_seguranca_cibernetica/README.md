# Sistema de Autoavaliação de Segurança Cibernética para Prefeituras

![Logo](https://via.placeholder.com/800x150?text=Sistema+de+Autoavalia%C3%A7%C3%A3o+de+Seguran%C3%A7a+Cibern%C3%A9tica)

**Versão 1.0.0**

## Visão Geral

O Sistema de Autoavaliação de Segurança Cibernética para Prefeituras é uma aplicação web desenvolvida para proporcionar às administrações municipais uma ferramenta robusta para avaliar, monitorar e aprimorar suas práticas de segurança digital. Desenvolvido em conformidade com as melhores práticas internacionais e adaptado às necessidades específicas das organizações governamentais brasileiras, este sistema oferece uma metodologia estruturada para identificar vulnerabilidades, avaliar riscos e implementar medidas corretivas.

## Índice

1. [Requisitos e Especificações Técnicas](#1-requisitos-e-especificações-técnicas)
2. [Guia de Instalação](#2-guia-de-instalação)
3. [Criação do Executável](#3-criação-do-executável)
4. [Implantação em Ambiente de Produção](#4-implantação-em-ambiente-de-produção)
5. [Segurança e Conformidade](#5-segurança-e-conformidade)
6. [Manutenção e Suporte](#6-manutenção-e-suporte)
7. [Solução de Problemas](#7-solução-de-problemas)
8. [Glossário de Termos](#8-glossário-de-termos)
9. [Apêndices](#9-apêndices)

---

## 1. Requisitos e Especificações Técnicas

### 1.1 Requisitos de Hardware

| Componente     | Desenvolvimento                 | Produção (Recomendado)         |
|----------------|--------------------------------|--------------------------------|
| Processador    | Intel/AMD dual-core ou superior | Intel/AMD quad-core ou superior |
| Memória RAM    | 4GB mínimo                     | 8GB ou superior                |
| Armazenamento  | 10GB disponíveis               | 20GB disponíveis SSD preferível |
| Rede           | Conectividade Internet padrão   | Largura de banda dedicada     |

### 1.2 Requisitos de Software

| Software                | Versão                               | Observações                           |
|-------------------------|------------------------------------|--------------------------------------|
| Sistema Operacional     | Linux (recomendado), Windows, macOS | Ubuntu Server 20.04 LTS (produção)    |
| Python                  | 3.8 ou superior                     | 3.10+ recomendado                     |
| SGBD                    | SQLite (dev), PostgreSQL (prod)     | PostgreSQL 14+ para produção          |
| Servidor Web (produção) | Nginx ou Apache                     | Nginx recomendado                     |
| SSL/TLS                 | Let's Encrypt                       | Obrigatório para produção             |

### 1.3 Dependências do Sistema

As principais bibliotecas e frameworks utilizados incluem:

- Flask (framework web)
- SQLAlchemy (ORM)
- Flask-Login (gerenciamento de autenticação)
- Flask-WTF (validação de formulários)
- Flask-Bcrypt (criptografia de senhas)
- Bootstrap 5 (framework CSS)
- Chart.js (visualização de dados)

---

## 2. Guia de Instalação

### 2.1 Preparação do Ambiente

#### 2.1.1 Ambiente Virtual Python

```bash
# Instalar virtualenv
pip install virtualenv

# Criar ambiente virtual
python -m virtualenv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

#### 2.1.2 Instalação das Dependências

```bash
# Instalar dependências do sistema
pip install -r requirements.txt
```

### 2.2 Configuração Inicial

#### 2.2.1 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```properties
# Aplicação
SECRET_KEY=use_uma_chave_segura_gerada_aleatoriamente
FLASK_APP=app.py
FLASK_ENV=production

# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost/cybersec_assessment

# Email (opcional)
MAIL_SERVER=smtp.exemplo.com.br
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu_email@exemplo.com.br
MAIL_PASSWORD=sua_senha_de_email
```

Para gerar uma chave secreta:

```python
# No terminal Python
import secrets
secrets.token_hex(32)
```

#### 2.2.2 Inicialização do Banco de Dados

Para inicializar o banco de dados, execute:

```bash
# Usando método simplificado
python run.py
```

O script automaticamente criará as tabelas necessárias e um usuário administrador.

### 2.3 Execução Manual do Sistema

Para executar o sistema em modo de desenvolvimento:

```bash
python run.py
```

O sistema estará disponível em `http://127.0.0.1:5000/` e abrirá automaticamente no navegador padrão.

---

## 3. Criação do Executável

Para distribuir o sistema como um arquivo executável independente, sem necessidade de instalação do Python ou outras dependências, siga as etapas abaixo:

### 3.1 Instalação do PyInstaller

```bash
pip install pyinstaller
```

### 3.2 Criação do Executável

#### 3.2.1 Para Windows

Note que o PyInstaller em diferentes versões pode ter sintaxe ligeiramente diferente. A sintaxe correta para adicionar dados é:

```bash
# Windows (usando ponto-e-vírgula como separador)
pyinstaller --name="Cybersec-Prefeitura" --icon=static/images/icon.ico --onefile --noconsole --add-data="static;static" --add-data="templates;templates" run.py
```

Se você ainda encontrar o erro de sintaxe, tente:

```bash
pyinstaller --name="Cybersec-Prefeitura" --icon=static/images/icon.ico --onefile --noconsole --add-data "static;static" --add-data "templates;templates" run.py
```

**Observação**: Certifique-se de que não há espaços entre `--add-data` e `=` ou entre `=` e o caminho especificado.

#### 3.2.2 Para Linux/macOS

```bash
# Linux/macOS (usando dois-pontos como separador)
pyinstaller --name="Cybersec-Prefeitura" --icon=static/images/icon.ico --onefile --add-data="static:static" --add-data="templates:templates" run.py
```

### 3.3 Adição de Metadados ao Executável

Para adicionar metadados (somente Windows), crie um arquivo chamado `version_info.txt`:

```
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Prefeitura Municipal'),
        StringStruct(u'FileDescription', u'Sistema de Autoavaliação de Segurança Cibernética'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'cybersec'),
        StringStruct(u'LegalCopyright', u'© 2025 Prefeitura Municipal'),
        StringStruct(u'OriginalFilename', u'Cybersec-Prefeitura.exe'),
        StringStruct(u'ProductName', u'Cybersec Assessment'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

E então execute o comando:

```bash
pyinstaller --name="Cybersec-Prefeitura" --icon=static/images/icon.ico --onefile --noconsole --add-data="static;static" --add-data="templates;templates" --version-file="version_info.txt" run.py
```

### 3.4 Estrutura do Executável

O executável será gerado na pasta `dist/` e conterá:
- Aplicação principal
- Interpretador Python embutido
- Todas as dependências necessárias
- Arquivos estáticos e templates

### 3.5 Solução de Problemas com PyInstaller

Se você continuar encontrando problemas com a sintaxe:

1. Verifique a versão do PyInstaller:
   ```bash
   pyinstaller --version
   ```

2. Consulte a documentação específica da sua versão:
   ```bash
   pyinstaller --help
   ```

3. Tente usando uma abordagem alternativa, com a sintaxe explícita:
   ```bash
   pyinstaller run.py --name="Cybersec-Prefeitura" --onefile --noconsole --add-data="templates;templates" --add-data="static;static"
   ```

4. Se o ícone estiver causando problemas, você pode omiti-lo inicialmente:
   ```bash
   pyinstaller --onefile --noconsole --add-data="static;static" --add-data="templates;templates" run.py
   ```

### 3.6 Distribuição do Executável

O executável resultante é um arquivo único que pode ser distribuído para qualquer computador com o mesmo sistema operacional. O usuário final não precisará ter o Python ou quaisquer dependências instaladas.

#### 3.6.1 Requisitos Mínimos para Execução

- Windows 10/11 (64-bit) ou
- macOS 10.14+ ou
- Ubuntu 20.04+/Debian 10+
- 4GB RAM
- 1GB de espaço em disco disponível

#### 3.6.2 Instruções para Usuário Final

1. Copie o arquivo executável para o computador de destino
2. Execute o arquivo (duplo clique)
3. O navegador padrão será aberto automaticamente
4. Se solicitado pelo firewall, permita o acesso à rede
5. Faça login usando as credenciais fornecidas

---

## 4. Implantação em Ambiente de Produção

### 4.1 Arquitetura de Implantação

Para ambientes de produção, recomenda-se a seguinte arquitetura:

```
Internet → Firewall → [Servidor Web (Nginx/Apache)] → [Aplicação (Gunicorn/uWSGI)] → [Banco de Dados]
```

### 4.2 Configuração do Servidor Nginx

#### 4.2.1 Instalação do Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install epel-release
sudo yum install nginx
```

#### 4.2.2 Configuração do Proxy Reverso

Crie um arquivo de configuração em `/etc/nginx/sites-available/cybersec-assessment`:

```nginx
server {
    listen 80;
    server_name cybersec.suaprefeitura.gov.br;

    # Redirecionar HTTP para HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cybersec.suaprefeitura.gov.br;

    # Certificados SSL
    ssl_certificate /etc/letsencrypt/live/cybersec.suaprefeitura.gov.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/cybersec.suaprefeitura.gov.br/privkey.pem;
    
    # Configurações de segurança SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Headers de segurança
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data:; font-src 'self' https://cdnjs.cloudflare.com; connect-src 'self';" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Configuração do proxy reverso
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Arquivos estáticos
    location /static {
        alias /caminho/para/cybersec-assessment/static;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # Configurações adicionais
    client_max_body_size 10M; # Limite para upload de arquivos
    
    access_log /var/log/nginx/cybersec-access.log;
    error_log /var/log/nginx/cybersec-error.log;
}
```

Ativar configuração e reiniciar Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/cybersec-assessment /etc/nginx/sites-enabled/
sudo nginx -t  # Testar configuração
sudo systemctl restart nginx
```

### 4.3 Configuração do SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d cybersec.suaprefeitura.gov.br
```

### 4.4 Criação do Serviço Systemd

Crie o arquivo `/etc/systemd/system/cybersec-assessment.service`:

```ini
[Unit]
Description=CyberSec Assessment Application
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/caminho/para/cybersec-assessment
ExecStart=/caminho/para/cybersec-assessment/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:application
Restart=always
RestartSec=5
Environment="PATH=/caminho/para/cybersec-assessment/venv/bin"
Environment="FLASK_ENV=production"
Environment="FLASK_APP=app.py"
Environment="PYTHONUNBUFFERED=1"
Environment="DATABASE_URL=postgresql://usuario:senha@localhost/cybersec_assessment"
Environment="SECRET_KEY=sua_chave_secreta"

[Install]
WantedBy=multi-user.target
```

Ative e inicie o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cybersec-assessment
sudo systemctl start cybersec-assessment
```

---

## 5. Segurança e Conformidade

### 5.1 Medidas de Segurança Implementadas

O sistema implementa as seguintes medidas de segurança:

- Autenticação multi-fator (opcional)
- Criptografia de senhas com bcrypt
- Proteção contra CSRF em formulários
- Validação de entrada de dados
- Sessões seguras com cookies httpOnly
- Configurações HTTPS com cabeçalhos de segurança
- Sanitização de dados de entrada
- Controle granular de permissões

### 5.2 Recomendações de Segurança Adicionais

Para maior segurança em ambiente de produção:

#### 5.2.1 Configuração de Firewall

```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

#### 5.2.2 Proteção contra Ataques de Força Bruta

Instale e configure o Fail2ban:

```bash
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Adicione ao arquivo:

```ini
[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 5
findtime = 300
bantime = 3600
```

Reinicie o serviço:

```bash
sudo systemctl restart fail2ban
```

### 5.3 Políticas de Backup

Implemente uma estratégia de backup abrangente:

#### 5.3.1 Backup Automatizado do Banco de Dados

Crie um script `backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/cybersec"
DATE=$(date +"%Y-%m-%d_%H-%M")
FILENAME="cybersec_db_backup_$DATE.sql"
ARCHIVE="cybersec_db_backup_$DATE.tar.gz"

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Backup do banco
PGPASSWORD=senha_database pg_dump -h localhost -U usuario_db -d nome_db > $BACKUP_DIR/$FILENAME

# Compressão
tar -czf $BACKUP_DIR/$ARCHIVE $BACKUP_DIR/$FILENAME
rm $BACKUP_DIR/$FILENAME

# Rotação (manter últimos 30 dias)
find $BACKUP_DIR -name "cybersec_db_backup_*.tar.gz" -type f -mtime +30 -delete
```

Adicione ao crontab:

```bash
# Executar às 01:00 da manhã
0 1 * * * /caminho/para/backup_db.sh
```

---

## 6. Manutenção e Suporte

### 6.1 Manutenção Regular

Procedimentos recomendados para manutenção regular:

| Atividade                         | Frequência       | Descrição                                       |
|-----------------------------------|------------------|------------------------------------------------|
| Atualização de dependências       | Mensal           | Atualizar bibliotecas para correções de segurança |
| Verificação de logs               | Semanal          | Revisar logs em busca de erros ou atividades suspeitas |
| Backup do banco de dados          | Diário           | Backup automatizado com verificação de integridade |
| Teste de restauração de backup    | Mensal           | Validar o processo de recuperação de dados |
| Análise de desempenho             | Mensal           | Monitorar uso de recursos e tempo de resposta |
| Verificação de segurança          | Trimestral       | Auditar configurações e permissões |

### 6.2 Atualização do Sistema

Para atualizar o sistema para uma nova versão:

1. Crie backup do banco de dados
2. Desligue o serviço: `sudo systemctl stop cybersec-assessment`
3. Backup dos arquivos atuais
4. Atualize os arquivos da aplicação:
   ```bash
   git pull # Se usando controle de versão
   # ou substitua manualmente os arquivos
   ```
5. Atualize dependências: `pip install -r requirements.txt`
6. Execute migração do banco de dados (se necessário): `flask db upgrade`
7. Reinicie o serviço: `sudo systemctl start cybersec-assessment`
8. Verifique logs para confirmar a inicialização sem erros

### 6.3 Monitoramento

Ferramentas recomendadas para monitoramento do sistema:

- **Prometheus + Grafana**: Monitoramento completo de infraestrutura
- **Sentry**: Rastreamento de erros em tempo real
- **ELK Stack**: Análise centralizada de logs
- **Netdata**: Monitoramento de recursos em tempo real

---

## 7. Solução de Problemas

### 7.1 Problemas Comuns e Soluções

| Problema                           | Possíveis Causas                      | Solução                                      |
|-----------------------------------|--------------------------------------|----------------------------------------------|
| Erro 500 ao acessar o sistema      | - Configuração incorreta do banco<br>- Erro na aplicação<br>- Permissões incorretas | - Verificar logs em `/var/log/nginx/cybersec-error.log`<br>- Verificar logs da aplicação<br>- Verificar permissões de arquivos |
| Sistema lento                      | - Recursos insuficientes<br>- Consultas ineficientes | - Aumentar recursos da VM<br>- Adicionar índices ao banco<br>- Otimizar consultas |
| Falha na autenticação              | - Credenciais incorretas<br>- Banco de dados corrompido | - Redefinir senha<br>- Restaurar backup do banco |
| Erro ao gerar relatórios           | - Dados inconsistentes<br>- Falta de permissões | - Verificar integridade dos dados<br>- Verificar permissões do usuário |
| Executável não inicia              | - Antivírus bloqueando<br>- Dependências faltantes | - Adicionar exceção no antivírus<br>- Verificar instalação do Visual C++ Redistributable (Windows) |

### 7.2 Logs do Sistema

Locais importantes para verificação de logs:

- **Logs da aplicação**: `/var/log/cybersec/app.log`
- **Logs do servidor web**: `/var/log/nginx/cybersec-access.log` e `/var/log/nginx/cybersec-error.log`
- **Logs do sistema operacional**: `/var/log/syslog` ou `/var/log/messages`
- **Logs do serviço**: `sudo journalctl -u cybersec-assessment`

---

## 8. Glossário de Termos

| Termo                     | Descrição                                                                                 |
|---------------------------|---------------------------------------------------------------------------------------------|
| CSRF                      | Cross-Site Request Forgery - Tipo de ataque que força um usuário a executar ações indesejadas |
| ORM                       | Object-Relational Mapping - Técnica de conversão entre sistemas de tipos incompatíveis       |
| Proxy Reverso             | Servidor que encaminha requisições para servidores de backend                               |
| SSL/TLS                   | Protocolos criptográficos que fornecem comunicações seguras pela Internet                     |
| Gunicorn                  | Servidor WSGI HTTP para Unix, usado para servir aplicações Python                            |
| Virtualenv                | Ferramenta para criar ambientes Python isolados                                            |
| WSGI                      | Web Server Gateway Interface - Especificação para interface entre servidores web e aplicações |
| Let's Encrypt             | Autoridade certificadora que fornece certificados X.509 gratuitos                           |
| Systemd                   | Sistema de gerenciamento de serviços para Linux                                             |

---

## 9. Apêndices

### 9.1 Checklist de Implantação

- [ ] Verificar todos os requisitos de hardware e software
- [ ] Instalar todas as dependências necessárias
- [ ] Configurar variáveis de ambiente
- [ ] Inicializar banco de dados
- [ ] Criar usuário administrador
- [ ] Configurar servidor web e SSL
- [ ] Configurar firewall e medidas de segurança
- [ ] Configurar backups automáticos
- [ ] Testar acesso ao sistema
- [ ] Validar todas as funcionalidades

### 9.2 Diagrama de Arquitetura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Usuários      │────▶│  Servidor Web   │────▶│  Aplicação      │
│   (Navegador)   │     │  (Nginx)        │     │  (Gunicorn)     │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                                               ┌─────────────────┐
                                               │                 │
                                               │  Banco de Dados │
                                               │  (PostgreSQL)   │
                                               │                 │
                                               └─────────────────┘
```

### 9.3 Informações de Contato para Suporte

Para suporte técnico, entre em contato:

- **Email**: suporte@cybersecprefeitura.gov.br
- **Telefone**: (XX) XXXX-XXXX
- **Portal de Suporte**: https://suporte.cybersecprefeitura.gov.br
- **Horário de Atendimento**: Segunda a Sexta, 08:00 às 18:00

---

© 2025 Sistema de Autoavaliação de Segurança Cibernética para Prefeituras. Todos os direitos reservados.

*Documento Produzido por: Equipe de Desenvolvimento de Sistemas*  
*Última Atualização: 24 de Abril de 2025*