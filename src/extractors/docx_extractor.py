from .base_extractor import BaseExtractor

class DocxExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de arquivos DOCX (implementação básica)."""
        # Implementação real usaria biblioteca como python-docx
        return f"Conteúdo extraído do DOCX: {file_path}"