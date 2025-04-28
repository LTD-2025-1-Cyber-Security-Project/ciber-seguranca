# Instruções para Criação do Executável

A partir do script `run.py` fornecido, você pode criar um arquivo executável para facilitar a distribuição e execução do sistema. O executável encapsulará todo o código Python e dependências necessárias em um único arquivo.

## Pré-requisitos

Antes de criar o executável, certifique-se de ter todas as dependências instaladas:

```bash
pip install pyinstaller
pip install -r requirements.txt
```

## Criação do Executável

Para criar um executável único contendo todos os arquivos necessários, use o seguinte comando:

```bash
pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" run.py
```

Se você tiver arquivos de dados adicionais, como o arquivo mencionado `checklist_data.json`, adicione-o da seguinte forma:

```bash
pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" --add-data "checklist_data.json:." run.py
```

### Observações Importantes

1. **Sintaxe específica para Windows**: Se você estiver no Windows, a sintaxe do comando `--add-data` é ligeiramente diferente:

   ```bash
   pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" run.py
   ```

   Note o uso de ponto-e-vírgula (`;`) em vez de dois-pontos (`:`) como separador.

2. **Tempo de construção**: A criação do executável pode levar alguns minutos, dependendo do tamanho do projeto e das dependências.

3. **Tamanho do executável**: O executável resultante será relativamente grande (pode exceder 100MB) porque incluirá o interpretador Python e todas as bibliotecas necessárias.

## Localização do Executável

Após a conclusão do comando, o executável será encontrado na pasta `dist/` criada no diretório atual:

```
dist/run.exe       # No Windows
dist/run           # No Linux/macOS
```

## Executando o Aplicativo

Simplesmente clique duas vezes no executável ou execute-o a partir da linha de comando:

```bash
./dist/run         # No Linux/macOS
dist\run.exe       # No Windows
```

O executável irá:
1. Criar a estrutura de diretórios necessária
2. Inicializar o banco de dados
3. Criar um usuário administrador (se não existir)
4. Iniciar o servidor web Flask
5. Abrir automaticamente o navegador no endereço http://127.0.0.1:5000/

## Resolução de Problemas

Se encontrar problemas ao criar ou executar o arquivo:

1. **Dependências faltando**: Certifique-se de que todas as dependências estão instaladas
2. **Erros de importação**: Verifique se todos os módulos personalizados estão sendo importados corretamente
3. **Erros de caminho**: O PyInstaller pode ter problemas com caminhos absolutos; use caminhos relativos

Para debugging mais detalhado, você pode adicionar a flag `--debug=all` ao comando do PyInstaller:

```bash
pyinstaller --debug=all --onefile --add-data "templates:templates" --add-data "static:static" run.py
```