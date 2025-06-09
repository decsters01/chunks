# Source: EXEMPLOS.md
Original Path: `.\EXEMPLOS.md`

---
source_file: .\EXEMPLOS.md
file_type: .md
file_hash: 86de81505f14dc9ee80db632701641b23257276b857cffde91ffa10374eabeb2
chunk_index: 1
total_chunks: 4
content_hash: 5cbf996d01e591f301eeccdad9dde6bd9b9fda840a566e94e3dea05b3d2bf865
summary: 'Casos de Uso Avançados: Documentação Automatizada de Código-Fonte. Processamento
  de Documentos Jurídicos: Extrair cláusulas importantes de contratos.'
timestamp_utc: '2025-06-09T10:23:35.195469+00:00'
---

```
Casos de Uso Avançados
1. Documentação Automatizada de Código-Fonte
Objetivo: Gerar documentação técnica para um projeto Python complexo
Passos:
1. Crie um arquivo config_code.yaml:
```yaml
extractors:
  text:
    enabled: true
  py:
    enabled: true
chunking:
  strategy: semantic
  max_tokens: 1024
  min_lines: 10
output:
  directory: docs_code
```


Execute o pipeline:
bash
python src/main.py --input src/ --config config_code.yaml


Saída gerada:

Documentação estruturada por módulo
Chunks semânticos preservando contexto
Resumos automáticos de funcionalidades

2. Processamento de Documentos Jurídicos
Objetivo: Extrair cláusulas importantes de contratos
Configuração Especial:
```yaml
config_legal.yaml
chunking:
  strategy: fixed
  size: 200  # Pequenos chunks para precisão
  overlap: 0.0
summarization:
  enabled: true
  model: facebook/bart-large
  max_length: 50
output:
  include_metadata: false
```
Fluxo:
```python
from src.core.pipeline import DocumentPipeline
pipeline = DocumentPipeline('config_legal.yaml')
results = pipeline.process_directory("contratos/")
Análise adicional
for chunk in results:
    if "confidencial" in chunk['content']:
        print(f"Cláusula confidencial encontrada: {chunk['summary']}")
```

---

---
source_file: .\EXEMPLOS.md
file_type: .md
file_hash: 86de81505f14dc9ee80db632701641b23257276b857cffde91ffa10374eabeb2
chunk_index: 2
total_chunks: 4
content_hash: e4d9bd877cdec964c8bbf6d35af88ddf9d4c0dc9dabf60878a136d0b1b528cea
summary: 'OCR em Lote para Digitalização de Arquivos: Processar 1000 imagens de documentos
  escaneados. OCR em Sistema de Tickets: processar anexos de tickets automaticamente.
  Solução: Integração com Sistemas de Tickets.'
timestamp_utc: '2025-06-09T10:23:35.196467+00:00'
---

```
```
3. OCR em Lote para Digitalização de Arquivos
Objetivo: Processar 1000 imagens de documentos escaneados
Solução:
```python
batch_ocr.py
from src.extractors.image_extractor import ImageExtractor
from src.utils.caching import FileCache
import concurrent.futures
import os
extractor = ImageExtractor()
cache = FileCache('ocr_cache.db')
def process_image(file_path):
    if cache.is_cached(file_path):
        return cache.get(file_path)
    text = extractor.extract(file_path)
    cache.set(file_path, text)
    return text
with concurrent.futures.ThreadPoolExecutor() as executor:
    image_files = [f for f in os.listdir('scanned/') if f.endswith(('.png','.jpg'))]
    results = list(executor.map(process_image, image_files))
Salvar resultados
with open('ocr_output.txt', 'w') as f:
    for text in results:
        f.write(text + "\n\n")
```
4. Integração com Sistema de Tickets
Objetivo: Processar anexos de tickets automaticamente
Fluxo:
1. Monitorar diretório de novos tickets
2. Processar anexos com pipeline
3. Enviar resumo para API de tickets
```python
ticket_integration.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.core.pipeline import DocumentPipeline
pipeline = DocumentPipeline('config_tickets.yaml')
class TicketHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            result = pipeline.process_file(event.src_path)
            send_to_ticket_system(result['summary'])
def send_to_ticket_system(summary):
    # Implementação da API
    pass
