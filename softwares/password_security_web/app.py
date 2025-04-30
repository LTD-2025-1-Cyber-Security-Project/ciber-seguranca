import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from wtforms import Form as WTForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from werkzeug.middleware.proxy_fix import ProxyFix

# Importar módulos personalizados
from modules.password_checker import PasswordSecurityChecker
from modules.breach_detector import BreachDetector

# Importar configurações
from config import get_config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='security_app.log'
)

# Função para fornecer ano atual nos templates
def current_time():
    """
    Função auxiliar para fornecer o ano atual
    """
    return datetime.now().year

# Criar aplicação Flask
def create_app(config_class=None):
    """
    Função de fábrica para criar aplicação Flask
    
    :param config_class: Classe de configuração personalizada
    :return: Aplicação Flask configurada
    """
    # Selecionar configuração
    if config_class is None:
        config_class = get_config()
    
    # Inicializar aplicação
    app = Flask(__name__)
    
    # Aplicar configurações
    app.config.from_object(config_class)
    
    # Adicionar suporte para proxy reverso
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    
    # Adicionar função de ano atual ao contexto do Jinja2
    app.jinja_env.globals['current_time'] = current_time

    # Inicializar módulos de segurança
    password_checker = PasswordSecurityChecker()
    breach_detector = BreachDetector()

    # Formulário de Verificação de Força de Senha
    class PasswordStrengthForm(WTForm):
        password = PasswordField('Senha', [
            DataRequired(message="Senha é obrigatória"),
            Length(min=8, message="Senha deve ter no mínimo 8 caracteres")
        ])
        submit = SubmitField('Verificar Força da Senha')

    # Formulário de Verificação de Email Comprometido
    class BreachCheckForm(WTForm):
        email = StringField('Email', [
            DataRequired(message="Email é obrigatório"),
            Email(message="Email inválido")
        ])
        submit = SubmitField('Verificar Vazamentos')

    # Rotas da Aplicação
    @app.route('/')
    def index():
        """
        Página inicial do sistema de segurança de senhas
        """
        return render_template('index.html')

    @app.route('/verificar-senha', methods=['GET', 'POST'])
    def verificar_senha():
        """
        Rota para verificação de força de senha
        """
        form = PasswordStrengthForm(request.form)
        resultado = None
        
        if request.method == 'POST' and form.validate():
            try:
                # Verificar força da senha
                resultado = password_checker.validar_senha(form.password.data)
                
                # Converter resultado para template
                return render_template(
                    'verificar_senha.html', 
                    form=form, 
                    resultado=resultado
                )
            
            except Exception as e:
                logging.error(f"Erro na verificação de senha: {e}")
                flash("Ocorreu um erro ao verificar a senha.", "error")
        
        return render_template('verificar_senha.html', form=form, resultado=resultado)

    @app.route('/gerar-senha', methods=['GET'])
    def gerar_senha():
        """
        Rota para geração de senha forte
        """
        try:
            # Gerar senha forte
            senha_gerada = password_checker.gerar_senha_forte()
            return render_template('gerar_senha.html', senha=senha_gerada)
        
        except Exception as e:
            logging.error(f"Erro na geração de senha: {e}")
            flash("Ocorreu um erro ao gerar a senha.", "error")
            return render_template('gerar_senha.html', senha=None)

    @app.route('/verificar-vazamentos', methods=['GET', 'POST'])
    def verificar_vazamentos():
        """
        Rota para verificação de vazamentos de email
        """
        form = BreachCheckForm(request.form)
        resultado = None
        vazamentos_recentes = []
        
        if request.method == 'POST' and form.validate():
            try:
                # Verificar vazamentos
                resultado = breach_detector.analisar_senhas_comprometidas(form.email.data)
                
                # Buscar vazamentos recentes
                vazamentos_recentes = breach_detector.buscar_vazamentos_recentes()
                
                # Gerar relatório de segurança completo
                relatorio_seguranca = breach_detector.gerar_relatorio_seguranca(form.email.data)
                
                return render_template(
                    'analise_comprometidas.html', 
                    form=form, 
                    resultado=resultado,
                    vazamentos_recentes=vazamentos_recentes,
                    relatorio_seguranca=relatorio_seguranca
                )
            
            except Exception as e:
                logging.error(f"Erro na verificação de vazamentos: {e}")
                flash("Ocorreu um erro ao verificar vazamentos.", "error")
        
        return render_template('analise_comprometidas.html', form=form, resultado=resultado)

    @app.route('/instrucoes')
    def instrucoes():
        """
        Página de instruções de uso
        """
        return render_template('instrucoes.html')

    # Tratamento de erros
    @app.errorhandler(404)
    def page_not_found(e):
        """
        Tratamento de erro 404
        """
        return render_template('erro.html', codigo=404, mensagem="Página não encontrada"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """
        Tratamento de erro 500
        """
        return render_template('erro.html', codigo=500, mensagem="Erro interno do servidor"), 500

    # API de Verificação de Vazamentos
    @app.route('/api/verificar-vazamentos', methods=['POST'])
    def api_verificar_vazamentos():
        """
        Endpoint de API para verificação de vazamentos
        """
        try:
            # Receber dados JSON
            dados = request.get_json()
            email = dados.get('email')
            
            # Validar entrada
            if not email:
                return jsonify({
                    'erro': 'Email não fornecido',
                    'status': 400
                }), 400
            
            # Verificar vazamentos
            resultado = breach_detector.analisar_senhas_comprometidas(email)
            
            # Gerar relatório de segurança
            relatorio_seguranca = breach_detector.gerar_relatorio_seguranca(email)
            
            # Combinar resultados
            resposta = {
                'vazamentos': resultado,
                'relatorio_seguranca': relatorio_seguranca,
                'status': 200
            }
            
            return jsonify(resposta)
        
        except Exception as e:
            logging.error(f"Erro na API de verificação de vazamentos: {e}")
            return jsonify({
                'erro': 'Erro interno',
                'status': 500
            }), 500

    # Rota de Diagnóstico de Segurança
    @app.route('/diagnostico-seguranca', methods=['GET', 'POST'])
    def diagnostico_seguranca():
        """
        Página de diagnóstico de segurança
        """
        if request.method == 'POST':
            try:
                # Realizar diagnóstico completo
                diagnostico = {
                    'sistema_operacional': os.name,
                    'python_version': sys.version,
                    'dependencias': {
                        'flask': flask.__version__,
                        'werkzeug': werkzeug.__version__,
                        # Adicionar outras dependências
                    },
                    'logs_recentes': _obter_ultimos_logs(),
                    'vulnerabilidades_conhecidas': _verificar_vulnerabilidades()
                }
                
                return render_template(
                    'diagnostico_seguranca.html', 
                    diagnostico=diagnostico
                )
            
            except Exception as e:
                logging.error(f"Erro no diagnóstico de segurança: {e}")
                flash("Ocorreu um erro ao realizar o diagnóstico.", "error")
        
        return render_template('diagnostico_seguranca.html')

    def _obter_ultimos_logs(self, linhas=50):
        """
        Obtém as últimas linhas do arquivo de log
        
        :param linhas: Número de linhas a recuperar
        :return: Lista de linhas de log
        """
        try:
            with open('security_app.log', 'r') as arquivo_log:
                return arquivo_log.readlines()[-linhas:]
        except Exception as e:
            logging.error(f"Erro ao ler logs: {e}")
            return []

    def _verificar_vulnerabilidades():
        """
        Verifica vulnerabilidades conhecidas
        
        :return: Lista de vulnerabilidades
        """
        vulnerabilidades = []
        
        # Verificações de segurança básicas
        try:
            # Verificar versões de dependências
            import pkg_resources
            
            # Lista de pacotes para verificar
            pacotes_criticos = [
                'flask', 'werkzeug', 'requests', 'wtforms'
            ]
            
            for pacote in pacotes_criticos:
                try:
                    versao = pkg_resources.get_distribution(pacote).version
                    # Aqui você poderia adicionar lógica para comparar com versões conhecidas como inseguras
                except pkg_resources.DistributionNotFound:
                    vulnerabilidades.append(f"Pacote crítico não encontrado: {pacote}")
        
        except Exception as e:
            logging.error(f"Erro na verificação de vulnerabilidades: {e}")
        
        return vulnerabilidades

    # Rota de Backup de Configurações
    @app.route('/backup-configuracoes', methods=['GET', 'POST'])
    def backup_configuracoes():
        """
        Realizar backup de configurações
        """
        try:
            # Definir diretório de backup
            dir_backup = os.path.join(app.root_path, 'backups')
            os.makedirs(dir_backup, exist_ok=True)
            
            # Nome do arquivo de backup
            nome_backup = f"backup_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            caminho_backup = os.path.join(dir_backup, nome_backup)
            
            # Dados para backup
            dados_backup = {
                'data_backup': datetime.now().isoformat(),
                'configuracoes_app': dict(app.config),
                'variaveis_ambiente': dict(os.environ)
            }
            
            # Salvar backup
            with open(caminho_backup, 'w') as arquivo:
                json.dump(dados_backup, arquivo, indent=2)
            
            flash(f"Backup de configurações realizado: {nome_backup}", "success")
            
            return render_template('backup_configuracoes.html', backup_realizado=nome_backup)
        
        except Exception as e:
            logging.error(f"Erro no backup de configurações: {e}")
            flash("Erro ao realizar backup de configurações.", "error")
            return render_template('backup_configuracoes.html')

    return app

# Execução do aplicativo
if __name__ == '__main__':
    # Importações necessárias para diagnóstico
    import sys
    import flask
    import werkzeug
    
    # Criar e configurar aplicação
    app = create_app()
    
    # Determinar porta
    porta = int(os.environ.get('PORT', 5000))
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0', 
        port=porta, 
        debug=app.config.get('DEBUG', True)
    )