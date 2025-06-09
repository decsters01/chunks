import os
import click
from src.core.pipeline import Pipeline
from src.utils.config import load_config
from src.utils.logger import logger, setup_logger

@click.command()
@click.option('--config', 'config_path', default='config.yaml', help='Caminho para o arquivo de configuração.')
@click.option('--input-dir', help='Diretório de entrada (sobrescreve config.yaml).')
@click.option('--output-dir', help='Diretório de saída (sobrescreve config.yaml).')
@click.option('--max-files', 'max_markdown_files', type=int, help='Número máximo de arquivos Markdown para agrupar chunks (sobrescreve config.yaml).')
@click.option('--force', 'force_reprocess', is_flag=True, help='Forçar o reprocessamento de todos os arquivos, ignorando o cache.')
@click.option('--verbose', is_flag=True, help='Ativar logging detalhado (DEBUG).')
def main(config_path, input_dir, output_dir, max_markdown_files, force_reprocess, verbose):
    """
    Pipeline para extrair, chunkificar e documentar o conteúdo de repositórios de código.
    """
    setup_logger()
    if verbose:
        logger.setLevel('DEBUG')

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        logger.warning(f"Arquivo de configuração '{config_path}' não encontrado. Usando apenas argumentos da CLI e padrões.")
        config = {'processing': {}, 'logging': {}}

    # Sobrescrever config com argumentos da CLI
    if input_dir:
        config['processing']['input_directory'] = input_dir
    if output_dir:
        config['processing']['output_directory'] = output_dir
    if max_markdown_files is not None:
        config['processing']['max_markdown_files'] = max_markdown_files
    
    # Validar configurações
    input_dir_path = config['processing'].get('input_directory')
    output_dir_path = config['processing'].get('output_directory')
    
    if not input_dir_path or not output_dir_path:
        logger.error("Os diretórios de entrada e saída devem ser especificados via CLI ou config.yaml.")
        return
        
    if not os.path.isdir(input_dir_path):
        logger.error(f"Diretório de entrada não encontrado: {input_dir_path}")
        return

    # Executar pipeline
    logger.info("Iniciando pipeline de processamento...")
    pipeline = Pipeline(cache_path=config.get('cache_file', 'pipeline_cache.json'))
    
    pipeline.process_directory(
        root_dir=input_dir_path,
        output_dir=output_dir_path,
        exclude_dirs=config['processing'].get('ignored_directories'),
        max_markdown_files=config['processing'].get('max_markdown_files'),
        force_reprocess=force_reprocess
    )

    logger.info("Pipeline concluído com sucesso.")

if __name__ == '__main__':
    main() 