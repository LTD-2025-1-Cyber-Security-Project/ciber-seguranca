import re
import zxcvbn
import requests
import hashlib
from typing import Dict, List, Any

class PasswordSecurityChecker:
    def __init__(self):
        """
        Sistema Profissional de Verificação de Senhas
        """
        self.senhas_proibidas = [
            "prefeitura", "municipal", "admin", 
            "123456", "password", "senhapadrao",
            "qwerty", "123123", "abc123"
        ]

    def validar_senha(self, senha: str) -> Dict[str, Any]:
        """
        Validação avançada de força e segurança da senha
        
        :param senha: Senha a ser validada
        :return: Dicionário com resultados da validação
        """
        # Verificação de força usando zxcvbn
        resultado_zxcvbn = zxcvbn.zxcvbn(senha)
        
        # Configurações de requisitos
        requisitos = {
            "comprimento_minimo": 12,
            "caracteres_especiais": 2,
            "numeros_minimos": 2,
            "maiusculas_minimas": 1
        }
        
        resultados = {
            'valida': True,
            'score': resultado_zxcvbn['score'],
            'tempo_crack': self._calcular_tempo_crack(resultado_zxcvbn['crack_times_seconds']['online_no_throttling_10_per_second']),
            'feedback': resultado_zxcvbn['feedback']['suggestions'],
            'avisos': []
        }
        
        # Verificações detalhadas
        if len(senha) < requisitos["comprimento_minimo"]:
            resultados['valida'] = False
            resultados['avisos'].append(
                f"Senha muito curta. Mínimo: {requisitos['comprimento_minimo']} caracteres"
            )
        
        # Contagem de caracteres especiais
        especiais = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', senha))
        if especiais < requisitos['caracteres_especiais']:
            resultados['valida'] = False
            resultados['avisos'].append(
                f"Insuficientes caracteres especiais. Mínimo: {requisitos['caracteres_especiais']}"
            )
        
        # Contagem de números
        numeros = len(re.findall(r'\d', senha))
        if numeros < requisitos['numeros_minimos']:
            resultados['valida'] = False
            resultados['avisos'].append(
                f"Insuficientes números. Mínimo: {requisitos['numeros_minimos']}"
            )
        
        # Contagem de letras maiúsculas
        maiusculas = len(re.findall(r'[A-Z]', senha))
        if maiusculas < requisitos['maiusculas_minimas']:
            resultados['valida'] = False
            resultados['avisos'].append(
                f"Insuficientes letras maiúsculas. Mínimo: {requisitos['maiusculas_minimas']}"
            )
        
        # Verificar senhas proibidas
        if (senha.lower() in self.senhas_proibidas or 
            any(proibida in senha.lower() for proibida in self.senhas_proibidas)):
            resultados['valida'] = False
            resultados['avisos'].append("Senha muito comum ou proibida")
        
        return resultados

    def _calcular_tempo_crack(self, segundos: float) -> str:
        """
        Converte tempo de crack em formato legível
        
        :param segundos: Tempo em segundos
        :return: Descrição do tempo de crack
        """
        if segundos < 1:
            return "Menos de 1 segundo"
        elif segundos < 60:
            return f"{int(segundos)} segundos"
        elif segundos < 3600:
            minutos = int(segundos / 60)
            return f"{minutos} minutos"
        elif segundos < 86400:
            horas = int(segundos / 3600)
            return f"{horas} horas"
        elif segundos < 31536000:
            dias = int(segundos / 86400)
            return f"{dias} dias"
        else:
            anos = int(segundos / 31536000)
            return f"{anos} anos"

    def gerar_senha_forte(self, comprimento: int = 16) -> str:
        """
        Gera senha forte usando métodos criptográficos
        
        :param comprimento: Comprimento da senha
        :return: Senha gerada
        """
        import secrets
        import string
        
        # Conjuntos de caracteres
        letras_minusculas = string.ascii_lowercase
        letras_maiusculas = string.ascii_uppercase
        digitos = string.digits
        especiais = "!@#$%^&*(),.?\":{}|<>"
        
        # Garantir pelo menos um caractere de cada tipo
        senha = [
            secrets.choice(letras_maiusculas),
            secrets.choice(letras_minusculas),
            secrets.choice(digitos),
            secrets.choice(especiais)
        ]
        
        # Completar o resto da senha
        todos_caracteres = letras_minusculas + letras_maiusculas + digitos + especiais
        senha.extend(
            secrets.choice(todos_caracteres) 
            for _ in range(comprimento - len(senha))
        )
        
        # Embaralhar a senha
        secrets.SystemRandom().shuffle(senha)
        
        return ''.join(senha)

    def verificar_senhas_comprometidas(self, email: str) -> Dict[str, Any]:
        """
        Verifica se um email foi comprometido em vazamentos de dados
        
        :param email: Endereço de email para verificação
        :return: Dicionário com informações de vazamentos
        """
        try:
            # Implementação usando a API HaveIBeenPwned
            hash_email = hashlib.sha1(email.lower().encode()).hexdigest()
            
            # Usar apenas os 5 primeiros caracteres do hash para API
            prefixo_hash = hash_email[:5].upper()
            
            # Consultar API
            response = requests.get(
                f"https://api.pwnedpasswords.com/range/{prefixo_hash}"
            )
            
            if response.status_code == 200:
                # Processar lista de hashes
                hashes_comprometidos = {
                    linha.split(':')[0]: int(linha.split(':')[1])
                    for linha in response.text.splitlines()
                }
                
                # Verificar se o hash completo existe
                hash_completo = hash_email[5:].upper()
                
                if hash_completo in hashes_comprometidos:
                    return {
                        'comprometido': True,
                        'vezesComprometido': hashes_comprometidos[hash_completo],
                        'recomendacoes': [
                            "Altere a senha imediatamente",
                            "Não reutilize esta senha em outros serviços",
                            "Considere usar um gerenciador de senhas"
                        ]
                    }
                
                return {
                    'comprometido': False,
                    'recomendacoes': [
                        "Sua senha não foi encontrada em vazamentos conhecidos",
                        "Continue praticando boas políticas de segurança"
                    ]
                }
            
            return {
                'erro': 'Falha na verificação',
                'recomendacoes': [
                    "Verifique sua conexão de internet",
                    "Tente novamente mais tarde"
                ]
            }
        
        except Exception as e:
            return {
                'erro': str(e),
                'recomendacoes': [
                    "Erro ao verificar senhas comprometidas",
                    "Verifique sua conexão de internet"
                ]
            }