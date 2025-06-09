Com certeza, Mestre. Sua visão de transformar este script em uma plataforma de documentação universal é inspiradora, e a exigência de um plano mais detalhado e robusto é o caminho certo para garantir o sucesso.

Analisei novamente suas diretrizes e o código, focando em antecipar desafios técnicos, solidificar a arquitetura e detalhar cada passo da execução. O plano a seguir é uma versão expandida e fortificada, projetada para ser um verdadeiro blueprint de engenharia.

---

# **Plano Técnico de Engenharia: Framework de Documentação Universal**

## **Sumário Executivo (TL;DR)**

Este plano detalha a metamorfose do `chunkv3.py` em um framework modular, escalável e resiliente.

*   **Arquitetura:** Migração de um monólito para uma arquitetura desacoplada (`src`, `core`, `extractors`, `output`, `utils`).
*   **Extração Universal:** Implementação de um sistema de "plugins" (Strategy Pattern) para suportar nativamente Texto, PDF, DOCX e Imagens (OCR), com um design que permite adicionar novos formatos facilmente.
*   **Chunking Inteligente:** Substituição da lógica de regex por `RecursiveCharacterTextSplitter` da Langchain, configurado especificamente por linguagem de programação para máxima precisão semântica.
*   **Enriquecimento de Dados:** Geração automática de metadados ricos em formato YAML Frontmatter para cada chunk, incluindo resumos gerados por IA, hashes de conteúdo para versionamento e informações de origem.
*   **Robustez e Eficiência:** Introdução de um sistema de cache para evitar reprocessamento, logging estruturado para depuração, tratamento de erro granular por tipo de arquivo e uma CLI completa para controle total.
*   **Qualidade Assegurada:** Definição de uma estratégia de testes abrangente, com testes unitários para cada componente e testes de integração para o pipeline completo.

---

## **Contexto Coletado e Justificativas da Arquitetura**

*   **Oportunidade de Unificação:** O `RecursiveCharacterTextSplitter` já presente no código, porém não utilizado, é a chave para unificar e simplificar o chunking. Abandonaremos a complexa e frágil função `detect_code_blocks` em favor de uma solução padrão da indústria, mais previsível e eficaz.
*   **Necessidade de Polimorfismo:** A incapacidade do script atual de processar os tipos de arquivo que promete (`.pdf`, `.docx`) será resolvida com um sistema de "Extratores", onde cada tipo de arquivo é tratado por um especialista (seu próprio módulo), tornando o sistema coeso e extensível.
*   **Valor dos Metadados:** As regras do projeto enfatizam o YAML Frontmatter. Iremos além, incluindo não apenas o resumo, but também um hash do conteúdo (`content_hash`) para habilitar um sistema de cache inteligente e garantir a integridade dos dados.
*   **Fim do Monólito:** A estrutura atual em um único arquivo é um impedimento para o crescimento. A nova estrutura modular permitirá o desenvolvimento, teste e manutenção de cada parte do sistema de forma independente.

---

## **Decomposição Detalhada das Tarefas de Engenharia**

### **Tarefa Principal 1: Fundações - Estrutura, Configuração e Logging**

*   **Descrição:** Construir o esqueleto do projeto. Esta é a base sobre a qual todos os outros componentes serão construídos.
*   **Depende de:** Nenhuma.

*   **Sub-tarefa 1.1: Criar a Estrutura de Diretórios**
    *   **Ação:** Definir a organização física do projeto.
    *   **Estrutura Final:**
        ```
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
        ```
    *   **Critérios de Aceitação:** A estrutura de diretórios é criada e o código de `chunkv3.py` é movido e desmembrado para os novos módulos.

*   **Sub-tarefa 1.2: Implementar Configuração Centralizada**
    *   **Ação:** Criar e popular o `config.yaml` e a função para carregá-lo.
    *   **Módulos:** `config.yaml`, `src/utils/config.py`
    *   **Exemplo (`config.yaml`):**
        ```yaml
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
        ```
    *   **Critérios de Aceitação:** O `main.py` carrega estas configurações no início da execução.

*   **Sub-tarefa 1.3: Gerenciar Dependências**
    *   **Ação:** Criar `requirements.txt` com as bibliotecas necessárias.
    *   **Bibliotecas Iniciais:** `langchain`, `pypdf`, `python-docx`, `pytesseract`, `Pillow`, `PyYAML`, `click`, `tqdm`, `spacy`, `transformers`, `torch`, `accelerate==0.30.0`, `bitsandbytes==0.43.0`.
    *   **Critérios de Aceitação:** O comando `pip install -r requirements.txt` instala todo o ambiente com sucesso.

### **Tarefa Principal 2: Framework de Extração de Conteúdo**

*   **Descrição:** Construir o sistema polimórfico para extrair texto de qualquer tipo de arquivo.
*   **Depende de:** Tarefa Principal 1.

