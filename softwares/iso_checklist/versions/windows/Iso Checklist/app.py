from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime
import os

# Para o PyInstaller encontrar os arquivos quando empacotado
def resource_path(relative_path):
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = Flask(__name__)

# Create templates directory if it doesn't exist
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
# Checklist data structure
CHECKLIST_SECTIONS = [
    {
        "id": 1,
        "title": "Documentos e Dados Sensíveis",
        "items": [
            {"id": "1.1", "text": "Verificar ausência de documentos sensíveis em mesas de trabalho", "ref": "ISO 27002:2022 (7.7); LGPD Art. 6"},
            {"id": "1.2", "text": "Garantir armazenamento seguro de papéis sensíveis em gavetas trancadas", "ref": "ISO 27002:2022 (7.3)"},
            {"id": "1.3", "text": "Garantir destruição adequada de documentos físicos descartados (ex.: triturador)", "ref": "ISO 27002:2022 (8.10); LGPD Art. 46"},
            {"id": "1.4", "text": "Verificar ausência de documentos confidenciais em impressoras ou scanners", "ref": "ISO 27002:2022 (5.12)"},
            {"id": "1.5", "text": "Validar autorização antes de digitalizar documentos sensíveis", "ref": "ISO 27701:2019 (6.10.2.1); LGPD Art. 46"},
            {"id": "1.6", "text": "Confirmar que mídias removíveis não estão expostas em áreas de trabalho", "ref": "ISO 27002:2022 (7.10)"},
            {"id": "1.7", "text": "Conferir se documentos com dados pessoais estão devidamente rotulados", "ref": "ISO 27002:2022 (5.13)"},
            {"id": "1.8", "text": "Avaliar se não houve cópias indevidas de informações sensíveis", "ref": "ISO 27002:2022 (5.34); LGPD Art. 46"},
            {"id": "1.9", "text": "Garantir que documentos digitais estejam protegidos por senha ou criptografia", "ref": "ISO 27002:2022 (8.24); LGPD Art. 46"},
            {"id": "1.10", "text": "Verificar se documentos sensíveis estão armazenados em locais seguros (ex.: servidores autorizados)", "ref": "ISO 27002:2022 (7.3)"},
            {"id": "1.11", "text": "Evitar deixar documentos sensíveis em áreas comuns ou compartilhadas", "ref": "ISO 27002:2022 (7.7)"},
            {"id": "1.12", "text": "Garantir que documentos descartados sejam triturados ou incinerados", "ref": "ISO 27002:2022 (8.10); LGPD Art. 46"},
            {"id": "1.13", "text": "Verificar se pastas compartilhadas têm permissões de acesso restritas", "ref": "ISO 27002:2022 (8.3)"},
            {"id": "1.14", "text": "Garantir que documentos digitais sejam excluídos com segurança após uso (ex.: limpeza de lixeira)", "ref": "ISO 27002:2022 (8.10); LGPD Art. 46"},
            {"id": "1.15", "text": "Evitar impressão de documentos sensíveis sem necessidade justificada", "ref": "ISO 27002:2022 (7.9); LGPD Art. 46"},
            {"id": "1.16", "text": "Garantir que documentos sensíveis não sejam deixados em veículos ou locais externos", "ref": "ISO 27002:2022 (7.7)"},
            {"id": "1.17", "text": "Verificar se arquivos digitais sensíveis estão em pastas com controle de versão", "ref": "ISO 27002:2022 (8.10)"},
            {"id": "1.18", "text": "Evitar uso de impressoras compartilhadas para documentos sensíveis sem supervisão", "ref": "ISO 27002:2022 (7.9)"},
            {"id": "1.19", "text": "Garantir que documentos físicos sensíveis sejam transportados em envelopes lacrados", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "1.20", "text": "Conferir se há backups regulares de documentos digitais sensíveis", "ref": "ISO 27002:2022 (8.13)"}
        ]
    },
    {
        "id": 2,
        "title": "Segurança no Computador e Navegador",
        "items": [
            {"id": "2.1", "text": "Bloquear computador ao se ausentar (Windows+L ou equivalente)", "ref": "ISO 27002:2022 (7.7)"},
            {"id": "2.2", "text": "Verificar navegador atualizado (ex.: Chrome, Firefox, Edge)", "ref": "ISO 27002:2022 (8.8)"},
            {"id": "2.3", "text": "Confirmar ausência de software instalado sem aprovação do TI", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "2.4", "text": "Garantir não conexão de dispositivos pessoais ao computador corporativo", "ref": "ISO 27002:2022 (7.10)"},
            {"id": "2.5", "text": "Desativar cookies desnecessários no navegador", "ref": "ISO 27701:2019 (6.10.2.2); LGPD Art. 46"},
            {"id": "2.6", "text": "Verificar que senhas não estão salvas no navegador", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "2.7", "text": "Confirmar antivírus ativo e atualizado em todos os dispositivos", "ref": "ISO 27002:2022 (8.7)"},
            {"id": "2.8", "text": "Garantir não uso de dispositivos pessoais para atividades corporativas", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "2.9", "text": "Limpar arquivos temporários do computador regularmente", "ref": "ISO 27002:2022 (8.10)"},
            {"id": "2.10", "text": "Verificar ausência de TI sombra (aplicativos não autorizados)", "ref": "ISO 27002:2022 (5.23); LGPD Art. 46"},
            {"id": "2.11", "text": "Garantir que o sistema operacional esteja atualizado com os últimos patches", "ref": "ISO 27002:2022 (8.8)"},
            {"id": "2.12", "text": "Evitar uso de navegadores desatualizados ou não suportados (ex.: Internet Explorer antigo)", "ref": "ISO 27002:2022 (8.8)"},
            {"id": "2.13", "text": "Verificar se extensões do navegador são confiáveis e autorizadas", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "2.14", "text": "Garantir que o firewall do computador esteja ativo e configurado", "ref": "ISO 27002:2022 (8.20)"},
            {"id": "2.15", "text": "Evitar salvar arquivos corporativos em desktops ou locais não seguros", "ref": "ISO 27002:2022 (8.10); LGPD Art. 46"},
            {"id": "2.16", "text": "Garantir que atualizações de segurança sejam aplicadas em todos os aplicativos", "ref": "ISO 27002:2022 (8.8)"},
            {"id": "2.17", "text": "Evitar uso de sistemas operacionais não suportados (ex.: Windows XP)", "ref": "ISO 27002:2022 (8.8)"},
            {"id": "2.18", "text": "Verificar se há proteção contra ransomware ativa no antivírus", "ref": "ISO 27002:2022 (8.7)"},
            {"id": "2.19", "text": "Garantir que arquivos corporativos sejam salvos apenas em servidores seguros", "ref": "ISO 27002:2022 (8.10); LGPD Art. 46"},
            {"id": "2.20", "text": "Evitar uso de computadores compartilhados para acessar dados sensíveis", "ref": "ISO 27002:2022 (7.7); LGPD Art. 46"}
        ]
    },
    {
        "id": 3,
        "title": "E-mails e Comunicação Segura",
        "items": [
            {"id": "3.1", "text": "Evitar abertura de e-mails ou links suspeitos", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "3.2", "text": "Marcar e-mails sensíveis como confidenciais", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "3.3", "text": "Garantir envio de dados pessoais apenas com criptografia (ex.: e-mails seguros)", "ref": "ISO 27002:2022 (8.24)"},
            {"id": "3.4", "text": "Evitar compartilhar dados pessoais via WhatsApp ou telefone sem validação", "ref": "ISO 27002:2022 (5.34)"},
            {"id": "3.5", "text": "Usar apenas e-mail oficial para comunicações corporativas", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "3.6", "text": "Reportar e-mails de phishing ao setor de TI imediatamente", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "3.7", "text": "Evitar responder a solicitações de dados pessoais não verificadas", "ref": "ISO 27701:2019 (6.3.2.2)"},
            {"id": "3.8", "text": "Verificar remetentes antes de abrir anexos em e-mails", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "3.9", "text": "Garantir não uso de aplicativos de mensagens não autorizados para comunicações corporativas", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "3.10", "text": "Evitar responder a mensagens solicitando pagamentos via Pix sem validação", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "3.11", "text": "Garantir que e-mails com dados sensíveis sejam excluídos após uso", "ref": "ISO 27002:2022 (8.10)"},
            {"id": "3.12", "text": "Verificar se comunicações via videoconferência são seguras (ex.: Zoom, Teams)", "ref": "ISO 27002:2022 (6.7)"},
            {"id": "3.13", "text": "Evitar compartilhar tela com informações sensíveis em videoconferências", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "3.14", "text": "Garantir que mensagens corporativas não sejam encaminhadas para terceiros", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "3.15", "text": "Evitar uso de e-mails pessoais para comunicações relacionadas ao trabalho", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "3.16", "text": "Garantir que videoconferências usem senhas e salas de espera", "ref": "ISO 27002:2022 (6.7)"},
            {"id": "3.17", "text": "Evitar envio de dados sensíveis em e-mails sem autenticação do destinatário", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "3.18", "text": "Verificar se e-mails de trabalho não estão sendo sincronizados em dispositivos pessoais", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "3.19", "text": "Garantir que mensagens de texto (SMS) corporativas sejam criptografadas", "ref": "ISO 27002:2022 (8.24)"},
            {"id": "3.20", "text": "Evitar uso de plataformas de mensagens públicas para assuntos corporativos", "ref": "ISO 27002:2022 (5.10); LGPD Art. 46"}
        ]
    },
    {
        "id": 4,
        "title": "Senhas e Acessos",
        "items": [
            {"id": "4.1", "text": "Confirmar senha forte (mínimo 12 caracteres, com letras, números e símbolos)", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.2", "text": "Garantir que senhas não foram compartilhadas com colegas ou terceiros", "ref": "ISO 27002:2022 (6.3)"},
            {"id": "4.3", "text": "Trocar senha se não alterada nos últimos 3 meses", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.4", "text": "Acessar apenas sistemas autorizados para suas funções específicas", "ref": "ISO 27002:2022 (8.3)"},
            {"id": "4.5", "text": "Utilizar autenticação multifator (MFA) em todos os sistemas disponíveis", "ref": "ISO 27002:2022 (8.5)"},
            {"id": "4.6", "text": "Evitar uso de Wi-Fi público para acesso a sistemas corporativos", "ref": "ISO 27017:2015 (5.1.1)"},
            {"id": "4.7", "text": "Verificar ausência de senhas anotadas em locais visíveis (ex.: post-its)", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.8", "text": "Reportar tentativas de login suspeitas ao setor de TI", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "4.9", "text": "Garantir que senhas não sejam reutilizadas em diferentes sistemas", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.10", "text": "Evitar salvar senhas em aplicativos ou documentos desprotegidos", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.11", "text": "Verificar se contas inativas foram desativadas pelo setor de TI", "ref": "ISO 27002:2022 (5.18)"},
            {"id": "4.12", "text": "Garantir que sessões sejam encerradas ao final do expediente", "ref": "ISO 27002:2022 (8.5)"},
            {"id": "4.13", "text": "Evitar usar senhas padrão ou fáceis (ex.: '123456', 'senha')", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.14", "text": "Garantir que senhas sejam alteradas após suspeita de comprometimento", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.15", "text": "Verificar se permissões de acesso foram revisadas pelo TI recentemente", "ref": "ISO 27002:2022 (5.18)"},
            {"id": "4.16", "text": "Garantir que senhas sejam alteradas após uso temporário (ex.: acesso emergencial)", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.17", "text": "Evitar uso de senhas em dispositivos compartilhados sem logout", "ref": "ISO 27002:2022 (8.5)"},
            {"id": "4.18", "text": "Verificar se há políticas de expiração de sessão em sistemas corporativos", "ref": "ISO 27002:2022 (8.5)"},
            {"id": "4.19", "text": "Garantir que senhas não sejam enviadas por e-mail ou mensagens", "ref": "ISO 27002:2022 (5.17)"},
            {"id": "4.20", "text": "Evitar uso de senhas padrão fornecidas por fornecedores ou sistemas", "ref": "ISO 27002:2022 (5.17)"}
        ]
    },
    {
        "id": 5,
        "title": "Conformidade LGPD e Prevenção",
        "items": [
            {"id": "5.1", "text": "Garantir coleta de dados pessoais com consentimento explícito", "ref": "ISO 27701:2019 (6.2.2.1); LGPD Art. 7"},
            {"id": "5.2", "text": "Reportar solicitações de titulares (ex.: exclusão de dados) ao DPO", "ref": "ISO 27701:2019 (6.3.2.2); LGPD Art. 18"},
            {"id": "5.3", "text": "Evitar acesso a redes sociais no ambiente de trabalho", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "5.4", "text": "Orientar colegas sobre boas práticas de proteção de dados", "ref": "ISO 27002:2022 (6.3)"},
            {"id": "5.5", "text": "Ler e seguir a política de segurança da organização", "ref": "ISO 27002:2022 (5.1)"},
            {"id": "5.6", "text": "Reportar incidentes (ex.: perda de dados) ao gestor ou TI", "ref": "ISO 27002:2022 (6.8); LGPD Art. 48"},
            {"id": "5.7", "text": "Evitar uso de serviços de nuvem pessoais para dados corporativos", "ref": "ISO 27017:2015 (5.1.1); LGPD Art. 46"},
            {"id": "5.8", "text": "Verificar proteção de dados em contratos com fornecedores", "ref": "ISO 27036:2013 (4.2.2); LGPD Art. 39"},
            {"id": "5.9", "text": "Garantir não uso de ferramentas não autorizadas no trabalho", "ref": "ISO 27002:2022 (5.23); LGPD Art. 46"},
            {"id": "5.10", "text": "Confirmar participação no último treinamento de segurança", "ref": "ISO 27002:2022 (6.3)"},
            {"id": "5.11", "text": "Garantir que dados pessoais coletados sejam mínimos (princípio da necessidade)", "ref": "ISO 27701:2019 (6.2.2.1); LGPD Art. 6"},
            {"id": "5.12", "text": "Verificar se há registros de acessos a dados sensíveis (logs)", "ref": "ISO 27002:2022 (8.15); LGPD Art. 48"},
            {"id": "5.13", "text": "Evitar compartilhar dados pessoais em grupos de mensagens", "ref": "ISO 27002:2022 (5.14); LGPD Art. 46"},
            {"id": "5.14", "text": "Garantir que backups de dados sensíveis sejam armazenados com segurança", "ref": "ISO 27002:2022 (8.13); LGPD Art. 46"},
            {"id": "5.15", "text": "Reportar qualquer acesso não autorizado a dados pessoais ao DPO", "ref": "ISO 27002:2022 (6.8); LGPD Art. 48"},
            {"id": "5.16", "text": "Garantir que dados pessoais sejam tratados apenas para finalidades específicas", "ref": "LGPD Art. 6"},
            {"id": "5.17", "text": "Verificar se há plano de resposta a incidentes de segurança ativo", "ref": "ISO 27002:2022 (6.8); LGPD Art. 48"},
            {"id": "5.18", "text": "Evitar armazenamento de dados pessoais além do prazo necessário", "ref": "LGPD Art. 16"},
            {"id": "5.19", "text": "Garantir que dados pessoais não sejam usados para fins discriminatórios", "ref": "LGPD Art. 6"},
            {"id": "5.20", "text": "Verificar se há políticas de retenção e descarte de dados implementadas", "ref": "ISO 27002:2022 (8.10); LGPD Art. 46"}
        ]
    },
    {
        "id": 6,
        "title": "Proteção contra Ameaças e Práticas de Home Office",
        "items": [
            {"id": "6.1", "text": "Evitar responder a mensagens de redes sociais que solicitem dados pessoais", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "6.2", "text": "Reportar mensagens suspeitas de golpes via Pix ao setor de TI", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "6.3", "text": "Garantir uso de VPN em conexões remotas (ex.: home office)", "ref": "ISO 27002:2022 (6.7)"},
            {"id": "6.4", "text": "Evitar uso de dispositivos pessoais não autorizados em home office", "ref": "ISO 27002:2022 (6.7); LGPD Art. 46"},
            {"id": "6.5", "text": "Verificar segurança de impressoras e scanners usados em home office", "ref": "ISO 27002:2022 (7.9)"},
            {"id": "6.6", "text": "Garantir que reuniões virtuais não sejam gravadas sem autorização", "ref": "ISO 27002:2022 (5.14); LGPD Art. 46"},
            {"id": "6.7", "text": "Evitar compartilhar tela com informações sensíveis em videoconferências", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "6.8", "text": "Garantir que dispositivos usados em casa tenham antivírus ativo", "ref": "ISO 27002:2022 (8.7)"},
            {"id": "6.9", "text": "Evitar abrir links ou QR Codes suspeitos em mensagens pessoais", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "6.10", "text": "Reportar qualquer incidente de segurança ocorrido em home office", "ref": "ISO 27002:2022 (6.8); LGPD Art. 48"},
            {"id": "6.11", "text": "Garantir que impressoras domésticas não armazenem dados sensíveis", "ref": "ISO 27002:2022 (7.9)"},
            {"id": "6.12", "text": "Evitar uso de redes Wi-Fi abertas ou públicas em deslocamentos", "ref": "ISO 27017:2015 (5.1.1); LGPD Art. 46"},
            {"id": "6.13", "text": "Garantir que dispositivos pessoais usados em casa estejam protegidos por senha", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "6.14", "text": "Evitar deixar dispositivos desbloqueados em casa durante o trabalho remoto", "ref": "ISO 27002:2022 (6.7)"},
            {"id": "6.15", "text": "Verificar se o roteador doméstico tem senha forte e criptografia WPA3", "ref": "ISO 27002:2022 (8.20)"},
            {"id": "6.16", "text": "Garantir que dispositivos usados em casa não sejam compartilhados com terceiros", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "6.17", "text": "Evitar uso de dispositivos corporativos em redes domésticas não seguras", "ref": "ISO 27002:2022 (6.7); LGPD Art. 46"},
            {"id": "6.18", "text": "Verificar se há atualizações de segurança no roteador doméstico", "ref": "ISO 27002:2022 (8.20)"},
            {"id": "6.19", "text": "Garantir que documentos impressos em casa sejam armazenados com segurança", "ref": "ISO 27002:2022 (7.9); LGPD Art. 46"},
            {"id": "6.20", "text": "Evitar uso de aplicativos de videoconferência não autorizados", "ref": "ISO 27002:2022 (5.10); LGPD Art. 46"}
        ]
    },
    {
        "id": 7,
        "title": "Conscientização e Boas Práticas",
        "items": [
            {"id": "7.1", "text": "Evitar clicar em links de promoções ou descontos suspeitos", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "7.2", "text": "Reportar mensagens de engenharia social (ex.: falsas promoções) ao TI", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "7.3", "text": "Garantir que dispositivos móveis usados no trabalho tenham bloqueio de tela", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "7.4", "text": "Evitar uso de aplicativos de mensagens para enviar dados sensíveis", "ref": "ISO 27002:2022 (5.14); LGPD Art. 46"},
            {"id": "7.5", "text": "Verificar se backups corporativos são feitos regularmente pelo TI", "ref": "ISO 27002:2022 (8.13)"},
            {"id": "7.6", "text": "Garantir que dispositivos pessoais não sejam usados em redes corporativas", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "7.7", "text": "Evitar baixar aplicativos não confiáveis em dispositivos corporativos", "ref": "ISO 27002:2022 (5.10)"},
            {"id": "7.8", "text": "Participar de treinamentos de segurança da informação sempre que oferecidos", "ref": "ISO 27002:2022 (6.3)"},
            {"id": "7.9", "text": "Garantir que dados pessoais tratados sejam anonimizados quando possível", "ref": "ISO 27701:2019 (6.11); LGPD Art. 13"},
            {"id": "7.10", "text": "Evitar uso de dispositivos USB pessoais para transferir dados corporativos", "ref": "ISO 27002:2022 (7.10); LGPD Art. 46"},
            {"id": "7.11", "text": "Verificar se há atualizações de segurança em aplicativos corporativos", "ref": "ISO 27002:2022 (8.8)"},
            {"id": "7.12", "text": "Garantir que informações sensíveis não sejam exibidas em monitores visíveis", "ref": "ISO 27002:2022 (7.7)"},
            {"id": "7.13", "text": "Evitar discutir informações sensíveis em locais públicos (ex.: cafés)", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "7.14", "text": "Garantir que dispositivos corporativos não sejam usados por terceiros", "ref": "ISO 27002:2022 (8.1); LGPD Art. 46"},
            {"id": "7.15", "text": "Reportar qualquer comportamento suspeito de colegas ao gestor ou TI", "ref": "ISO 27002:2022 (6.8)"}
        ]
    },
    {
        "id": 8,
        "title": "Gestão de Incidentes e Resposta",
        "items": [
            {"id": "8.1", "text": "Garantir que incidentes de segurança sejam documentados detalhadamente", "ref": "ISO 27002:2022 (6.8); LGPD Art. 48"},
            {"id": "8.2", "text": "Verificar se há um plano de resposta a incidentes ativo e atualizado", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "8.3", "text": "Evitar divulgar detalhes de incidentes de segurança a terceiros não autorizados", "ref": "ISO 27002:2022 (5.14); LGPD Art. 48"},
            {"id": "8.4", "text": "Garantir que incidentes de vazamento de dados sejam reportados em até 72 horas", "ref": "LGPD Art. 48"},
            {"id": "8.5", "text": "Verificar se há backups recentes para recuperação após incidentes", "ref": "ISO 27002:2022 (8.13)"},
            {"id": "8.6", "text": "Evitar uso de dispositivos comprometidos até avaliação pelo TI", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "8.7", "text": "Garantir que incidentes sejam analisados para prevenir reincidências", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "8.8", "text": "Verificar se há um canal oficial para reportar incidentes de segurança", "ref": "ISO 27002:2022 (6.8)"},
            {"id": "8.9", "text": "Evitar compartilhar informações de incidentes em redes sociais", "ref": "ISO 27002:2022 (5.14)"},
            {"id": "8.10", "text": "Garantir que medidas corretivas sejam implementadas após incidentes", "ref": "ISO 27002:2022 (6.8)"}
        ]
    }
]


# # Helper functions for loading and saving checklist data
def load_or_create_checklist():
    if os.path.exists('checklist_data.json'):
        try:
            with open('checklist_data.json', 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Create a new checklist
    checklist_data = {}
    for section in CHECKLIST_SECTIONS:
        for item in section['items']:
            checklist_data[item['id']] = False
    
    return checklist_data

def save_checklist(checklist_data):
    with open('checklist_data.json', 'w') as f:
        json.dump(checklist_data, f)

# Create home page with introduction and principles
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Checklist de Segurança da Informação</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
            }
            .header {
                background-color: #0a2c5c;
                color: white;
                padding: 30px 0;
                margin-bottom: 30px;
                text-align: center;
            }
            .card {
                margin-bottom: 25px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .card-header {
                background-color: #0a2c5c;
                color: white;
                font-weight: bold;
            }
            .principle-icon {
                font-size: 2rem;
                margin-bottom: 15px;
                color: #0a2c5c;
            }
            .btn-primary {
                background-color: #0a2c5c;
                border-color: #0a2c5c;
            }
            .btn-primary:hover {
                background-color: #06193a;
                border-color: #06193a;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>Checklist Mensal de Segurança da Informação</h1>
                <p class="lead">Protegendo Dados, Preservando Futuros</p>
            </div>
        </div>
        
        <div class="container">
            <div class="row mb-5">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">Introdução</div>
                        <div class="card-body">
                            <p>Este documento é um farol de proteção no oceano digital, projetado para servidores públicos e funcionários internos que navegam pelas águas turbulentas da segurança da informação no Brasil. Ele guia, protege e assegura a conformidade com as normas mais elevadas, transformando cada verificação mensal em um ato de responsabilidade e cuidado. Ao seguir este checklist, você não apenas protege dados sensíveis, mas também constrói um futuro onde a privacidade é um direito inalienável.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-5">
                <div class="col-md-6">
                    <div class="card h-100">
                        <div class="card-header">Dados do Documento</div>
                        <div class="card-body">
                            <table class="table table-striped">
                                <tr>
                                    <th>Objetivo:</th>
                                    <td>Proteger dados sensíveis e assegurar conformidade com normas de segurança da informação, promovendo verificações mensais que mitiguem riscos e fortaleçam a cultura de proteção de dados no Brasil.</td>
                                </tr>
                                <tr>
                                    <th>Escopo:</th>
                                    <td>Abrange atividades de segurança da informação realizadas por servidores públicos e funcionários internos, incluindo manuseio de dados sensíveis, uso de dispositivos, comunicação segura, práticas de home office, prevenção contra ameaças digitais comuns no contexto brasileiro e conscientização para um futuro digital seguro.</td>
                                </tr>
                                <tr>
                                    <th>Base normativa:</th>
                                    <td>ISO/IEC 27001:2022, 27002:2022, 27005:2019, 27017:2015, 27701:2019, 27036:2013, 27018:2019, LGPD</td>
                                </tr>
                                <tr>
                                    <th>Última atualização:</th>
                                    <td>20/04/2025 por Vagner Cordeiro</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card h-100">
                        <div class="card-header">Princípios Fundamentais de Segurança da Informação</div>
                        <div class="card-body">
                            <div class="row text-center">
                                <div class="col-md-4 mb-3">
                                    <div class="principle-icon">
                                        <i class="fas fa-lock"></i>
                                    </div>
                                    <h5>Confidencialidade</h5>
                                    <p>Um escudo invisível que garante que apenas os autorizados acessem o tesouro das informações sensíveis.</p>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="principle-icon">
                                        <i class="fas fa-shield-alt"></i>
                                    </div>
                                    <h5>Integridade</h5>
                                    <p>A promessa de que os dados permanecerão puros e verdadeiros, imunes a mãos não autorizadas.</p>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="principle-icon">
                                        <i class="fas fa-server"></i>
                                    </div>
                                    <h5>Disponibilidade</h5>
                                    <p>A certeza de que os sistemas estarão sempre ao alcance, prontos para servir quando o dever chamar.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-5">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">Quadro de Conformidade LGPD: Pilares para um Futuro Seguro</div>
                        <div class="card-body">
                            <table class="table table-bordered">
                                <thead class="table-light">
                                    <tr>
                                        <th>Pilar</th>
                                        <th>Descrição</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Transparência</td>
                                        <td>Garantir clareza no uso e tratamento de dados pessoais, promovendo confiança e ética.</td>
                                    </tr>
                                    <tr>
                                        <td>Segurança</td>
                                        <td>Implementar medidas técnicas robustas para proteger dados contra vazamentos e ataques.</td>
                                    </tr>
                                    <tr>
                                        <td>Responsabilização</td>
                                        <td>Demonstrar conformidade com a LGPD através de registros e auditorias, assegurando compromisso.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-5">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">Instruções de Preenchimento</div>
                        <div class="card-body">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">Realizar a verificação no primeiro dia útil de cada mês, com diligência e atenção.</li>
                                <li class="list-group-item">Marcar com um [X] os itens verificados, selando a conformidade com responsabilidade.</li>
                                <li class="list-group-item">Reportar irregularidades ao setor de TI ou ao DPO imediatamente, protegendo o coletivo.</li>
                                <li class="list-group-item">Arquivar este documento para eventual auditoria ou conformidade legal, como um registro de compromisso.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="d-flex justify-content-center mb-5">
                <a href="/checklist" class="btn btn-primary btn-lg px-5 py-3">Iniciar Verificação</a>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    </body>
    </html>
    '''

@app.route('/checklist')
def checklist():
    checklist_data = load_or_create_checklist()
    
    # Count items
    total_items = 0
    checked_items = 0
    for section in CHECKLIST_SECTIONS:
        for item in section['items']:
            total_items += 1
            if checklist_data.get(item['id'], False):
                checked_items += 1
    
    # Calculate percentage
    percentage = round((checked_items / total_items) * 100) if total_items > 0 else 0
    
    # Create HTML content
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Checklist de Segurança da Informação</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                padding-bottom: 70px; /* Space for fixed bottom bar */
            }
            .header {
                background-color: #0a2c5c;
                color: white;
                padding: 20px 0;
                margin-bottom: 30px;
                text-align: center;
            }
            .item-ref {
                font-size: 0.8em;
                color: #6c757d;
            }
            .card {
                margin-bottom: 25px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .accordion-button:not(.collapsed) {
                background-color: #e7f1ff;
                color: #0a2c5c;
            }
            .fixed-bottom-bar {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: white;
                border-top: 1px solid #dee2e6;
                padding: 10px 0;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            }
            .btn-primary {
                background-color: #0a2c5c;
                border-color: #0a2c5c;
            }
            .btn-primary:hover {
                background-color: #06193a;
                border-color: #06193a;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>Checklist Mensal de Segurança da Informação</h1>
                <p class="lead">Protegendo Dados, Preservando Futuros</p>
            </div>
        </div>
        
        <div class="container">
            <div class="row mb-4">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-body">
                            <h4>Progresso da Verificação</h4>
                            <div class="progress mt-3" style="height: 25px;">
                                <div class="progress-bar bg-success" role="progressbar" style="width: ''' + str(percentage) + '''%;" 
                                    aria-valuenow="''' + str(percentage) + '''" aria-valuemin="0" aria-valuemax="100">
                                    ''' + str(percentage) + '''% (''' + str(checked_items) + '''/''' + str(total_items) + ''')
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    '''
    
    # Add accordion for sections
    html += '''
            <div class="accordion" id="checklistAccordion">
    '''
    
    for section in CHECKLIST_SECTIONS:
        html += '''
                <div class="accordion-item">
                    <h2 class="accordion-header" id="heading''' + str(section['id']) + '''">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse" 
                               data-bs-target="#collapse''' + str(section['id']) + '''" aria-expanded="true" 
                               aria-controls="collapse''' + str(section['id']) + '''">
                            <i class="fas fa-lock me-2"></i> ''' + str(section['id']) + '''. ''' + section['title'] + '''
                        </button>
                    </h2>
                    <div id="collapse''' + str(section['id']) + '''" class="accordion-collapse collapse show" 
                         aria-labelledby="heading''' + str(section['id']) + '''" data-bs-parent="#checklistAccordion">
                        <div class="accordion-body">
                            <div class="list-group list-group-flush">
        '''
        
        for item in section['items']:
            is_checked = checklist_data.get(item['id'], False)
            html += '''
                                <div class="list-group-item">
                                    <div class="form-check">
                                        <input class="form-check-input item-checkbox" type="checkbox" id="''' + item['id'] + '''" 
                                              data-item-id="''' + item['id'] + '''" ''' + (' checked' if is_checked else '') + '''>
                                        <label class="form-check-label" for="''' + item['id'] + '''">
                                            ''' + item['text'] + '''
                                            <div class="item-ref">''' + item['ref'] + '''</div>
                                        </label>
                                    </div>
                                </div>
            '''
        
        html += '''
                            </div>
                        </div>
                    </div>
                </div>
        '''
    
    html += '''
            </div>
        </div>
        
        <div class="fixed-bottom-bar">
            <div class="container">
                <div class="row">
                    <div class="col-md-6 text-center text-md-start">
                        <a href="/report" class="btn btn-primary">Gerar Relatório</a>
                        <button id="resetBtn" class="btn btn-danger">Resetar Checklist</button>
                    </div>
                    <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
                        <div class="text-muted">
                            Progresso: ''' + str(percentage) + '''% (''' + str(checked_items) + '''/''' + str(total_items) + ''')
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
        <script>
            $(document).ready(function() {
                // Handle checkbox change
                $('.item-checkbox').change(function() {
                    const itemId = $(this).data('item-id');
                    const isChecked = $(this).prop('checked');
                    
                    // Send update to server
                    $.ajax({
                        url: '/api/update_item',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({
                            id: itemId,
                            checked: isChecked
                        }),
                        success: function(response) {
                            // Reload page to update progress
                            location.reload();
                        }
                    });
                });
                
                // Reset checklist
                $('#resetBtn').click(function() {
                    if (confirm('Tem certeza que deseja resetar o checklist? Esta ação não pode ser desfeita.')) {
                        $.post('/reset_checklist', function() {
                            location.reload();
                        });
                    }
                });
            });
        </script>
    </body>
    </html>
    '''
    
    return html

@app.route('/report')
def report():
    checklist_data = load_or_create_checklist()
    
    # Count statistics
    total_items = 0
    checked_items = 0
    section_stats = []
    
    for section in CHECKLIST_SECTIONS:
        section_total = len(section['items'])
        section_checked = sum(1 for item in section['items'] if checklist_data.get(item['id'], False))
        
        section_stats.append({
            'title': section['title'],
            'total': section_total,
            'checked': section_checked,
            'percentage': round((section_checked / section_total) * 100) if section_total > 0 else 0
        })
        
        total_items += section_total
        checked_items += section_checked
    
    overall_percentage = round((checked_items / total_items) * 100) if total_items > 0 else 0
    verification_date = datetime.now().strftime("%d/%m/%Y")
    
    # Create HTML
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Relatório - Checklist de Segurança da Informação</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
            }
            .header {
                background-color: #0a2c5c;
                color: white;
                padding: 20px 0;
                margin-bottom: 30px;
                text-align: center;
            }
            .card {
                margin-bottom: 25px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .card-header {
                background-color: #0a2c5c;
                color: white;
                font-weight: bold;
            }
            .btn-primary {
                background-color: #0a2c5c;
                border-color: #0a2c5c;
            }
            .btn-primary:hover {
                background-color: #06193a;
                border-color: #06193a;
            }
            @media print {
                .no-print {
                    display: none;
                }
                .card {
                    break-inside: avoid;
                }
                .card-header {
                    background-color: #0a2c5c !important;
                    color: white !important;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                .progress-bar {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>Relatório de Verificação de Segurança da Informação</h1>
                <p class="lead">Protegendo Dados, Preservando Futuros</p>
            </div>
        </div>
        
        <div class="container">
            <div class="card mb-4">
                <div class="card-header">Informações da Verificação</div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Data da verificação:</strong> ''' + verification_date + '''</p>
                        </div>
                        <div class="col-md-6 text-md-end">
                            <p><strong>Responsável:</strong> ________________________</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">Resumo da Verificação</div>
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-4 text-center">
                            <div class="display-1 fw-bold text-''' + ('success' if overall_percentage >= 75 else 'warning' if overall_percentage >= 50 else 'danger') + '''">
                                ''' + str(overall_percentage) + '''%
                            </div>
                            <p class="lead">Conformidade Geral</p>
                        </div>
                        <div class="col-md-8">
                            <div class="progress mb-3" style="height: 25px;">
                                <div class="progress-bar bg-''' + ('success' if overall_percentage >= 75 else 'warning' if overall_percentage >= 50 else 'danger') + '''" 
                                     role="progressbar" 
                                     style="width: ''' + str(overall_percentage) + '''%" 
                                     aria-valuenow="''' + str(overall_percentage) + '''" 
                                     aria-valuemin="0" 
                                     aria-valuemax="100">
                                    ''' + str(overall_percentage) + '''%
                                </div>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span>Itens verificados: <strong>''' + str(checked_items) + '''/''' + str(total_items) + '''</strong></span>
                                <span>Itens pendentes: <strong>''' + str(total_items - checked_items) + '''</strong></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">Detalhamento por Seção</div>
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Seção</th>
                                <th class="text-center">Itens Verificados</th>
                                <th class="text-center">Total</th>
                                <th class="text-center">Percentual</th>
                                <th class="text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody>
    '''
    
    for stat in section_stats:
        html += '''
                            <tr>
                                <td>''' + stat['title'] + '''</td>
                                <td class="text-center">''' + str(stat['checked']) + '''</td>
                                <td class="text-center">''' + str(stat['total']) + '''</td>
                                <td class="text-center">''' + str(stat['percentage']) + '''%</td>
                                <td class="text-center">
                                    <span class="badge bg-''' + ('success' if stat['percentage'] >= 75 else 'warning' if stat['percentage'] >= 50 else 'danger') + '''">
                                        ''' + ('Conforme' if stat['percentage'] >= 75 else 'Atenção' if stat['percentage'] >= 50 else 'Não Conforme') + '''
                                    </span>
                                </td>
                            </tr>
        '''
    
    html += '''
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">Recomendações</div>
                <div class="card-body">
    '''
    
    if overall_percentage < 50:
        html += '''
                    <div class="alert alert-danger">
                        <h4 class="alert-heading">Atenção: Conformidade Baixa!</h4>
                        <p>A verificação apresenta um nível de conformidade abaixo do aceitável. É necessário tomar ações imediatas para mitigar riscos de segurança da informação.</p>
                        <hr>
                        <p class="mb-0">Recomenda-se agendar uma reunião com o DPO e equipe de TI para discutir as não conformidades e estabelecer um plano de ação.</p>
                    </div>
        '''
    elif overall_percentage < 75:
        html += '''
                    <div class="alert alert-warning">
                        <h4 class="alert-heading">Atenção: Melhorias Necessárias</h4>
                        <p>A verificação apresenta um nível de conformidade aceitável, mas existem pontos de melhoria importantes.</p>
                        <hr>
                        <p class="mb-0">Recomenda-se revisar os itens não conformes e estabelecer um plano de ação para os mesmos.</p>
                    </div>
        '''
    else:
        html += '''
                    <div class="alert alert-success">
                        <h4 class="alert-heading">Parabéns: Alta Conformidade!</h4>
                        <p>A verificação apresenta um excelente nível de conformidade com as normas de segurança da informação.</p>
                        <hr>
                        <p class="mb-0">Recomenda-se manter as boas práticas e continuar com o processo de melhoria contínua.</p>
                    </div>
        '''
    
    html += '''
                    <div class="mt-4">
                        <h4>Próximos Passos</h4>
                        <ol>
                            <li>Revise os itens não conformes e estabeleça prazos para resolução.</li>
                            <li>Compartilhe este relatório com o DPO e equipe de TI.</li>
                            <li>Arquive este relatório para fins de auditoria e conformidade legal.</li>
                            <li>Agende a próxima verificação para o primeiro dia útil do próximo mês.</li>
                        </ol>
                    </div>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">Assinaturas</div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <p><strong>Responsável pela verificação:</strong></p>
                            <div style="border-bottom: 1px solid #ccc; height: 40px;"></div>
                            <p class="mt-2">Nome: _______________________ Cargo: _______________________</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <p><strong>Ciência do Gestor/DPO:</strong></p>
                            <div style="border-bottom: 1px solid #ccc; height: 40px;"></div>
                            <p class="mt-2">Nome: _______________________ Cargo: _______________________</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="no-print text-center mb-5">
                <a href="/checklist" class="btn btn-secondary me-2">Voltar ao Checklist</a>
                <button onclick="window.print();" class="btn btn-primary">Imprimir Relatório</button>
            </div>
        </div>
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    
    return html

@app.route('/api/update_item', methods=['POST'])
def update_item():
    data = request.get_json()
    item_id = data.get('id')
    checked = data.get('checked')
    
    checklist_data = load_or_create_checklist()
    checklist_data[item_id] = checked
    save_checklist(checklist_data)
    
    return jsonify({'success': True})

@app.route('/reset_checklist', methods=['POST'])
def reset_checklist():
    # Create a new empty checklist
    checklist_data = {}
    for section in CHECKLIST_SECTIONS:
        for item in section['items']:
            checklist_data[item['id']] = False
    
    save_checklist(checklist_data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)