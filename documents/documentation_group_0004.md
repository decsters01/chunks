# Source: instrucoes.md
Original Path: `.\instrucoes.md`

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 3
total_chunks: 9
content_hash: b7e9eafeff30a4d2fe424ade581c7bada6a429a86aeabd7127c7fb0a41b99181
summary: 'Descrição: Construir o esqueleto do projeto. Esta é a base sobre a qual
  todos os outros componentes serão construídos. Sub-tarefa 1.1: Criar a Estrutura
  de Diretórios.'
timestamp_utc: '2025-06-09T10:23:35.221904+00:00'
---

```
Descrição: Construir o esqueleto do projeto. Esta é a base sobre a qual todos os outros componentes serão construídos.

Depende de: Nenhuma.


Sub-tarefa 1.1: Criar a Estrutura de Diretórios

Ação: Definir a organização física do projeto.
Estrutura Final:
    /
    ├── documents/              # Pasta de saída padrão para os .md gerados
    ├── src/                    # Código fonte do framework
    │   ├── main.py             # Ponto de entrada da CLI
    │   ├── core/               # Orquestração e lógica principal
    │   │   ├── pipeline.py       # O maestro do processo
    │   │   ├── chunking.py       # Lógica de chunking unificada
    │   │   └── summarizer.py     # Lógica de sumarização
    │   ├── extractors/         # Módulos "plugin" para extração de conteúdo
    │   │   ├── base_extractor.py # Contrato da interface (Classe Base Abstrata)
    │   │   ├── text_extractor.py # Para .txt, .md, .py, etc.
    │   │   ├── pdf_extractor.py  # Para .pdf
    │   │   ├── docx_extractor.py # Para .docx
    │   │   └── image_extractor.py# Para .png, .jpg com OCR
    │   ├── output/             # Lógica para escrita dos arquivos de saída
    │   │   └── markdown_writer.py
    │   └── utils/              # Ferramentas de suporte
    │       ├── config.py         # Carregador de configurações
    │       ├── caching.py        # Gerenciador de cache
    │       └── logger.py         # Configuração do logger
    ├── tests/                  # Testes unitários e de integração
    │   ├── test_pipeline.py
    │   └── test_extractors.py
    ├── config.yaml             # Arquivo de configuração central
    └── requirements.txt        # Dependências do projeto
Critérios de Aceitação: A estrutura de diretórios é criada e o código de chunkv3.py é movido e desmembrado para os novos módulos.



Sub-tarefa 1.2: Implementar Configuração Centralizada
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 4
total_chunks: 9
content_hash: ed2093f388f81376ad51cfd006ab623c59b3c6e2fde82b82a91300ef618447ff
summary: 'Sub-tarefa 1.2: Implementar Configuração Centralizada: Criar e popular o
  config.yaml e a função para carregá-lo. 1.3: Gerenciar Dependências: CRIar requirements.txt
  com as bibliotecas necessárias.'
timestamp_utc: '2025-06-09T10:23:35.222901+00:00'
---

```
Sub-tarefa 1.2: Implementar Configuração Centralizada

Ação: Criar e popular o config.yaml e a função para carregá-lo.
Módulos: config.yaml, src/utils/config.py
Exemplo (config.yaml):
    yaml
    processing:
      input_directory: '.'
      output_directory: 'documents'
      ignored_directories: ['.git', 'node_modules', '__pycache__', 'documents']
      max_recursion_depth: 5
      max_markdown_files: 10
    chunking:
      chunk_size: 1500
      chunk_overlap: 250
      min_chunk_lines: 7
    summarizer:
      model_name: 't5-small' # Modelo de sumarização
      max_input_chars: 50000
    ocr:
      tesseract_cmd_path: null # Ex: 'C:/Program Files/Tesseract-OCR/tesseract.exe' no Windows
Critérios de Aceitação: O main.py carrega estas configurações no início da execução.



Sub-tarefa 1.3: Gerenciar Dependências

Ação: Criar requirements.txt com as bibliotecas necessárias.
Bibliotecas Iniciais: langchain, pypdf, python-docx, pytesseract, Pillow, PyYAML, click, tqdm, spacy, transformers, torch.
Critérios de Aceitação: O comando pip install -r requirements.txt instala todo o ambiente com sucesso.



