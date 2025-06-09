# Instalação e Configuração do Framework

## Pré-requisitos
- Python 3.9 ou superior
- Gerenciador de pacotes pip atualizado
- Ambiente virtual (recomendado)

## Passo 1: Configurar Ambiente Virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
```

## Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

## Passo 3: Instalar Dependências Adicionais
Dependendo dos formatos que deseja processar, instale:

### Para processamento de PDF
```bash
pip install pdfminer.six
```

### Para processamento de DOCX
```bash
pip install python-docx
```

### Para processamento de imagens (OCR)
```bash
pip install pillow pytesseract
```

### Para sumarização avançada
```bash
pip install transformers torch
```

## Passo 4: Configuração Inicial
Edite o arquivo `config.yaml` para definir suas preferências:

```yaml
# Exemplo de configuração
extractors:
  pdf:
    enabled: true
  docx:
    enabled: true
  image:
    enabled: false

chunking:
  max_tokens: 512
  overlap: 0.2

output:
  format: markdown
  directory: docs_output
```

## Passo 5: Execução Inicial
```bash
python src/main.py
```

## Verificação da Instalação
Execute o teste básico para confirmar:
```bash
pytest tests/
```

## Solução de Problemas Comuns
- **Erro de dependência faltante**: Verifique se instalou todos os pacotes necessários
- **Problemas com OCR**: Certifique-se que o Tesseract está instalado no sistema
- **Erros de permissão**: Execute com permissões adequadas ou em ambiente virtual