# Resolução de Problemas com Certificados SSL

Se você está enfrentando erros relacionados à verificação de certificados SSL ao enviar e-mails, como:

```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

Você tem várias opções para resolver este problema:

## Opção 1: Atualizar a função de envio de e-mail (Solução Rápida)

A solução mais rápida é modificar a função `send_email_with_tracking` no arquivo `app.py` para desabilitar a verificação de certificado:

```python
# Configurar conexão SMTP com verificação de certificado desabilitada
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Desabilita verificação de certificado
```

**Observação**: Esta solução desabilita a verificação de segurança SSL, o que deve ser usado apenas em ambientes de desenvolvimento/testes. Em produção, a verificação de certificados SSL é uma importante camada de segurança.

## Opção 2: Instalar Certificados para Python (Solução Recomendada)

### macOS

O Python no macOS frequentemente tem problemas com certificados SSL. Você pode resolver isso executando:

```bash
# Se você usa Python 3 do python.org ou do Homebrew:
cd /Applications/Python\ 3.x/
./Install\ Certificates.command

# Ou, se estiver usando Homebrew:
/Applications/Python\ 3.x/Install\ Certificates.command
```

Para versões mais recentes do macOS:

```bash
# Instale o certificado do macOS para o Python
pip install certifi
python -m pip install --upgrade certifi
```

### Windows

No Windows, você pode precisar instalar os certificados manualmente:

```bash
pip install certifi
```

E depois adicionar o seguinte código antes de criar o contexto SSL:

```python
import certifi
context = ssl.create_default_context(cafile=certifi.where())
```

### Linux

No Linux, atualize os certificados do sistema:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ca-certificates

# CentOS/RHEL
sudo yum update ca-certificates
```

## Opção 3: Usar SMTP sem SSL para Testes

Para fins de desenvolvimento, você pode configurar o envio de e-mails sem SSL:

1. Use a porta 25 em vez de 587
2. Remova a chamada `server.starttls()`

**Observação**: Esta opção envia os e-mails sem criptografia, e deve ser usada APENAS em redes privadas para testes.

## Opção 4: Usar Serviços de E-mail Alternativos

Alguns serviços de e-mail são mais fáceis de configurar para desenvolvimento:

1. **Mailtrap.io**: Um serviço seguro para testes de e-mail
2. **Gmail com XOAUTH2**: Autenticação mais moderna e segura
3. **Serviços SMTP locais**: Como Mailhog

## Para Gmail Especificamente

Se você está usando Gmail, pode ser necessário:

1. Ativar "Acesso a app menos seguro" na sua conta Google (para contas pessoais, não disponível para contas Google Workspace)
2. Criar uma senha de aplicativo específica (recomendado):
   - Acesse: https://myaccount.google.com/security
   - Ative verificação em duas etapas
   - Acesse "Senhas de app"
   - Selecione "Outro (Nome personalizado)"
   - Use esta senha no lugar da sua senha normal