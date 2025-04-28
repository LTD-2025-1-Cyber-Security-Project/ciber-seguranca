from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.assessment import Assessment
from models.recommendation import Recommendation
from datetime import datetime
import json
from utils.security import require_same_user_or_admin

assessment_bp = Blueprint('assessment', __name__)

# Dicionário de questões para cada categoria
ASSESSMENT_QUESTIONS = {
    'network': [
        {'id': 'network_1', 'text': 'Sua prefeitura utiliza firewall gerenciado e atualizado?'},
        {'id': 'network_2', 'text': 'Existe segmentação de rede entre departamentos?'},
        {'id': 'network_3', 'text': 'A rede WiFi possui protocolos de segurança adequados (WPA2/WPA3)?'},
        {'id': 'network_4', 'text': 'São realizadas análises de vulnerabilidade na rede periodicamente?'},
        {'id': 'network_5', 'text': 'Existe monitoramento de tráfego de rede e detecção de intrusão?'}
    ],
    'credentials': [
        {'id': 'credentials_1', 'text': 'Existe política de senhas fortes implementada?'},
        {'id': 'credentials_2', 'text': 'É utilizada autenticação de dois fatores (2FA) para acesso a sistemas críticos?'},
        {'id': 'credentials_3', 'text': 'Existe processo formal para gerenciamento de credenciais de funcionários?'},
        {'id': 'credentials_4', 'text': 'São realizadas revisões periódicas de permissões de acesso?'},
        {'id': 'credentials_5', 'text': 'Existe um processo de revogação imediata de acessos após desligamento de funcionários?'}
    ],
    'malware': [
        {'id': 'malware_1', 'text': 'Todos os computadores possuem antivírus atualizado?'},
        {'id': 'malware_2', 'text': 'Existe política de atualização regular de sistemas operacionais e aplicativos?'},
        {'id': 'malware_3', 'text': 'São realizados treinamentos de conscientização sobre engenharia social e phishing?'},
        {'id': 'malware_4', 'text': 'Existe filtragem de e-mails e bloqueio de anexos potencialmente perigosos?'},
        {'id': 'malware_5', 'text': 'Existe controle sobre instalação de aplicativos nos dispositivos?'}
    ],
    'backup': [
        {'id': 'backup_1', 'text': 'Existe política formal de backup de dados?'},
        {'id': 'backup_2', 'text': 'Os backups são armazenados em local seguro e fisicamente separado?'},
        {'id': 'backup_3', 'text': 'São realizados testes periódicos de restauração dos backups?'},
        {'id': 'backup_4', 'text': 'Existe plano de recuperação de desastres documentado?'},
        {'id': 'backup_5', 'text': 'Os backups são criptografados?'}
    ],
    'compliance': [
        {'id': 'compliance_1', 'text': 'Existe conformidade com a LGPD (Lei Geral de Proteção de Dados)?'},
        {'id': 'compliance_2', 'text': 'São realizadas auditorias periódicas de segurança da informação?'},
        {'id': 'compliance_3', 'text': 'Existe política formal de segurança da informação documentada?'},
        {'id': 'compliance_4', 'text': 'Existe um DPO (Encarregado de Proteção de Dados) designado?'},
        {'id': 'compliance_5', 'text': 'São mantidos registros (logs) de acesso a dados sensíveis?'}
    ]
}

