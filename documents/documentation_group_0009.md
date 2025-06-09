# Source: config.py
Original Path: `.\src\utils\config.py`

---
source_file: .\src\utils\config.py
file_type: .py
file_hash: e1fa7b81d3fe6da2dee30501325cd717fcd5061607008aa76d3f87bac4b27c7b
chunk_index: 1
total_chunks: 1
content_hash: 5797721c0cc7902ac05954929aa5f341ae83242e425286230b0c5c58f984b166
summary: 'def load_config(config_path: str, dict: dict) : "Load configuration from
  a YAML file" yaml.safe_load(f) = "YAML: load configuration" pathlib.path: "path"
  = "path/to/path" path: "Path: Path"'
timestamp_utc: '2025-06-09T10:23:35.252260+00:00'
---

```
import yaml
from pathlib import Path

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
```

---

# Source: logger.py
Original Path: `.\src\utils\logger.py`

---
source_file: .\src\utils\logger.py
file_type: .py
file_hash: 370e7e0ce7a57ad95560182a39624c10a21ef5ebcac0f3eaf8f4bc52dab4954f
chunk_index: 1
total_chunks: 1
content_hash: 4ff795cafb5096d5011b75aa198c91aa6d1c5617f458abbe861b8ae0c4d2a5b8
summary: import logging.basicConfig(.), level=logging.INFO, format='%(asctime)s -
  %(name)s, %(levelname) s - % (message)s', handlers=Logging.StreamHandler(os.environ['LOG_FILE'),
  logger.addHandler(file_handler).), setup_logger(){ logger.setFormatter('%( asctime),%(name),%
  (levelname), %(message),%('message') }); logger.logger()()()(); logger.getLogger('pipeline_
  logger')()()()); logger.startLogger()(){ logging.Stream Handler()() }); logger
timestamp_utc: '2025-06-09T10:23:35.252260+00:00'
---

```
import logging
import os

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Criação do logger principal
logger = logging.getLogger('pipeline_logger')

# Adiciona handler para arquivo se variável de ambiente estiver definida
if os.environ.get('LOG_FILE'):
    file_handler = logging.FileHandler(os.environ['LOG_FILE'])
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

def setup_logger():
    """Configura e retorna o logger principal."""
    return logger
```

---

# Source: test_chunkv3.py
Original Path: `.\test_chunkv3.py`

---
source_file: .\test_chunkv3.py
file_type: .py
file_hash: 1593010f8fe252101f439b86a2749b9a05fc1f5de0f67f0974e772edf8b67bda
chunk_index: 1
total_chunks: 3
content_hash: 138459ab193a2f23737309c6eb056e647d6d945c539e677bfff7051e55104b3b
summary: ' import detect_code_blocks, convert_to_text, process_file, tempfile, re,
  shutil. import unittest, os, re and shutil from chunkv3.'
timestamp_utc: '2025-06-09T10:23:35.253269+00:00'
---

```
import unittest
import os
import re
from chunkv3 import detect_code_blocks, convert_to_text, process_file
import tempfile
import shutil
```

---

---
source_file: .\test_chunkv3.py
file_type: .py
file_hash: 1593010f8fe252101f439b86a2749b9a05fc1f5de0f67f0974e772edf8b67bda
chunk_index: 2
total_chunks: 3
content_hash: 99037310e6b86a922e2269d4de09119004a88ad755edffa6b2f0cc006d8bf831
summary: 'class TestChunkv3(unittest.TestCase): configure.TestChunk(TestCase) { def
  test_regex_patterns(self): self.assertIsNotNone(re.match(r"^\s*#{1,6}\s+", md_line),
  chat_line: "John (10:30): Hello world!" }); def test-variable_initialization(self:
  self: test_variable_Initialization) { self.test_variable-initialization (self: test-
  variable-initialize) });'
timestamp_utc: '2025-06-09T10:23:35.253269+00:00'
---

