# Tutorial Completo: Framework de Processamento de Documentos

## Introdução
Este tutorial guiará você passo a passo no uso completo do framework, desde a configuração inicial até operações avançadas. O framework permite processar diversos tipos de documentos (PDF, DOCX, texto, imagens) e gerar documentação estruturada.

## Pré-requisitos
- Python 3.9+
- Dependências instaladas (veja [INSTALACAO.md](INSTALACAO.md))
- Conhecimento básico de linha de comando

## Configuração Inicial
### Arquivo config.yaml
Edite o arquivo de configuração para definir seu fluxo de trabalho:
```yaml
# config.yaml
extractors:
  pdf:
    enabled: true
    ocr_fallback: true  # Usa OCR se texto não extraível
  docx:
    enabled: true
  text:
    enabled: true
  image:
    enabled: true
    languages: ['por', 'eng']  # Idiomas para OCR

chunking:
  strategy: semantic
  max_tokens: 512
  overlap: 0.2
  min_lines: 5

summarization:
  enabled: true
  model: facebook/bart-large-cnn
  max_length: 150

output:
  format: markdown
  directory: docs_output
  include_metadata: true
```

### Estrutura de Diretórios Recomendada
```
projeto/
├── documentos/       # Arquivos de entrada
├── config.yaml       # Configuração
└── src/              # Código fonte
```

## Fluxo Básico de Trabalho
### Passo 1: Preparar Documentos
Coloque seus arquivos na pasta `documentos/`. Exemplo:
- manual.pdf
- contrato.docx
- relatorio.txt
- diagrama.png

### Passo 2: Executar o Pipeline
```bash
python src/main.py --config config.yaml
```

### Passo 3: Analisar Saída
Os arquivos processados serão gerados em `docs_output/`:
```
docs_output/
├── manual_0001.md
├── manual_0002.md
├── contrato_0001.md
└── diagrama_0001.md
```

## Processamento Avançado
### Chunking Semântico
O sistema divide documentos mantendo contexto:
```python
# Exemplo de chunking
from src.core.chunking import SemanticChunker

chunker = SemanticChunker(max_tokens=512, overlap=0.2)
chunks = chunker.chunk_text(long_document)
```

### Sumarização Automática
Gere resumos com modelos de NLP:
```python
from src.core.summarizer import Summarizer

summarizer = Summarizer(model_name="facebook/bart-large-cnn")
summary = summarizer.summarize(text, max_length=150)
```

### Exemplo Completo: Processar Pasta
```python
from src.core.pipeline import DocumentPipeline

pipeline = DocumentPipeline(config_path="config.yaml")
pipeline.process_directory("documentos/")
```

## Casos de Uso
### 1. Documentação Técnica
Processe código-fonte para gerar documentação:
```bash
python src/main.py --input src/ --output docs_code/
```

### 2. Análise de Contratos
Extraia cláusulas importantes de documentos legais:
```yaml
# config-contratos.yaml
chunking:
  strategy: fixed
  size: 200
summarization:
  enabled: true
```

### 3. Processamento em Lote
Use o script `batch_process.py` para grandes volumes:
```bash
python batch_process.py --dir documentos_lote/ --config config.yaml
```

## Solução de Problemas
### Erros Comuns e Soluções
| Problema | Solução |
|----------|---------|
| Falha na extração PDF | Instale `pdfminer.six` e ative OCR |
| Chunks muito pequenos | Aumente `min_lines` no config.yaml |
| Sumarização lenta | Use modelo menor como `t5-small` |
| Codificação inválida | Especifique `encoding` no config.yaml |

### Logs e Monitoramento
Verifique os logs em tempo real:
```bash
tail -f processing.log
```

## Melhores Práticas
1. Use ambiente virtual para evitar conflitos
2. Teste configurações em pequenos lotes primeiro
3. Use cache para processamentos recorrentes
4. Atualize periodicamente as dependências
5. Valide saídas com scripts de teste

## Próximos Passos
- Explore [EXEMPLOS.md](EXEMPLOS.md) para casos avançados
- Consulte [REFERENCIA.md](REFERENCIA.md) para detalhes técnicos
- Reporte problemas no repositório do projeto