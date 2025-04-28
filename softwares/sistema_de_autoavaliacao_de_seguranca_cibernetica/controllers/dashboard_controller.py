from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from models import db
from models.assessment import Assessment
from models.recommendation import Recommendation
from sqlalchemy import func
import json
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Estatísticas gerais
    assessments_count = Assessment.query.filter_by(user_id=current_user.id).count()
    completed_assessments = Assessment.query.filter_by(user_id=current_user.id, status='completed').count()
    
    # Última avaliação
    latest_assessment = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).first()
    
    # Pontuação média por categoria
    avg_scores = db.session.query(
        func.avg(Assessment.score_network).label('network'),
        func.avg(Assessment.score_credentials).label('credentials'),
        func.avg(Assessment.score_malware).label('malware'),
        func.avg(Assessment.score_backup).label('backup'),
        func.avg(Assessment.score_compliance).label('compliance'),
        func.avg(Assessment.total_score).label('total')
    ).filter(
        Assessment.user_id == current_user.id,
        Assessment.status == 'completed'
    ).first()
    
    # Recomendações pendentes de alta prioridade
    high_priority_recs = db.session.query(Recommendation)\
        .join(Assessment, Assessment.id == Recommendation.assessment_id)\
        .filter(
            Assessment.user_id == current_user.id,
            Recommendation.priority == 'high',
            Recommendation.status == 'pending'
        ).limit(5).all()
    
    # Progresso de implementação
    implementation_stats = db.session.query(
        Recommendation.status,
        func.count(Recommendation.id).label('count')
    ).join(
        Assessment, Assessment.id == Recommendation.assessment_id
    ).filter(
        Assessment.user_id == current_user.id
    ).group_by(
        Recommendation.status
    ).all()
    
    implementation_progress = {
        'pending': 0,
        'in_progress': 0,
        'implemented': 0
    }
    
    for status, count in implementation_stats:
        implementation_progress[status] = count
    
    return render_template(
        'dashboard/index.html',
        assessments_count=assessments_count,
        completed_assessments=completed_assessments,
        latest_assessment=latest_assessment,
        avg_scores=avg_scores,
        high_priority_recs=high_priority_recs,
        implementation_progress=implementation_progress
    )

@dashboard_bp.route('/stats')
@login_required
def stats():
    # Avaliações nos últimos 6 meses
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    
    assessments_by_month = db.session.query(
        func.date_format(Assessment.created_at, '%Y-%m').label('month'),
        func.count(Assessment.id).label('count')
    ).filter(
        Assessment.user_id == current_user.id,
        Assessment.created_at >= six_months_ago
    ).group_by(
        'month'
    ).order_by(
        'month'
    ).all()
    
    # Categorias com maiores e menores pontuações
    avg_by_category = db.session.query(
        func.avg(Assessment.score_network).label('network'),
        func.avg(Assessment.score_credentials).label('credentials'),
        func.avg(Assessment.score_malware).label('malware'),
        func.avg(Assessment.score_backup).label('backup'),
        func.avg(Assessment.score_compliance).label('compliance')
    ).filter(
        Assessment.user_id == current_user.id,
        Assessment.status == 'completed'
    ).first()
    
    # Converter para dicionário para facilitar processamento
    avg_scores = {
        'Segurança de Rede': avg_by_category.network or 0,
        'Controle de Acesso': avg_by_category.credentials or 0,
        'Proteção contra Malware': avg_by_category.malware or 0,
        'Backup e Recuperação': avg_by_category.backup or 0,
        'Conformidade': avg_by_category.compliance or 0
    }
    
    # Encontrar categorias com maior e menor pontuação
    strongest_category = max(avg_scores.items(), key=lambda x: x[1]) if avg_scores else ('N/A', 0)
    weakest_category = min(avg_scores.items(), key=lambda x: x[1]) if avg_scores else ('N/A', 0)
    
    # Recomendações por categoria
    recs_by_category = db.session.query(
        Recommendation.category,
        func.count(Recommendation.id).label('count')
    ).join(
        Assessment, Assessment.id == Recommendation.assessment_id
    ).filter(
        Assessment.user_id == current_user.id
    ).group_by(
        Recommendation.category
    ).all()
    
    category_names = {
        'network': 'Segurança de Rede',
        'credentials': 'Controle de Acesso',
        'malware': 'Proteção contra Malware',
        'backup': 'Backup e Recuperação',
        'compliance': 'Conformidade'
    }
    
    recs_categories = {category_names.get(cat, cat): count for cat, count in recs_by_category}
    
    return render_template(
        'dashboard/stats.html',
        assessments_by_month=assessments_by_month,
        avg_scores=avg_scores,
        strongest_category=strongest_category,
        weakest_category=weakest_category,
        recs_categories=recs_categories
    )

@dashboard_bp.route('/compare')
@login_required
def compare():
    # Obter avaliações completadas para comparação
    completed_assessments = Assessment.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).order_by(Assessment.created_at.desc()).all()
    
    return render_template('dashboard/compare.html', assessments=completed_assessments)

@dashboard_bp.route('/api/compare', methods=['POST'])
@login_required
def api_compare():
    assessment_ids = request.json.get('assessment_ids', [])
    
    if not assessment_ids or len(assessment_ids) < 1 or len(assessment_ids) > 3:
        return jsonify({'success': False, 'message': 'Selecione de 1 a 3 avaliações para comparar'}), 400
    
    assessments = []
    for assessment_id in assessment_ids:
        assessment = Assessment.query.get(assessment_id)
        
        # Verificar se a avaliação existe e pertence ao usuário
        if not assessment or (assessment.user_id != current_user.id and not current_user.is_admin):
            continue
            
        assessments.append({
            'id': assessment.id,
            'title': assessment.title,
            'created_at': assessment.created_at.strftime('%d/%m/%Y'),
            'scores': {
                'network': assessment.score_network,
                'credentials': assessment.score_credentials,
                'malware': assessment.score_malware,
                'backup': assessment.score_backup,
                'compliance': assessment.score_compliance,
                'total': assessment.total_score
            }
        })
    
    return jsonify({
        'success': True,
        'assessments': assessments,
        'categories': [
            'Segurança de Rede',
            'Controle de Acesso',
            'Proteção contra Malware',
            'Backup e Recuperação',
            'Conformidade',
            'Pontuação Total'
        ]
    })