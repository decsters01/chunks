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