import os
import markdown
import re
from .base_extractor import BaseExtractor
from typing import Tuple, Optional

class TextExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """
        Extrai conteúdo textual de arquivos de texto, código e markdown.
        
        Args:
            file_path: Caminho do arquivo a ser processado
            
        Returns:
            Conteúdo textual extraído
            
        Raises:
            UnicodeDecodeError: Se ocorrer erro de decodificação
            Exception: Para outros erros durante a extração
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Converter markdown para texto puro removendo marcações
            if file_path.endswith('.md'):
                html = markdown.markdown(content)
                plain_text = re.sub(r'<[^>]*>', '', html)
                return plain_text
            
            return content
        except UnicodeDecodeError as ude:
            raise ude
        except Exception as e:
            raise Exception(f"Erro ao extrair texto de {file_path}: {str(e)}")