```
class TestChunkv3(unittest.TestCase):
    def test_regex_patterns(self):
        """Testa os padrões regex corrigidos"""
        # Teste padrão de chat
        chat_line = "John (10:30): Hello world!"
        self.assertIsNotNone(re.match(r"^\s*[\w\s.-]+(?:\s*\(\d{2}:\d{2}(?::\d{2})?\))?\s*:\s+", chat_line))
        
        # Teste padrão markdown
        md_line = "### Título"
        self.assertIsNotNone(re.match(r"^\s*#{1,6}\s+", md_line))
        
        # Teste padrão apostila
        apostila_line = "CAPÍTULO 1 Introdução"
        self.assertIsNotNone(re.match(r"^(?:CAP[IÍ]TULO|SECTION|SE[CÇ][ÃA]O)\s*\d+|^\d+(?:\.\d+)*\s+[A-ZÀ-ÖØ-Þ][\w\sÀ-ÖØ-Þ]*|^[A-ZÀ-ÖØ-Þ\s_]{5,}$", apostila_line, re.IGNORECASE))

    def test_variable_initialization(self):
        """Verifica se variáveis são inicializadas em todos os caminhos"""
        # Teste com arquivo vazio
        markers = detect_code_blocks("", ".txt")
        self.assertEqual(markers, [0])
        
        # Teste com conteúdo mínimo
        markers = detect_code_blocks("single line", ".txt")
        self.assertTrue(len(markers) >= 2)

    def test_exception_handling(self):
        """Testa o tratamento de exceções"""
        # Criar arquivo temporário inválido
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(b"\x80invalid utf-8")
            tmp_path = tmp.name
        
        try:
            content, error_info = convert_to_text(tmp_path)
            self.assertEqual(content, "")
            self.assertIsNotNone(error_info)  # Verifica se houve informações de erro
        finally:
            os.unlink(tmp_path)
```

---

---
source_file: .\test_chunkv3.py
file_type: .py
file_hash: 1593010f8fe252101f439b86a2749b9a05fc1f5de0f67f0974e772edf8b67bda
chunk_index: 3
total_chunks: 3
content_hash: bbabb99374adac31e6ad4fd639c4e9a358e4ba0f697aab72c81329a3c12fe3eb
summary: 'def test_parallel_processing(self): """Testa o processamento paralelo com
  tratamento de erros" # Criar arquivos válidos devem gerar chunks. # Verificar resultados"
  self.assertEqual(len(chunks), 3)'
timestamp_utc: '2025-06-09T10:23:35.254306+00:00'
---

```
def test_parallel_processing(self):
        """Testa o processamento paralelo com tratamento de erros"""
        # Criar diretório de teste
        test_dir = "test_data"
        os.makedirs(test_dir, exist_ok=True)
        
        # Criar arquivos válidos e inválidos
        valid_files = []
        for i in range(3):
            path = os.path.join(test_dir, f"valid_{i}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Arquivo válido {i}")
            valid_files.append(path)
        
        invalid_file = os.path.join(test_dir, "invalid.bin")
        with open(invalid_file, "wb") as f:
            f.write(b"\x80invalid")
        
        # Processar arquivos
        chunks = []
        for file in valid_files + [invalid_file]:
            chunks.extend(process_file(file))
        
        # Verificar resultados
        self.assertEqual(len(chunks), 3)  # Apenas arquivos válidos devem gerar chunks
        self.assertTrue(os.path.exists("erros_paralelos.log"))
        
        # Limpar
        shutil.rmtree(test_dir)
        os.remove("erros_paralelos.log")

if __name__ == '__main__':
    unittest.main()
```

---

# Source: test_pipeline.py
Original Path: `.\tests\test_pipeline.py`

