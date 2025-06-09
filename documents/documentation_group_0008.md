# Source: main.py
Original Path: `.\src\main.py`

---
source_file: .\src\main.py
file_type: .py
file_hash: dda8da6d0512551f8515a96507677981fd012b965f61ef821594d4556c9e438a
chunk_index: 2
total_chunks: 2
content_hash: 49617a2d1a5778bf30683a3a3325a22f6b7a70c7bce32d195517be3a0380b0e6
summary: 'def main( input_dir, output_dir,. force_reprocess): configure = load_config(''config.yaml'')
  force_ reprocess = force-reprocess. try: try: configure. error (f"Diretório de saída
  inválido: {config[''processing'']''): logger.info(f"Iniciando pipeline com configuração:
  { config}") logger.error (f "Pipeline_cache.json"): try: config.error(f "Configure
  pipeline": {config}. error ( f "Configurado pipeline"): true) logger.logger.status
  (f ''Configurada pipeline''): true.'
timestamp_utc: '2025-06-09T10:23:35.246138+00:00'
---

```
def main(input_dir, output_dir, force_reprocess):
    """
    CLI principal para execução do pipeline de processamento de documentos.
    """
    try:
        # Carregar configuração padrão
        config = load_config('config.yaml')
        
        # Sobrescrever configuração com parâmetros CLI
        if input_dir:
            config['processing']['input_directory'] = os.path.abspath(input_dir)
        if output_dir:
            config['processing']['output_directory'] = os.path.abspath(output_dir)
        config['force_reprocess'] = force_reprocess
        
        # Validar diretórios
        if not os.path.isdir(config['processing']['input_directory']):
            raise ValueError(f"Diretório de entrada inválido: {config['processing']['input_directory']}")
        if not os.path.isdir(config['processing']['output_directory']):
            raise ValueError(f"Diretório de saída inválido: {config['processing']['output_directory']}")
        
        logger.info(f"Iniciando pipeline com configuração: {config}")
        
        # Inicializar pipeline
        cache_path = os.path.join(config['processing']['output_directory'], 'pipeline_cache.json')
        pipeline = Pipeline(cache_path)
        
        # Executar pipeline com barra de progresso
        pipeline.process_directory(
            root_dir=config['processing']['input_directory'],
            output_dir=config['processing']['output_directory'],
            exclude_dirs=config['processing'].get('ignored_directories', None)
        )
        logger.info("Processamento concluído.")
        click.echo("✅ Processamento concluído com sucesso!")
    
    except Exception as e:
        logger.exception("Erro durante a execução do pipeline")
        click.echo(f"❌ Erro: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()
```

---

# Source: markdown_writer.py
Original Path: `.\src\output\markdown_writer.py`

---
source_file: .\src\output\markdown_writer.py
file_type: .py
file_hash: 405df2fc6d97fa8d99a8c81cc811c7283294faf9a37d8561fabf7aafa8744115
chunk_index: 1
total_chunks: 4
content_hash: 786344b947fb53cd29750e90476b515e48424eb54cb5ba7d2bdb9c8929904052
summary: import yaml.import hashlib.import datetime, timezone.import Dict, Any, List.import
  os.from collections. import defaultdict.import logger.import generate_frontmatter.
timestamp_utc: '2025-06-09T10:23:35.247148+00:00'
---

```
import yaml
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List
import os
from collections import defaultdict
from ..utils.logger import logger

def generate_frontmatter(
    source_file: str,
    file_type: str,
    file_hash: str,
    chunk_index: int,
    total_chunks: int,
    content: str,
    summary: str
) -> str:
    """
    Gera metadados em formato YAML Frontmatter para um chunk.
    
    Args:
        source_file: Caminho do arquivo original
        file_type: Tipo do arquivo (ex: 'python', 'markdown')
        file_hash: Hash SHA256 do arquivo original
        chunk_index: Índice do chunk atual
        total_chunks: Total de chunks gerados do arquivo
        content: Conteúdo do chunk
        summary: Resumo do conteúdo do chunk
        
    Returns:
        String formatada com o YAML Frontmatter
    """
    # Calcular hash do conteúdo do chunk
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    # Gerar timestamp atual em UTC
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    # Construir dicionário de metadados
    metadata = {
        'source_file': source_file,
        'file_type': file_type,
        'file_hash': file_hash,
        'chunk_index': chunk_index,
        'total_chunks': total_chunks,
        'content_hash': content_hash,
        'summary': summary,
        'timestamp_utc': timestamp_utc
    }
    
    # Gerar YAML formatado
    yaml_content = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
    return f"---\n{yaml_content}---\n\n"
```

---

---
source_file: .\src\output\markdown_writer.py
file_type: .py
file_hash: 405df2fc6d97fa8d99a8c81cc811c7283294faf9a37d8561fabf7aafa8744115
chunk_index: 2
total_chunks: 4
content_hash: 43eb3a8e2fc68979200daeab62530a524275ca0e15de1660ebb5de38a4ddb66a
summary: 'def write_markdown_file( output_path: str, file_type: str and file_hash:
  SHA256, content: str) = generate_frontmatter.write(frontmatter) with open(output_path,
  ''w'', encoding=''utf-8'') as f: f:.write(''markdown'', f:write(''frontmatter''),
  f:f:. write(''content'', f):.write("markdown", f:file_hash, f:output), f:frontmatter),
  f.write (''content'', ''markdown'') = f:writer(''writeMarkdown'', ''frontmatter'',
  ''content''):. WriteMarkdown() = writeMarkdown(''front'
timestamp_utc: '2025-06-09T10:23:35.247148+00:00'
---

```
def write_markdown_file(
    output_path: str,
    source_file: str,
    file_type: str,
    file_hash: str,
    chunk_index: int,
    total_chunks: int,
    content: str,
    summary: str
) -> None:
    """
    Escreve um arquivo Markdown com YAML Frontmatter.
    
    Args:
        output_path: Caminho do arquivo de saída
        source_file: Caminho do arquivo original
        file_type: Tipo do arquivo
        file_hash: Hash SHA256 do arquivo original
        chunk_index: Índice do chunk
        total_chunks: Total de chunks
        content: Conteúdo do chunk
        summary: Resumo do conteúdo
    """
    frontmatter = generate_frontmatter(
        source_file=source_file,
        file_type=file_type,
        file_hash=file_hash,
        chunk_index=chunk_index,
        total_chunks=total_chunks,
        content=content,
        summary=summary
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(content)
```

---

---
source_file: .\src\output\markdown_writer.py
file_type: .py
file_hash: 405df2fc6d97fa8d99a8c81cc811c7283294faf9a37d8561fabf7aafa8744115
chunk_index: 3
total_chunks: 4
content_hash: 3898aba93dfe00c865447ce4def2290fb73365a9f3d58d1f383e09327e2573b1
summary: 'def write_grouped_markdown_files(all_chunks_info: List[Dict], output_dir:
  str, max_files: int): """ Escreve todos os chunks em um número limitado de arquivos
  Markdown, agrupando por fonte.'
timestamp_utc: '2025-06-09T10:23:35.248159+00:00'
---

```
def write_grouped_markdown_files(all_chunks_info: List[Dict], output_dir: str, max_files: int):
    """
    Escreve todos os chunks em um número limitado de arquivos Markdown, agrupando por fonte.
    """
    total_chunks = len(all_chunks_info)
    if not total_chunks:
        return

    num_output_files = min(max_files, total_chunks) if total_chunks > 0 else 0
    if num_output_files <= 0:
        num_output_files = 1
    
    all_chunks_info.sort(key=lambda x: x['source_file'])

    # Distribute chunks evenly across files
    chunk_start_idx = 0
    for i in range(num_output_files):
        num_chunks_this_file = total_chunks // num_output_files
        if i < total_chunks % num_output_files:
            num_chunks_this_file += 1
        
        chunk_end_idx = min(chunk_start_idx + num_chunks_this_file, total_chunks)
        file_chunks = all_chunks_info[chunk_start_idx:chunk_end_idx]
        chunk_start_idx = chunk_end_idx

        if not file_chunks:
            continue

        output_path = os.path.join(output_dir, f"documentation_group_{i:04d}.md")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Group chunks within the file by their original source
            chunks_by_source = defaultdict(list)
            for chunk_info in file_chunks:
                chunks_by_source[chunk_info['source_file']].append(chunk_info)
            
            for source_file, chunks_from_source in chunks_by_source.items():
                base_name = os.path.basename(source_file)
                f.write(f"# Source: {base_name}\n")
                f.write(f"Original Path: `{source_file}`\n\n")
                
                chunks_from_source.sort(key=lambda c: c['chunk_index'])
```

---

---
source_file: .\src\output\markdown_writer.py
file_type: .py
file_hash: 405df2fc6d97fa8d99a8c81cc811c7283294faf9a37d8561fabf7aafa8744115
chunk_index: 4
total_chunks: 4
content_hash: 6778496faee1a3de01433ce73201502ed0560eaa294d0f709a4bea71d216f670
summary: 'for chunk in chunks_from_source: # Regenerate frontmatter for clarity within
  the grouped file. frontmatter = generate_frontmatter( source_file, file_hash, summary,
  total_chunks, chunk_index) frontmatter.write(frontmatter) logger.info(f"Saved: {output_path}")
  logger.write("---\n\n") f.write($frontmatter), f. write(''frontmatter'', ''frontmatter'')
  logger.get(''summary'', ''N/A'', ''total_chunk'', ''chunk_index'', ''TotalChunks'',
  ''content'', ''file_hash'', ''ChunkChunkIndex'', '' totalChunks'''
timestamp_utc: '2025-06-09T10:23:35.248159+00:00'
---

```
for chunk in chunks_from_source:
                    # Regenerate frontmatter for clarity within the grouped file
                    frontmatter = generate_frontmatter(
                        source_file=chunk['source_file'],
                        file_type=chunk['file_type'],
                        file_hash=chunk['file_hash'],
                        chunk_index=chunk['chunk_index'],
                        total_chunks=chunk['total_chunks'],
                        content=chunk['content'],
                        summary=chunk.get('summary', 'N/A')
                    )
                    f.write(frontmatter)
                    f.write(f"```\n{chunk['content']}\n```\n\n")
                    f.write("---\n\n")
        logger.info(f"Saved: {output_path}")
```

---

# Source: caching.py
Original Path: `.\src\utils\caching.py`

---
source_file: .\src\utils\caching.py
file_type: .py
file_hash: a05ae2271b53aa6610ecca5e9961c510fa410c8d9e7954c8e3249be71021c588
chunk_index: 1
total_chunks: 4
content_hash: 0e8df080f708548e3ba620bf19887d728024c2acd876036554698ddf52e31dfc
summary: ' import Dict, Optional from .logger import logger. import threading from
  .threading import msvcrt.import json from .jstl import json.import os from .os from
  .stl.'
timestamp_utc: '2025-06-09T10:23:35.249211+00:00'
---

```
import json
import os
import threading
import msvcrt
from typing import Dict, Optional
from .logger import logger
```

---

---
source_file: .\src\utils\caching.py
file_type: .py
file_hash: a05ae2271b53aa6610ecca5e9961c510fa410c8d9e7954c8e3249be71021c588
chunk_index: 2
total_chunks: 4
content_hash: 55258d127798cfa5fbea2b18bedba0701064d40d7f3dfaebafbc73b4161a895b
summary: 'class CacheManager: configureCacheManager() { def __init__(self, cache_path:
  str): self.lock = threading.RLock() self.cache: Dict[str, str] = {} self.Cache =
  self.load_cache() def _load_ cache(self) : self. cache = self._load_Cache() except
  (PermissionError, OSError) as e: logger.warning(f"Falha no cache em disco: {e}.
  Usando cache em memória.") # Verifica permissões e carrega cache.'
timestamp_utc: '2025-06-09T10:23:35.249211+00:00'
---

```
class CacheManager:
    def __init__(self, cache_path: str):
        """
        Inicializa o gerenciador de cache com fallback para memória.
        
        Args:
            cache_path: Caminho para o arquivo de cache JSON
        """
        self.cache_path = cache_path
        self._in_memory_only = False
        self._lock = threading.RLock()
        self.cache: Dict[str, str] = {}
        
        try:
            # Verifica permissões e carrega cache inicial
            if os.path.exists(self.cache_path):
                if not os.access(self.cache_path, os.R_OK):
                    raise PermissionError(f"Sem permissão de leitura: {self.cache_path}")
                
            self.cache = self._load_cache()
        except (PermissionError, OSError) as e:
            logger.warning(f"Falha no cache em disco: {e}. Usando cache em memória.")
            self._in_memory_only = True
            self.cache = {}

    def _load_cache(self) -> Dict[str, str]:
        """Carrega cache do arquivo com file locking."""
        if not os.path.exists(self.cache_path):
            return {}
        
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                # Lock compartilhado para leitura
                msvcrt.locking(f.fileno(), msvcrt.LK_NBRLCK, 1)
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar cache: {str(e)}")
            return {}
        finally:
            try:
                if f:
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass
```

---

---
source_file: .\src\utils\caching.py
file_type: .py
file_hash: a05ae2271b53aa6610ecca5e9961c510fa410c8d9e7954c8e3249be71021c588
chunk_index: 3
total_chunks: 4
content_hash: c6634fa637b0649f977421686c5703771101c4d0cdc95b7ae416cbb7508b12e8
summary: 'def _save_cache(self): """Salva cache no arquivo com verificação de permissões
  e locking.""" if self._in_memory_only: return return. # Verifica permissão de escrita
  if os.path.exists(self.cache_path): return.'
timestamp_utc: '2025-06-09T10:23:35.250223+00:00'
---

```
def _save_cache(self):
        """Salva cache no arquivo com verificação de permissões e locking."""
        if self._in_memory_only:
            return
            
        try:
            # Verifica permissões de escrita
            if os.path.exists(self.cache_path):
                if not os.access(self.cache_path, os.W_OK):
                    raise PermissionError(f"Sem permissão de escrita: {self.cache_path}")
            else:
                dir_path = os.path.dirname(self.cache_path)
                if not os.access(dir_path, os.W_OK):
                    raise PermissionError(f"Sem permissão de escrita no diretório: {dir_path}")
            
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                # Lock exclusivo para escrita
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                json.dump(self.cache, f, indent=2)
        except (PermissionError, OSError) as e:
            logger.error(f"Falha ao salvar cache: {e}. Ativando modo memória.")
            self._in_memory_only = True
        except Exception as e:
            logger.error(f"Erro não tratado ao salvar cache: {str(e)}")
        finally:
            try:
                if f:
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

    def is_unchanged(self, file_path: str, current_hash: str) -> bool:
        """Verifica se arquivo está inalterado com thread locking."""
        with self._lock:
            cached_hash = self.cache.get(file_path)
            return cached_hash == current_hash

    def update(self, file_path: str, new_hash: str):
        """Atualiza cache com thread locking e fallback."""
        with self._lock:
            self.cache[file_path] = new_hash
            if not self._in_memory_only:
                self._save_cache()
            logger.debug(f"Cache atualizado para {file_path}")
```

---

---
source_file: .\src\utils\caching.py
file_type: .py
file_hash: a05ae2271b53aa6610ecca5e9961c510fa410c8d9e7954c8e3249be71021c588
chunk_index: 4
total_chunks: 4
content_hash: 08f8fea9d986aa824c224959a74fccab97236ed8e6bbd8fd2a93d89b81a078a0
summary: 'def clear(self): """Limpa cache com tratamento de erros granular.""" self.cache
  = {} with self.lock as self: self. cache = self.Cache; if self.in_memory_only: return
  self; if os.path.exists(self.cache_path): return os.Path.Exists; if OSError is not
  existent: return oserror; if PermissionError is not present: return e; if Exception
  is present, return e. If self.locked is true, return self.Lock.'
timestamp_utc: '2025-06-09T10:23:35.250223+00:00'
---

```
def clear(self):
        """Limpa cache com tratamento de erros granular."""
        with self._lock:
            self.cache = {}
            if self._in_memory_only:
                return
                
            try:
                if os.path.exists(self.cache_path):
                    os.remove(self.cache_path)
            except PermissionError as e:
                logger.error(f"Sem permissão para limpar cache: {str(e)}")
            except OSError as e:
                logger.error(f"Erro ao limpar cache: {str(e)}")
            except Exception as e:
                logger.error(f"Erro não tratado ao limpar cache: {str(e)}")
```

---