observer = Observer()
observer.schedule(TicketHandler(), path='tickets/')
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

---

---
source_file: .\EXEMPLOS.md
file_type: .md
file_hash: 86de81505f14dc9ee80db632701641b23257276b857cffde91ffa10374eabeb2
chunk_index: 3
total_chunks: 4
content_hash: d59da48cb1731b113d64bf5a3ec213b4314a1accd8ae7e1ab99bf87977507512
summary: '```pythonsentiment_analysis.py: Análise de Sentimento em Feedback de Clientes.
  Analisar sentimentos em avaliações de produtos. Estendido: SentimentPipeline.'
timestamp_utc: '2025-06-09T10:23:35.196467+00:00'
---

```
```
5. Análise de Sentimento em Feedback de Clientes
Objetivo: Analisar sentimentos em avaliações de produtos
Pipeline Estendido:
```python
sentiment_analysis.py
from transformers import pipeline
from src.core.pipeline import DocumentPipeline
class SentimentPipeline(DocumentPipeline):
    def init(self, config):
        super().init(config)
        self.sentiment_analyzer = pipeline("sentiment-analysis")
def process_chunk(self, chunk):
    result = super().process_chunk(chunk)
    sentiment = self.sentiment_analyzer(result['content'])[0]
    return {**result, 'sentiment': sentiment}

Uso
config = {
    'extractors': {'text': True},
    'chunking': {'max_tokens': 512}
}
pipeline = SentimentPipeline(config)
results = pipeline.process_file("feedback.txt")
Agregar resultados
positive = sum(1 for r in results if r['sentiment']['label'] == 'POSITIVE')
print(f"Feedback positivo: {positive/len(results)*100:.2f}%")
```
6. Processamento de Documentos em Nuvem
Arquitetura:
mermaid
graph LR
    A[S3 Bucket] --&gt; B[Lambda Trigger]
    B --&gt; C[Processamento]
    C --&gt; D[Salvar no S3]
    C --&gt; E[Enviar para DynamoDB]
Implementação AWS Lambda:
```python
lambda_function.py
import boto3
from src.core.pipeline import DocumentPipeline
s3 = boto3.client('s3')
pipeline = DocumentPipeline('config_cloud.yaml')
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
    # Download file
    file_path = f"/tmp/{key}"
    s3.download_file(bucket, key, file_path)

    # Process document
    result = pipeline.process_file(file_path)

    # Save to output bucket
    output_key = f"processed/{key}.md"
    s3.put_object(Bucket="output-bucket", Key=output_key, Body=result['content'])
```

---

---
source_file: .\EXEMPLOS.md
file_type: .md
file_hash: 86de81505f14dc9ee80db632701641b23257276b857cffde91ffa10374eabeb2
chunk_index: 4
total_chunks: 4
content_hash: 4ee74165c03965e463907f255305b50fa213b09d3c9afe5946830089fcc9cd69
summary: 'pythoncustom_extractor.py. Customização de Extrator para Formato Proprietário.Implementação:
  implementations: pythoncustom-extractor-7.7.2.'
timestamp_utc: '2025-06-09T10:23:35.197464+00:00'
---

```
```
7. Customização de Extrator para Formato Proprietário
Implementação:
```python
custom_extractor.py
from src.extractors.base_extractor import BaseExtractor
import proprietary_lib
class CustomExtractor(BaseExtractor):
    def extract(self, file_path: str) -&gt; str:
        if not file_path.endswith('.xyz'):
            raise ValueError("Formato não suportado")
    # Lógica de extração específica
    data = proprietary_lib.parse(file_path)
    return data['text_content']

Registrar no pipeline
from src.core.pipeline import DocumentPipeline
pipeline = DocumentPipeline(config)
pipeline.register_extractor('.xyz', CustomExtractor())
```

---

# Source: FAQ.md
Original Path: `.\FAQ.md`

---
source_file: .\FAQ.md
file_type: .md
file_hash: f9bf9b2a3ffe699fbd61901143b3b457e5bd0aa99efd49edfc02588876d88015
chunk_index: 1
total_chunks: 2
content_hash: d2aeab5c88c4311bf626b14b5c83efa0e0d62d96940e09d644a9bab5afe62cda
summary: 'Perguntas Frequentes e Solução de Problemas. Instale pacotes de idioma:
  pip install tesseract-ocrpor. Desempenho: O processamento está muito lento para
  muitos arquivos. OCR: OCR para imagens não está funcionando.'
