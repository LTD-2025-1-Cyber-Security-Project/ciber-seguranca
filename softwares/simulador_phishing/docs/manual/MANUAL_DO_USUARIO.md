# Manual do Usuário - Simulador de Phishing Educacional

## Índice
1. [Introdução](#introdução)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Dashboard](#dashboard)
4. [Gerenciamento de Campanhas](#gerenciamento-de-campanhas)
5. [Templates de E-mail](#templates-de-e-mail)
6. [Gerenciamento de Alvos](#gerenciamento-de-alvos)
7. [Envio de Campanhas](#envio-de-campanhas)
8. [Análise de Resultados](#análise-de-resultados)
9. [Módulo Educacional](#módulo-educacional)
10. [Configurações de SMTP](#configurações-de-smtp)
11. [Solução de Problemas](#solução-de-problemas)

## Introdução

O Simulador de Phishing Educacional é uma ferramenta projetada para ajudar organizações a treinar seus funcionários na identificação e prevenção de ataques de phishing. Com este sistema, você pode criar campanhas de phishing simuladas, enviar e-mails de teste e monitorar como os usuários interagem com esses e-mails.

## Acesso ao Sistema

### Primeiro Acesso

1. Execute o aplicativo (arquivo executável ou via comando `python run.py`)
2. Um navegador abrirá automaticamente com a página de login
3. Clique em "Registre-se" para criar uma nova conta
4. O primeiro usuário registrado será automaticamente um administrador

### Login
- Acesse o sistema usando suas credenciais (nome de usuário e senha)
- Caso esqueça sua senha, entre em contato com um administrador

## Dashboard

O dashboard é a tela inicial após o login e fornece uma visão geral das suas campanhas.

### Elementos do Dashboard
- **Estatísticas gerais**: Total de campanhas, campanhas ativas, taxas de detecção
- **Lista de campanhas**: Todas as suas campanhas com status e estatísticas básicas
- **Botão "Nova Campanha"**: Para iniciar a criação de uma nova campanha

## Gerenciamento de Campanhas

### Criar Nova Campanha
1. Clique no botão "Nova Campanha" no dashboard
2. Preencha o formulário com:
   - **Nome da Campanha**: Um identificador único
   - **Descrição**: Detalhes sobre o objetivo da campanha
3. Clique em "Criar Campanha"

### Detalhes da Campanha
Na página de detalhes da campanha, você pode:
- Visualizar informações gerais
- Gerenciar templates de e-mail
- Gerenciar lista de alvos
- Visualizar e-mails enviados
- Enviar a campanha
- Ver resultados

### Editar Campanha
1. Acesse a campanha no dashboard
2. Clique em "Editar Campanha"
3. Altere os campos desejados
4. Clique em "Atualizar Campanha"

### Excluir Campanha
1. Acesse a campanha no dashboard
2. Clique em "Excluir Campanha"
3. Confirme a exclusão

## Templates de E-mail

Os templates definem o conteúdo dos e-mails de phishing que serão enviados.

### Criar Novo Template
1. Na página de detalhes da campanha, clique em "Adicionar Template"
2. Preencha o formulário com:
   - **Nome do Template**: Um identificador único
   - **Assunto**: O assunto do e-mail
   - **Corpo do E-mail**: O conteúdo HTML do e-mail
   - **Indicadores de Phishing**: Lista de elementos que indicam que é phishing
   - **Dificuldade**: Nível de dificuldade para identificar (fácil, médio, difícil)
3. Clique em "Adicionar Template"

### Dicas para Criar Templates Eficazes
- Use `{nome}` para incluir o nome do alvo automaticamente
- Use `{email}` para incluir o e-mail do alvo
- Use `{departamento}` para incluir o departamento do alvo
- Inclua links para rastrear cliques
- Varie os níveis de dificuldade para testar diferentes cenários

### Editar Template
1. Na página de detalhes da campanha, localize o template
2. Clique em "Editar Template"
3. Altere os campos desejados
4. Clique em "Atualizar Template"

## Gerenciamento de Alvos

Os alvos são as pessoas que receberão os e-mails de phishing simulados.

### Adicionar Alvo Individual
1. Na página de detalhes da campanha, clique em "Adicionar Alvo"
2. Preencha o formulário com:
   - **Nome**: Nome completo do alvo
   - **E-mail**: Endereço de e-mail
   - **Departamento**: Departamento ou setor (opcional)
3. Clique em "Adicionar Alvo"

### Importação em Massa
1. Na página de detalhes da campanha, clique em "Importar CSV"
2. Prepare um arquivo CSV com o formato: `Nome,Email,Departamento`
3. Cole o conteúdo do CSV na área de texto
4. Clique em "Importar Alvos"

### Excluir Alvo
1. Na página de detalhes da campanha, localize o alvo
2. Clique em "Excluir Alvo"
3. Confirme a exclusão

## Envio de Campanhas

### Preparação para Envio
Antes de enviar uma campanha, certifique-se de que:
- Pelo menos um template de e-mail foi criado
- Pelo menos um alvo foi adicionado
- As configurações de SMTP estão corretas (se não estiver usando o modo de simulação)

### Enviar a Campanha
1. Na página de detalhes da campanha, clique em "Enviar Campanha"
2. Selecione o template de e-mail a ser usado
3. Configure as opções de SMTP:
   - **Servidor SMTP**: Endereço do servidor (ex: smtp.gmail.com)
   - **Porta SMTP**: Geralmente 587 para TLS ou 465 para SSL
   - **Usuário SMTP**: Seu endereço de e-mail
   - **Senha SMTP**: Senha do e-mail ou senha de aplicativo
   - **Nome do Remetente**: Nome que aparecerá como remetente
   - **E-mail do Remetente**: Endereço de e-mail do remetente
4. Opcionalmente, ative o "Modo de Simulação" para testar sem enviar e-mails reais
5. Clique em "Enviar Campanha"

### Modo de Simulação
- Quando ativado, os e-mails não são enviados realmente
- Os registros são criados no sistema para fins de teste
- Útil para verificar a configuração da campanha antes do envio real

## Análise de Resultados

### Ver Resultados
1. Na página de detalhes da campanha, clique em "Ver Resultados"
2. Ou clique no ícone de gráfico na lista de campanhas no dashboard

### Estatísticas Disponíveis
- **Estatísticas gerais**: Total de e-mails, abertos, clicados, reportados
- **Taxas**: Abertura, clique, reporte (em porcentagem)
- **Gráficos**: Visualização gráfica dos resultados
- **Timeline**: Evolução dos resultados ao longo do tempo
- **Detalhes por Alvo**: Quem abriu, clicou ou reportou
- **Análise por Departamento**: Desempenho por departamento

### Exportar Resultados
1. Na página de resultados, clique em "Exportar como CSV"
2. O arquivo será baixado automaticamente
3. Abra com Excel ou outro programa de planilhas para análise adicional

## Módulo Educacional

### Material Educativo
1. Acesse "Aprender" no menu lateral
2. Explore o material educativo sobre phishing:
   - O que é phishing
   - Como identificar phishing
   - Como se proteger
   - Exemplos de e-mails de phishing

### Quiz
1. Acesse "Aprender" no menu lateral
2. Clique em "Fazer Quiz"
3. Responda às perguntas sobre phishing
4. Veja sua pontuação e recomendações

## Configurações de SMTP

### Gmail
Para usar o Gmail como servidor SMTP:
1. Use `smtp.gmail.com` como servidor
2. Use a porta `587`
3. Ative a verificação em duas etapas na sua conta Google
4. Gere uma senha de aplicativo em [https://myaccount.google.com/security](https://myaccount.google.com/security)
5. Use essa senha de aplicativo em vez da sua senha normal

### Outlook/Office 365
Para usar o Outlook como servidor SMTP:
1. Use `smtp.office365.com` como servidor
2. Use a porta `587`
3. Use seu endereço de e-mail completo como usuário
4. Use sua senha normal

### Servidor SMTP Corporativo
Consulte seu departamento de TI para obter as configurações corretas.

## Solução de Problemas

### E-mails não são enviados
**Possíveis causas e soluções:**
1. **Configurações SMTP incorretas**: Verifique servidor, porta, usuário e senha
2. **Modo de simulação ativado**: Desative o modo de simulação
3. **Erro de certificado SSL**: Veja a seção sobre problemas SSL no README
4. **Bloqueio pelo provedor de e-mail**: Use senha de aplicativo ou servidor SMTP corporativo

### Erro "Template Not Found"
**Possíveis causas e soluções:**
1. **Executando a partir do executável**: Reinstale usando o script de build atualizado
2. **Problema de permissão**: Execute como administrador
3. **Arquivos corrompidos**: Baixe novamente o aplicativo

### Erro "No such table: user"
**Possíveis causas e soluções:**
1. **Banco de dados não inicializado**: Execute o script de inicialização
2. **Problema com o executável**: Use a versão mais recente com o banco de dados automático
3. **Diretório sem permissão de escrita**: Execute em um diretório com permissões adequadas

### Outras dúvidas
Consulte o arquivo README.md para informações adicionais ou entre em contato com o desenvolvedor.

---

Esperamos que este manual ajude você a utilizar o Simulador de Phishing Educacional com eficiência. Lembre-se de que esta ferramenta deve ser usada apenas para fins educacionais e com o consentimento de todos os participantes.