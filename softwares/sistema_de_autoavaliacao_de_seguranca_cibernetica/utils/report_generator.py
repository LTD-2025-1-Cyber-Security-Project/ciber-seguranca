from flask import render_template
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from models.recommendation import Recommendation

def generate_assessment_report(assessment, recommendations):
    """Gera um relatório detalhado baseado na avaliação e recomendações"""
    
    # Gerar gráfico radar
    radar_chart = generate_radar_chart(assessment)
    
    # Categorizar recomendações por prioridade
    high_priority = [r for r in recommendations if r.priority == 'high']
    medium_priority = [r for r in recommendations if r.priority == 'medium']
    low_priority = [r for r in recommendations if r.priority == 'low']
    
    # Categorizar recomendações por categoria
    recs_by_category = {
        'network': [r for r in recommendations if r.category == 'network'],
        'credentials': [r for r in recommendations if r.category == 'credentials'],
        'malware': [r for r in recommendations if r.category == 'malware'],
        'backup': [r for r in recommendations if r.category == 'backup'],
        'compliance': [r for r in recommendations if r.category == 'compliance']
    }
    
    # Categorias em português
    category_names = {
        'network': 'Segurança de Rede',
        'credentials': 'Controle de Acesso',
        'malware': 'Proteção contra Malware',
        'backup': 'Backup e Recuperação',
        'compliance': 'Conformidade'
    }
    
    # Análise e conclusões
    overall_status = get_overall_status(assessment.total_score)
    key_strengths = get_key_strengths(assessment)
    key_weaknesses = get_key_weaknesses(assessment)
    
    return {
        'assessment': assessment,
        'radar_chart': radar_chart,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'recs_by_category': recs_by_category,
        'category_names': category_names,
        'overall_status': overall_status,
        'key_strengths': key_strengths,
        'key_weaknesses': key_weaknesses
    }

def generate_radar_chart(assessment):
    """Gera um gráfico de radar para a avaliação"""
    
    # Categorias e valores
    categories = [
        'Segurança de Rede', 
        'Controle de Acesso',
        'Proteção contra Malware',
        'Backup e Recuperação',
        'Conformidade'
    ]
    
    values = [
        assessment.score_network,
        assessment.score_credentials,
        assessment.score_malware,
        assessment.score_backup,
        assessment.score_compliance
    ]
    
    # Número de variáveis
    N = len(categories)
    
    # Ângulos para cada eixo (em radianos)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    
    # Fechar o polígono adicionando o primeiro valor ao final
    values += values[:1]
    angles += angles[:1]
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Adicionar grades circulares com níveis específicos
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
    ax.set_ylim(0, 100)
    
    # Plotar dados
    ax.plot(angles, values, 'o-', linewidth=2, color='#36A2EB')
    ax.fill(angles, values, alpha=0.25, color='#36A2EB')
    
    # Adicionar rótulos dos eixos
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    
    # Adicionar título
    ax.set_title('Pontuação por Categoria', size=15, pad=15)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Converter figura para string base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Fechar figura para liberar memória
    plt.close(fig)
    
    # Converter para base64 para usar em HTML
    graph = base64.b64encode(image_png).decode('utf-8')
    
    return graph

def get_overall_status(total_score):
    """Determina o status geral da segurança com base na pontuação total"""
    if total_score >= 80:
        return {
            'level': 'Bom',
            'color': 'success',
            'description': 'Sua prefeitura possui um bom nível de segurança cibernética. Continue mantendo as práticas atuais e implemente melhorias contínuas.'
        }
    elif total_score >= 60:
        return {
            'level': 'Moderado',
            'color': 'warning',
            'description': 'Sua prefeitura possui um nível moderado de segurança cibernética. Existem áreas importantes que precisam de atenção.'
        }
    else:
        return {
            'level': 'Crítico',
            'color': 'danger',
            'description': 'Sua prefeitura possui vulnerabilidades críticas que requerem atenção imediata. Priorize as recomendações de alta prioridade.'
        }

def get_key_strengths(assessment):
    """Identifica os pontos fortes com base nas pontuações por categoria"""
    strengths = []
    
    scores = {
        'Segurança de Rede': assessment.score_network,
        'Controle de Acesso': assessment.score_credentials,
        'Proteção contra Malware': assessment.score_malware,
        'Backup e Recuperação': assessment.score_backup,
        'Conformidade': assessment.score_compliance
    }
    
    # Considerar categorias com pontuação acima de 70% como pontos fortes
    for category, score in scores.items():
        if score >= 70:
            strengths.append(category)
    
    return strengths

def get_key_weaknesses(assessment):
    """Identifica os pontos fracos com base nas pontuações por categoria"""
    weaknesses = []
    
    scores = {
        'Segurança de Rede': assessment.score_network,
        'Controle de Acesso': assessment.score_credentials,
        'Proteção contra Malware': assessment.score_malware,
        'Backup e Recuperação': assessment.score_backup,
        'Conformidade': assessment.score_compliance
    }
    
    # Considerar categorias com pontuação abaixo de 50% como pontos fracos
    for category, score in scores.items():
        if score < 50:
            weaknesses.append(category)
    
    return weaknesses