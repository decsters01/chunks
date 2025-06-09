# Source: REFERENCIA.md
Original Path: `.\REFERENCIA.md`

---
source_file: .\REFERENCIA.md
file_type: .md
file_hash: 47e7bda6b5a6163e580034268b9473e397cad6dca03283a02dd13ad3b7dd80af
chunk_index: 3
total_chunks: 3
content_hash: f01a100a807cebb1b6bdc8d5c167b75114410863dfbf3d29cce07d0d537e719a
summary: 'Dependências Externas: Módulo | Dependêscias |    Dependência |  Módulos
  |  Departamento |  Diagrama de Sequências |  ------ ---- ------------- ---------
  ----—------- --. Document X: DOCX | python-docx |  python- docx | 9.6 | PDF | pdfminer.six
  | PDFMiner.Six | PDF miner. six | PDFminer 6.0 | PDF Miner. 6.6.6 --- --'
timestamp_utc: '2025-06-09T10:23:35.201453+00:00'
---

```
Dependências Externas
| Módulo | Dependências |
|--------|--------------|
| PDF | pdfminer.six |
| DOCX | python-docx |
| Imagens | pytesseract, pillow |
| Sumarização | transformers, torch |
Diagrama de Sequência
```mermaid
sequenceDiagram
    participant Usuário
    participant Main
    participant Pipeline
    participant Extrator
    participant Chunker
    participant Summarizer
    participant Output
Usuário-&gt;&gt;Main: Executa script
Main-&gt;&gt;Pipeline: process_directory()
Pipeline-&gt;&gt;Extrator: extract()
Extrator--&gt;&gt;Pipeline: Texto
Pipeline-&gt;&gt;Chunker: chunk_text()
Chunker--&gt;&gt;Pipeline: Chunks
Pipeline-&gt;&gt;Summarizer: summarize()
Summarizer--&gt;&gt;Pipeline: Resumos
Pipeline-&gt;&gt;Output: write()
Output--&gt;&gt;Pipeline: Confirmação
Pipeline--&gt;&gt;Main: Relatório
Main--&gt;&gt;Usuário: Conclusão
```

---

# Source: TUTORIAL.md
Original Path: `.\TUTORIAL.md`

---
source_file: .\TUTORIAL.md
file_type: .md
file_hash: c3f33e901c2df3b5aa27732120cce1a05133d2fc7e132dba183967478bb7fc86
chunk_index: 1
total_chunks: 2
content_hash: 6c17e49e694ad4004703be6dc4db65649574dda1b4adfbca4df1a9d30c5bcc52
summary: 'Tutorial Completo: Framework de Processamento de Documentos. O framework
  permite processar diversos tipos de documentos (PDF, DOCX, texto, imagens) and gerar
  documentação estruturada. Este tutorial guiará você passo a passo no uso completo.'
timestamp_utc: '2025-06-09T10:23:35.202451+00:00'
---

```
Tutorial Completo: Framework de Processamento de Documentos
Introdução
Este tutorial guiará você passo a passo no uso completo do framework, desde a configuração inicial até operações avançadas. O framework permite processar diversos tipos de documentos (PDF, DOCX, texto, imagens) e gerar documentação estruturada.
Pré-requisitos

Python 3.9+
Dependências instaladas (veja INSTALACAO.md)
Conhecimento básico de linha de comando

