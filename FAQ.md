# Perguntas Frequentes e Solução de Problemas

## 1. Instalação e Configuração
### P: Como resolver erros de dependência durante a instalação?
**R**: 
1. Verifique a versão do Python (`python --version` deve ser 3.9+)
2. Atualize o pip: `pip install --upgrade pip`
3. Instale dependências manualmente:
```bash
pip install pdfminer.six python-docx pytesseract pillow
```

### P: O sistema não reconhece meu arquivo PDF/DOCX
**R**:
1. Verifique se o extrator está habilitado no `config.yaml`
2. Para PDFs, instale o pdfminer: `pip install pdfminer.six`
3. Para DOCX, instale: `pip install python-docx`

## 2. Processamento de Arquivos
### P: Meus chunks estão muito pequenos ou muito grandes
**R**: Ajuste os parâmetros no `config.yaml`:
```yaml
chunking:
  max_tokens: 768  # Aumente para chunks maiores
  min_lines: 8     # Aumente o mínimo de linhas
  strategy: semantic # Ou 'fixed' para tamanho fixo
```

### P: O OCR para imagens não está funcionando
**R**:
1. Verifique instalação do Tesseract:
   - Windows: Baixe do site oficial
   - Linux: `sudo apt install tesseract-ocr`
   - MacOS: `brew install tesseract`
2. Instale pacotes de idioma: `sudo apt install tesseract-ocr-por`

## 3. Desempenho
### P: O processamento está muito lento para muitos arquivos
**R**:
1. Ative o cache no `config.yaml`:
```yaml
caching:
  enabled: true
  path: .processing_cache
```
2. Use processamento paralelo:
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    executor.map(pipeline.process_file, file_list)
```

### P: Como processar apenas arquivos modificados?
**R**: Use o sistema de cache integrado:
```python
from src.utils.caching import FileCache

cache = FileCache()
if not cache.is_cached(file_path):
    process_file(file_path)
```

## 4. Saída e Resultados
### P: Os arquivos de saída não estão sendo gerados
**R**:
1. Verifique permissões de escrita no diretório de saída
2. Confira o caminho no `config.yaml`:
```yaml
output:
  directory: /caminho/valido
```
3. Verifique logs em `processing.log`

### P: Metadados estão faltando na saída
**R**: Ative a opção no config:
```yaml
output:
  include_metadata: true
```

## 5. Erros Comuns
### Erro: `ModuleNotFoundError: No module named '...'`
**Solução**: Instale o módulo faltante com `pip install nome_do_modulo`

### Erro: `UnsupportedFileFormatError`
**Solução**:
1. Verifique a extensão do arquivo
2. Implemente um extrator customizado (veja [EXEMPLOS.md](EXEMPLOS.md))

### Erro: `EncodingError` em arquivos de texto
**Solução**: Especifique a codificação no config:
```yaml
extractors:
  text:
    encoding: 'latin-1' # Ou 'utf-8'
```

## 6. Personalização
### P: Como adicionar suporte a um novo formato de arquivo?
**R**: 
1. Crie um novo extrator herdando de `BaseExtractor`
2. Implemente o método `extract()`
3. Registre no pipeline:
```python
pipeline.register_extractor('.minhaext', MeuExtrator())
```
(Exemplo completo em [EXEMPLOS.md](EXEMPLOS.md))

### P: Como alterar o modelo de sumarização?
**R**: 
1. Escolha um modelo do [Hugging Face](https://huggingface.co/models)
2. Atualize o config:
```yaml
summarization:
  model: nome_do_modelo
```

## 7. Contribuição
### P: Como contribuir para o projeto?
**R**:
1. Faça fork do repositório
2. Siga as diretrizes de código
3. Envie pull requests com:
   - Testes unitários para novas funcionalidades
   - Documentação atualizada
   - Exemplos de uso

### P: Onde reportar bugs?
**R**: Abra issues no repositório do projeto incluindo:
1. Passos para reproduzir o erro
2. Mensagem de erro completa
3. Ambiente (SO, versão do Python)
4. Arquivo de configuração relevante