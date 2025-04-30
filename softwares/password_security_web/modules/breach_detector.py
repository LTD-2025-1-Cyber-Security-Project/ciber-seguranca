import os
import re
import json
import requests
import logging
import hashlib
from typing import Dict, List, Any
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

class BreachDetector:
    def __init__(self):
        """
        Sistema de Detecção de Vazamentos de Dados
        """
        # Configurações de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='breach_detector.log'
        )
        
        # Configurações de API
        self.fontes_verificacao = [
            self._verificar_hibp_api_v3,
            self._verificar_hibp_api_v2,
            self._verificar_vazamentos_mock
        ]
    
    def validar_email(self, email: str) -> bool:
        """
        Valida formato do email
        
        :param email: Email para validação
        :return: Booleano indicando validade
        """
        try:
            # Validação RFC usando email_validator
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def _gerar_hash_email(self, email: str) -> str:
        """
        Gera hash SHA-1 do email
        
        :param email: Email para gerar hash
        :return: Hash SHA-1 do email
        """
        return hashlib.sha1(email.lower().encode('utf-8')).hexdigest()
    
    def _verificar_hibp_api_v3(self, email: str) -> Dict[str, Any]:
        """
        Verificação usando API v3 do HaveIBeenPwned
        
        :param email: Email para verificação
        :return: Dicionário de resultados
        """
        try:
            # Chave de API (substitua pela sua chave)
            api_key = os.getenv('HIBP_API_KEY', '')
            
            headers = {
                'User-Agent': 'CyberSecurityMunicipal/1.0',
                'hibp-api-key': api_key
            }
            
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                dados_vazamentos = response.json()
                return {
                    'comprometido': True,
                    'total_vazamentos': len(dados_vazamentos),
                    'detalhes_vazamentos': [
                        {
                            'nome': vazamento.get('Name', 'Desconhecido'),
                            'data': vazamento.get('BreachDate', 'Data não disponível'),
                            'tipos_dados': vazamento.get('DataClasses', [])
                        } for vazamento in dados_vazamentos
                    ]
                }
            
            return None
        
        except Exception as e:
            logging.warning(f"Erro na verificação HIBP API v3: {e}")
            return None
    
    def _verificar_hibp_api_v2(self, email: str) -> Dict[str, Any]:
        """
        Verificação usando API v2 do HaveIBeenPwned (sem chave)
        
        :param email: Email para verificação
        :return: Dicionário de resultados
        """
        try:
            # Hash do email para API v2
            hash_email = self._gerar_hash_email(email)
            
            # Usar apenas os 5 primeiros caracteres
            prefixo_hash = hash_email[:5]
            
            # Consultar API
            url = f"https://api.pwnedpasswords.com/range/{prefixo_hash}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Processar lista de hashes
                hashes = response.text.splitlines()
                hash_completo = hash_email[5:].upper()
                
                # Verificar se o hash está na lista
                for linha in hashes:
                    partes = linha.split(':')
                    if partes[0] == hash_completo:
                        # Encontrado em vazamentos
                        return {
                            'comprometido': True,
                            'total_vazamentos': int(partes[1]),
                            'detalhes_vazamentos': [
                                {
                                    'nome': 'Vazamento não especificado',
                                    'data': 'Data não disponível',
                                    'tipos_dados': ['Email', 'Credenciais']
                                }
                            ]
                        }
                
                return None
            
            return None
        
        except Exception as e:
            logging.warning(f"Erro na verificação HIBP API v2: {e}")
            return None
    
    def _verificar_vazamentos_mock(self, email: str) -> Dict[str, Any]:
        """
        Método mockup de verificação de vazamentos
        
        :param email: Email para verificação
        :return: Dicionário de resultados
        """
        # Lista de domínios conhecidos por vazamentos
        dominios_vazados = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 
            'outlook.com', 'facebook.com'
        ]
        
        try:
            # Verificação simples baseada em domínio
            dominio = email.split('@')[-1].lower()
            
            if dominio in dominios_vazados:
                return {
                    'comprometido': True,
                    'total_vazamentos': 1,
                    'detalhes_vazamentos': [
                        {
                            'nome': f'Vazamento genérico - {dominio}',
                            'data': datetime.now().strftime('%Y-%m-%d'),
                            'tipos_dados': ['Email', 'Possivelmente Credenciais']
                        }
                    ]
                }
            
            return None
        
        except Exception as e:
            logging.warning(f"Erro na verificação mockup: {e}")
            return None

    def analisar_senhas_comprometidas(self, email: str) -> Dict[str, Any]:
        """
        Análise detalhada de senhas comprometidas para um email
        
        :param email: Email para verificação
        :return: Dicionário com informações de vazamentos
        """
        # Validar email
        if not self.validar_email(email):
            return {
                'erro': 'Email inválido',
                'recomendacoes': [
                    "Verifique o formato do email digitado",
                    "Use um endereço de email válido"
                ]
            }
        
        # Tentar diferentes métodos de verificação
        for metodo in self.fontes_verificacao:
            try:
                resultado = metodo(email)
                
                if resultado:
                    return {
                        'comprometido': resultado.get('comprometido', False),
                        'total_vazamentos': resultado.get('total_vazamentos', 0),
                        'detalhes_vazamentos': resultado.get('detalhes_vazamentos', []),
                        'recomendacoes': [
                            "Altere imediatamente suas senhas",
                            "Não reutilize senhas em diferentes serviços",
                            "Ative autenticação de dois fatores",
                            "Monitore atividades suspeitas"
                        ]
                    }
            
            except Exception as e:
                logging.warning(f"Erro em método de verificação: {e}")
        
        # Se nenhum método encontrar vazamentos
        return {
            'comprometido': False,
            'recomendacoes': [
                "Nenhum vazamento encontrado para este email",
                "Continue praticando boas políticas de segurança"
            ]
        }
    
    def buscar_vazamentos_recentes(self) -> List[Dict[str, Any]]:
        """
        Busca informações sobre vazamentos de dados recentes
        
        :return: Lista de vazamentos encontrados
        """
        try:
            # URLs de fontes de notícias de segurança
            urls = [
                "https://www.bleepingcomputer.com/news/security/data-breaches/",
                "https://techcrunch.com/security/"
            ]
            
            # Headers para requisições
            headers = {
                'User-Agent': 'CyberSecurityMunicipal/1.0'
            }
            
            vazamentos = []
            
            for url in urls:
                try:
                    # Fazer requisição
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        # Processar conteúdo (exemplo simplificado)
                        linhas = response.text.split('\n')
                        
                        # Buscar padrões de vazamentos
                        padroes_vazamento = [
                            r'data breach',
                            r'leaked data',
                            r'security incident'
                        ]
                        
                        for linha in linhas[:50]:  # Limitar linhas para performance
                            for padrao in padroes_vazamento:
                                if re.search(padrao, linha, re.IGNORECASE):
                                    vazamento = {
                                        'titulo': linha[:100],  # Limitar tamanho
                                        'descricao': 'Potencial vazamento de dados',
                                        'link': url
                                    }
                                    vazamentos.append(vazamento)
                                    break
                    
                except requests.exceptions.RequestException as e:
                    logging.warning(f"Erro ao buscar vazamentos em {url}: {e}")
            
            return vazamentos[:5]  # Limitar a 5 vazamentos
        
        except Exception as e:
            logging.error(f"Erro ao buscar vazamentos recentes: {e}")
            return []

# Exemplo de uso
if __name__ == '__main__':
    detector = BreachDetector()
    
    # Teste de verificação de email
    emails_teste = [
        'teste@exemplo.com',
        'usuario_invalido',
        'exemplo@dominio.com'
    ]
    
    for email in emails_teste:
        print(f"\nAnalisando {email}:")
        resultado = detector.analisar_senhas_comprometidas(email)
        print(json.dumps(resultado, indent=2))