# CyberForce - Gerador de Senhas Avançado

![Versão](https://img.shields.io/badge/Versão-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)
![Licença](https://img.shields.io/badge/Licença-MIT-yellow)

Um gerador de senhas profissional e seguro baseado em Flask com uma interface futurista, alta entropia criptográfica e seguindo os padrões NIST SP 800-63B.

<div align="center">
  <img src="docs/screenshots/main-screen.png" alt="Tela principal do CyberForce" width="80%">
</div>

## 📋 Índice

- [Recursos](#-recursos)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação](#-instalação)
- [Execução](#-execução)
- [Empacotamento](#-empacotamento)
- [Guia de Segurança de Senhas](#-guia-de-segurança-de-senhas)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura e Design](#-arquitetura-e-design)
- [Conformidade e Segurança](#-conformidade-e-segurança)
- [Resolução de Problemas](#-resolução-de-problemas)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

## 🌟 Recursos

### Geração de Senhas
- Cria senhas aleatórias com comprimento configurável (8 a 64 caracteres)
- Permite selecionar tipos de caracteres (maiúsculas, minúsculas, números, especiais)
- Exclui caracteres semelhantes (i, l, 1, I, O, 0) e ambíguos ({}, [], (), /\)
- Gera frases-senha (passphrases) com palavras aleatórias
- Garante alta entropia criptográfica e aleatoriedade verdadeira
- Análise em tempo real da força da senha

### Interface do Usuário
- Design responsivo, moderno e futurista
- Modo claro/escuro com persistência de preferência
- Sistema de abas para organizar funcionalidades
- Armazenamento local de senhas salvas
- Tutorial interativo para novos usuários
- Indicador visual de força de senha e tempo estimado para quebrar

### Segurança
- Implementa padrões NIST SP 800-63B e ISO/IEC 27002:2022
- Geração de entropia usando o módulo `secrets` do Python
- Proteção contra ataques XSS e CSRF
- Cabeçalhos de segurança HTTP rigorosos
- Verificação de força de senha em tempo real

### Acessibilidade
- Compatível com WCAG 2.1 AA
- Suporte a leitores de tela (atributos ARIA)
- Modo de alto contraste automático
- Suporte a navegação por teclado
- Redução de animações para usuários com preferências de movimento reduzido

## 💻 Requisitos do Sistema

### Para Desenvolvimento
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Navegador moderno com suporte a JavaScript ES6
- 50MB de espaço em disco
- 512MB de RAM (mínimo)

### Para Execução como Aplicativo
- Windows 10/11, macOS 10.15+, ou Linux (Ubuntu 20.04+, Fedora 35+)
- 100MB de espaço em disco
- 256MB de RAM (mínimo)

## 🔧 Instalação

### Via Git (Desenvolvedores)

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/cyberforce-password-generator.git
   cd cyberforce-password-generator
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Via Download (Usuários)

1. Baixe o arquivo ZIP do [último lançamento](https://github.com/seu-usuario/cyberforce-password-generator/releases/latest)
2. Extraia o conteúdo em um diretório de sua preferência
3. Siga as instruções de execução abaixo

## 🚀 Execução

### Como Aplicação Web (Desenvolvimento)

1. Ative o ambiente virtual (caso ainda não esteja ativo):
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. Execute o aplicativo:
   ```bash
   python app.py
   ```

3. Acesse o aplicativo no navegador:
   ```
   http://127.0.0.1:5000
   ```

### Como Servidor de Produção

1. Instale o Gunicorn (Linux/macOS):
   ```bash
   pip install gunicorn
   ```

2. Execute com Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

   Para Windows, use waitress:
   ```bash
   pip install waitress
   waitress-serve --port=8000 app:app
   ```

3. Acesse o aplicativo:
   ```
   http://seu-ip:8000
   ```

## 📦 Empacotamento

### Windows Executável

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Crie o executável:
   ```bash
   pyinstaller --name CyberForcePasswordGen --icon=static/img/icon.ico --add-data "templates;templates" --add-data "static;static" --onefile --windowed app.py
   ```

3. O executável será criado na pasta `dist/`

### macOS Aplicativo

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Crie o aplicativo:
   ```bash
   pyinstaller --name "CyberForce Password Generator" --icon=static/img/icon.icns --add-data "templates:templates" --add-data "static:static" --onefile --windowed app.py
   ```

3. O aplicativo será criado na pasta `dist/`

### Linux AppImage

1. Instale as ferramentas necessárias:
   ```bash
   pip install pyinstaller
   sudo apt-get install fuse libfuse2 # Para Ubuntu/Debian
   ```

2. Crie o pacote do aplicativo:
   ```bash
   pyinstaller --name CyberForcePasswordGen --icon=static/img/icon.png --add-data "templates:templates" --add-data "static:static" --onefile --windowed app.py
   ```

3. Use o [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy) para criar o AppImage

### Docker

1. Construa a imagem:
   ```bash
   docker build -t cyberforce-password-generator .
   ```

2. Execute o contêiner:
   ```bash
   docker run -p 8000:5000 cyberforce-password-generator
   ```

3. Acesse: `http://localhost:8000`

## 🔐 Guia de Segurança de Senhas

### Melhores Práticas

1. **Comprimento Mínimo**: Senhas devem ter pelo menos 12 caracteres, idealmente 16+.
2. **Complexidade**: Use uma combinação de maiúsculas, minúsculas, números e caracteres especiais.
3. **Unicidade**: Nunca reutilize senhas entre serviços diferentes.
4. **Evite Informações Pessoais**: Não inclua nomes, datas de nascimento ou informações facilmente descobertas.
5. **Frases-Senha**: Considere usar frases-senha longas para maior segurança e facilidade de memorização.

### Força de Senha e Entropia

| Tipo de Senha | Exemplo | Entropia (bits) | Tempo para Quebrar* |
|---------------|---------|-----------------|---------------------|
| Fraca | senha123 | ~30 | Minutos |
| Média | S3nh@_2025 | ~50 | Semanas |
| Forte | 7Gx$tP9!aR#v2K | ~80 | Séculos |
| Muito Forte | correct-horse-battery-staple-9! | ~100+ | Milênios |

*Assumindo um ataque de força bruta a 10 bilhões de tentativas por segundo.

### Armazenamento Seguro

1. **Gerenciador de Senhas**: Use um gerenciador de senhas confiável para armazenar suas credenciais.
2. **2FA/MFA**: Sempre que possível, ative a autenticação de dois fatores.
3. **Atualizações Regulares**: Altere senhas críticas a cada 6-12 meses.
4. **Verificação de Vazamentos**: Verifique regularmente se suas senhas foram comprometidas em vazamentos de dados.

## 🛠️ Tecnologias Utilizadas

- **Backend**:
  - Python 3.8+
  - Flask 2.3+
  - Werkzeug
  - Módulo `secrets` para geração criptográfica

- **Frontend**:
  - HTML5, CSS3, JavaScript ES6+
  - Font Awesome (ícones)
  - LocalStorage API (armazenamento de senhas)
  - CSS Grid e Flexbox para layout responsivo

- **Segurança**:
  - Cabeçalhos HTTP de segurança
  - Sanitização de entradas
  - Proteção CSRF
  - Validações client e server-side

- **Empacotamento**:
  - PyInstaller
  - Docker
  - Gunicorn/Waitress para deploy

## 🏗️ Arquitetura e Design

### Estrutura de Diretórios

```
cyberforce-password-generator/
├── app.py                   # Aplicação principal Flask
├── Dockerfile               # Configuração para criação de contêiner
├── requirements.txt         # Dependências do projeto
├── static/                  # Recursos estáticos
│   ├── css/
│   │   └── styles.css       # Estilos da aplicação
│   ├── js/
│   │   └── script.js        # JavaScript para interatividade
│   └── img/                 # Imagens e ícones
├── templates/               # Templates HTML
│   └── index.html           # Interface principal
├── docs/                    # Documentação
│   └── screenshots/         # Capturas de tela
└── README.md                # Esta documentação
```

### Fluxo de Dados

1. O usuário configura os parâmetros de senha na interface.
2. A solicitação é enviada ao backend via requisição AJAX.
3. O backend gera a senha usando o módulo `secrets` do Python.
4. A senha é retornada ao frontend, onde é exibida e analisada.
5. O frontend calcula e exibe métricas de força e segurança.
6. O usuário pode salvar a senha no localStorage do navegador.

### Diagrama de Componentes

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|  Interface do     |     |  Backend Flask    |     |  Armazenamento    |
|  Usuário          |<--->|  (Geração de      |<--->|  Local            |
|  (HTML/CSS/JS)    |     |  Senha)           |     |  (LocalStorage)   |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +-------------------+
         ^
         |
         v
+-------------------+
|                   |
|  Análise de       |
|  Segurança        |
|  (Client-side)    |
|                   |
+-------------------+
```

## 🔒 Conformidade e Segurança

### Padrões Implementados

- **NIST SP 800-63B**: Diretrizes para autenticação digital e gerenciamento de ciclo de vida
- **ISO/IEC 27002:2022**: Código de prática para controles de segurança da informação
- **OWASP Top 10**: Proteção contra vulnerabilidades web comuns
- **WCAG 2.1 AA**: Diretrizes de acessibilidade para conteúdo web

### Medidas de Segurança

- Uso do módulo `secrets` para geração criptograficamente segura de valores aleatórios
- Implementação de Content Security Policy (CSP) para mitigar XSS
- Cabeçalhos HTTP de segurança como X-Content-Type-Options e X-Frame-Options
- Sanitização rigorosa de entradas para prevenir injeções
- Nenhum dado é transmitido pela rede ou armazenado em servidores externos

## ❓ Resolução de Problemas

### Problemas Comuns

| Problema | Solução |
|----------|---------|
| A aplicação não inicia | Verifique se todas as dependências estão instaladas: `pip install -r requirements.txt` |
| Erro "Address already in use" | Outra aplicação está usando a porta. Altere a porta em `app.py` |
| JavaScript não funciona | Verifique se está usando um navegador moderno com suporte a ES6 |
| Senhas não estão salvando | Verifique se o localStorage está habilitado no seu navegador |
| Interface com aparência quebrada | Limpe o cache do navegador e recarregue a página |

### Log de Depuração

Para ativar logs detalhados durante o desenvolvimento:

```python
# Modificar em app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

## 👥 Contribuindo

Adoraríamos sua contribuição para melhorar o CyberForce Password Generator! Aqui está como você pode ajudar:

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Faça commit das suas mudanças: `git commit -am 'Adiciona nova funcionalidade'`
4. Faça push para a branch: `git push origin feature/nova-funcionalidade`
5. Envie um Pull Request

### Diretrizes de Contribuição

- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Verifique se todos os testes passam antes de enviar o PR

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📬 Contato

- **Website**: [https://www.cyberforce-generator.com](https://www.cyberforce-generator.com)
- **Email**: contato@cyberforce-generator.com
- **GitHub**: [https://github.com/seu-usuario/cyberforce-password-generator](https://github.com/seu-usuario/cyberforce-password-generator)
- **Twitter**: [@CyberForceGen](https://twitter.com/CyberForceGen)

---

<div align="center">
  <p>
    <img src="docs/screenshots/logo-small.png" alt="CyberForce Logo" width="80px">
    <br>
    <b>CyberForce Password Generator</b> - Segurança digital ao seu alcance
    <br>
    Desenvolvido com 💙 por Sua Equipe
  </p>
</div>