---
source_file: .\tests\test_pipeline.py
file_type: .py
file_hash: 4060201c311d413ea1969f853ea9758b9ca2275399ebb0a078a05335f36cb066
chunk_index: 1
total_chunks: 4
content_hash: 5625e7fbfcf7f75260430a55415476f2aebbfbe5fbbfb29e3d5a846c17991c47
summary: 'import pytestimport osimport shutilfrom unittest.mock import patch, MagicMockfromsrc.core.pipeline
  import run_pipelinesfrom src.caching import CacheManager@pytest.fixturedef setup_test_environment(tmp_path):
  # Configurar diretórios temporários.'
timestamp_utc: '2025-06-09T10:23:35.254306+00:00'
---

```
import pytest
import os
import shutil
from unittest.mock import patch, MagicMock
from src.core.pipeline import run_pipeline
from src.utils.caching import CacheManager

@pytest.fixture
def setup_test_environment(tmp_path):
    # Configurar diretórios temporários
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    cache_dir = tmp_path / "cache"
    
    input_dir.mkdir()
    output_dir.mkdir()
    cache_dir.mkdir()
    
    # Criar arquivos de teste
    (input_dir / "test.py").write_text("print('Hello Python')")
    (input_dir / "test.txt").write_text("Text file content")
    (input_dir / "test.pdf").write_bytes(b"%PDF-1.4 dummy content")
    (input_dir / "test.docx").write_bytes(b"dummy docx content")
    (input_dir / "invalid_file.invalid").write_text("Invalid content")
    
    return input_dir, output_dir, cache_dir
```

---

---
source_file: .\tests\test_pipeline.py
file_type: .py
file_hash: 4060201c311d413ea1969f853ea9758b9ca2275399ebb0a078a05335f36cb066
chunk_index: 2
total_chunks: 4
content_hash: 01ce29d10501f14a4d9c19ed2dc033ef5c84965868678f4cff6708f30a76ea49
summary: 'def test_pipeline_integration(setup_test_environment): # Mock dos extractors    with
  patch("src.extractors.text_extractor.TextExtractor") as mock_ text_extract. # Verificar
  geração de arquivos Markdown (chunks)'
timestamp_utc: '2025-06-09T10:23:35.255338+00:00'
---

```
def test_pipeline_integration(setup_test_environment):
    input_dir, output_dir, cache_dir = setup_test_environment
    
    # Mock dos extractors
    with patch("src.extractors.text_extractor.TextExtractor.extract") as mock_text_extract, \
         patch("src.extractors.pdf_extractor.PDFExtractor.extract") as mock_pdf_extract, \
         patch("src.extractors.docx_extractor.DocxExtractor.extract") as mock_docx_extract:
        
        mock_text_extract.return_value = "Extracted text content"
        mock_pdf_extract.return_value = "Extracted PDF content"
        mock_docx_extract.return_value = "Extracted DOCX content"
        
        # Executar pipeline
        run_pipeline(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            cache_dir=str(cache_dir)
        )
    
    # Verificar geração de arquivos Markdown (chunks)
    assert os.path.exists(output_dir / "test.py.md.chunk1")
    assert os.path.exists(output_dir / "test.txt.md.chunk1")
    assert os.path.exists(output_dir / "test.pdf.md.chunk1")
    assert os.path.exists(output_dir / "test.docx.md.chunk1")
    assert not os.path.exists(output_dir / "invalid_file.invalid.md.chunk1")
    
    # Verificar frontmatter e conteúdo em um chunk
    with open(output_dir / "test.py.md.chunk1", "r") as f:
        content = f.read()
        assert "---" in content
        assert "Extracted text content" in content
    
    # Verificar funcionamento do cache (acesso direto ao dicionário)
    cache = CacheManager(str(cache_dir))
    assert cache.cache.get(str(input_dir / "test.py")) is not None
    
    # Verificar tratamento de erro (arquivo inválido)
    # (Assume-se que erros são logados - verificação seria via captura de logs)
```

---