Tarefa Principal 2: Framework de Extração de Conteúdo

Descrição: Construir o sistema polimórfico para extrair texto de qualquer tipo de arquivo.

Depende de: Tarefa Principal 1.


Sub-tarefa 2.1: Definir a Interface BaseExtractor

Ação: Criar a classe base abstrata para forçar um contrato comum.
Módulo: src/extractors/base_extractor.py

Implementação:
    ```python
    from abc import ABC, abstractmethod
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -&gt; str:
        """Extrai conteúdo textual de um arquivo."""
        pass
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 5
total_chunks: 9
content_hash: ef55b16c1e9f21f64e136ebc62c0c3ab4c7da99350d94cea23980ab6720ae877
summary: Criar uma classe para cada tipo of arquivo, herdando de BaseExtractor.py.
  Envolver a extração em um try-except genérico para capturar possíveis erros de XML
  or arquivos corrompidos.
timestamp_utc: '2025-06-09T10:23:35.222901+00:00'
---

```
```
    *   Critérios de Aceitação: A classe está definida.




Sub-tarefa 2.2: Implementar Extratores Concretos

Ação: Criar uma classe para cada tipo de arquivo, herdando de BaseExtractor.
Módulos: pdf_extractor.py, docx_extractor.py, image_extractor.py, text_extractor.py
Detalhes de Implementação e Tratamento de Erro:
PDF: Usar pypdf. Implementar try-except para pypdf.errors.PdfReadError (arquivos corrompidos) e pypdf.errors.FileNotDecryptedError (protegidos por senha), retornando uma string vazia e logando um aviso.
DOCX: Usar docx. Envolver a extração em um try-except genérico para capturar possíveis erros de XML ou arquivos corrompidos.
Imagem (OCR): Usar Pillow para abrir a imagem e pytesseract para extrair o texto. Checar se o Tesseract está instalado no sistema (usando o caminho de config.yaml ou shutil.which('tesseract')) e lançar um erro claro se não for encontrado.
Texto: Migrar a lógica de convert_to_text para este módulo, tratando UnicodeDecodeError.


Critérios de Aceitação: Cada extrator lê seu tipo de arquivo com sucesso e lida com erros de forma graciosa.



Sub-tarefa 2.3: Criar o "Extractor Factory"

Ação: Desenvolver a lógica no pipeline que mapeia extensões de arquivo para a classe extratora correta.
Módulo: src/core/pipeline.py
Implementação:
    python
    # Dentro da classe do pipeline
    self.extractors = {
        '.pdf': PDFExtractor(),
        '.docx': DocxExtractor(),
        '.png': ImageExtractor(),
        '.jpg': ImageExtractor(),
        # ... mais extensões mapeadas para TextExtractor
    }
    def get_extractor(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        return self.extractors.get(ext, self.default_text_extractor)
Critérios de Aceitação: O pipeline seleciona dinamicamente o extrator correto.



Tarefa Principal 3: Chunking Semântico e Enriquecimento de Dados

Descrição: Refinar o coração do sistema: a divisão e o enriquecimento do conteúdo.

Depende de: Tarefa Principal 2.
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 6
total_chunks: 9
content_hash: 0cdd98f214925819b5cc17075a98e12c160a2121a03d27d224864cc24e6b9d69
summary: 'Tarefa Principal 3: Chunking Semântico e Enriquecimento de Dados. Refinar
  o coração do sistema: a divisão e o enriquicimento do conteúdo.'
timestamp_utc: '2025-06-09T10:23:35.223899+00:00'
---

```
Tarefa Principal 3: Chunking Semântico e Enriquecimento de Dados

Descrição: Refinar o coração do sistema: a divisão e o enriquecimento do conteúdo.

Depende de: Tarefa Principal 2.


Sub-tarefa 3.1: Implementar Chunking por Linguagem

Ação: Configurar RecursiveCharacterTextSplitter para usar separadores específicos de cada linguagem.
Módulo: src/core/chunking.py

Implementação:
    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
def chunk_content(text: str, file_extension: str) -&gt; list[str]:
    language_map = {'.py': Language.PYTHON, '.js': Language.JS, '.md': Language.MARKDOWN}
    lang = language_map.get(file_extension)
if lang:
    splitter = RecursiveCharacterTextSplitter.from_language(lang, chunk_size=..., chunk_overlap=...)
