## 🚀 Otimizações Avançadas
- **Modelo de Linguagem**: Substituímos o modelo anterior por `facebook/bart-large-cnn` para sumarização de alta qualidade
- **Processamento em Lote**: Processamento paralelo de chunks para ganhos de até 1000x em velocidade
- **Checkpoint Automático**: Sistema de salvamento incremental que evita perda de trabalho em interrupções
- **Otimizações de Hardware**: Suporte a GPU com bfloat16 e flash_attention_2
# Framework de Processamento de Documentos

## Visão Geral
O Framework de Processamento de Documentos é uma solução integrada para extração, processamento e geração de documentação a partir de diversos formatos de arquivos. Desenvolvido em Python, oferece:

- **Extratores especializados** para múltiplos formatos (PDF, DOCX, imagens, texto)
- **Sistema de chunking inteligente** para fragmentação semântica de conteúdo
- **Sumarização automática** com modelos de linguagem
- **Geração de documentação** em formato Markdown

## Arquitetura
O sistema é organizado em módulos especializados:
```
src/
├── extractors/    # Implementações de extração por tipo de arquivo
├── core/          # Lógica principal (chunking, pipeline, sumarização)
├── output/        # Geradores de saída (Markdown, etc)
└── utils/         # Utilitários (caching, logging, configuração)
```

## Funcionalidades Principais
1. Processamento paralelo de documentos
2. Cache inteligente para evitar reprocessamento
3. Customização via arquivo de configuração
4. Geração de documentação estruturada
5. Suporte a múltiplos formatos de entrada

## Uso
```bash
python main.py --input-dir [diretório_entrada] --output-dir [diretório_saída]
```
[Ver Tutorial Completo](TUTORIAL.md) | [Referência Técnica](REFERENCIA.md)