---
source_file: .\tests\test_pipeline.py
file_type: .py
file_hash: 4060201c311d413ea1969f853ea9758b9ca2275399ebb0a078a05335f36cb066
chunk_index: 3
total_chunks: 4
content_hash: 568b097f192255f8d2f6acbdd98c63d9858add0a4fc8a22715a5e195052b44d4
summary: 'def test_cache_behavior(setup_test_environment): input, output, cache_dir,
  mock_extract = true; test_error_handling = false; test.assert_not_called() # Primeira
  execução (preenche cache) with patch("src.extractors.text_extractor.TextExtractor.extractor"),
  side_effect=Exception("Extraction error"): test.test_error.handling() # Segunda
  execuça (deve usar cache), mock.test.test()    # Forçar erro em um extractor with
  patch(''src.pdf_extraction.PDFExtractor''), side_'
timestamp_utc: '2025-06-09T10:23:35.255338+00:00'
---

```
def test_cache_behavior(setup_test_environment):
    input_dir, output_dir, cache_dir = setup_test_environment
    
    # Primeira execução (preenche cache)
    run_pipeline(
        input_dir=str(input_dir),
        output_dir=str(output_dir),
        cache_dir=str(cache_dir)
    )
    
    # Segunda execução (deve usar cache)
    with patch("src.extractors.text_extractor.TextExtractor.extract") as mock_extract:
        run_pipeline(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            cache_dir=str(cache_dir)
        )
        mock_extract.assert_not_called()

def test_error_handling(setup_test_environment, caplog):
    input_dir, output_dir, cache_dir = setup_test_environment
    
    # Forçar erro em um extractor
    with patch("src.extractors.pdf_extractor.PDFExtractor.extract", 
               side_effect=Exception("Extraction error")):
        run_pipeline(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            cache_dir=str(cache_dir)
        )
    
    # Verificar se erro foi tratado corretamente (mensagem em português)
    assert "Erro ao processar" in caplog.text
    assert "test.pdf" in caplog.text

def test_cache_permission_errors(setup_test_environment, caplog):
    """Testa resiliência do cache a erros de permissão"""
    input_dir, output_dir, cache_dir = setup_test_environment
    cache_file = cache_dir / "cache.json"
    
    # Criar arquivo de cache sem permissões de escrita
    cache_file.write_text("{}")
    os.chmod(cache_file, 0o400)  # Somente leitura
    
    # Forçar atualização do cache para disparar erro de escrita
    cache = CacheManager(str(cache_file))
    cache.update("test_file.txt", "hash123")
    
    # Verificar logs de fallback
    assert "Falha ao salvar cache" in caplog.text
    assert "Ativando modo memória" in caplog.text
    assert "Falha ao salvar cache" in caplog.text
```

---

---
source_file: .\tests\test_pipeline.py
file_type: .py
file_hash: 4060201c311d413ea1969f853ea9758b9ca2275399ebb0a078a05335f36cb066
chunk_index: 4
total_chunks: 4
content_hash: a63216d208a5b03dbbe51fdf49dfc91f2d4515a5104049bf8df22df27c09ab50
summary: 'def test_cache_concurrency(setup_test_environment): """Testa comportamento
  do cache em operações concorrentes" cache_file = cache_dir / "cache.json" # Criar
  múltiplas threads. threads = [] for t in range(5): t = threading.Thread(target=worker)
  t.append(t)'
timestamp_utc: '2025-06-09T10:23:35.256391+00:00'
---

```
def test_cache_concurrency(setup_test_environment):
    """Testa comportamento do cache em operações concorrentes"""
    import threading
    input_dir, output_dir, cache_dir = setup_test_environment
    cache_file = cache_dir / "cache.json"
    
    # Criar arquivo de cache
    cache_file.write_text("{}")
    
    # Função para simular acesso concorrente
    def worker():
        cache = CacheManager(str(cache_file))
        cache.update("file.txt", "hash123")
    
    # Criar múltiplas threads
    threads = []
    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    # Aguardar conclusão
    for t in threads:
        t.join()
    
    # Verificar se o cache foi atualizado corretamente
    cache = CacheManager(str(cache_file))
    assert cache.is_unchanged("file.txt", "hash123")
```

---