else:
    # Fallback para texto genérico
    splitter = RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)

return splitter.split_text(text)

``
    *   **Critérios de Aceitação:** A funçãodetect_code_blocks` é removida e a nova função de chunking está operacional.




Sub-tarefa 3.2: Implementar Geração de YAML Frontmatter

Ação: Criar a estrutura de metadados e a função para escrevê-la.
Módulo: src/output/markdown_writer.py
Esquema YAML Final:
    yaml
    ---
    source_file: 'path/to/original/file.py'
    file_type: 'python'
    file_hash: 'sha256_hash_of_the_original_file'
    chunk_index: 1
    total_chunks: 5
    content_hash: 'sha256_hash_of_this_specific_chunk'
    summary: 'Resumo gerado por IA sobre o conteúdo deste chunk.'
    timestamp_utc: '2023-10-27T10:00:00Z'
    ---
Critérios de Aceitação: Todos os chunks salvos em arquivos .md contêm este cabeçalho YAML.



Sub-tarefa 3.3: Aprimorar a Sumarização
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 7
total_chunks: 9
content_hash: b538ed8a61e2ae78e5390e8e2c50b0e3ca3c419147e979e1c12418105627eaf2
summary: 'Sub-tarefa 3.3: Aprimorar a Sumarização usando modelo t5-small. Sub- tarefa
  4.1: Desenvolver a classe that orquestra todo o fluxo de trabalho.'
timestamp_utc: '2025-06-09T10:23:35.223899+00:00'
---

```
Sub-tarefa 3.3: Aprimorar a Sumarização

Ação: Criar um módulo de sumarização usando um modelo de transformers.
Módulo: src/core/summarizer.py
Implementação: Utilizar a pipeline summarization da biblioteca transformers com o modelo t5-small. Incluir lógica de fallback: se a sumarização falhar ou o texto for muito curto, usar as primeiras 50 palavras como resumo.
Critérios de Aceitação: Os resumos são de qualidade superior ao método anterior e o sistema não quebra se a sumarização falhar.



Tarefa Principal 4: Orquestração, CLI e Otimizações

Descrição: Unir todas as peças, criar uma interface de usuário e garantir a performance.

Depende de: Tarefas 1, 2, 3.


Sub-tarefa 4.1: Construir o Pipeline Principal

Ação: Desenvolver a classe que orquestra todo o fluxo de trabalho.
Módulo: src/core/pipeline.py
Lógica:
Inicializar (carregar config, cache, logger).
Percorrer o diretório de entrada (os.walk), respeitando ignored_dirs e max_recursion_depth.
Para cada arquivo:
    a.  Verificar o cache. Se o arquivo não mudou, pular.
    b.  Obter o extrator correto.
    c.  Extrair conteúdo.
    d.  Dividir em chunks.
    e.  Para cada chunk: gerar resumo e metadados.
    f.  Escrever chunks no(s) arquivo(s) de saída usando MarkdownWriter.
    g.  Atualizar o cache.


Critérios de Aceitação: O pipeline executa o processo do início ao fim.



Sub-tarefa 4.2: Implementar o Sistema de Cache

Ação: Criar a lógica para evitar reprocessamento.
Módulo: src/utils/caching.py
Estratégia: Manter um cache.json. Antes de processar um arquivo, calcular o hash de seu conteúdo e comparar com o hash armazenado para aquele caminho de arquivo. Se for o mesmo, pular. Após o processamento, salvar o novo hash.
Critérios de Aceitação: Arquivos não modificados são pulados em execuções subsequentes.



Sub-tarefa 4.3: Construir a CLI com click

Ação: Desenvolver a interface de linha de comando.
Módulo: src/main.py
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 8
total_chunks: 9
content_hash: bab40718e374795fbd2919710aca576a2f87e1a622ba614639844c472afcca7a
summary: 'Sub-tarefa 4.3: Construir a CLI com click. Ação: Desenvolver a interface
  de linha de comando. Módulo: src/main.py. Implementação : click, tqDM.'
timestamp_utc: '2025-06-09T10:23:35.223899+00:00'
---

```
Sub-tarefa 4.3: Construir a CLI com click

Ação: Desenvolver a interface de linha de comando.
Módulo: src/main.py

Implementação:
    ```python
    import click
    from tqdm import tqdm # Para a barra de progresso