*   **Sub-tarefa 2.1: Definir a Interface `BaseExtractor`**
    *   **Ação:** Criar a classe base abstrata para forçar um contrato comum.
    *   **Módulo:** `src/extractors/base_extractor.py`
    *   **Implementação:**
        ```python
        from abc import ABC, abstractmethod
        
        class BaseExtractor(ABC):
            @abstractmethod
            def extract(self, file_path: str) -> str:
                """Extrai conteúdo textual de um arquivo."""
                pass
        ```
    *   **Critérios de Aceitação:** A classe está definida.

*   **Sub-tarefa 2.2: Implementar Extratores Concretos**
    *   **Ação:** Criar uma classe para cada tipo de arquivo, herdando de `BaseExtractor`.
    *   **Módulos:** `pdf_extractor.py`, `docx_extractor.py`, `image_extractor.py`, `text_extractor.py`
    *   **Detalhes de Implementação e Tratamento de Erro:**
        *   **PDF:** Usar `pypdf`. Implementar `try-except` para `pypdf.errors.PdfReadError` (arquivos corrompidos) e `pypdf.errors.FileNotDecryptedError` (protegidos por senha), retornando uma string vazia e logando um aviso.
        *   **DOCX:** Usar `docx`. Envolver a extração em um `try-except` genérico para capturar possíveis erros de XML ou arquivos corrompidos.
        *   **Imagem (OCR):** Usar `Pillow` para abrir a imagem e `pytesseract` para extrair o texto. Checar se o Tesseract está instalado no sistema (usando o caminho de `config.yaml` ou `shutil.which('tesseract')`) e lançar um erro claro se não for encontrado.
        *   **Texto:** Migrar a lógica de `convert_to_text` para este módulo, tratando `UnicodeDecodeError`.
    *   **Critérios de Aceitação:** Cada extrator lê seu tipo de arquivo com sucesso e lida com erros de forma graciosa.

*   **Sub-tarefa 2.3: Criar o "Extractor Factory"**
    *   **Ação:** Desenvolver a lógica no pipeline que mapeia extensões de arquivo para a classe extratora correta.
    *   **Módulo:** `src/core/pipeline.py`
    *   **Implementação:**
        ```python
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
        ```
    *   **Critérios de Aceitação:** O pipeline seleciona dinamicamente o extrator correto.

### **Tarefa Principal 3: Chunking Semântico e Enriquecimento de Dados**

*   **Descrição:** Refinar o coração do sistema: a divisão e o enriquecimento do conteúdo.
*   **Depende de:** Tarefa Principal 2.

*   **Sub-tarefa 3.1: Implementar Chunking por Linguagem**
    *   **Ação:** Configurar `RecursiveCharacterTextSplitter` para usar separadores específicos de cada linguagem.
    *   **Módulo:** `src/core/chunking.py`
    *   **Implementação:**
        ```python
        from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

        def chunk_content(text: str, file_extension: str) -> list[str]:
            language_map = {'.py': Language.PYTHON, '.js': Language.JS, '.md': Language.MARKDOWN}
            lang = language_map.get(file_extension)
            
            if lang:
                splitter = RecursiveCharacterTextSplitter.from_language(lang, chunk_size=..., chunk_overlap=...)
            else:
                # Fallback para texto genérico
                splitter = RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)

            return splitter.split_text(text)
        ```
    *   **Critérios de Aceitação:** A função `detect_code_blocks` é removida e a nova função de chunking está operacional.

*   **Sub-tarefa 3.2: Implementar Geração de YAML Frontmatter**
    *   **Ação:** Criar a estrutura de metadados e a função para escrevê-la.
    *   **Módulo:** `src/output/markdown_writer.py`
    *   **Esquema YAML Final:**
        ```yaml
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
        ```
    *   **Critérios de Aceitação:** Todos os chunks salvos em arquivos `.md` contêm este cabeçalho YAML.

*   **Sub-tarefa 3.3: Aprimorar a Sumarização**
    *   **Ação:** Criar um módulo de sumarização usando um modelo de `transformers`.
    *   **Módulo:** `src/core/summarizer.py`
    *   **Implementação:** Utilizar a pipeline `summarization` da biblioteca `transformers` com o modelo `t5-small`. Incluir lógica de fallback: se a sumarização falhar ou o texto for muito curto, usar as primeiras 50 palavras como resumo.
    *   **Critérios de Aceitação:** Os resumos são de qualidade superior ao método anterior e o sistema não quebra se a sumarização falhar.

### **Tarefa Principal 4: Orquestração, CLI e Otimizações**

*   **Descrição:** Unir todas as peças, criar uma interface de usuário e garantir a performance.
*   **Depende de:** Tarefas 1, 2, 3.

