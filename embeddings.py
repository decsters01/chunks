import os
import json
import time
from typing import List, Union, Optional

import click
import requests

DEFAULT_API_URL = "https://chutes-baai-bge-large-en-v1-5.chutes.ai/embed"


def _read_api_token_from_environment() -> str:
    api_token = os.getenv("CHUTES_API_TOKEN")
    if not api_token:
        raise RuntimeError(
            "Variável de ambiente CHUTES_API_TOKEN não encontrada. Defina-a com o seu token de API."
        )
    return api_token


def invoke_chute(
    inputs: Union[str, List[str]],
    api_token: Optional[str] = None,
    api_url: str = DEFAULT_API_URL,
    timeout_seconds: int = 30,
    max_retries: int = 2,
    backoff_factor_seconds: float = 1.5,
) -> dict:
    """
    Invoca o endpoint de embeddings do Chutes.

    - inputs: Texto único (str) ou lista de textos (List[str]).
    - api_token: Token de API. Se None, será lido de CHUTES_API_TOKEN.
    - api_url: URL do endpoint de embeddings.
    - timeout_seconds: Timeout por requisição.
    - max_retries: Número máximo de tentativas adicionais em erros transitórios.
    - backoff_factor_seconds: Fator de backoff exponencial entre tentativas.

    Retorna o JSON da resposta.
    """
    if api_token is None:
        api_token = _read_api_token_from_environment()

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    request_payload = {"inputs": inputs}

    retry_status_codes = {429, 500, 502, 503, 504}
    attempt_index = 0
    last_exception: Optional[Exception] = None

    with requests.Session() as session:
        while attempt_index <= max_retries:
            try:
                response = session.post(
                    api_url,
                    headers=headers,
                    json=request_payload,
                    timeout=timeout_seconds,
                )

                if 200 <= response.status_code < 300:
                    return response.json()

                if response.status_code in retry_status_codes and attempt_index < max_retries:
                    sleep_seconds = backoff_factor_seconds ** attempt_index
                    time.sleep(sleep_seconds)
                    attempt_index += 1
                    continue

                raise RuntimeError(
                    f"Falha ao obter embeddings (status={response.status_code}): {response.text}"
                )
            except requests.RequestException as exc:
                last_exception = exc
                if attempt_index < max_retries:
                    sleep_seconds = backoff_factor_seconds ** attempt_index
                    time.sleep(sleep_seconds)
                    attempt_index += 1
                    continue
                raise RuntimeError(f"Erro de rede ao chamar o endpoint de embeddings: {exc}") from exc


@click.command()
@click.option(
    "--text",
    "texts",
    multiple=True,
    help="Texto(s) a serem embarcados. Pode ser usado múltiplas vezes.",
)
@click.option(
    "--input-file",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    help="Arquivo de entrada. Cada linha será tratada como um texto separado.",
)
@click.option(
    "--output-file",
    type=click.Path(dir_okay=False, path_type=str),
    help="Arquivo para salvar a resposta JSON.",
)
@click.option(
    "--api-url",
    default=DEFAULT_API_URL,
    show_default=True,
    help="URL do endpoint de embeddings.",
)
@click.option(
    "--timeout",
    "timeout_seconds",
    default=30,
    show_default=True,
    help="Timeout por requisição (segundos).",
)
@click.option(
    "--max-retries",
    default=2,
    show_default=True,
    help="Número de tentativas adicionais em erros transitórios.",
)
@click.option(
    "--backoff",
    "backoff_factor_seconds",
    default=1.5,
    show_default=True,
    help="Fator de backoff exponencial entre tentativas.",
)
def cli(
    texts: List[str],
    input_file: Optional[str],
    output_file: Optional[str],
    api_url: str,
    timeout_seconds: int,
    max_retries: int,
    backoff_factor_seconds: float,
) -> None:
    """
    CLI para gerar embeddings via Chutes API.

    Exemplos:
    - Embedding de um texto único:
      python embeddings.py --text "exemplo de texto"
    - Embedding de múltiplos textos:
      python embeddings.py --text "texto 1" --text "texto 2"
    - Ler textos linha a linha de um arquivo e salvar saída:
      python embeddings.py --input-file frases.txt --output-file saida.json
    """
    collected_texts: List[str] = []

    if input_file:
        with open(input_file, "r", encoding="utf-8") as handle:
            file_lines = [line.strip() for line in handle.readlines()]
            collected_texts.extend([line for line in file_lines if line])

    if texts:
        collected_texts.extend(list(texts))

    if not collected_texts:
        raise click.UsageError("Forneça pelo menos um --text ou um --input-file com conteúdo.")

    payload_inputs: Union[str, List[str]] = (
        collected_texts[0] if len(collected_texts) == 1 else collected_texts
    )

    result_json = invoke_chute(
        inputs=payload_inputs,
        api_token=None,
        api_url=api_url,
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
        backoff_factor_seconds=backoff_factor_seconds,
    )

    pretty_json = json.dumps(result_json, ensure_ascii=False, indent=2)
    click.echo(pretty_json)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as handle:
            handle.write(pretty_json)


if __name__ == "__main__":
    cli()