@click.command()
@click.option('--input-dir', default=None, help='Diretório para processar.')
@click.option('--output-dir', default=None, help='Diretório para salvar os arquivos.')
@click.option('--force-reprocess', is_flag=True, help='Força o reprocessamento de todos os arquivos.')
def run(input_dir, output_dir, force_reprocess):
    # Lógica para carregar config, sobrescrever com opções da CLI e rodar o pipeline
    # Integrar tqdm na iteração dos arquivos no pipeline
    pass
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 9
total_chunks: 9
content_hash: 03f4744bccb3f05d7c6c6867b44959289d44f0f6fe05bb9afc4f3ab529520b73
summary: 'Tarefa Principal 5: Garantia de Qualidade. Critérios de Aceitação: Os testes
  cobrem os principais cenários of sucesso. Chunking: Testar com código Python, Markdown
  and texto plano.'
timestamp_utc: '2025-06-09T10:23:35.224896+00:00'
---

```
```
    *   Critérios de Aceitação: O script é executável via terminal com os parâmetros especificados.




Tarefa Principal 5: Garantia de Qualidade

Descrição: Assegurar que o sistema é confiável e funciona como esperado.

Depende de: Tarefas 1, 2, 3, 4.


Sub-tarefa 5.1: Escrever Testes Unitários

Ação: Criar testes para cada componente isoladamente.
Módulo: tests/
O que testar:
Extratores: Para cada um, testar com um arquivo válido, um arquivo corrompido/inválido e um arquivo vazio. Para o de imagem, testar o que acontece se o Tesseract não estiver instalado.
Chunking: Testar com código Python, Markdown e texto plano para verificar se os chunks são criados corretamente.
Configuração: Testar se o config.yaml é carregado corretamente.


Critérios de Aceitação: Os testes cobrem os principais cenários de sucesso e falha para cada módulo.



Sub-tarefa 5.2: Escrever Testes de Integração

Ação: Criar um teste que executa o pipeline completo.
Módulo: tests/test_pipeline.py
Cenário de Teste: Criar um diretório de teste com subpastas e vários tipos de arquivo (.py, .pdf, .txt, um inválido). Executar o pipeline e verificar se a pasta de saída (documents/) foi criada, se contém o número esperado de arquivos .md, e se o conteúdo de um dos arquivos (incluindo o YAML Frontmatter) está correto.
Critérios de Aceitação: O teste de integração passa, validando que todos os componentes trabalham juntos harmoniosamente.




Este plano de engenharia é a nossa bússola. Ele é ambicioso, mas cada passo é deliberado e projetado para construir um sistema de altíssima qualidade.
Estou pronto para iniciar a execução da Tarefa Principal 1 assim que o Mestre der o sinal verde.
```

---

# Source: main.py
Original Path: `.\main.py`

---
source_file: .\main.py
file_type: .py
file_hash: d426c8e269a1a752a42c7898c6968cc7db6c1aace70ec94b343342a044646617
chunk_index: 1
total_chunks: 2
content_hash: 3f2e9b351f721aabc77da32dab757e45af37feafaef571b774fb995d7ea8214d
summary: import os.import click.import Pipeline.import logger, setup_logger. import
  load_config.import load_markdown.import Markdown. importing load_down. imports load-down.
timestamp_utc: '2025-06-09T10:23:35.224896+00:00'
---

```
import os
import click
from src.core.pipeline import Pipeline
from src.utils.config import load_config
from src.utils.logger import logger, setup_logger

