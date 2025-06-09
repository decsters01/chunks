import torch
from transformers import BartForConditionalGeneration, BartTokenizer
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

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