Configuração Inicial
Arquivo config.yaml
Edite o arquivo de configuração para definir seu fluxo de trabalho:
```yaml
config.yaml
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
Estrutura de Diretórios Recomendada
projeto/
├── documentos/       # Arquivos de entrada
├── config.yaml       # Configuração
└── src/              # Código fonte
Fluxo Básico de Trabalho
Passo 1: Preparar Documentos
Coloque seus arquivos na pasta documentos/. Exemplo:
- manual.pdf
- contrato.docx
- relatorio.txt
- diagrama.png
Passo 2: Executar o Pipeline
bash
python src/main.py --config config.yaml
Passo 3: Analisar Saída
Os arquivos processados serão gerados em docs_output/:
docs_output/
├── manual_0001.md
├── manual_0002.md
├── contrato_0001.md
└── diagrama_0001.md
Processamento Avançado
Chunking Semântico
O sistema divide documentos mantendo contexto:
```python
Exemplo de chunking
from src.core.chunking import SemanticChunker
chunker = SemanticChunker(max_tokens=512, overlap=0.2)
chunks = chunker.chunk_text(long_document)
```

---

---
source_file: .\TUTORIAL.md
file_type: .md
file_hash: c3f33e901c2df3b5aa27732120cce1a05133d2fc7e132dba183967478bb7fc86
chunk_index: 2
total_chunks: 2
content_hash: 209e3731a18f72a531c86a2ff3da1d9df0f826ef412202a08cf4a79bbbeccbc8
summary: Python's Summarizer is a tool for processing documents. It can be used to
  generate PDFs, e-mails, mails, and other documents. Summarizão de documentação is
  análise de Contratos de documentos legais.
timestamp_utc: '2025-06-09T10:23:35.203448+00:00'
---

```
```
Sumarização Automática
Gere resumos com modelos de NLP:
```python
from src.core.summarizer import Summarizer
summarizer = Summarizer(model_name="facebook/bart-large-cnn")
summary = summarizer.summarize(text, max_length=150)
```
Exemplo Completo: Processar Pasta
```python
from src.core.pipeline import DocumentPipeline
pipeline = DocumentPipeline(config_path="config.yaml")
pipeline.process_directory("documentos/")
```
Casos de Uso
1. Documentação Técnica
Processe código-fonte para gerar documentação:
bash
python src/main.py --input src/ --output docs_code/
2. Análise de Contratos
Extraia cláusulas importantes de documentos legais:
```yaml
config-contratos.yaml
chunking:
  strategy: fixed
  size: 200
summarization:
  enabled: true
```
3. Processamento em Lote
Use o script batch_process.py para grandes volumes:
bash
python batch_process.py --dir documentos_lote/ --config config.yaml
Solução de Problemas
Erros Comuns e Soluções
| Problema | Solução |
|----------|---------|
| Falha na extração PDF | Instale pdfminer.six e ative OCR |
| Chunks muito pequenos | Aumente min_lines no config.yaml |
| Sumarização lenta | Use modelo menor como t5-small |
| Codificação inválida | Especifique encoding no config.yaml |
Logs e Monitoramento
Verifique os logs em tempo real:
bash
tail -f processing.log
Melhores Práticas

Use ambiente virtual para evitar conflitos
Teste configurações em pequenos lotes primeiro
Use cache para processamentos recorrentes
Atualize periodicamente as dependências
Valide saídas com scripts de teste

Próximos Passos

Explore EXEMPLOS.md para casos avançados
Consulte REFERENCIA.md para detalhes técnicos
Reporte problemas no repositório do projeto
```

---

# Source: chunkv3.py
Original Path: `.\chunkv3.py`

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 1
total_chunks: 24
content_hash: d651e25c98507515b167a0da53b0e98c94f7e195971d6dc92b7e99aef3e16516
summary: ' importlib.util  # Adicionado para verificação de instalação. import defaultdict
  import spacyimport timeimport glob. # Função para converter arquivos .py, .json
  e .md para texto puro.'
timestamp_utc: '2025-06-09T10:23:35.204446+00:00'
---

```
import os
import sys  # Adicionado para verificação de instalação
import importlib.util  # Adicionado para verificação robusta
import markdown
import re
import math
import time
import glob  # Adicionado para listagem de arquivos
import concurrent.futures  # Adicionado para processamento paralelo
from collections import defaultdict
import spacy
import importlib.metadata

# Removidas verificações e importações do Docling
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Função para converter arquivos .py, .json e .md para texto puro
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 2
total_chunks: 24
content_hash: 36da9c6b3d1788fb6c526df1756001abebcc554e56279238f8cf54008d213592
summary: 'def convert_to_text(file_path): return plain_text, None. If file_path.endswith(''.md''):
  html = markdown.markdown(content) return content, None, except Exception as e: return
  e, (error_msg, tb)'
timestamp_utc: '2025-06-09T10:23:35.205443+00:00'
---

```
def convert_to_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Converter markdown para texto puro removendo marcações
        if file_path.endswith('.md'):
            html = markdown.markdown(content)
            # Remover tags HTML usando regex
            plain_text = re.sub(r'<[^>]*>', '', html)
            return plain_text, None
        # Para .py e .json, retornar conteúdo diretamente
        return content, None
    except Exception as e:
        import traceback
        error_msg = f"Erro ao converter {file_path}: {str(e)}"
        tb = traceback.format_exc()
        print(f"{error_msg}\n{tb}")
        return "", (error_msg, tb)