@click.command()
@click.option('--config', 'config_path', default='config.yaml', help='Caminho para o arquivo de configuração.')
@click.option('--input-dir', help='Diretório de entrada (sobrescreve config.yaml).')
@click.option('--output-dir', help='Diretório de saída (sobrescreve config.yaml).')
@click.option('--max-files', 'max_markdown_files', type=int, help='Número máximo de arquivos Markdown para agrupar chunks (sobrescreve config.yaml).')
@click.option('--force', 'force_reprocess', is_flag=True, help='Forçar o reprocessamento de todos os arquivos, ignorando o cache.')
@click.option('--verbose', is_flag=True, help='Ativar logging detalhado (DEBUG).')
```

---

---
source_file: .\main.py
file_type: .py
file_hash: d426c8e269a1a752a42c7898c6968cc7db6c1aace70ec94b343342a044646617
chunk_index: 2
total_chunks: 2
content_hash: 62e86ec4ee37ea1383655a71c85fadff5b29ac1be6838877a7ced54b8435cf97
summary: 'def main(config_path, input_dir, output_dir,. max_markdown_ files, force_reprocess,
  verbose): """ Pipeline para extrair, chunkificar e documentar o conteúdo de repositórios
  de código" config = {''processing'': {}, ''logging'': {}} config.load_config( config_path)
  except FileNotFoundError: logger.warning(f"Arquivo de configuração ''{Config_path}''
  não encontrado. Usando apenas argumentos da CLI e padrões.")'
timestamp_utc: '2025-06-09T10:23:35.225893+00:00'
---

```
def main(config_path, input_dir, output_dir, max_markdown_files, force_reprocess, verbose):
    """
    Pipeline para extrair, chunkificar e documentar o conteúdo de repositórios de código.
    """
    setup_logger()
    if verbose:
        logger.setLevel('DEBUG')

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        logger.warning(f"Arquivo de configuração '{config_path}' não encontrado. Usando apenas argumentos da CLI e padrões.")
        config = {'processing': {}, 'logging': {}}

    # Sobrescrever config com argumentos da CLI
    if input_dir:
        config['processing']['input_directory'] = input_dir
    if output_dir:
        config['processing']['output_directory'] = output_dir
    if max_markdown_files is not None:
        config['processing']['max_markdown_files'] = max_markdown_files
    
    # Validar configurações
    input_dir_path = config['processing'].get('input_directory')
    output_dir_path = config['processing'].get('output_directory')
    
    if not input_dir_path or not output_dir_path:
        logger.error("Os diretórios de entrada e saída devem ser especificados via CLI ou config.yaml.")
        return
        
    if not os.path.isdir(input_dir_path):
        logger.error(f"Diretório de entrada não encontrado: {input_dir_path}")
        return

    # Executar pipeline
    logger.info("Iniciando pipeline de processamento...")
    pipeline = Pipeline(cache_path=config.get('cache_file', 'pipeline_cache.json'))
    
    pipeline.process_directory(
        root_dir=input_dir_path,
        output_dir=output_dir_path,
        exclude_dirs=config['processing'].get('ignored_directories'),
        max_markdown_files=config['processing'].get('max_markdown_files'),
        force_reprocess=force_reprocess
    )

    logger.info("Pipeline concluído com sucesso.")

if __name__ == '__main__':
    main()
```

---

# Source: relatorio.py
Original Path: `.\relatorio.py`

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 1
total_chunks: 14
content_hash: 31037d20beb077b56a65548f75b5f20a42aa1e00d97f315d2b39ffd2beccd57a
summary: import pandas as pd, bs4, BeautifulSoup, io, re, datetime, defaultdict. import
  os.import io.import re.import sys.import defaultdict# Função Principal de Análise.
timestamp_utc: '2025-06-09T10:23:35.225893+00:00'
---

```
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
from collections import defaultdict
import os
import io
import sys

# --- Funções Auxiliares ---
def extrair_timestamp_do_titulo(title_attr):
    """Extrai e converte o timestamp do atributo title."""
    if not title_attr:
        return None
    # Formato: "15.05.2025 08:34:06 UTC-03:00"
    try:
        timestamp_str = title_attr.split(" UTC")[0]
        return pd.to_datetime(timestamp_str, format="%d.%m.%Y %H:%M:%S")
    except ValueError:
        print(f"Erro ao converter data: {title_attr}")
        return None

def extrair_nome_usuario(texto_usuario_raw):
    """Extrai o nome do usuário de forma mais limpa."""
    if not texto_usuario_raw:
        return "Desconhecido"
    # Remove tags HTML e conteúdo de links, como @telegramhandle
    clean_name = re.sub(r'<a.*?>.*?</a>', '', texto_usuario_raw).strip()
    # Se o nome começar com "ID: " e for seguido por um número (possivelmente de telefone),
    # podemos considerar manter assim ou extrair apenas o ID. Por ora, mantém.
    return clean_name if clean_name else "Desconhecido"

# --- Função Principal de Análise ---
```

---

