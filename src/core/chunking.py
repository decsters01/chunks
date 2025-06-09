from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from typing import List
import logging

def chunk_content(text: str, file_extension: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Divide o conteúdo em chunks usando separadores específicos por linguagem.
    
    Args:
        text: Conteúdo textual a ser dividido
        file_extension: Extensão do arquivo para determinar a linguagem
        chunk_size: Tamanho máximo de cada chunk (em caracteres)
        chunk_overlap: Sobreposição entre chunks consecutivos (em caracteres)
    
    Returns:
        Lista de chunks de texto
    """
    try:
        # Mapeamento de extensões para linguagens
        language_map = {
            '.py': Language.PYTHON,
            '.js': Language.JS,
            '.ts': Language.JS,  # TypeScript usa separadores de JS
            '.md': Language.MARKDOWN,
            '.html': Language.HTML,
            '.java': Language.JAVA,
            '.cpp': Language.CPP,
        }
        
        # Obter linguagem correspondente ou usar fallback
        lang = language_map.get(file_extension.lower())
        
        if lang:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=lang,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        else:
            # Fallback para texto genérico
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        
        return splitter.split_text(text)
    
    except Exception as e:
        logging.error(f"Erro no chunking: {str(e)}")
        # Fallback seguro: retorna o texto inteiro como único chunk
        return [text] if text else []