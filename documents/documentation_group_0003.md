# Source: chunkv3.py
Original Path: `.\chunkv3.py`

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 18
total_chunks: 24
content_hash: bcd234db9e667da4896f2194a72e070e7fbe8343ba08dd66f5f936d0c964f3bb
summary: 'def main(): if not. os.path.exists(PASTA_DOCUMENTACAO): # Ignorar diretórios
  especificados. for item in os.listdir(PasTA_ DOCUMENTACO): item_path = os. path.join(P
  ASTA_documentACAO, item) if item.isfile(item_path): os.remove(item) # Remove todos
  subdiretórioos para evitar processamento. for dirpath, dirnames, filenames inos.walk(
  input_ folder): if. dirnames[:] = [d for d in dirnames if d'
timestamp_utc: '2025-06-09T10:23:35.215920+00:00'
---

```
def main():
    if not os.path.exists(PASTA_DOCUMENTACAO):
        os.makedirs(PASTA_DOCUMENTACAO)
    else:
        for item in os.listdir(PASTA_DOCUMENTACAO):
            item_path = os.path.join(PASTA_DOCUMENTACAO, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
    
    todos_os_chunks_info = []
    input_folder = "."  # Diretório atual
    arquivos_a_processar = []
    ignore_directories = IGNORED_DIRS

    for dirpath, dirnames, filenames in os.walk(input_folder):
        # Ignorar diretórios especificados
        dirnames[:] = [d for d in dirnames if d not in ignore_directories]
        
        # Calcular profundidade do diretório atual (0 = raiz, 1 = subdiretório, etc.)
        rel_path = os.path.relpath(dirpath, input_folder)
        depth = len(rel_path.split(os.sep)) - (1 if rel_path == '.' else 0)
        
        # Ignorar diretórios que excedam a profundidade máxima
        if depth > MAX_DEPTH:
            dirnames[:] = []  # Remove todos subdiretórios para evitar processamento
            continue          # Pula processamento de arquivos neste diretório
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1]
            if file_ext in supported_extensions:
                arquivos_a_processar.append(file_path)
    
    print(f"Encontrados {len(arquivos_a_processar)} arquivos para processar.")
    
    # Configurar o splitter do langchain
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 19
total_chunks: 24
content_hash: c1c13470fcf606f03ea474a63b2c4fed9c5ca92672e80ba0d1fea2db910b6cc1
summary: 'print(f"Iniciando processamento paralelo com {os.cpu_count()} workers...")
  with concurrent.futures.ThreadPoolExecutor(max_workers=os. CPU_count()) as executor:
  futures = {executor.submit(process_file, file): file for file in arquivos_a_processar}
  completed = 0.'
timestamp_utc: '2025-06-09T10:23:35.215920+00:00'
---

```
print(f"Iniciando processamento paralelo com {os.cpu_count()} workers...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(process_file, file): file for file in arquivos_a_processar}
        completed = 0
        total_files = len(arquivos_a_processar)
        
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            file_path = futures[future]
            try:
                file_results = future.result()
                todos_os_chunks_info.extend(file_results)
                print(f"✅ [{completed}/{total_files}] Processado: {file_path}")
            except Exception as e:
                print(f"⛔ Erro no arquivo {file_path}: {str(e)}")
                # Registrar erro mas continuar processamento
                with open("erros_processamento.log", "a") as log_file:
                    log_file.write(f"Erro em {file_path}: {str(e)}\n")

    total_chunks_reais = len(todos_os_chunks_info)
    if total_chunks_reais == 0:
        print("Nenhum chunk para processar e salvar.")
        return
        
    print(f'Total de chunks reais a serem distribuídos: {total_chunks_reais}')
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 20
total_chunks: 24
content_hash: 1abf0d5c639892113a2edd3b4ed80e794dc176b5be8378c24fbe69a15cb93836
summary: '# Determinar quantos arquivos Markdown serão realmente gerados. # Para simplicidade
  e dado o context, vamos gerar o total of chunks como arquvos. # A função salvar_chunks_em_markdown
  vai lidar com isso no modo ''else'''
timestamp_utc: '2025-06-09T10:23:35.216917+00:00'
---

```
# Determinar quantos arquivos Markdown serão realmente gerados.
    if MAX_ARQUIVOS_MARKDOWN <= 0:
        # Se MAX_ARQUIVOS_MARKDOWN é 0 ou negativo, idealmente seria um MD por chunk,
        # mas para evitar um número excessivo de arquivos, vamos limitar um pouco ou usar o total de chunks.
        # Para simplicidade e dado o contexto, vamos gerar o total de chunks como arquivos,
        # a função salvar_chunks_em_markdown vai lidar com isso no modo 'else' (sem indice_arquivo).
        # No entanto, para manter a lógica极 N arquivos, vamos definir arquivos_markdown_a_gerar.
        # Se a intenção é realmente 1 chunk por MD, a lógica de chamada a salvar_chunks_em_markdown mudaria.
        # Por ora, manteremos a lógica de agrupar em N arquivos.
        # Se MAX_ARQUIVOS_MARKDOWN é 0, e queremos N arquivos, fazemos N = total_chunks_reais.
        arquivos_markdown_a_gerar = total_chunks_reais
    elif MAX_ARQUIVOS_MARKDOWN >= total_chunks_reais:
        # Menos chunks que o limite, então cada "grupo" de chunks (idealmente 1, mas depende de como salvar_chunks_em_markdown agrupa)
        # poderia ir para um arquivo. Para distribuição uniforme, definimos o total de arquivos como o total de chunks.
        arquivos_markdown_a_gerar = total_chunks_reais
    else:
        # Limita ao máximo definido
        arquivos_markdown_a_gerar = MAX_ARQUIVOS_MARKDOWN
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 21
total_chunks: 24
content_hash: 14977d36f2e8950d6383341b454caa36b8b25f1be13811e55271cd6b15d1f037
summary: '# Se após os cálculos acima, arquivos_markdown_a_gerar for 0, mas há chunks.
  # Garante ao menos um arquivo se houver chunks e MAX_ARQUIVOS_MARKDOWN era problemático.
  # A ordenação por ''origem'' ajuda a manter chunks.'
timestamp_utc: '2025-06-09T10:23:35.216917+00:00'
---

```
# Se após os cálculos acima, arquivos_markdown_a_gerar for 0, mas há chunks,
    # isso significa que MAX_ARQUIVOS_MARKDOWN provavelmente era <= 0 e total_chunks_reais > 0.
    # A lógica acima já define arquivos_markdown_a_gerar = total_chunks_reais nesses casos.
    # Uma verificação final para o caso de total_chunks_reais > 0 e arquivos_markdown_a_gerar acabar sendo 0.
    if arquivos_markdown_a_gerar == 0 and total_chunks_reais > 0:
        print(f"Aviso: arquivos_markdown_a_gerar é 0, mas há {total_chunks_reais} chunks. Gerando 1 arquivo MD.")
        arquivos_markdown_a_gerar = 1 # Garante ao menos um arquivo se houver chunks e MAX_ARQUIVOS_MARKDOWN era problemático.
    elif arquivos_markdown_a_gerar == 0 and total_chunks_reais == 0:
        print("Nenhum chunk e nenhum arquivo Markdown a ser gerado.")
        return

    print(f"Distribuindo {total_chunks_reais} chunks em {arquivos_markdown_a_gerar} arquivos Markdown de forma equilibrada.")

    # A ordenação por 'origem' ajuda a manter chunks do mesmo arquivo fonte próximos na lista inicial,
    # o que pode ajudar a mantê-los no mesmo arquivo MD de destino ou em arquivos MD sequenciais.
    todos_os_chunks_info.sort(key=lambda x: x['origem'])

    chunk_global_start_idx = 0 # Ponteiro para o início da fatia atual na lista todos_os_chunks_info
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 22
total_chunks: 24
content_hash: 7b7d977525aaed60a8b563cb0331108c487a96d58bbc20aeff88644504f01eef
summary: 'for i_md_file in range(arquivos_markdown_a_gerar): # Atualizar progresso
  a cada 5 arquivo ou no início/fim. if i_MD_file % 5 == 0 or i_ MD_file == 0: print(f"Criando
  arquivo Markdown {i_md file + 1}/{arquvos_Markdown_A_gerr}...") if i-md_ file %
  5 != 0 or I-md-file % 0 != 1: print (f" criando arquivo markdown a gerar {i'
timestamp_utc: '2025-06-09T10:23:35.217914+00:00'
---

```
for i_md_file in range(arquivos_markdown_a_gerar):
        # Atualizar progresso a cada 5 arquivos ou no início/fim
        if i_md_file % 5 == 0 or i_md_file == 0 or i_md_file == arquivos_markdown_a_gerar - 1:
            print(f"Criando arquivo Markdown {i_md_file + 1}/{arquivos_markdown_a_gerar}...")
        
        # Calcular quantos chunks este arquivo Markdown específico deve receber para distribuição uniforme
        base_chunks_para_este_arquivo = total_chunks_reais // arquivos_markdown_a_gerar
        chunks_extras_distribuir = total_chunks_reais % arquivos_markdown_a_gerar
        
        num_chunks_neste_md = base_chunks_para_este_arquivo + (1 if i_md_file < chunks_extras_distribuir else 0)
        
        # Determinar a fatia de chunks para este arquivo MD
        # Garantir que não ultrapassemos o total de chunks disponíveis
        chunk_global_end_idx = min(chunk_global_start_idx + num_chunks_neste_md, total_chunks_reais)
        
        chunks_para_este_md_info_fatia = todos_os_chunks_info[chunk_global_start_idx : chunk_global_end_idx]
        
        if not chunks_para_este_md_info_fatia:
            if chunk_global_start_idx >= total_chunks_reais:
                # Todos os chunks já foram distribuídos.
                # Isso pode acontecer se, por exemplo, total_chunks_reais < arquivos_markdown_a_gerar
                # e já passamos pelo número de arquivos MD necessários para cobrir todos os chunks.
                # print(f"Todos os chunks já distribuídos. Arquivo MD {i_md_file + 1} (índice {i_md_file}) não será criado ou estará vazio.")
                continue 
            else:
                # Isso seria um erro de lógica se ainda há chunks mas a fatia é vazia e num_chunks_neste_md > 0.
                print(f"Aviso: Fatia de chunks vazia para o arquivo MD {i_md_file + 1} (índice {i_md_file}) mas deveria haver chunks.")
                continue
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 23
total_chunks: 24
content_hash: 8464d24a9bdf8492067efb2b2ff1f9b6a10a899978f886f3b578f242fab426b1
summary: '# print(f"  Arquivo MD {i_md_file + 1}/{arquivos_markdown_a_gerar} (índice
  {i-MD_file) chunks.") # usar o nome do arquivo original correto nos cabeçalhos.
  # Cada chamada a salvar_chunks_em_mark down aqui é para o MESMO arquIVO MD de destino.'
timestamp_utc: '2025-06-09T10:23:35.218912+00:00'
---

```
# print(f"  Arquivo MD {i_md_file + 1}/{arquivos_markdown_a_gerar} (índice {i_md_file}) receberá {len(chunks_para_este_md_info_fatia)} chunks.")

        # Agrupar os chunks desta fatia por sua origem para que salvar_chunks_em_markdown possa
        # usar o nome do arquivo original correto nos cabeçalhos DENTRO do mesmo arquivo_markdown_XXXX.md
        chunks_agrupados_por_origem_para_este_md = defaultdict(list)
        for chunk_info_item in chunks_para_este_md_info_fatia:
            chunks_agrupados_por_origem_para_este_md[chunk_info_item['origem']].append(chunk_info_item['texto'])

        for origem_do_grupo, textos_dos_chunks_do_grupo in chunks_agrupados_por_origem_para_este_md.items():
            # Cada chamada a salvar_chunks_em_markdown aqui é para o MESMO arquivo MD de destino (i_md_file),
            # mas com diferentes "sub-cabeçalhos" baseados na origem do chunk.
            # A função salvar_chunks_em_markdown usa 'a' (append) mode.
            salvar_chunks_em_markdown(
                origem_do_grupo,
                textos_dos_chunks_do_grupo,
                PASTA_DOCUMENTACAO,
                i_md_file, # Passa o índice do arquivo de destino
                arquivos_markdown_a_gerar 
            )
            # print(f"    Chunks de '{os.path.basename(origem_do_grupo)}' adicionados ao arquivo MD {i_md_file + 1}.")

        # Atualizar o ponteiro de início para a próxima iteração
        chunk_global_start_idx = chunk_global_end_idx

    if chunk_global_start_idx < total_chunks_reais:
        print(f"ALERTA: {total_chunks_reais - chunk_global_start_idx} chunks não foram distribuídos! Verifique a lógica de distribuição.")
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 24
total_chunks: 24
content_hash: 98a78c597b851b92bc3dc0a4d4ba3593f4ebb20d8b04945a49b3f138ea342251
summary: 'if chunk_global_start_idx < total_chunks_reais: print(f"ALERTA: {total_chunk_
  reais - chunk_ global_start-idx} chunks não foram distribuídos! Verifique a lógica
  de distribuição.") Arquivos_md_criados = len([ name for name in os.listdir(PASTA_DOCUMENTACAO)],
  len(arquivo_md), len (arquivo_md) }); main() { fim = time.time() time_total = fim
  - inicio; time.strftime(''%'
timestamp_utc: '2025-06-09T10:23:35.218912+00:00'
---

```
if chunk_global_start_idx < total_chunks_reais:
        print(f"ALERTA: {total_chunks_reais - chunk_global_start_idx} chunks não foram distribuídos! Verifique a lógica de distribuição.")

    arquivos_md_criados = len([
        name for name in os.listdir(PASTA_DOCUMENTACAO)
        if os.path.isfile(os.path.join(PASTA_DOCUMENTACAO, name)) and name.startswith("documentacao_")
    ])
    print(f"Processamento concluído. {total_chunks_reais} chunks distribuídos em {arquivos_md_criados} arquivos Markdown na pasta '{PASTA_DOCUMENTACAO}'.")

# Função removida (não mais necessária com o novo método de listagem)

if __name__ == '__main__':
    inicio = time.time()
    print(f"Iniciando processamento em {time.strftime('%H:%M:%S')}")
    try:
        main()
    except Exception as e:
        print(f"Erro crítico durante a execução: {str(e)}")
    finally:
        fim = time.time()
        tempo_total = fim - inicio
        print(f"Processamento concluído em {time.strftime('%H:%M:%S')}")
        print(f"Tempo total de execução: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")
```

---

# Source: config.yaml
Original Path: `.\config.yaml`

---
source_file: .\config.yaml
file_type: .yaml
file_hash: a600e44c44cfb24433229f38fa2072deb6c08f70c324b63a1b7efdb276709476
chunk_index: 1
total_chunks: 1
content_hash: 3239fa9946dcc64fc7592987d12ac2e835c90157549e9ca6b7f48861174e4752
summary: 'processing: behaviors: input_ directory: ''.'' output_directory: ''documents''
  ignored_directories: [''.git'', ''node_modules'', ''__pycache__'', ''document'']
  max_recursion_depth: 5 max_markdown_files: 10 max_marksdown_ files: 10. max_input_chars:
  50000 max_ input_characters: ''50000'' max_chunk_size: 1500 chunk_overlap: 250 chunk_line_lines:
  7 min_chunks_ lines: 7 max_summarizer: ''t5-small'' model_name: ''T5-Small'' model-size:
  '' t'
timestamp_utc: '2025-06-09T10:23:35.219909+00:00'
---

```
processing:
  input_directory: '.'
  output_directory: 'documents'
  ignored_directories: ['.git', 'node_modules', '__pycache__', 'documents']
  max_recursion_depth: 5
  max_markdown_files: 10  # Configura o número máximo de arquivos markdown gerados
chunking:
  chunk_size: 1500
  chunk_overlap: 250
  min_chunk_lines: 7
summarizer:
  model_name: 't5-small'
  max_input_chars: 50000
ocr:
  tesseract_cmd_path: null
```

---

# Source: instrucoes.md
Original Path: `.\instrucoes.md`

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 1
total_chunks: 9
content_hash: 69c2495dc055bf3968112f0e0ab0788210e9503a778942da4a05c8804f9c5f1a
summary: Mestre.ly is a toolkit for writing a modern version of chunkv3.py. The goal
  is to turn this script into a plataforma de documentação universal.
timestamp_utc: '2025-06-09T10:23:35.219909+00:00'
---

```
Com certeza, Mestre. Sua visão de transformar este script em uma plataforma de documentação universal é inspiradora, e a exigência de um plano mais detalhado e robusto é o caminho certo para garantir o sucesso.
Analisei novamente suas diretrizes e o código, focando em antecipar desafios técnicos, solidificar a arquitetura e detalhar cada passo da execução. O plano a seguir é uma versão expandida e fortificada, projetada para ser um verdadeiro blueprint de engenharia.

Plano Técnico de Engenharia: Framework de Documentação Universal
Sumário Executivo (TL;DR)
Este plano detalha a metamorfose do chunkv3.py em um framework modular, escalável e resiliente.

Arquitetura: Migração de um monólito para uma arquitetura desacoplada (src, core, extractors, output, utils).
Extração Universal: Implementação de um sistema de "plugins" (Strategy Pattern) para suportar nativamente Texto, PDF, DOCX e Imagens (OCR), com um design que permite adicionar novos formatos facilmente.
Chunking Inteligente: Substituição da lógica de regex por RecursiveCharacterTextSplitter da Langchain, configurado especificamente por linguagem de programação para máxima precisão semântica.
Enriquecimento de Dados: Geração automática de metadados ricos em formato YAML Frontmatter para cada chunk, incluindo resumos gerados por IA, hashes de conteúdo para versionamento e informações de origem.
Robustez e Eficiência: Introdução de um sistema de cache para evitar reprocessamento, logging estruturado para depuração, tratamento de erro granular por tipo de arquivo e uma CLI completa para controle total.
Qualidade Assegurada: Definição de uma estratégia de testes abrangente, com testes unitários para cada componente e testes de integração para o pipeline completo.


Contexto Coletado e Justificativas da Arquitetura
```

---

---
source_file: .\instrucoes.md
file_type: .md
file_hash: c4216048ec2cb12a2906c59e7df941b6fd242a2a93fb9d7880d8f75acba8f0ae
chunk_index: 2
total_chunks: 9
content_hash: 8b5e90dd25e8696a7c59c222f5d7ebc4366be523a20a963ac845f276db2cedc3
summary: O RecursiveCharacterTextSplitter já presente no código, porém não utilizado,
  is a chave para unificar e simplificar o chunking. A incapacidade do script atual
  de processar os tipos of arquivo será resolvida. A nova estrutura modular permitirá
  o desenvolvimento, teste e manutenção of cada parte do sistema.
timestamp_utc: '2025-06-09T10:23:35.220906+00:00'
---

```
Contexto Coletado e Justificativas da Arquitetura

Oportunidade de Unificação: O RecursiveCharacterTextSplitter já presente no código, porém não utilizado, é a chave para unificar e simplificar o chunking. Abandonaremos a complexa e frágil função detect_code_blocks em favor de uma solução padrão da indústria, mais previsível e eficaz.
Necessidade de Polimorfismo: A incapacidade do script atual de processar os tipos de arquivo que promete (.pdf, .docx) será resolvida com um sistema de "Extratores", onde cada tipo de arquivo é tratado por um especialista (seu próprio módulo), tornando o sistema coeso e extensível.
Valor dos Metadados: As regras do projeto enfatizam o YAML Frontmatter. Iremos além, incluindo não apenas o resumo, but também um hash do conteúdo (content_hash) para habilitar um sistema de cache inteligente e garantir a integridade dos dados.
Fim do Monólito: A estrutura atual em um único arquivo é um impedimento para o crescimento. A nova estrutura modular permitirá o desenvolvimento, teste e manutenção de cada parte do sistema de forma independente.


Decomposição Detalhada das Tarefas de Engenharia
Tarefa Principal 1: Fundações - Estrutura, Configuração e Logging

Descrição: Construir o esqueleto do projeto. Esta é a base sobre a qual todos os outros componentes serão construídos.

Depende de: Nenhuma.


Sub-tarefa 1.1: Criar a Estrutura de Diretórios
```

---