timestamp_utc: '2025-06-09T10:23:35.197464+00:00'
---

```
Perguntas Frequentes e Solução de Problemas
1. Instalação e Configuração
P: Como resolver erros de dependência durante a instalação?
R: 
1. Verifique a versão do Python (python --version deve ser 3.9+)
2. Atualize o pip: pip install --upgrade pip
3. Instale dependências manualmente:
bash
pip install pdfminer.six python-docx pytesseract pillow
P: O sistema não reconhece meu arquivo PDF/DOCX
R:
1. Verifique se o extrator está habilitado no config.yaml
2. Para PDFs, instale o pdfminer: pip install pdfminer.six
3. Para DOCX, instale: pip install python-docx
2. Processamento de Arquivos
P: Meus chunks estão muito pequenos ou muito grandes
R: Ajuste os parâmetros no config.yaml:
yaml
chunking:
  max_tokens: 768  # Aumente para chunks maiores
  min_lines: 8     # Aumente o mínimo de linhas
  strategy: semantic # Ou 'fixed' para tamanho fixo
P: O OCR para imagens não está funcionando
R:
1. Verifique instalação do Tesseract:
   - Windows: Baixe do site oficial
   - Linux: sudo apt install tesseract-ocr
   - MacOS: brew install tesseract
2. Instale pacotes de idioma: sudo apt install tesseract-ocr-por
3. Desempenho
P: O processamento está muito lento para muitos arquivos
R:
1. Ative o cache no config.yaml:
yaml
caching:
  enabled: true
  path: .processing_cache
2. Use processamento paralelo:
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    executor.map(pipeline.process_file, file_list)
```
P: Como processar apenas arquivos modificados?
R: Use o sistema de cache integrado:
```python
from src.utils.caching import FileCache
cache = FileCache()
if not cache.is_cached(file_path):
    process_file(file_path)
```

---

---
source_file: .\FAQ.md
file_type: .md
file_hash: f9bf9b2a3ffe699fbd61901143b3b457e5bd0aa99efd49edfc02588876d88015
chunk_index: 2
total_chunks: 2
content_hash: 75a74166bd9ff1fc148a680679ada3243bfaf4cde6cbcdc0b73d74e6ed480b4c
summary: Arquivos de saída não estão sendo gerados. Verifique a extensão do arquivo.
  Implemente um extrator customizado (veja EXEMPLOS.md)
timestamp_utc: '2025-06-09T10:23:35.198461+00:00'
---

```
```
4. Saída e Resultados
P: Os arquivos de saída não estão sendo gerados
R:
1. Verifique permissões de escrita no diretório de saída
2. Confira o caminho no config.yaml:
yaml
output:
  directory: /caminho/valido
3. Verifique logs em processing.log
P: Metadados estão faltando na saída
R: Ative a opção no config:
yaml
output:
  include_metadata: true
5. Erros Comuns
Erro: ModuleNotFoundError: No module named '...'
Solução: Instale o módulo faltante com pip install nome_do_modulo
Erro: UnsupportedFileFormatError
Solução:
1. Verifique a extensão do arquivo
2. Implemente um extrator customizado (veja EXEMPLOS.md)
Erro: EncodingError em arquivos de texto
Solução: Especifique a codificação no config:
yaml
extractors:
  text:
    encoding: 'latin-1' # Ou 'utf-8'
6. Personalização
P: Como adicionar suporte a um novo formato de arquivo?
R: 
1. Crie um novo extrator herdando de BaseExtractor
2. Implemente o método extract()
3. Registre no pipeline:
python
pipeline.register_extractor('.minhaext', MeuExtrator())
(Exemplo completo em EXEMPLOS.md)
P: Como alterar o modelo de sumarização?
R: 
1. Escolha um modelo do Hugging Face
2. Atualize o config:
yaml
summarization:
  model: nome_do_modelo
7. Contribuição
P: Como contribuir para o projeto?
R:
1. Faça fork do repositório
2. Siga as diretrizes de código
3. Envie pull requests com:
   - Testes unitários para novas funcionalidades
   - Documentação atualizada
   - Exemplos de uso