# Recomendações por categoria e nível de pontuação
RECOMMENDATIONS = {
    'network': {
        'low': [
            {
                'title': 'Implementar firewall gerenciado',
                'description': 'Implemente um firewall gerenciado e configure regras para filtrar tráfego malicioso.',
                'priority': 'high',
                'implementation_steps': '1. Adquirir solução de firewall;\n2. Configurar regras básicas;\n3. Testar implementação;\n4. Monitorar logs.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            },
            {
                'title': 'Segregar rede por departamentos',
                'description': 'Implemente VLANs para separar tráfego entre departamentos e limitar potenciais violações.',
                'priority': 'medium',
                'implementation_steps': '1. Mapear departamentos;\n2. Configurar VLANs no switch;\n3. Atribuir dispositivos às VLANs corretas.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'medium': [
            {
                'title': 'Implementar sistema de detecção de intrusão',
                'description': 'Adicione um IDS/IPS para monitorar e bloquear atividades suspeitas na rede.',
                'priority': 'medium',
                'implementation_steps': '1. Avaliar soluções IDS/IPS;\n2. Implementar em modo de monitoramento;\n3. Ajustar regras para reduzir falsos positivos.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'high': [
            {
                'title': 'Realizar análise de vulnerabilidade periódica',
                'description': 'Estabeleça uma rotina trimestral de análise de vulnerabilidades na infraestrutura.',
                'priority': 'low',
                'implementation_steps': '1. Contratar serviço especializado;\n2. Definir escopo de análise;\n3. Estabelecer periodicidade.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ]
    },
    'credentials': {
        'low': [
            {
                'title': 'Implementar política de senhas fortes',
                'description': 'Estabeleça regras para senhas com mínimo de 12 caracteres, combinando letras, números e símbolos.',
                'priority': 'high',
                'implementation_steps': '1. Definir política de senhas;\n2. Configurar no Active Directory ou sistema equivalente;\n3. Comunicar aos usuários.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/cartilha-de-seguranca-para-usuario-final'
            },
            {
                'title': 'Implementar autenticação de dois fatores',
                'description': 'Adicione uma camada extra de segurança com 2FA para sistemas críticos.',
                'priority': 'high',
                'implementation_steps': '1. Identificar sistemas críticos;\n2. Selecionar solução de 2FA;\n3. Implementar e treinar usuários.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/cartilha-de-seguranca-para-usuario-final'
            }
        ],
        'medium': [
            {
                'title': 'Revisar permissões de acesso periodicamente',
                'description': 'Estabeleça rotina de revisão trimestral de permissões de acesso para todos os sistemas.',
                'priority': 'medium',
                'implementation_steps': '1. Mapear todos os sistemas;\n2. Definir responsáveis por aprovação;\n3. Documentar processo de revisão.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'high': [
            {
                'title': 'Implementar gerenciador de senhas corporativo',
                'description': 'Adote uma solução de gerenciamento de senhas para toda a prefeitura.',
                'priority': 'low',
                'implementation_steps': '1. Avaliar soluções de mercado;\n2. Implementar solução escolhida;\n3. Treinar funcionários.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ]
    },
    'malware': {
        'low': [
            {
                'title': 'Implementar solução de antivírus centralizada',
                'description': 'Adote uma solução de antivírus gerenciada centralmente para todos os dispositivos.',
                'priority': 'high',
                'implementation_steps': '1. Selecionar solução de antivírus;\n2. Implementar servidor central;\n3. Instalar e configurar em todos os endpoints.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            },
            {
                'title': 'Estabelecer política de atualização de software',
                'description': 'Crie processo formal para atualização periódica de sistemas operacionais e aplicativos.',
                'priority': 'high',
                'implementation_steps': '1. Inventariar software em uso;\n2. Definir janelas de manutenção;\n3. Configurar atualizações automáticas quando possível.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'medium': [
            {
                'title': 'Implementar filtro de conteúdo web',
                'description': 'Adicione proteção contra acesso a sites maliciosos e download de arquivos suspeitos.',
                'priority': 'medium',
                'implementation_steps': '1. Selecionar solução de filtragem web;\n2. Definir políticas por grupo de usuários;\n3. Implementar e monitorar.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'high': [
            {
                'title': 'Realizar treinamentos regulares de conscientização',
                'description': 'Estabeleça programa de treinamento trimestral sobre ameaças cibernéticas.',
                'priority': 'medium',
                'implementation_steps': '1. Desenvolver material de treinamento;\n2. Agendar sessões regulares;\n3. Avaliar conhecimento após treinamentos.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/cartilha-de-seguranca-para-usuario-final'
            }
        ]
    },
    'backup': {
        'low': [
            {
                'title': 'Implementar política formal de backup',
                'description': 'Estabeleça processo documentado de backup diário com retenção adequada.',
                'priority': 'high',
                'implementation_steps': '1. Identificar dados críticos;\n2. Definir frequência e retenção;\n3. Implementar solução de backup;\n4. Documentar procedimentos.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            },
            {
                'title': 'Implementar backup off-site',
                'description': 'Adicione armazenamento de backup em local fisicamente separado ou na nuvem.',
                'priority': 'high',
                'implementation_steps': '1. Avaliar opções de armazenamento;\n2. Implementar transmissão segura;\n3. Verificar integridade periodicamente.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'medium': [
            {
                'title': 'Implementar criptografia de backups',
                'description': 'Adicione criptografia para todos os dados de backup.',
                'priority': 'medium',
                'implementation_steps': '1. Selecionar algoritmo de criptografia;\n2. Configurar solução de backup;\n3. Estabelecer gestão segura de chaves.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'high': [
            {
                'title': 'Estabelecer plano de recuperação de desastres',
                'description': 'Documente procedimentos detalhados para recuperação em caso de incidentes.',
                'priority': 'medium',
                'implementation_steps': '1. Identificar sistemas críticos;\n2. Documentar procedimentos;\n3. Realizar testes periódicos.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ]
    },
    'compliance': {
        'low': [
            {
                'title': 'Implementar programa de conformidade com LGPD',
                'description': 'Estabeleça processo formal para adequação à Lei Geral de Proteção de Dados.',
                'priority': 'high',
                'implementation_steps': '1. Mapear dados pessoais tratados;\n2. Documentar base legal;\n3. Implementar medidas técnicas e administrativas.',
                'resources': 'https://www.gov.br/secretariageral/pt-br/guia-de-implementacao-da-lei-geral-de-protecao-de-dados-lgpd.pdf'
            },
            {
                'title': 'Designar Encarregado de Proteção de Dados (DPO)',
                'description': 'Nomeie formalmente um responsável por garantir conformidade com a LGPD.',
                'priority': 'high',
                'implementation_steps': '1. Definir responsabilidades;\n2. Selecionar pessoa com conhecimento adequado;\n3. Formalizar nomeação.',
                'resources': 'https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado.pdf'
            }
        ],
        'medium': [
            {
                'title': 'Formalizar política de segurança da informação',
                'description': 'Documente política abrangente de segurança da informação para a prefeitura.',
                'priority': 'medium',
                'implementation_steps': '1. Mapear requisitos legais e normativos;\n2. Desenvolver documento da política;\n3. Obter aprovação da alta administração;\n4. Comunicar a todos os funcionários.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ],
        'high': [
            {
                'title': 'Implementar programa de auditoria periódica',
                'description': 'Estabeleça processo de auditoria interna anual para verificar conformidade.',
                'priority': 'low',
                'implementation_steps': '1. Definir escopo da auditoria;\n2. Estabelecer checklist;\n3. Designar responsáveis;\n4. Documentar resultados e melhorias.',
                'resources': 'https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias-operacionais-de-seguranca-da-informacao'
            }
        ]
    }
}

@assessment_bp.route('/assessments')
@login_required
def list_assessments():
    assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).all()
    return render_template('assessment/list.html', assessments=assessments)

@assessment_bp.route('/assessments/new', methods=['GET', 'POST'])
@login_required
def new_assessment():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('O título da avaliação é obrigatório.', 'danger')
            return render_template('assessment/new.html')
        
        assessment = Assessment(
            title=title,
            description=description,
            user_id=current_user.id,
            status='in_progress',
            responses_data='{}'
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        flash('Avaliação criada com sucesso! Agora você pode iniciar o questionário.', 'success')
        return redirect(url_for('assessment.edit_assessment', assessment_id=assessment.id))
    
    return render_template('assessment/new.html')

@assessment_bp.route('/assessments/<int:assessment_id>')
@login_required
def view_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Verificar se o usuário tem permissão para ver esta avaliação
    if assessment.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar esta avaliação.', 'danger')
        return redirect(url_for('assessment.list_assessments'))
    
    recommendations = Recommendation.query.filter_by(assessment_id=assessment_id).order_by(Recommendation.priority).all()
    
    return render_template(
        'assessment/view.html', 
        assessment=assessment, 
        questions=ASSESSMENT_QUESTIONS,
        responses=assessment.get_responses(),
        recommendations=recommendations
    )

@assessment_bp.route('/assessments/<int:assessment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Verificar se o usuário tem permissão para editar esta avaliação
    if assessment.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para editar esta avaliação.', 'danger')
        return redirect(url_for('assessment.list_assessments'))
    
    if assessment.status == 'completed':
        flash('Esta avaliação já foi concluída e não pode ser editada.', 'warning')
        return redirect(url_for('assessment.view_assessment', assessment_id=assessment_id))
    
    if request.method == 'POST':
        # Atualizar informações básicas da avaliação
        assessment.title = request.form.get('title')
        assessment.description = request.form.get('description')
        
        # Coletar respostas
        responses = {}
        for category in ASSESSMENT_QUESTIONS:
            for question in ASSESSMENT_QUESTIONS[category]:
                question_id = question['id']
                if question_id in request.form:
                    responses[question_id] = request.form.get(question_id)
        
        # Salvar respostas
        assessment.set_responses(responses)
        
        # Verificar se todas as perguntas foram respondidas
        all_question_ids = [q['id'] for cat in ASSESSMENT_QUESTIONS.values() for q in cat]
        all_answered = all(qid in responses for qid in all_question_ids)
        
        if all_answered and 'finish' in request.form:
            assessment.status = 'completed'
            assessment.calculate_scores()
            
            # Gerar recomendações baseadas nas pontuações
            generate_recommendations(assessment)
            
            flash('Avaliação concluída com sucesso!', 'success')
            return redirect(url_for('assessment.view_assessment', assessment_id=assessment.id))
        else:
            # Salvar como rascunho
            db.session.commit()
            flash('Avaliação salva com sucesso!', 'success')
            
            if 'finish' in request.form and not all_answered:
                flash('Para concluir a avaliação, você precisa responder todas as perguntas.', 'warning')
                
            return redirect(url_for('assessment.edit_assessment', assessment_id=assessment.id))
    
    return render_template(
        'assessment/edit.html',
        assessment=assessment,
        questions=ASSESSMENT_QUESTIONS,
        responses=assessment.get_responses()
    )

@assessment_bp.route('/assessments/<int:assessment_id>/delete', methods=['POST'])
@login_required
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Verificar se o usuário tem permissão para excluir esta avaliação
    if assessment.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para excluir esta avaliação.', 'danger')
        return redirect(url_for('assessment.list_assessments'))
    
    # Excluir recomendações associadas
    Recommendation.query.filter_by(assessment_id=assessment_id).delete()
    
    # Excluir avaliação
    db.session.delete(assessment)
    db.session.commit()
    
    flash('Avaliação excluída com sucesso!', 'success')
    return redirect(url_for('assessment.list_assessments'))

def generate_recommendations(assessment):
    # Limpar recomendações anteriores
    Recommendation.query.filter_by(assessment_id=assessment.id).delete()
    
    # Definir nível por categoria baseado na pontuação
    categories = {
        'network': assessment.score_network,
        'credentials': assessment.score_credentials,
        'malware': assessment.score_malware,
        'backup': assessment.score_backup,
        'compliance': assessment.score_compliance
    }
    
    new_recommendations = []
    
    for category, score in categories.items():
        # Determinar nível de recomendações baseado na pontuação
        level = 'high'  # Padrão para pontuações altas
        
        if score < 40:
            level = 'low'
        elif score < 70:
            level = 'medium'
        
        # Obter recomendações para esta categoria e nível
        recommendations_for_level = RECOMMENDATIONS[category].get(level, [])
        
        # Adicionar recomendações ao banco de dados
        for rec_data in recommendations_for_level:
            recommendation = Recommendation(
                assessment_id=assessment.id,
                category=category,
                priority=rec_data['priority'],
                title=rec_data['title'],
                description=rec_data['description'],
                implementation_steps=rec_data['implementation_steps'],
                resources=rec_data['resources'],
                status='pending'
            )
            new_recommendations.append(recommendation)
    
    # Salvar todas as recomendações de uma vez
    db.session.add_all(new_recommendations)
    db.session.commit()

@assessment_bp.route('/assessments/<int:assessment_id>/recommendations/<int:recommendation_id>/status', methods=['POST'])
@login_required
def update_recommendation_status(assessment_id, recommendation_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Verificar se o usuário tem permissão
    if assessment.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permissão negada'}), 403
    
    recommendation = Recommendation.query.get_or_404(recommendation_id)
    
    if recommendation.assessment_id != assessment_id:
        return jsonify({'success': False, 'message': 'Recomendação não pertence a esta avaliação'}), 400
    
    new_status = request.json.get('status')
    if new_status not in ['pending', 'in_progress', 'implemented']:
        return jsonify({'success': False, 'message': 'Status inválido'}), 400
    
    recommendation.status = new_status
    db.session.commit()
    
    return jsonify({'success': True})

@assessment_bp.route('/api/chart-data/<int:assessment_id>')
@login_required
def chart_data(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Verificar se o usuário tem permissão
    if assessment.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permissão negada'}), 403
    
    # Dados para o gráfico de radar
    radar_data = {
        'categories': [
            'Segurança de Rede',
            'Controle de Acesso',
            'Proteção contra Malware',
            'Backup e Recuperação',
            'Conformidade'
        ],
        'values': [
            assessment.score_network,
            assessment.score_credentials,
            assessment.score_malware,
            assessment.score_backup,
            assessment.score_compliance
        ]
    }
    
    # Dados para o gráfico de barras de recomendações
    recommendations = Recommendation.query.filter_by(assessment_id=assessment_id).all()
    
    rec_by_category = {
        'network': {'pending': 0, 'in_progress': 0, 'implemented': 0},
        'credentials': {'pending': 0, 'in_progress': 0, 'implemented': 0},
        'malware': {'pending': 0, 'in_progress': 0, 'implemented': 0},
        'backup': {'pending': 0, 'in_progress': 0, 'implemented': 0},
        'compliance': {'pending': 0, 'in_progress': 0, 'implemented': 0}
    }
    
    rec_by_priority = {
        'high': {'pending': 0, 'in_progress': 0, 'implemented': 0},
        'medium': {'pending': 0, 'in_progress': 0, 'implemented': 0},
        'low': {'pending': 0, 'in_progress': 0, 'implemented': 0}
    }
    
    for rec in recommendations:
        rec_by_category[rec.category][rec.status] += 1
        rec_by_priority[rec.priority][rec.status] += 1
    
    return jsonify({
        'success': True,
        'radar_data': radar_data,
        'rec_by_category': rec_by_category,
        'rec_by_priority': rec_by_priority,
        'total_score': assessment.total_score
    })