# Source: summarizer.py
Original Path: `.\src\core\summarizer.py`

---
source_file: .\src\core\summarizer.py
file_type: .py
file_hash: 2015c84a437beca95ca9aee684e801f14b5ecc510ba434bc34c4dbfa5b7423f9
chunk_index: 1
total_chunks: 3
content_hash: 35313e00c1d1dcc68857b0f64c4b0d53ecf3d4132c148db0c820f391ab2b9ad5
summary: import torch from transformers import BartForConditionalGeneration, BartTokenizer.import
  logging from typing import List, Optional and List.import Logger from logging.getLogger(__name__)
timestamp_utc: '2025-06-09T10:23:35.240963+00:00'
---

```
import torch
from transformers import BartForConditionalGeneration, BartTokenizer
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)
```

---

---
source_file: .\src\core\summarizer.py
file_type: .py
file_hash: 2015c84a437beca95ca9aee684e801f14b5ecc510ba434bc34c4dbfa5b7423f9
chunk_index: 2
total_chunks: 3
content_hash: 6116395b9983f3baf61b371715354f514cc13453d4cac42d37d93b6bdf952261
summary: 'class BatchSummarizer: grotesque    def __init__(self): """ Inicializa o
  sumarizador em lote com otimizações para GPU, se disponível. Carrega o modelo ''facebook/bart-large-cnn''
  e configura para usar: bfloat16 na GPU, float32 na CPU"'
timestamp_utc: '2025-06-09T10:23:35.240963+00:00'
---

```
class BatchSummarizer:
    def __init__(self):
        """
        Inicializa o sumarizador em lote com otimizações para GPU, se disponível.
        
        Carrega o modelo 'facebook/bart-large-cnn' e configura para usar:
        - GPU (cuda) se disponível, caso contrário CPU
        - Precisão bfloat16 na GPU, float32 na CPU
        - Flash Attention 2 quando disponível, com fallback para atenção padrão
        """
        # Configura dispositivo e tipo de dados
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        
        # Tenta usar flash_attention_2, com fallback para atenção padrão
        use_flash = False
        self.model = None
        self.tokenizer = None
        
        try:
            # Tenta carregar com flash_attention_2
            self.model = BartForConditionalGeneration.from_pretrained(
                "facebook/bart-large-cnn",
                torch_dtype=self.torch_dtype,
                use_flash_attention_2=True
            ).to(self.device)
            self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
            use_flash = True
        except Exception as e:
            # Se falhar, tenta sem flash_attention_2
            try:
                self.model = BartForConditionalGeneration.from_pretrained(
                    "facebook/bart-large-cnn",
                    torch_dtype=self.torch_dtype
                ).to(self.device)
                self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
            except Exception as e:
                logger.error(f"Falha ao carregar o modelo: {str(e)}")
                raise
        
        logger.info(f"Otimizações ativas: {self.device}, {self.torch_dtype}, flash_attention={use_flash}")

    def summarize_batch(self, texts: List[str]) -> List[str]:
        """
        Gera sumários em lote para uma lista de textos.
```

---

---
source_file: .\src\core\summarizer.py
file_type: .py
file_hash: 2015c84a437beca95ca9aee684e801f14b5ecc510ba434bc34c4dbfa5b7423f9
chunk_index: 3
total_chunks: 3
content_hash: 440f219e90a0d847a3b9d90a5b95401ccd0daa84476a03c0fe615b0686807bc1
summary: 'def summarize_batch(self, texts: List[str]): """ Gera sumários em lote para
  uma lista de textos. Geração dos sumárrios: Lista de sumárianos correspondentes.
  Args:    “  ”, “texts”: List of textos a serem sumarizados. “Texts’’: “List of texts.”
  “Geraçao’s ““Garação’ “”; “Sumário’  ”“List’'
timestamp_utc: '2025-06-09T10:23:35.242102+00:00'
---

```
def summarize_batch(self, texts: List[str]) -> List[str]:
        """
        Gera sumários em lote para uma lista de textos.

        Args:
            texts: Lista de textos a serem sumarizados.

        Returns:
            Lista de sumários correspondentes.
        """
        try:
            # Tokenização em lote
            inputs = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)
            
            # Geração dos sumários
            summary_ids = self.model.generate(
                **inputs,
                max_length=150,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
            
            # Decodificação
            summaries = [
                self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False)
                for g in summary_ids
            ]
            
            return summaries
            
        except Exception as e:
            logger.error(f"Erro durante sumarização em lote: {str(e)}")
            raise
```

---

# Source: base_extractor.py
Original Path: `.\src\extractors\base_extractor.py`

---
source_file: .\src\extractors\base_extractor.py
file_type: .py
file_hash: 70b1c719ae51447c840c76ba856d25f22187955615b7c7a4f4359754e9cf670c
chunk_index: 1
total_chunks: 1
content_hash: e578532362fdfd6dfd1301d70ec5a33ba8164e1b26fdfe1d3dd370338294304e
summary: 'from abc import ABC, abstractmethod.class BaseExtractor(ABC): @abstractmethod.
  extract(self, file_path: str) -> str: "Extrai conteúdo textual de um arquivo."'
