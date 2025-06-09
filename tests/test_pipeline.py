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