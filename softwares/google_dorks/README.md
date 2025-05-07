# DorkOptimizer - Sistema de Otimização de Buscas com Google Dorks

Um sistema web completo para otimização de buscas utilizando Google Dorks, especialmente desenvolvido para funcionários públicos e da administração municipal localizarem documentos e informações de forma eficiente.

## Funcionalidades Principais

- **Interface Intuitiva**: Recebe consultas de pesquisa longas do usuário em linguagem natural
- **Integração com IA**: Utiliza a API do Google Gemini para processar e otimizar consultas
- **Aplicação Automática de Dorks**: Transforma buscas comuns em consultas avançadas com operadores do Google
- **Personalização por Tipo de Arquivo**: Customiza dorks específicas baseadas no tipo de arquivo desejado
- **Seção Educativa**: Guia completo sobre o uso profissional e ético de Google Dorks
- **Exemplos por Departamento**: Casos de uso específicos para diferentes setores da administração pública

## Estrutura do Projeto

```
dorkoptimizer/
├── app.py                 # Aplicação Flask principal
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos CSS
│   ├── js/
│   │   └── main.js        # JavaScript principal
│   └── img/
│       └── search-illustration.svg  # Ilustração SVG
├── templates/             # Templates HTML
│   ├── base.html          # Template base (layout)
│   ├── home.html          # Página inicial
│   ├── search.html        # Ferramenta de busca
│   ├── guide.html         # Guia tutorial
│   ├── examples.html      # Exemplos de uso
│   ├── 404.html           # Página de erro 404
│   └── 500.html           # Página de erro 500
└── requirements.txt       # Dependências do projeto
```

## Requisitos do Sistema

- Python 3.8 ou superior
- Flask 2.0 ou superior
- Conexão com internet para acessar a API do Google Gemini

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/sua-organizacao/dorkoptimizer.git
   cd dorkoptimizer
   ```

2. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente (opcional, a chave da API já está no código):
   ```
   # Linux/Mac
   export GEMINI_API_KEY="AIzaSyCY5JQRIAZlq7Re-GNDtwn8b1Hmza_hk8Y"
   
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="AIzaSyCY5JQRIAZlq7Re-GNDtwn8b1Hmza_hk8Y"
   ```

5. Execute a aplicação:
   ```
   python app.py
   ```

6. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Criando o Arquivo de Dependências

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```
flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
```

## Considerações de Segurança

- O sistema inclui limitações para evitar abusos:
  - Restrição de tamanho das consultas
  - Tempo limite para respostas da API
  - Avisos sobre uso ético
  
- Recomendações para implantação em produção:
  - Adicione autenticação de usuários
  - Implemente HTTPS
  - Configure logs para auditoria
  - Adicione rate limiting para evitar sobrecarga

## Uso Ético

Este sistema foi desenvolvido para auxiliar funcionários públicos na localização de informações públicas de forma legítima. Não deve ser utilizado para:

- Explorar vulnerabilidades em sistemas
- Acessar informações confidenciais ou restritas
- Violar leis de privacidade ou proteção de dados
- Qualquer atividade ilegal ou antiética

## Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo LICENSE para mais detalhes.

## Contato

Para sugestões, dúvidas ou contribuições para o projeto, entre em contato pelo email: suporte@dorkoptimizer.gov.br