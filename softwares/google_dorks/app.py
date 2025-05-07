from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import os
import requests
import json
import logging
import datetime
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração de logs
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuração da API do Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCY5JQRIAZlq7Re-GNDtwn8b1Hmza_hk8Y")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

def optimize_query_with_gemini(query, file_type=None, context=None):
    """
    Otimiza a consulta do usuário usando a API do Google Gemini
    """
    # Verificar se a consulta é uma instrução em linguagem natural ou já é uma dork
    is_natural_language = any([
        query.lower().startswith("preciso"),
        query.lower().startswith("quero"),
        query.lower().startswith("encontre"),
        query.lower().startswith("buscar"),
        query.lower().startswith("localizar"),
        query.lower().startswith("procurar"),
        "como encontrar" in query.lower(),
        "ajude-me a" in query.lower(),
        len(query.split()) > 8 and not any(operator in query for operator in ["site:", "filetype:", "intitle:", "inurl:", "intext:"])
    ])
    
    # Se não for linguagem natural, retornar com pequenas melhorias
    if not is_natural_language:
        # Adicionar apenas filetype se especificado e não estiver presente
        if file_type and f"filetype:{file_type}" not in query:
            query += f" filetype:{file_type}"
        return query
    
    # Preparar prompt específico para dorks de cibersegurança
    is_cybersec_related = any([
        "vulnerabilidade" in query.lower(),
        "segurança" in query.lower(),
        "pentest" in query.lower(),
        "cibersegurança" in query.lower(),
        "vazamento" in query.lower(),
        "exploit" in query.lower(),
        "senha" in query.lower(),
        "password" in query.lower(),
        "config" in query.lower(),
        "credencial" in query.lower(),
        "admin" in query.lower(),
        "painel" in query.lower(),
        "dashboard" in query.lower(),
        "login" in query.lower(),
        "confidencial" in query.lower()
    ])
    
    if is_cybersec_related:
        prompt = f"""
        Converta a seguinte consulta em uma busca avançada de Google Dorks voltada para cibersegurança.
        
        Consulta original: {query}
        
        {"Tipo de arquivo desejado: " + file_type if file_type else ""}
        
        Aplique operadores avançados como site:, filetype:, intitle:, inurl:, intext:, ext:, etc.
        Inclua combinações poderosas para encontrar painéis de administração, diretórios expostos, 
        configurações, credenciais ou outros aspectos relevantes para cibersegurança.
        
        Considere operadores como -401 -403 -404 para excluir páginas de erro.
        Utilize combinações com "index of" para diretórios abertos.
        
        Use aspas para termos exatos e operadores booleanos (OR, AND) quando apropriado.
        Não inclua explicações, apenas a consulta otimizada pronta para usar no Google.
        """
    else:
        # Adequar o prompt ao contexto específico da busca
        context_info = ""
        if context == "licitacoes":
            context_info = "Busca por documentos de licitações e contratos públicos"
        elif context == "legislacao":
            context_info = "Busca por legislação e documentos normativos municipais"
        elif context == "documentos":
            context_info = "Busca por documentos administrativos públicos"
        elif context == "transparencia":
            context_info = "Busca nos portais de transparência"
        else:
            context_info = "Busca geral de documentos públicos"
            
        prompt = f"""
        Otimize a seguinte consulta de pesquisa transformando-a em uma busca avançada com operadores de Google Dorks.
        
        Consulta original: {query}
        
        Contexto de uso: {context_info}
        
        {"Tipo de arquivo desejado: " + file_type if file_type else ""}
        
        Aplique as seguintes técnicas:
        1. Use site: para restringir a domínios relevantes (gov.br, org.br, etc. se aplicável)
        2. Use filetype: para o tipo de arquivo especificado (ou escolha o mais relevante como PDF se não especificado)
        3. Use intitle: ou intext: para termos principais
        4. Use aspas para frases exatas importantes
        5. Use operadores booleanos (OR) para termos alternativos
        6. Use operadores de exclusão (-) para remover resultados irrelevantes
        7. Se apropriado, use after: para filtrar por data
        
        Responda apenas com a consulta otimizada usando operadores de Google Dorks apropriados.
        Não inclua explicações, apenas a consulta formatada para ser usada diretamente no Google.
        """
    
    # Configurar a chamada para a API Gemini
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1024,
            "topP": 0.8,
            "topK": 40
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }
    
    # Fazer requisição para API do Gemini
    try:
        app.logger.info(f"Enviando consulta para API Gemini: {query[:50]}...")
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data,
            timeout=10  # Timeout de 10 segundos
        )
        
        app.logger.info(f"Resposta da API recebida: Status {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            try:
                optimized_query = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                app.logger.info(f"Consulta otimizada com sucesso: {optimized_query[:50]}...")
                return optimized_query
            except (KeyError, IndexError) as e:
                app.logger.error(f"Erro ao processar resposta da API: {str(e)}")
                return "Erro ao processar a consulta. Tente novamente."
        else:
            app.logger.error(f"Erro na API: {response.status_code}. Response: {response.text}")
            return f"Erro na API: {response.status_code}"
    except Exception as e:
        app.logger.error(f"Exceção ao chamar API: {str(e)}")
        return f"Erro de conexão: {str(e)}"

def basic_query_optimization(query, file_type, context):
    """
    Otimização avançada da consulta sem usar IA (plano B)
    Transforma consultas em linguagem natural em dorks eficientes
    """
    app.logger.info(f"Usando otimização básica para: {query[:50]}...")
    original_query = query
    
    # Verificar se a consulta é uma instrução em linguagem natural
    is_natural_language = any([
        query.lower().startswith("preciso"),
        query.lower().startswith("quero"),
        query.lower().startswith("encontre"),
        query.lower().startswith("buscar"),
        query.lower().startswith("localizar"),
        query.lower().startswith("procurar"),
        "como encontrar" in query.lower(),
        "ajude-me a" in query.lower(),
        len(query.split()) > 8 and not any(operator in query for operator in ["site:", "filetype:", "intitle:", "inurl:", "intext:"])
    ])
    
    # Se não for linguagem natural, retornar a consulta com pequenas melhorias
    if not is_natural_language:
        if file_type and f"filetype:{file_type}" not in query:
            query += f" filetype:{file_type}"
        return query
    
    # Extrair informações da consulta em linguagem natural
    keywords = []
    optimized = ""
    
    # Detectar se é relacionado à cibersegurança
    is_cybersec_related = any([
        "vulnerabilidade" in query.lower(),
        "segurança" in query.lower(),
        "pentest" in query.lower(),
        "cibersegurança" in query.lower(),
        "vazamento" in query.lower(),
        "exploit" in query.lower(),
        "senha" in query.lower(),
        "password" in query.lower(),
        "config" in query.lower(),
        "credencial" in query.lower(),
        "admin" in query.lower(),
        "painel" in query.lower(),
        "login" in query.lower(),
        "confidencial" in query.lower()
    ])
    
    # Extrair palavras-chave relevantes
    words = query.split()
    
    # Remover palavras introdutórias em linguagem natural
    skip_words = ["preciso", "quero", "encontrar", "buscar", "localizar", "procurar", 
                  "como", "ajude-me", "de", "para", "um", "uma", "uns", "umas", "o", "a", "os", "as"]
    
    cleaned_words = []
    for word in words:
        word_lower = word.lower().strip(',.?!:;"\'')
        if word_lower not in skip_words and len(word) > 2:
            cleaned_words.append(word)
    
    # Identificar frases relevantes (2-3 palavras consecutivas)
    phrases = []
    for i in range(len(cleaned_words) - 1):
        if len(cleaned_words[i]) > 3 and len(cleaned_words[i+1]) > 3:
            phrases.append(f'"{cleaned_words[i]} {cleaned_words[i+1]}"')
    
    # Para sequências de 3 palavras
    for i in range(len(cleaned_words) - 2):
        if all(len(cleaned_words[i+j]) > 3 for j in range(3)):
            phrases.append(f'"{cleaned_words[i]} {cleaned_words[i+1]} {cleaned_words[i+2]}"')
    
    # Determinar tipo de documento com base nas palavras-chave
    doc_types = []
    doc_type_keywords = {
        "edital": ["edital", "licitação", "pregão", "concorrência", "tomada de preço"],
        "currículo": ["currículo", "curriculum", "cv", "resume"],
        "relatório": ["relatório", "report", "análise", "análise técnica"],
        "artigo": ["artigo", "paper", "científico", "acadêmico", "publicação"],
        "manual": ["manual", "guia", "instrução", "procedimento", "tutorial"],
        "apresentação": ["apresentação", "slides", "powerpoint", "palestra"],
        "código": ["código", "source", "código fonte", "programa", "script"],
        "planilha": ["planilha", "excel", "cálculo", "financeiro", "orçamento"]
    }
    
    for word in cleaned_words:
        for doc_type, keywords in doc_type_keywords.items():
            if word.lower() in keywords:
                doc_types.append(doc_type)
    
    # Construir consulta otimizada com base no contexto e tipo de documento
    
    # Se for relacionado à cibersegurança, usar dorks específicos
    if is_cybersec_related:
        # Identificar tipos de alvos de cibersegurança
        targets = []
        target_keywords = {
            "admin": ["admin", "administração", "administrador", "dashboard", "painel"],
            "config": ["config", "configuração", "configurações", "setup"],
            "login": ["login", "entrar", "acesso", "senha", "password"],
            "database": ["database", "banco de dados", "db", "dump", "backup"],
            "servidor": ["servidor", "server", "host", "hospedagem", "vps"],
            "rede": ["rede", "network", "intranet", "vpn"]
        }
        
        for word in cleaned_words:
            for target_type, keywords in target_keywords.items():
                if word.lower() in keywords:
                    targets.append(target_type)
        
        # Construir dork específico de cibersegurança
        if "admin" in targets:
            optimized = 'intitle:"index of" | intitle:"admin" | intitle:"login" | inurl:admin | inurl:login'
            if phrases:
                optimized += f' ({" OR ".join(phrases[:2])})'
                
        elif "config" in targets:
            optimized = 'intitle:"index of" intext:config | intext:configuration | filetype:conf | filetype:env | filetype:ini'
            if phrases:
                optimized += f' ({" OR ".join(phrases[:2])})'
                
        elif "login" in targets:
            optimized = 'inurl:login | inurl:signin | intitle:"login" | intitle:"sign in"'
            if phrases:
                optimized += f' ({" OR ".join(phrases[:2])})'
                
        elif "database" in targets:
            optimized = 'filetype:sql "CREATE TABLE" | intitle:"index of" intext:backup | intitle:"index of" intext:dump'
            if phrases:
                optimized += f' ({" OR ".join(phrases[:2])})'
                
        else:
            # Dork genérico de cibersegurança
            optimized = 'intitle:"index of" | intext:password | inurl:config'
            if phrases:
                optimized += f' ({" OR ".join(phrases[:2])})'
        
        # Adicionar exclusões comuns de segurança
        optimized += ' -404 -403 -401'
        
    else:
        # Construção de dork normal (não relacionado à cibersegurança)
        
        # Aplicar site: se for busca governamental
        gov_keywords = ["prefeitura", "governo", "municipal", "público", "oficial", "gov"]
        needs_gov_site = any(kw in query.lower() for kw in gov_keywords)
        
        if needs_gov_site:
            optimized += 'site:gov.br '
        
        # Se tiver tipo de documento específico, usar intitle
        if doc_types:
            optimized += f'intitle:"{doc_types[0]}" '
        
        # Adicionar frases importantes
        if phrases:
            optimized += " ".join(phrases[:3]) + " "
        
        # Se não tiver frases ou termos específicos suficientes, adicionar palavras-chave
        if len(phrases) < 2:
            important_keywords = [word for word in cleaned_words 
                                 if len(word) > 4 and word.lower() not in [p.replace('"', '') for p in phrases]]
            
            if important_keywords:
                optimized += " ".join(important_keywords[:4]) + " "
        
        # Adicionar contexto específico
        if context == "licitacoes":
            optimized += '("edital" OR "licitação" OR "pregão") '
        elif context == "legislacao":
            optimized += '("lei municipal" OR "decreto" OR "portaria") '
        elif context == "documentos":
            optimized += '("ofício" OR "memorando" OR "circular") '
            
        # Verificar se há menção a períodos ou datas
        date_terms = ["último", "últimos", "recente", "recentes", "atual", "atuais", 
                      "janeiro", "fevereiro", "março", "abril", "maio", "junho", 
                      "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
                      "2024", "2025"]
        
        has_date = any(date_term in query.lower() for date_term in date_terms)
        
        if has_date:
            if "último" in query.lower() or "últimos" in query.lower():
                if "mês" in query.lower() or "meses" in query.lower():
                    # Extrair número de meses
                    for i, word in enumerate(words):
                        if word.lower() in ["último", "últimos"] and i+1 < len(words) and words[i+1].isdigit():
                            months = int(words[i+1])
                            today = datetime.datetime.now()
                            past_date = today - datetime.timedelta(days=months*30)
                            optimized += f'after:{past_date.strftime("%Y-%m-%d")} '
                            break
                    else:
                        # Se não encontrou número específico, assume 3 meses
                        optimized += 'after:2025-02-07 '
            elif "2024" in query or "2025" in query:
                optimized += 'after:2024-01-01 '
    
    # Sempre adicionar o tipo de arquivo, se especificado
    if file_type:
        optimized += f'filetype:{file_type} '
    else:
        # Se for currículo e não tiver filetype, adicionar PDF
        if "currículo" in query.lower() or "curriculum" in query.lower() or "cv" in query.lower():
            optimized += 'filetype:pdf '
        # Se for edital, adicionar PDF
        elif "edital" in query.lower() or "licitação" in query.lower():
            optimized += 'filetype:pdf '
    
    # Adicionar exclusões comuns
    optimized += '-modelo -exemplo'
    
    # Limpar espaços extras
    optimized = ' '.join(optimized.split())
    
    app.logger.info(f"Consulta otimizada com algoritmo básico: {optimized[:50]}...")
    return optimized

def generate_explanation(query):
    """
    Gera uma explicação detalhada dos operadores utilizados na consulta
    """
    explanation = []
    
    if 'site:' in query:
        explanation.append("site: - Restringe a busca a domínios ou sites específicos")
    
    if 'filetype:' in query or 'ext:' in query:
        explanation.append("filetype: - Busca apenas arquivos de um tipo específico (PDF, DOC, etc.)")
    
    if 'intitle:' in query:
        explanation.append("intitle: - Busca páginas que tenham a palavra especificada no título")
    
    if 'inurl:' in query:
        explanation.append("inurl: - Busca páginas que tenham a palavra especificada na URL")
    
    if 'intext:' in query:
        explanation.append("intext: - Busca páginas que tenham a palavra especificada no corpo do texto")
    
    if '"' in query:
        explanation.append('"termo exato" - Busca pela frase ou expressão exata entre aspas')
    
    if ' -' in query:
        explanation.append("-termo - Exclui páginas que contenham o termo específico")
    
    if ' OR ' in query or ' | ' in query:
        explanation.append("OR ou | - Operador booleano que busca resultados contendo um termo OU outro")
    
    if 'after:' in query:
        explanation.append("after: - Filtra resultados por data, mostrando apenas conteúdo publicado após a data especificada")
    
    if 'before:' in query:
        explanation.append("before: - Filtra resultados por data, mostrando apenas conteúdo publicado antes da data especificada")
    
    if 'index of' in query:
        explanation.append("index of - Busca por diretórios listados em servidores web (útil para encontrar arquivos diretamente)")
    
    if is_cybersecurity_dork(query):
        explanation.append("Esta consulta usa técnicas avançadas de Google Dorks voltadas para análise de segurança, como busca por páginas de login, arquivos de configuração e possíveis vulnerabilidades.")
    
    if not explanation:
        explanation.append("Esta consulta utiliza termos simples combinados para otimizar os resultados de busca.")
    
    return explanation

def is_cybersecurity_dork(query):
    """
    Verifica se a consulta é relacionada à cibersegurança
    """
    cybersec_indicators = [
        "inurl:admin", 
        "inurl:login", 
        "inurl:config", 
        "inurl:backup",
        "intitle:index.of",
        "filetype:conf", 
        "filetype:env", 
        "filetype:sql",
        "filetype:log",
        "filetype:ini",
        "password",
        "-401", "-403", "-404"
    ]
    
    return any(indicator in query.lower() for indicator in cybersec_indicators)

# Rotas da aplicação
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search_tool():
    return render_template('search.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

# Adicionar ao arquivo app.py após as outras rotas e antes do bloco if __name__ == '__main__':

# Rota para o manual de Google Dorks em PDF
@app.route('/manual')
def manual_pdf():
    """
    Rota para fornecer informações sobre o Manual de Google Dorks
    """
    # O manual já está disponível no sistema
    return render_template('manual.html')

# Rota para download do manual em PDF
@app.route('/manual/download')
def download_manual():
    """
    Rota para download direto do manual em PDF
    """
    try:
        # O caminho correto onde o manual está armazenado
        return send_from_directory(
            directory='docs/manual',
            path='Google_Dorks.pdf',
            as_attachment=True,
            download_name='Manual_Completo_Google_Dorks_Ciberseguranca.pdf'
        )
    except FileNotFoundError:
        app.logger.error("Tentativa de download do manual falhou - arquivo não encontrado")
        abort(404)

@app.route('/api/optimize', methods=['POST'])
def optimize_query():
    data = request.json
    query = data.get('query', '')
    file_type = data.get('file_type', '')
    context = data.get('context', '')
    
    if not query:
        return jsonify({"error": "Consulta vazia"}), 400
    
    # Limitar tamanho da consulta para prevenir abusos
    if len(query) > 1000:
        return jsonify({"error": "Consulta muito longa"}), 400
    
    try:
        # Otimizar a consulta usando IA
        optimized_query = optimize_query_with_gemini(query, file_type, context)
        
        # Se ocorrer um erro na API, retornar uma mensagem amigável
        if optimized_query.startswith("Erro"):
            app.logger.warning(f"Fallback para algoritmo básico devido a erro: {optimized_query}")
            # Plano B: Aplicar regras básicas de otimização sem IA
            optimized_query = basic_query_optimization(query, file_type, context)
            
        # Gerar a URL do Google com a consulta otimizada
        google_search_url = f"https://www.google.com/search?q={optimized_query.replace(' ', '+')}"
        
        # Gerar uma explicação dos operadores usados
        explanation = generate_explanation(optimized_query)
        
        return jsonify({
            "original_query": query,
            "optimized_query": optimized_query,
            "search_url": google_search_url,
            "explanation": explanation
        })
    except Exception as e:
        app.logger.error(f"Erro ao processar a consulta: {str(e)}")
        return jsonify({
            "error": "Erro ao processar a consulta. Por favor, tente novamente."
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Rota para verificar a saúde do sistema
@app.route('/health')
def health_check():
    try:
        # Verificar se pode acessar a API do Gemini
        response = requests.get(
            f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}",
            timeout=5
        )
        
        api_status = "ok" if response.status_code == 200 else f"error: {response.status_code}"
        
        return jsonify({
            "status": "ok",
            "api_gemini": api_status,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.2.0"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 500

if __name__ == '__main__':
    app.logger.info("Iniciando aplicação DorkOptimizer...")
    app.run(debug=True)