# List of text-based file extensions that can be read with UTF-8 encoding
EXTENSOES = ['.py', '.js', '.ts', '.java', '.cs', '.cpp', '.c', '.h', '.hpp',
             '.mq4', '.mq5', '.mqh', '.php', '.rb', '.pl', '.swift', '.go',
             '.rs', '.kt', '.dart', '.scala', '.html', '.css', '.scss', '.less',
             '.xml', '.json', '.yaml', '.yml', '.md', '.txt', '.csv', '.pdf',
             '.docx', '.xlsx', '.pptx', '.jpg', '.png', '.bmp', '.tiff', '.gif']

# List of text-based file extensions for documentation or plain text
EXTENSOES_DOCUMENTACAO = [
    '.txt', '.md', '.rst', '.tex' # Adicionar outras extensões de documentação conforme necessário
]

# Constantes
PASTA_DOCUMENTACAO = 'chat'
MAX_ARQUIVOS_MARKDOWN = 10
FIXED_CHUNK_SIZE_DOCS = 50 # Aumentado para documentos genéricos
MIN_LINES_PER_CODE_BLOCK = 7 # Aumentado para tentar blocos maiores
CHAT_MESSAGES_PER_CHUNK = 10 # Para agrupar mensagens de chat
IGNORED_DIRS = ['.git', 'node_modules', '__pycache__']   # Diretórios a ignorar durante a varredura

MAX_DEPTH = 5  # Profundidade máxima padrão para varredura de diretórios

# Extensões suportadas para processamento
supported_extensions = ['.py', '.json', '.md', '.txt']
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 3
total_chunks: 24
content_hash: 68d793282fcf3a6b34df1572234777f4c4447ee9f09559222918673104230f91
summary: 'def detect_code_blocks(content, file_extension=None): # Determina dinamicamente
  os marcadores de início de chunks. # Mais robusto para código e mais inteligente
  para documentos. # Lógica específica para arquivos de documentação.'
timestamp_utc: '2025-06-09T10:23:35.206440+00:00'
---

```
def detect_code_blocks(content, file_extension=None):
    """
    Determina dinamicamente os marcadores de início de chunks.
    Mais robusto para código e mais inteligente para documentos.
    """
    lines = content.splitlines()
    num_lines = len(lines)
    if num_lines == 0:
        return [0]

    marcadores = {0}

    # --- Lógica específica para arquivos de documentação ---
    doc_type_handler_used = False
    chat_detected = False
    if file_extension and file_extension in EXTENSOES_DOCUMENTACAO:
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 4
total_chunks: 24
content_hash: 979df3fe151100d5f7ead7bba0ecf45f0cb53121224b02bc4ac0153939334b81
summary: '# 1. Tentar detectar CHAT primeiro para qualquer tipo de documento de texto.
  # Nome (opcional HH:MM): mensagem. # Heurística: mais de 3 linhas de chat nas primeiras
  50 for line in lines[:50]: # Analisa as primeir as 50 linhas. # Indica que um handler
  específ is being used.'
timestamp_utc: '2025-06-09T10:23:35.206943+00:00'
---

```
# 1. Tentar detectar CHAT primeiro para qualquer tipo de documento de texto
        chat_pattern = r"^\s*[\w\s.-]+(?:\s*\(\d{2}:\d{2}(?::\d{2})?\))?\s*:\s+" # Nome (opcional HH:MM): mensagem
        chat_occurrences = 0
        for line in lines[:50]: # Analisa as primeiras 50 linhas
            if re.match(chat_pattern, line):
                chat_occurrences += 1
        
        if chat_occurrences > 3: # Heurística: mais de 3 linhas de chat nas primeiras 50
            chat_detected = True
            chat_lines_count = 0
            for i, line in enumerate(lines):
                if re.match(chat_pattern, line):
                    chat_lines_count += 1
                    # Novo chunk a cada N mensagens ou na primeira mensagem
                    if chat_lines_count % CHAT_MESSAGES_PER_CHUNK == 1 or chat_lines_count == 1:
                       marcadores.add(i)
                       doc_type_handler_used = True # Indica que um handler específico foi usado
            if doc_type_handler_used:
                marcadores.add(num_lines)
                return sorted(list(set(marcadores)))
        
        # 2. Se não for chat, tentar detectar títulos Markdown para arquivos .md
        if not chat_detected and file_extension == '.md':
            markdown_titles_found = False
            for i, line in enumerate(lines):
                if re.match(r"^\s*#{1,6}\s+", line): # Títulos Markdown
                    marcadores.add(i)
                    markdown_titles_found = True
                elif re.match(r"^\s*([-*_]){3,}\s*$", line): # Separadores ---, ***, ___
                    marcadores.add(i)
                    if i + 1 < num_lines: marcadores.add(i + 1)
                    markdown_titles_found = True
            if markdown_titles_found:
                doc_type_handler_used = True
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 5
total_chunks: 24
content_hash: 7d0a3c8ab3c207ec8fed7ccb23bf1994bee17574e93fdf16cf3926ae80818d31
summary: '# 3. Se não for chat e (for .txt OU .md sem títulos claros), tentar modo
  "Apostila" apostila_titles_found = False if not chat_detected and not doc_type_handler_used.'
