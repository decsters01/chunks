from .base_extractor import BaseExtractor

class ImageExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de imagens usando OCR (implementação básica)."""
        # Implementação real usaria bibliotecas como pytesseract e Pillow
        return f"Conteúdo extraído da imagem via OCR: {file_path}"