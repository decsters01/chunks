import os
import hashlib
import json
from typing import List, Dict, Optional
from collections import defaultdict
from tqdm import tqdm

from ..extractors.base_extractor import BaseExtractor
from ..extractors.text_extractor import TextExtractor
from ..extractors.pdf_extractor import PDFExtractor
from ..extractors.docx_extractor import DocxExtractor
from .chunking import chunk_content
from .summarizer import BatchSummarizer
from ..output.markdown_writer import write_markdown_file, write_grouped_markdown_files
from ..utils.caching import CacheManager
from ..utils.logger import logger

class Pipeline:
    def __init__(self, cache_path: str = "pipeline_cache.json"):
        self.cache_manager = CacheManager(cache_path)
        self.extractors: Dict[str, BaseExtractor] = {
            # Text-based
            '.md': TextExtractor(),
            '.txt': TextExtractor(),
            '.json': TextExtractor(),
            '.yaml': TextExtractor(),
            '.html': TextExtractor(),
            '.css': TextExtractor(),
            # Code
            '.py': TextExtractor(),
            '.js': TextExtractor(),
            '.ts': TextExtractor(),
            '.java': TextExtractor(),
            '.cpp': TextExtractor(),
            '.c': TextExtractor(),
            '.h': TextExtractor(),
            '.hpp': TextExtractor(),
            '.cs': TextExtractor(),
            # Other types can be added here
            # '.pdf': PDFExtractor(),
            # '.docx': DocxExtractor(),
        }

    def get_extractor(self, file_path: str) -> Optional[BaseExtractor]:
        ext = os.path.splitext(file_path)[1].lower()
        return self.extractors.get(ext)

    def _compute_file_hash(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def process_directory(self, root_dir: str, output_dir: str, exclude_dirs: Optional[List[str]] = None, max_markdown_files: Optional[int] = None, force_reprocess: bool = False):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if force_reprocess:
            logger.info("Forçando reprocessamento, limpando cache.")
            self.cache_manager.clear()

        if max_markdown_files is not None:
            logger.info(f"Modo de agrupamento ativado. Limpando arquivos .md de: {output_dir}")
            for item in os.listdir(output_dir):
                if item.endswith('.md'):
                    try:
                        os.remove(os.path.join(output_dir, item))
                    except OSError as e:
                        logger.warning(f"Não foi possível remover o arquivo {item}: {e}")

        # Configuração do checkpoint
        checkpoint_file = os.path.join(output_dir, '.processing_checkpoint.json')
        processed_chunks = set()
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r') as f:
                    processed_chunks = set(json.load(f))
                logger.info(f"Carregado checkpoint: {len(processed_chunks)} chunks já processados")
            except Exception as e:
                logger.warning(f"Erro ao carregar checkpoint: {e}")
                processed_chunks = set()

        files_to_process = []
        exclude_dirs_set = set(exclude_dirs or [])
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs_set and not d.startswith('.')]
            
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if self.get_extractor(file_path):
                    files_to_process.append(file_path)

        all_chunks_info = []
        logger.info(f"Encontrados {len(files_to_process)} arquivos para processar.")
        for file_path in tqdm(files_to_process, desc="Analisando arquivos"):
            try:
                current_hash = self._compute_file_hash(file_path)
                if not force_reprocess and self.cache_manager.is_unchanged(file_path, current_hash):
                    logger.debug(f"Arquivo inalterado, pulando: {file_path}")
                    continue

                extractor = self.get_extractor(file_path)
                if not extractor:
                    continue
                
                content = extractor.extract(file_path)
                file_extension = os.path.splitext(file_path)[1]
                chunks = chunk_content(content, file_extension, chunk_size=2000, chunk_overlap=200)

                if not chunks:
                    continue

                for i, chunk_text in enumerate(chunks):
                    chunk_id = f"{file_path}:{i+1}"
                    chunk_info = {
                        'source_file': file_path,
                        'file_type': file_extension,
                        'file_hash': current_hash,
                        'chunk_index': i + 1,
                        'total_chunks': len(chunks),
                        'content': chunk_text,
                        'chunk_id': chunk_id,
                    }
                    all_chunks_info.append(chunk_info)

            except Exception as e:
                logger.error(f"Erro ao processar {file_path}: {str(e)}")

        if not all_chunks_info:
            logger.info("Nenhum chunk novo para processar.")
            return

        # Filtrar chunks já processados
        chunks_to_process = [chunk for chunk in all_chunks_info if chunk['chunk_id'] not in processed_chunks]
        logger.info(f"Total de chunks a processar: {len(chunks_to_process)} (de um total de {len(all_chunks_info)} chunks)")

        try:
            logger.info(f"Gerando resumos em lote para {len(chunks_to_process)} chunks...")
            summarizer = BatchSummarizer()
            contents = [chunk['content'] for chunk in chunks_to_process]
            if contents:
                summaries = summarizer.summarize_batch(contents)
                for i, chunk in enumerate(chunks_to_process):
                    chunk['summary'] = summaries[i]
            else:
                logger.info("Nenhum chunk novo para resumir.")
        except Exception as e:
            logger.error(f"Erro durante o processamento em lote: {str(e)}")
            raise
        
        # Salvamento incremental
        if max_markdown_files is None:
            logger.info("Salvando chunks incrementalmente...")
            for chunk in tqdm(chunks_to_process, desc="Salvando chunks"):
                source_path = os.path.relpath(chunk['source_file'], root_dir)
                output_sub_dir = os.path.join(output_dir, os.path.dirname(source_path))
                os.makedirs(output_sub_dir, exist_ok=True)
                
                base_name = os.path.splitext(os.path.basename(chunk['source_file']))[0]
                chunk_file_name = f"{base_name}_chunk_{chunk['chunk_index']}.md"
                output_path = os.path.join(output_sub_dir, chunk_file_name)
                
                write_markdown_file(output_path=output_path, **chunk)
                
                # Atualizar checkpoint
                processed_chunks.add(chunk['chunk_id'])
                try:
                    with open(checkpoint_file, 'w') as f:
                        json.dump(list(processed_chunks), f)
                except Exception as e:
                    logger.error(f"Erro ao salvar checkpoint: {e}")
        else:
            logger.info(f"Agrupando {len(all_chunks_info)} chunks em até {max_markdown_files} arquivos.")
            write_grouped_markdown_files(all_chunks_info, output_dir, max_markdown_files)
        
        logger.info("Atualizando cache principal...")
        processed_files = {chunk['source_file']: chunk['file_hash'] for chunk in all_chunks_info}
        for file_path, file_hash in processed_files.items():
            self.cache_manager.update(file_path, file_hash)
        
        # Limpeza do checkpoint após sucesso
        if max_markdown_files is None:
            try:
                if os.path.exists(checkpoint_file):
                    os.remove(checkpoint_file)
                    logger.info("Checkpoint removido após processamento bem-sucedido.")
            except Exception as e:
                logger.warning(f"Erro ao remover checkpoint: {e}")
        
        logger.info("Processamento concluído.")