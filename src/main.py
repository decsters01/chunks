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
def main(input_dir, output_dir, force_reprocess):
    """
    CLI principal para execução do pipeline de processamento de documentos.
    """
    try:
        # Carregar configuração padrão
        config = load_config('config.yaml')
        
        # Sobrescrever configuração com parâmetros CLI
        if input_dir:
            config['processing']['input_directory'] = os.path.abspath(input_dir)
        if output_dir:
            config['processing']['output_directory'] = os.path.abspath(output_dir)
        config['force_reprocess'] = force_reprocess
        
        # Validar diretórios
        if not os.path.isdir(config['processing']['input_directory']):
            raise ValueError(f"Diretório de entrada inválido: {config['processing']['input_directory']}")
        if not os.path.isdir(config['processing']['output_directory']):
            raise ValueError(f"Diretório de saída inválido: {config['processing']['output_directory']}")
        
        logger.info(f"Iniciando pipeline com configuração: {config}")
        
        # Inicializar pipeline
        cache_path = os.path.join(config['processing']['output_directory'], 'pipeline_cache.json')
        pipeline = Pipeline(cache_path)
        
        # Executar pipeline com barra de progresso
        pipeline.process_directory(
            root_dir=config['processing']['input_directory'],
            output_dir=config['processing']['output_directory'],
            exclude_dirs=config['processing'].get('ignored_directories', None)
        )
        logger.info("Processamento concluído.")
        click.echo("✅ Processamento concluído com sucesso!")
    
    except Exception as e:
        logger.exception("Erro durante a execução do pipeline")
        click.echo(f"❌ Erro: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()