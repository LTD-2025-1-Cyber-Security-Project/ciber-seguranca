# Documentação: Checklist Mensal de Segurança da Informação

## Índice
1. [Introdução](#introdução)
2. [Visão Geral do Sistema](#visão-geral-do-sistema)
3. [Requisitos do Sistema](#requisitos-do-sistema)
4. [Instalação](#instalação)
5. [Estrutura do Aplicativo](#estrutura-do-aplicativo)
6. [Funcionalidades](#funcionalidades)
7. [Interface do Usuário](#interface-do-usuário)
8. [Fluxo de Trabalho](#fluxo-de-trabalho)
9. [Armazenamento de Dados](#armazenamento-de-dados)
10. [Extensão e Personalização](#extensão-e-personalização)
11. [Solução de Problemas](#solução-de-problemas)
12. [Perguntas Frequentes](#perguntas-frequentes)
13. [Contato e Suporte](#contato-e-suporte)

## Introdução

O **Checklist Mensal de Segurança da Informação** é uma aplicação desenvolvida para auxiliar servidores públicos e funcionários internos na realização de verificações periódicas de segurança da informação, garantindo conformidade com normas e regulamentações, incluindo a LGPD (Lei Geral de Proteção de Dados) e os padrões ISO.

Este aplicativo transforma o processo tradicional de verificação em papel em uma solução digital interativa que permite:
- Realizar verificações sistemáticas de segurança da informação
- Acompanhar o progresso das verificações
- Gerar relatórios detalhados
- Manter histórico de conformidade para fins de auditoria

O sistema foi projetado com base nos três pilares fundamentais da segurança da informação:
- **Confidencialidade**: Garantia de que apenas pessoas autorizadas acessem informações sensíveis
- **Integridade**: Preservação da precisão e completude dos dados
- **Disponibilidade**: Garantia de acesso aos sistemas quando necessário

## Visão Geral do Sistema

O aplicativo é construído usando a estrutura Flask, um microframework web Python, e fornece uma interface de usuário baseada em navegador para interagir com o checklist de segurança. O sistema é empacotado como um executável independente, permitindo fácil distribuição e uso sem requisitos adicionais de instalação.

### Componentes Principais

1. **Interface Web**: Fornece acesso ao checklist através de qualquer navegador web moderno
2. **Motor Flask**: Gerencia a lógica do aplicativo e o processamento de dados
3. **Sistema de Armazenamento**: Mantém os dados do checklist em arquivos JSON locais
4. **Gerador de Relatórios**: Produz relatórios detalhados de conformidade

## Requisitos do Sistema

### Requisitos Mínimos
- **Sistema Operacional**: Windows 10/11, macOS 10.14+, ou Linux (distribuições modernas)
- **Navegador Web**: Chrome, Firefox, Edge, Safari (versões atualizadas)
- **Armazenamento**: 50MB de espaço em disco
- **Memória**: 256MB RAM

### Requisitos Recomendados
- **Sistema Operacional**: Windows 10/11, macOS 11+, ou Ubuntu 20.04+
- **Navegador Web**: Chrome ou Firefox (últimas duas versões)
- **Armazenamento**: 100MB de espaço em disco
- **Memória**: 512MB RAM

## Instalação

### Uso do Executável (Recomendado)

1. Faça o download do arquivo executável apropriado para o seu sistema operacional
2. Execute o arquivo baixado
   - **Windows**: Dê dois cliques no arquivo `.exe`
   - **macOS**: Dê dois cliques no arquivo `.app`
   - **Linux**: Execute o arquivo binário através do terminal ou gerenciador de arquivos

O aplicativo iniciará automaticamente e abrirá a interface em seu navegador padrão.

### Instalação a partir do Código-Fonte

Para desenvolvedores ou usuários avançados que desejam personalizar ou estender o aplicativo:

1. **Pré-requisitos**:
   - Python 3.8 ou superior
   - pip (gerenciador de pacotes Python)

2. **Instalação de Dependências**:
   ```bash
   pip install flask pyinstaller
   ```

3. **Clone do Repositório**:
   ```bash
   git clone https://github.com/sua-organizacao/checklist-seguranca.git
   cd checklist-seguranca
   ```

4. **Execução do Aplicativo**:
   ```bash
   python run.py
   ```

5. **Criação do Executável** (opcional):
   ```bash
   pyinstaller --onefile run.py
   ```

## Estrutura do Aplicativo

### Arquivos Principais

- **app.py**: Contém a lógica principal do aplicativo Flask
- **run.py**: Script para iniciar o aplicativo e abrir automaticamente o navegador
- **data/checklist_data.json**: Armazena o estado do checklist (criado automaticamente)

### Estrutura de Diretórios

```
checklist-seguranca/
├── app.py                  # Aplicativo Flask principal
├── run.py                  # Script de inicialização
├── data/                   # Diretório para armazenamento de dados
│   └── checklist_data.json # Dados do checklist (criado automaticamente)
├── dist/                   # Diretório com executáveis (após compilação)
├── build/                  # Arquivos temporários de compilação
└── README.md               # Documentação básica
```

## Funcionalidades

### 1. Checklist Interativo

- Checklist organizado em seções temáticas
- Marcação de itens verificados com atualização em tempo real
- Cálculo automático de progresso
- Persistência de estado entre sessões

### 2. Geração de Relatórios

- Criação de relatórios detalhados de conformidade
- Estatísticas por seção e global
- Recomendações baseadas nos níveis de conformidade
- Versão para impressão com formatação otimizada

### 3. Gerenciamento de Sessão

- Armazenamento automático do progresso
- Capacidade de reiniciar o checklist quando necessário
- Rastreamento de data de verificação

### 4. Interface Responsiva

- Adaptação a diferentes tamanhos de tela
- Compatibilidade com dispositivos móveis e desktop
- Design intuitivo e amigável

## Interface do Usuário

### Tela Inicial

A tela inicial apresenta uma introdução ao sistema de checklist, destacando:
- Propósito e importância do checklist
- Princípios fundamentais de segurança da informação
- Instruções básicas de uso
- Botão de início da verificação

### Checklist Principal

A tela de checklist contém:
- Barra de progresso global
- Seções organizadas em acordeões expansíveis
- Itens de verificação com caixas de seleção
- Referências normativas para cada item
- Botões de ação no rodapé fixo

### Tela de Relatório

O relatório gerado inclui:
- Resumo da verificação com data
- Estatísticas de conformidade geral
- Detalhamento por seção
- Recomendações baseadas no nível de conformidade
- Espaço para assinaturas (relatório impresso)
- Opções para imprimir ou voltar ao checklist

## Fluxo de Trabalho

### Processo de Verificação Mensal

1. **Preparação**: O usuário inicia o aplicativo no primeiro dia útil do mês
2. **Verificação**: O usuário percorre cada seção do checklist, marcando os itens conformes
3. **Revisão**: Após completar todas as seções, o usuário revisa o progresso geral
4. **Geração de Relatório**: O usuário gera um relatório detalhado
5. **Documentação**: O relatório é impresso ou salvo para fins de auditoria
6. **Ação**: Itens não conformes são encaminhados para resolução

## Armazenamento de Dados

### Formato de Dados

Os dados do checklist são armazenados em formato JSON na seguinte estrutura:

```json
{
  "1.1": true,
  "1.2": false,
  "1.3": true,
  "1.4": true,
  "2.1": false,
  "2.2": true
  // ... outros itens
}
```

Onde a chave representa o ID do item e o valor booleano indica se o item foi verificado.

### Localização dos Dados

- **Versão Executável**: Os dados são armazenados no diretório `data` relativo ao local do executável
- **Versão Desenvolvimento**: Os dados são armazenados no diretório `data` no diretório do projeto

## Extensão e Personalização

### Adição de Novas Seções e Itens

Para adicionar mais seções ou itens ao checklist, modifique a variável `CHECKLIST_SECTIONS` no arquivo `app.py`:

```python
CHECKLIST_SECTIONS = [
    {
        "id": 3,  # Novo ID de seção
        "title": "Nova Seção",
        "items": [
            {"id": "3.1", "text": "Novo item de verificação", "ref": "ISO 27002:2022 (X.Y)"},
            {"id": "3.2", "text": "Outro item de verificação", "ref": "LGPD Art. Z"}
        ]
    }
]
```

### Personalização Visual

Para personalizar a aparência do aplicativo, modifique as seções CSS inline nos métodos de renderização HTML:

```python
html = '''
<style>
    .header {
        background-color: #0a2c5c;  /* Altere para a cor da sua organização */
        color: white;
    }
    /* Outros estilos personalizados */
</style>
'''
```

## Solução de Problemas

### Problemas Comuns e Soluções

| Problema | Possível Causa | Solução |
|----------|----------------|---------|
| Aplicativo não inicia | Permissões insuficientes | Execute como administrador |
| Navegador não abre automaticamente | Configuração do navegador padrão | Abra manualmente http://127.0.0.1:5000/ |
| Dados do checklist não são salvos | Problema de permissão de escrita | Verifique permissões do diretório `data` |
| Interface não carrega corretamente | JavaScript desativado | Ative JavaScript no navegador |
| Erro ao gerar relatório | Dados corrompidos | Reinicie o checklist |

### Registro de Erros

Para investigar problemas técnicos, verifique as mensagens de erro no console:

- **Windows**: Execute o aplicativo a partir do Prompt de Comando para ver mensagens
- **macOS/Linux**: Execute a partir do Terminal para visualizar saídas de diagnóstico

## Perguntas Frequentes

**P: Com que frequência devo realizar a verificação?**  
R: Conforme recomendado no documento, a verificação deve ser realizada no primeiro dia útil de cada mês.

**P: Preciso verificar todos os itens de uma vez?**  
R: Não. O aplicativo salva automaticamente seu progresso, permitindo que você continue a verificação posteriormente.

**P: Como posso compartilhar o relatório com o DPO?**  
R: Você pode imprimir o relatório usando a função "Imprimir Relatório" ou salvar como PDF usando a funcionalidade de impressão do navegador.

**P: Os dados ficam salvos para o próximo mês?**  
R: Sim, os dados permanecem salvos. Use o botão "Resetar Checklist" no início do próximo mês para começar uma nova verificação.

**P: Posso personalizar os itens do checklist?**  
R: Sim, desenvolvedores podem modificar o arquivo `app.py` para adicionar, remover ou modificar itens conforme necessário.

## Contato e Suporte

Para suporte técnico ou dúvidas sobre o uso do aplicativo, entre em contato com:
   https://github.com/LTD-2025-1-Cyber-Security-Project/ciberseguranca/tree/delete/main/iso
**Equipe de Segurança da Informação**  
Email: seguranca@suaorganizacao.gov.br  
Telefone: (48) 9 9999-9999

**Encarregado de Proteção de Dados (DPO)**  
Email: contato@LTD-2025-1-Cyber-Security-Project.com.br  
Telefone: (48) 9 9999-9999

---

© 2025 LTD-2025-1-Cyber-Security-Project. Todos os direitos reservados.  
Versão da documentação: 1.0  
Última atualização: 21/04/2025