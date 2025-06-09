import json
import os
import threading
import msvcrt
from typing import Dict, Optional
from .logger import logger

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