timestamp_utc: '2025-06-09T10:23:35.206943+00:00'
---

```
# 3. Se não for chat e (for .txt OU .md sem títulos claros), tentar modo "Apostila"
        apostila_titles_found = False
        if not chat_detected and not doc_type_handler_used:
            apostila_title_pattern = r"^(?:CAP[IÍ]TULO|SECTION|SE[CÇ][ÃA]O)\s*\d+|^\d+(?:\.\d+)*\s+[A-ZÀ-ÖØ-Þ][\w\sÀ-ÖØ-Þ]*|^[A-ZÀ-ÖØ-Þ\s_]{5,}$"
            for i, line in enumerate(lines):
                if re.match(apostila_title_pattern, line.strip(), re.IGNORECASE):
                    marcadores.add(i)
                    apostila_titles_found = True
                    if i + 1 < num_lines and not lines[i+1].strip() and i + 2 < num_lines:
                        marcadores.add(i+2)
                    elif i + 1 < num_lines:
                         marcadores.add(i+1)
            if apostila_titles_found:
                doc_type_handler_used = True

        # 4. Fallback para FIXED_CHUNK_SIZE_DOCS se nenhuma estrutura específica foi detectada
        if not doc_type_handler_used:
            for i in range(FIXED_CHUNK_SIZE_DOCS, num_lines, FIXED_CHUNK_SIZE_DOCS):
                marcadores.add(i)
        
        marcadores.add(num_lines)
        return sorted(list(set(marcadores)))
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 6
total_chunks: 24
content_hash: 90aaa5e2e55593e7b7a57e5454653815e8d0a70f46faa07dd72d5160f935c922
summary: '# --- Lógica para arquivos de código --- # Regex mais abrangentes e específicas
  para linguagens. # Comentários: (r"comment_pattern", "LANGUAGE_TAG_OR_GENERAL")
  - não usado diretamente aqui.'
timestamp_utc: '2025-06-09T10:23:35.207941+00:00'
---

```
# --- Lógica para arquivos de código ---
    # Regex mais abrangentes e específicas para linguagens
    # Comentários: (r"comment_pattern", "LANGUAGE_TAG_OR_GENERAL") - não usado diretamente aqui, mas para referência
    
    # Python specific
    py_def_block = r"^\\s*(?:@\\w+(?:\\(.*\\))?\\s*\\n\\s*)*async\\s+def\\s+\\w+\\s*\\(.*\\)\\s*:" # async def with optional decorators
    py_def_simple = r"^\\s*(?:@\\w+(?:\\(.*\\))?\\s*\\n\\s*)*def\\s+\\w+\\s*\\(.*\\)\\s*:" # def with optional decorators
    py_class_block = r"^\\s*(?:@\\w+(?:\\(.*\\))?\\s*\\n\\s*)*class\\s+\\w+\\s*(?:\\(.*\\))?\\s*:" # class with optional decorators and inheritance
    
    # JavaScript / TypeScript specific
    js_ts_func_trad = r"^\\s*(export\\s+(?:default\\s+)?)?(async\\s+)?function(?:\\s*\\*|\\s+)?\\s*\\w*\\s*\\([^\\)]*\\)\\s*\\{?"
    js_ts_arrow_func = r"^\\s*(export\\s+)?(?:const|let|var)\\s+\\w+\\s*=\\s*(async\\s*)?\\([^\\)]*\\)\\s*=>\\s*\\{?"
    js_ts_class = r"^\\s*(export\\s+(?:default\\s+)?)?class\\s+\\w+(?:\\s+extends\\s+[\\w\\.]+)?(?:\\s+implements\\s+[\\w\\.,\\s]+)?\\s*\\{?"
    js_ts_interface = r"^\\s*(export\\s+)?interface\\s+\\w+(?:\\s+extends\\s+[\\w\\.,\\s]+)?\\s*\\{?"
    
    # Java / C# specific
    java_cs_method = r"^\\s*(?:@[\\w\\.]+(?:\\([^\\)]*\\))?\\s*\\n\\s*)*(?:public|private|protected|internal|static|final|sealed|abstract|virtual|override|synchronized|async|\\w+<[^>]+>)\\s+(?:\\w+|\\w+<[^>]+>)\s+\\w+\\s*\\([^\\)]*\\)\\s*(?:throws\\s+[\\w\\.,\\s]+)?\\s*\\{?"
    java_cs_class_interface_enum_struct_record = r"^\\s*(?:@[\\w\\.]+(?:\\([^\\)]*\\))?\\极*\\n\\s*)*(?:public|private|protected|internal|static|final|sealed|abstract)\\s+(?:class|interface|enum|struct|record)\\s+\\w+(?:<[^>]+>)?(?:\\s+extends\\s+[\\w\\.<>,\\s]+)?(?:\\s+implements\\s+[\\w\\.<>,\\s]+)?\\s*\\{?"
    java_constructor = r"^\\s*(?:public|private|protected)\\s+\\w+\\s*\\([^\\)]*\\)\\s*(?:throws\\s+[\\w\\.,\\s]+)?\\s*\\{?" # Simplified
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 7
total_chunks: 24
content_hash: 3a2e6ac683c22e859017bf57db6e9abc795bbb1379a5debb74c781e1d0eda199
summary: '# C / C++ specific c_cpp_func = r"^\\s*(?:template\\s*.s*<[^>]*>\\s*,(?:public|private|protected)\\s+\\w+)?’s*\\{?"
  # MQL4/MQL5 specific mql_function = r’(?:(int|void|double|bool|string|long|datetime|color|char|short|uchar|ushort|uint|ulong|ENUM_[\\w_]+)’)’.
  # Definitions    mQL_property =  “#property”, “property'
