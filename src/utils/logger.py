import logging
import os

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Criação do logger principal
logger = logging.getLogger('pipeline_logger')

# Adiciona handler para arquivo se variável de ambiente estiver definida
if os.environ.get('LOG_FILE'):
    file_handler = logging.FileHandler(os.environ['LOG_FILE'])
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

def setup_logger():
    """Configura e retorna o logger principal."""
    return logger