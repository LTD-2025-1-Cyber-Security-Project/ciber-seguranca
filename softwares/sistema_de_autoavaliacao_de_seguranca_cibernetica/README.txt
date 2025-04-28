# INSTRUÇÕES DE USO
# Sistema de Autoavaliação de Segurança Cibernética para Prefeituras
Versão 1.0.0

## INTRODUÇÃO

Este documento contém instruções básicas para instalação, configuração e utilização do Sistema de Autoavaliação de Segurança Cibernética para Prefeituras. O sistema foi desenvolvido para auxiliar administrações municipais a avaliar e melhorar suas práticas de segurança digital.

## REQUISITOS MÍNIMOS

### Hardware:
- Processador: Intel/AMD dual-core ou superior
- Memória RAM: 4GB (8GB recomendado para produção)
- Armazenamento: 10GB disponíveis (20GB para produção, SSD preferível)
- Conectividade: Acesso à internet

### Software:
- Sistema Operacional: Windows 10/11, macOS 10.14+ ou Linux (Ubuntu 20.04+ recomendado)
- Navegador atualizado (Chrome, Firefox, Edge ou Safari)

## INSTALAÇÃO RÁPIDA

### Para usuários finais (usando o executável):
1. Copie o arquivo "Cybersec-Prefeitura.exe" para o computador
2. Execute o arquivo com duplo clique
3. O navegador será aberto automaticamente com o sistema
4. Se solicitado pelo firewall, permita o acesso à rede
5. Faça login usando as credenciais fornecidas

### Para desenvolvedores (instalação manual):
1. Instale o Python 3.8+ em seu sistema
2. Clone ou baixe os arquivos do projeto
3. Crie um ambiente virtual:
   ```
   pip install virtualenv
   python -m virtualenv venv
   venv\Scripts\activate  (Windows)
   source venv/bin/activate  (Linux/macOS)
   ```
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
5. Configure o arquivo .env com suas variáveis de ambiente
6. Inicialize o banco de dados:
   ```
   python run.py
   ```

## INICIANDO O SISTEMA

1. Após a instalação, o sistema abrirá automaticamente no navegador
2. Acesse o endereço http://127.0.0.1:5000/ se não abrir automaticamente
3. Na tela de login, utilize as credenciais padrão:
   - Usuário: admin@prefeitura.gov.br
   - Senha: admin123
   - **IMPORTANTE**: Altere a senha padrão após o primeiro acesso

## PRIMEIROS PASSOS

1. **Criar perfil da prefeitura**:
   - Acesse o menu "Configurações" > "Perfil da Instituição"
   - Preencha os dados da prefeitura municipal
   - Salve as informações

2. **Configurar usuários**:
   - Acesse o menu "Administração" > "Usuários"
   - Adicione os usuários que terão acesso ao sistema
   - Atribua as permissões adequadas

3. **Iniciar avaliação**:
   - Acesse o menu "Avaliações" > "Nova Avaliação"
   - Selecione o questionário adequado ao seu contexto
   - Preencha as respostas com base na situação atual

4. **Gerar relatório**:
   - Após completar a avaliação, acesse "Relatórios" > "Gerar Relatório"
   - Selecione o tipo de relatório desejado
   - Visualize ou exporte o relatório em PDF

## FUNCIONALIDADES PRINCIPAIS

- **Dashboard**: Visão geral da situação de segurança da instituição
- **Avaliações**: Questionários para mensurar o nível de maturidade
- **Plano de Ação**: Ferramenta para criar e acompanhar ações corretivas
- **Relatórios**: Geração de relatórios detalhados e gráficos
- **Base de Conhecimento**: Recursos e recomendações de segurança
- **Administração**: Gerenciamento de usuários e configurações

## BACKUP DE DADOS

É altamente recomendável realizar backups regulares do banco de dados:

1. Para SQLite (ambiente de desenvolvimento):
   - Copie o arquivo .db da pasta do projeto
   
2. Para PostgreSQL (ambiente de produção):
   - Execute o script de backup fornecido:
     ```
     ./backup_db.sh
     ```
   - Verifique os backups na pasta /backup/cybersec

## SOLUÇÃO DE PROBLEMAS COMUNS

1. **Sistema não inicia**:
   - Verifique se todas as dependências estão instaladas
   - Confirme se o Python está no PATH do sistema
   - Verifique se o arquivo .env está configurado corretamente

2. **Erro de conexão ao banco de dados**:
   - Verifique se o banco de dados está em execução
   - Confirme as credenciais no arquivo .env
   - Verifique permissões de acesso

3. **Páginas não carregam corretamente**:
   - Limpe o cache do navegador
   - Verifique se os arquivos estáticos estão acessíveis
   - Confirme se não há bloqueios de firewall

4. **Erro ao gerar relatórios**:
   - Verifique se todos os dados necessários foram preenchidos
   - Confirme permissões do usuário

## SUPORTE TÉCNICO

Para obter suporte técnico, entre em contato:

- **Email**: suporte@cybersecprefeitura.gov.br
- **Telefone**: (XX) XXXX-XXXX
- **Portal**: https://suporte.cybersecprefeitura.gov.br
- **Horário**: Segunda a Sexta, 08:00 às 18:00

---

© 2025 Sistema de Autoavaliação de Segurança Cibernética para Prefeituras.
Todos os direitos reservados.

Última atualização: 26 de Abril de 2025