P: Onde reportar bugs?
R: Abra issues no repositório do projeto incluindo:
1. Passos para reproduzir o erro
2. Mensagem de erro completa
3. Ambiente (SO, versão do Python)
4. Arquivo de configuração relevante
```

---

# Source: INSTALACAO.md
Original Path: `.\INSTALACAO.md`

---
source_file: .\INSTALACAO.md
file_type: .md
file_hash: a26a5245331eda4a81fed88681ab00fbdb1fab7af43237f9ac4d4b79603299d8
chunk_index: 1
total_chunks: 1
content_hash: 5d36a827184da2df22a5051623488cf83f03749b95a2c85fb3134b26d672105d
summary: Instalação e Configuração do Framework do Python 3.9 ou superior. Gerenciador
  de pacotes pip atualizado. Ambiente virtual (recomendado)
timestamp_utc: '2025-06-09T10:23:35.198461+00:00'
---

```
Instalação e Configuração do Framework
Pré-requisitos

Python 3.9 ou superior
Gerenciador de pacotes pip atualizado
Ambiente virtual (recomendado)

Passo 1: Configurar Ambiente Virtual
bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
Passo 2: Instalar Dependências
bash
pip install -r requirements.txt
Passo 3: Instalar Dependências Adicionais
Dependendo dos formatos que deseja processar, instale:
Para processamento de PDF
bash
pip install pdfminer.six
Para processamento de DOCX
bash
pip install python-docx
Para processamento de imagens (OCR)
bash
pip install pillow pytesseract
Para sumarização avançada
bash
pip install transformers torch
Passo 4: Configuração Inicial
Edite o arquivo config.yaml para definir suas preferências:
```yaml
Exemplo de configuração
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
Passo 5: Execução Inicial
bash
python src/main.py
Verificação da Instalação
Execute o teste básico para confirmar:
bash
pytest tests/
Solução de Problemas Comuns

Erro de dependência faltante: Verifique se instalou todos os pacotes necessários
Problemas com OCR: Certifique-se que o Tesseract está instalado no sistema
Erros de permissão: Execute com permissões adequadas ou em ambiente virtual
```

---

# Source: README.md
Original Path: `.\README.md`

---
source_file: .\README.md
file_type: .md
file_hash: 2fe7eb31f6f45db34bcdd3606cbcf21a0004617b12193b72937e5f0ed5b27ede
chunk_index: 1
total_chunks: 1
content_hash: 33e078da5b1b575fa588b807dbdd7fe6a15cc3c7da527f011b4c032865f2d221
summary: Framework de Processamento de Documentos oferece:Extratores especializados
  for múltiplos formatos (PDF, DOCX, imagens, texto) Chunking inteligente para fragmentação
  semântica de conteúdo. Sumarização automática com modelos de linguagem. Geração
  de documentaçón em formato Markdown.
timestamp_utc: '2025-06-09T10:23:35.199459+00:00'
---

```
Framework de Processamento de Documentos
Visão Geral
O Framework de Processamento de Documentos é uma solução integrada para extração, processamento e geração de documentação a partir de diversos formatos de arquivos. Desenvolvido em Python, oferece:

Extratores especializados para múltiplos formatos (PDF, DOCX, imagens, texto)
Sistema de chunking inteligente para fragmentação semântica de conteúdo
Sumarização automática com modelos de linguagem
Geração de documentação em formato Markdown

Arquitetura
O sistema é organizado em módulos especializados:
src/
├── extractors/    # Implementações de extração por tipo de arquivo
├── core/          # Lógica principal (chunking, pipeline, sumarização)
├── output/        # Geradores de saída (Markdown, etc)
└── utils/         # Utilitários (caching, logging, configuração)
Funcionalidades Principais

Processamento paralelo de documentos
Cache inteligente para evitar reprocessamento
Customização via arquivo de configuração
Geração de documentação estruturada
Suporte a múltiplos formatos de entrada

Ver Tutorial Completo | Referência Técnica
```

---

# Source: REFERENCIA.md
Original Path: `.\REFERENCIA.md`