timestamp_utc: '2025-06-09T10:23:35.207941+00:00'
---

```
# C / C++ specific
    c_cpp_func = r"^\\s*(?:template\\s*<[^>]*>\\s*\\n\\s*)?(?:inline\\s+|static\\s+|virtual\\s+|explicit\\s+)?\\w+(?:\\s*::\\s*\\w+)?\\s*&?\\s*\\w+\\s*\\([^\\);]*\\)\\s*(?:const|override|final)?\\s*(?:throw\\s*\\([^\\)]*\\))?\\s*\\{?"
    c_cpp_struct_class_union_enum = r"^\\s*(?:template\\s*<[^>]*>\\s*\\n\\s*)?(?:struct|class|union|enum\\s+class|enum)\\s+\\w+(?:\\s*:\\s*(?:public|private|protected)\\s+\\w+)?\\s*\\{?"
    c_cpp_namespace = r"^\\s*namespace\\s+\\w+\\s*\\{?"
    c_cpp_define_func_like = r"^\\s*#define\\s+\\w+\\([^\\)]*\\)\\s+.*[^\\\\]$" # Function-like macro (single line)

    # MQL4/MQL5 specific
    mql_func = r"^\\s*(?:(int|void|double|bool|string|long|datetime|color|char|short|uchar|ushort|uint|ulong|ENUM_[\\w_]+)\\s+)?(On[A-Z]\\w*|\\w+)\\s*\\([^\\)]*\\)\\s*(?:const)?\\s*\\{?"
    mql_input_extern_sinput = r"^\\s*(?:input|extern|static|sinput)\\s+.*" # Definitions
    mql_property = r"^\\s*#property\\s+\\w+.*"
    mql_define = r"^\\s*#define\\s+\\w+.*"
    mql_class_struct_enum = r"^\\s*(class|struct|enum)\\s+\\w+(?:\\s*:\\s*(public|private|protected)\\s+\\w+)?\\s*\\{?"

    definition_patterns = [
        # Python
        py_def_block, py_def_simple, py_class_block,
        # JS/TS
        js_ts_func_trad, js_ts_arrow_func, js_ts_class, js_ts_interface,
        # Java/C#
        java_cs_method, java_cs_class_interface_enum_struct_record, java_constructor,
        # C/C++
        c_cpp_func, c_cpp_struct_class_union_enum, c_cpp_namespace, c_cpp_define_func_like,
        # MQL4/MQL5
        mql_func, mql_input_extern_sinput, mql_property, mql_define, mql_class_struct_enum,
        # General (fallback or simple cases) - Keep these less specific or at the end
        r"^\\s*\\w+\\s*\\([^\\)]*\\)\\s*\\{", # Simple function-like block
    ]
```

---