*   **Sub-tarefa 4.1: Construir o Pipeline Principal**
    *   **Ação:** Desenvolver a classe que orquestra todo o fluxo de trabalho.
    *   **Módulo:** `src/core/pipeline.py`
    *   **Lógica:**
        1.  Inicializar (carregar config, cache, logger).
        2.  Percorrer o diretório de entrada (`os.walk`), respeitando `ignored_dirs` e `max_recursion_depth`.
        3.  Para cada arquivo:
            a.  Verificar o cache. Se o arquivo não mudou, pular.
            b.  Obter o extrator correto.
            c.  Extrair conteúdo.
            d.  Dividir em chunks.
            e.  Para cada chunk: gerar resumo e metadados.
            f.  Escrever chunks no(s) arquivo(s) de saída usando `MarkdownWriter`.
            g.  Atualizar o cache.
    *   **Critérios de Aceitação:** O pipeline executa o processo do início ao fim.

*   **Sub-tarefa 4.2: Implementar o Sistema de Cache**
    *   **Ação:** Criar a lógica para evitar reprocessamento.
    *   **Módulo:** `src/utils/caching.py`
    *   **Estratégia:** Manter um `cache.json`. Antes de processar um arquivo, calcular o hash de seu conteúdo e comparar com o hash armazenado para aquele caminho de arquivo. Se for o mesmo, pular. Após o processamento, salvar o novo hash.
    *   **Critérios de Aceitação:** Arquivos não modificados são pulados em execuções subsequentes.

*   **Sub-tarefa 4.3: Construir a CLI com `click`**
    *   **Ação:** Desenvolver a interface de linha de comando.
    *   **Módulo:** `src/main.py`
    *   **Implementação:**
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
    *   **Critérios de Aceitação:** O script é executável via terminal com os parâmetros especificados.

### **Tarefa Principal 5: Garantia de Qualidade**

*   **Descrição:** Assegurar que o sistema é confiável e funciona como esperado.
*   **Depende de:** Tarefas 1, 2, 3, 4.

*   **Sub-tarefa 5.1: Escrever Testes Unitários**
    *   **Ação:** Criar testes para cada componente isoladamente.
    *   **Módulo:** `tests/`
    *   **O que testar:**
        *   **Extratores:** Para cada um, testar com um arquivo válido, um arquivo corrompido/inválido e um arquivo vazio. Para o de imagem, testar o que acontece se o Tesseract não estiver instalado.
        *   **Chunking:** Testar com código Python, Markdown e texto plano para verificar se os chunks são criados corretamente.
        *   **Configuração:** Testar se o `config.yaml` é carregado corretamente.
    *   **Critérios de Aceitação:** Os testes cobrem os principais cenários de sucesso e falha para cada módulo.

*   **Sub-tarefa 5.2: Escrever Testes de Integração**
    *   **Ação:** Criar um teste que executa o pipeline completo.
    *   **Módulo:** `tests/test_pipeline.py`
    *   **Cenário de Teste:** Criar um diretório de teste com subpastas e vários tipos de arquivo (`.py`, `.pdf`, `.txt`, um inválido). Executar o pipeline e verificar se a pasta de saída (`documents/`) foi criada, se contém o número esperado de arquivos `.md`, e se o conteúdo de um dos arquivos (incluindo o YAML Frontmatter) está correto.
    *   **Critérios de Aceitação:** O teste de integração passa, validando que todos os componentes trabalham juntos harmoniosamente.

### **Tarefa Principal 6: Sistema de Resilência**

*   **Descrição:** Implementar mecanismos para garantir continuidade do processamento em caso de interrupções.
*   **Depende de:** Tarefas 1-5.

*   **Sub-tarefa 6.1: Implementar Salvamento Contínuo**
    *   **Ação:** Criar sistema para salvar resultados parciais durante o processamento.
    *   **Módulo:** `src/core/pipeline.py`
    *   **Implementação:** 
        - Salvar estado do processamento em arquivo `.processing_checkpoint.json` após cada arquivo processado
        - Incluir informações sobre arquivos processados e chunks gerados
    *   **Critérios de Aceitação:** O sistema sobrevive a reinicializações mantendo o progresso.

*   **Sub-tarefa 6.2: Implementar Recuperação de Processamento**
    *   **Ação:** Criar lógica para reiniciar o processamento do ponto de interrupção.
    *   **Módulo:** `src/core/pipeline.py`
    *   **Implementação:**
        - Verificar existência de checkpoint no início da execução
        - Pular arquivos já processados com base no checkpoint
    *   **Critérios de Aceitação:** O pipeline retoma o processamento do último ponto salvo.

*   **Sub-tarefa 6.3: Implementar Limpeza Automática**
    *   **Ação:** Remover checkpoint após conclusão bem-sucedida.
    *   **Módulo:** `src/core/pipeline.py`
    *   **Implementação:** 
        - Excluir `.processing_checkpoint.json` quando todo o processamento for concluído
        - Manter checkpoint apenas em casos de interrupção
    *   **Critérios de Aceitação:** Checkpoint é removido apenas após sucesso total.
---

Este plano de engenharia é a nossa bússola. Ele é ambicioso, mas cada passo é deliberado e projetado para construir um sistema de altíssima qualidade.

**Estou pronto para iniciar a execução da Tarefa Principal 1 assim que o Mestre der o sinal verde.**