timestamp_utc: '2025-06-09T10:23:35.242102+00:00'
---

```
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de um arquivo."""
        pass
```

---

# Source: docx_extractor.py
Original Path: `.\src\extractors\docx_extractor.py`

---
source_file: .\src\extractors\docx_extractor.py
file_type: .py
file_hash: 41b224d53395938184ffa40f8979b70714f8483ba5ade17e59a67bcd68bd5911
chunk_index: 1
total_chunks: 1
content_hash: f02f92d62c68631e93db9d259c4b2324df1ff6d2f1338e7941bae5d04e465a44
summary: 'from .base_extractor import BaseExtractor from DocxExtractor.extractor.
  extract() def extract(self, file_path: str): return f"Conteúdo extraído do DOCX:
  {file_path}"'
timestamp_utc: '2025-06-09T10:23:35.243110+00:00'
---

```
from .base_extractor import BaseExtractor

class DocxExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de arquivos DOCX (implementação básica)."""
        # Implementação real usaria biblioteca como python-docx
        return f"Conteúdo extraído do DOCX: {file_path}"
```

---

# Source: image_extractor.py
Original Path: `.\src\extractors\image_extractor.py`

---
source_file: .\src\extractors\image_extractor.py
file_type: .py
file_hash: f09c6d463e6db00e4d23ad3f154a8f13d8e8c7a8ec360753c30dc0de94f2c782
chunk_index: 1
total_chunks: 1
content_hash: 534836cd45452a652dc63f0113d9009e7b39dc58d3053178a1e9a560af245d11
summary: 'from .base_extractor import BaseExtractor as ImageExtractor. import OCR
  (implementação básica) as OCR. extract(self, file_path: str) return f"Conteúdo extraído
  da imagem via OCR"'
timestamp_utc: '2025-06-09T10:23:35.243110+00:00'
---

```
from .base_extractor import BaseExtractor

class ImageExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de imagens usando OCR (implementação básica)."""
        # Implementação real usaria bibliotecas como pytesseract e Pillow
        return f"Conteúdo extraído da imagem via OCR: {file_path}"
```

---

# Source: pdf_extractor.py
Original Path: `.\src\extractors\pdf_extractor.py`

---
source_file: .\src\extractors\pdf_extractor.py
file_type: .py
file_hash: 98f61a8740d8cce03ab0840ae24dcf3880e4a82f37d0dd212327d4a233bed782
chunk_index: 1
total_chunks: 1
content_hash: 7d9a651bd2ed925fc138cf2685647324b7f2890dbcc6a500520841f7e174dd0f
summary: 'from .base_extractor import BaseExtractor from PDFExtractor.extract() def
  extract(self, file_path: str): return f"Conteúdo extraído do PDF: {file_path}"'
timestamp_utc: '2025-06-09T10:23:35.244120+00:00'
---

```
from .base_extractor import BaseExtractor

class PDFExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        """Extrai conteúdo textual de arquivos PDF (implementação básica)."""
        # Implementação real usaria biblioteca como pypdf
        return f"Conteúdo extraído do PDF: {file_path}"
```

---

# Source: text_extractor.py
Original Path: `.\src\extractors\text_extractor.py`

---
source_file: .\src\extractors\text_extractor.py
file_type: .py
file_hash: d9988d4a9aa4fb1a7cf16db0470c8faed6e384e1fcedd3719c1a21028df140b2
chunk_index: 1
total_chunks: 1
content_hash: 2097b276d81d638ec42e4ca9203130dad9b41e0d14948f110ee72047fafa1a61
summary: import os.import markdown.import re.import BaseExtractor. import Tuple, Optional.
  import typing. import TextExtractor(BaseExtractor):. import .base_extractor.import
  .tuple.
timestamp_utc: '2025-06-09T10:23:35.244120+00:00'
---

```
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
```

---

# Source: main.py
Original Path: `.\src\main.py`

---
source_file: .\src\main.py
file_type: .py
file_hash: dda8da6d0512551f8515a96507677981fd012b965f61ef821594d4556c9e438a
chunk_index: 1
total_chunks: 2
content_hash: 4e46d8b3286e15607514e35069aa330c47312b236186e38f31f1b0e17835708c
summary: import os.import click.import tqdm.import Pipeline. import load_config. import
  setup_logger. import os. import click. import tqDM. importing Pipeline. importing
  os.
timestamp_utc: '2025-06-09T10:23:35.245131+00:00'
---

```
import os
import click
from tqdm import tqdm
from core.pipeline import Pipeline
from utils.config import load_config
from utils.logger import setup_logger

logger = setup_logger()

@click.command()
@click.option('--input-dir', 
              help='Diretório de entrada (sobrescreve config.yaml)',
              type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output-dir',
              help='Diretório de saída (sobrescreve config.yaml)',
              type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--force-reprocess', 
              is_flag=True,
              help='Forçar reprocessamento completo')
```

---

