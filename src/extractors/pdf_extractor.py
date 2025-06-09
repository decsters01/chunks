from .base_extractor import BaseExtractor

class PDFExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de arquivos PDF (implementação básica)."""
        # Implementação real usaria biblioteca como pypdf
        return f"Conteúdo extraído do PDF: {file_path}"