---
source_file: .\REFERENCIA.md
file_type: .md
file_hash: 47e7bda6b5a6163e580034268b9473e397cad6dca03283a02dd13ad3b7dd80af
chunk_index: 1
total_chunks: 3
content_hash: df5c9df9e84ea7ea962db6273614d3eab115e366c2892a1e74606b76373cb4b5
summary: Módulo de Extração (src/extractors) implements BaseExtractor (ABC) and DocumentPipeline
  (Classe Principal) Módulos de Processamento Central (source/core/core) implements
  Pipeline (Source/Core/Core) Framework is based on the Técnica do Framework.
timestamp_utc: '2025-06-09T10:23:35.199459+00:00'
---

```
Referência Técnica do Framework
Visão Geral da Arquitetura
mermaid
graph TD
    A[Documentos de Entrada] --&gt; B[Extratores]
    B --&gt; C[Pipeline Central]
    C --&gt; D[Chunking]
    C --&gt; E[Sumarização]
    D --&gt; F[Geradores de Saída]
    E --&gt; F
    F --&gt; G[Documentação Formatada]
Módulos Principais
1. Módulo de Extração (src/extractors/)
BaseExtractor (Classe Abstrata)
python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -&gt; str:
        """Extrai texto de um arquivo"""
Extratores Implementados:

PDFExtractor: Extrai texto de PDFs usando pdfminer
DocxExtractor: Extrai texto de documentos DOCX
TextExtractor: Lê arquivos de texto simples
ImageExtractor: Usa OCR para extrair texto de imagens

2. Módulo de Processamento Central (src/core/)
Pipeline (Classe Principal)
```python
class DocumentPipeline:
    def init(self, config: dict):
        self.config = config
        self.extractors = self._init_extractors()
        self.chunker = SemanticChunker(config['chunking'])
        self.summarizer = Summarizer(config['summarization'])
def process_file(self, file_path: str):
    # Implementação do fluxo completo
```

---

---
source_file: .\REFERENCIA.md
file_type: .md
file_hash: 47e7bda6b5a6163e580034268b9473e397cad6dca03283a02dd13ad3b7dd80af
chunk_index: 2
total_chunks: 3
content_hash: c005456eb554d3fabcdd6b20cb99b4ed152faa49398fabf4a8c89e96577c748b
summary: Módulo de Saída (src/output/) includes MarkdownWriter. Módulos de Utilitários
  (source/utils/) include Cache de processamento. Logger (source) includes Logger.
timestamp_utc: '2025-06-09T10:23:35.200456+00:00'
---

```
```
SemanticChunker

Divide texto mantendo unidades semânticas
Parâmetros configuráveis: max_tokens, overlap, min_lines

Summarizer

Gera resumos usando modelos transformers
Suporta múltiplos modelos (Hugging Face)

3. Módulo de Saída (src/output/)
MarkdownWriter
python
class MarkdownWriter:
    def write(self, chunks: list, output_path: str):
        """Escreve chunks em arquivos Markdown formatados"""
4. Módulo de Utilitários (src/utils/)
Caching

Cache de processamento para evitar trabalho redundante
Usa hashing de arquivos para detecção de mudanças

ConfigLoader
python
def load_config(config_path: str) -&gt; dict:
    """Carrega configurações de arquivo YAML"""
Logger

Sistema de logging unificado com diferentes níveis

Configuração Completa (config.yaml)
| Seção | Parâmetro | Tipo | Descrição |
|-------|-----------|------|-----------|
| extractors | enabled | bool | Ativa/desativa extrator |
|  | ocr_fallback | bool | Usa OCR quando extração principal falha |
| chunking | strategy | string | 'semantic' ou 'fixed' |
|  | max_tokens | int | Tamanho máximo de tokens por chunk |
|  | overlap | float | Sobreposição entre chunks (0.0-1.0) |
| summarization | enabled | bool | Ativa sumarização |
|  | model | string | Modelo Hugging Face |
|  | max_length | int | Comprimento máximo do resumo |
| output | format | string | 'markdown' ou 'json' |
|  | directory | string | Pasta de saída |
Fluxo de Dados

Entrada: Arquivo é passado para o extrator apropriado
Processamento:
Texto é dividido em chunks
Cada chunk é sumarizado (se habilitado)
Saída:
Metadados são adicionados
Conteúdo é formatado
Arquivo final é salvo
```

---

