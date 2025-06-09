# Source: relatorio.py
Original Path: `.\relatorio.py`

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 12
total_chunks: 14
content_hash: fd8a41dda93725dac031acf735c8ddc9e088a9c184a0d88f92f7421731529fc4
summary: '# 3. Roleta mais usada e contagem print("🎰 Estatísticas de Roletas:") #
  4. Usuário com melhor placar total (Saldo de Vitórias) print("?!?") # 5. Most_used_roulette
  = roulette_counts.index[0] print("Dados de roleta não disponíveis.")'
timestamp_utc: '2025-06-09T10:23:35.233872+00:00'
---

```
# 3. Roleta mais usada e contagem
    print("🎰 Estatísticas de Roletas:")
    print("---------------------------")
    if 'Roulette' in df and not df['Roulette'].empty:
        roulette_counts = df['Roulette'].value_counts()
        if not roulette_counts.empty:
            most_used_roulette = roulette_counts.index[0]
            print(f"🥇 Roleta Mais Usada: {most_used_roulette} ({roulette_counts.iloc[0]} vezes)")
            print("\n📋 Contagem de Uso por Roleta:")
            for roleta, contagem in roulette_counts.items():
                print(f"   - {roleta}: {contagem} vezes")
        else:
            print("Nenhuma roleta registrada.")
    else:
        print("Dados de roleta não disponíveis.")
    print("\n===========================================\n")

    # 4. Usuário com melhor placar total (Saldo de Vitórias)
    print("🏆 Usuário com Melhor Saldo de Vitórias:")
    print("---------------------------------------")
    if not df.empty:
        user_scores = df.groupby(['UserID', 'UserName']).agg(
            TotalWins=('Wins', 'sum'),
            TotalLosses=('Losses', 'sum')
        ).reset_index()
        user_scores['NetWins'] = user_scores['TotalWins'] - user_scores['TotalLosses']
        best_user = user_scores.sort_values(by='NetWins', ascending=False).iloc[0]
        print(f"🥇 {best_user['UserName']}")
        print(f"   Saldo: ✅ {best_user['TotalWins']} x ❌ {best_user['TotalLosses']} (Líquido: {best_user['NetWins']})")
    else:
        print("Não há dados de placar para determinar o melhor usuário.")
    print("\n===========================================\n")
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 13
total_chunks: 14
content_hash: f468d9f4e70ebcd9af4874c78acf52ef55d0ff38f7e66e070c3e48cf87b79900
summary: '# 5. Quantas entradas (relatórios) cada usuário fez. print("📊 Entradas de
  Placar) por Usuário:") print("---------------------------------------------") if
  not df.empty: entries_per_user = df.groupby([''UserID'', ''UserName'']).size().reset_index(name=''Entries'')
  print("Nenhum usUário comEntradas.") print("\n===========================================\n")'
timestamp_utc: '2025-06-09T10:23:35.234869+00:00'
---

```
# 5. Quantas entradas (relatórios) cada usuário fez
    print("📊 Entradas (Relatórios de Placar) por Usuário:")
    print("---------------------------------------------")
    if not df.empty:
        entries_per_user = df.groupby(['UserID', 'UserName']).size().reset_index(name='Entries')
        entries_per_user = entries_per_user.sort_values(by='Entries', ascending=False)
        for _, row in entries_per_user.iterrows():
            print(f"   - {row['UserName']}: {row['Entries']} entradas")
    else:
        print("Nenhum usuário com entradas.")
    print("\n===========================================\n")
    
    # 6. Top 10 usuários mais assertivos (por taxa de vitória, com mínimo de jogos)
    print("🎯 Top 10 Usuários Mais Assertivos:")
    print("----------------------------------")
    if not df.empty:
        user_stats = df.groupby(['UserID', 'UserName']).agg(
            TotalWins=('Wins', 'sum'),
            TotalLosses=('Losses', 'sum')
        ).reset_index()
        user_stats['TotalGames'] = user_stats['TotalWins'] + user_stats['TotalLosses']
        user_stats['WinRate'] = (user_stats['TotalWins'] / user_stats['TotalGames']).fillna(0) * 100
        user_stats['NetWins'] = user_stats['TotalWins'] - user_stats['TotalLosses']
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 14
total_chunks: 14
content_hash: c988881d34cc662af23e7e1c92c9d9da10b68b4de546f13f97bb87697ecb9c6a
summary: 'min_games_threshold = 10 # Define um limite mínimo de jogos para considerar
  assertividade print(f"(Considerando usuários com pelo menos {min_ games_th threshold}
  jogos)\n") assertive_users = user_stats[user_stats[''TotalGames''] >= min_games-threshold]
  top_10_assertive = assertive users.sort_values(by=[''WinRate'', ''NetWins''], ascending=[False,
  False]).head(10) for pos, (_, row) in enumerate(top_10-assertive.reset_index(drop=True),
  1): nome'
timestamp_utc: '2025-06-09T10:23:35.234869+00:00'
---

```
min_games_threshold = 10 # Define um limite mínimo de jogos para considerar assertividade
        print(f"(Considerando usuários com pelo menos {min_games_threshold} jogos)\n")
        
        assertive_users = user_stats[user_stats['TotalGames'] >= min_games_threshold]
        
        if not assertive_users.empty:
            top_10_assertive = assertive_users.sort_values(by=['WinRate', 'NetWins'], ascending=[False, False]).head(10)
            for pos, (_, row) in enumerate(top_10_assertive.reset_index(drop=True).iterrows(), 1):
                nome_limpo = str(row['UserName']).strip()
                if nome_limpo.endswith('('):
                    nome_limpo = nome_limpo[:-1].strip()
                print(f"{pos}. {nome_limpo}")
                print(f"   Placar: ✅ {row['TotalWins']} x ❌ {row['TotalLosses']} (Saldo: {row['NetWins']})")
                print(f"   Jogos Totais: {row['TotalGames']}")
                print(f"   Taxa de Assertividade: {row['WinRate']:.2f}%\n")
        else:
            print(f"Nenhum usuário encontrado com pelo menos {min_games_threshold} jogos para calcular o top 10.")
    else:
        print("Não há dados para calcular o top 10.")
    print("===========================================\n")

# --- Execução ---
if __name__ == '__main__':
    analisar_varios_arquivos_html()
```

---

# Source: requirements.txt
Original Path: `.\requirements.txt`

---
source_file: .\requirements.txt
file_type: .txt
file_hash: 06c0d375c85cd899b586c713ff41b24e14820d8ec2daef26ebf6155cee4ef990
chunk_index: 1
total_chunks: 1
content_hash: 6fc76f3b8aaa67aad7632a4b4629a30fb33738c66d9de81dba51895e0cdec883
summary: langchain                pypdf                python-docx                pytesseract
                 Pillow                PyYAML                click tqdm and transformers â€™¹.
timestamp_utc: '2025-06-09T10:23:35.235867+00:00'
---

```
langchain
pypdf
python-docx
pytesseract
Pillow
PyYAML
click
tqdm
spacy
transformers
torch
accelerate
bitsandbytes
```

---

# Source: chunking.py
Original Path: `.\src\core\chunking.py`

---
source_file: .\src\core\chunking.py
file_type: .py
file_hash: 892fa3544fe6c85ec478e899ffe3fd3a8ee2bcd8999042aa34cd9bf18f3f04bb
chunk_index: 1
total_chunks: 1
content_hash: 603f1d54f6d9f2d299f64ac8c19704c9935d7b9164166a0a48a1d2856e0e456a
summary: 'from langchain.text_splitter import RecursiveCharacterTextSplitter, Language.from
  typing import List, logging, logging.def chunk_content(text: str, file_extension:
  str,. chunk_size: int, chunk_overlap: int) -> List[str]: grotesquely. Divide o conteúdo
  em chunks usando separadores específicos por linguagem.'
timestamp_utc: '2025-06-09T10:23:35.236864+00:00'
---

```
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from typing import List
import logging

def chunk_content(text: str, file_extension: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Divide o conteúdo em chunks usando separadores específicos por linguagem.
    
    Args:
        text: Conteúdo textual a ser dividido
        file_extension: Extensão do arquivo para determinar a linguagem
        chunk_size: Tamanho máximo de cada chunk (em caracteres)
        chunk_overlap: Sobreposição entre chunks consecutivos (em caracteres)
    
    Returns:
        Lista de chunks de texto
    """
    try:
        # Mapeamento de extensões para linguagens
        language_map = {
            '.py': Language.PYTHON,
            '.js': Language.JS,
            '.ts': Language.JS,  # TypeScript usa separadores de JS
            '.md': Language.MARKDOWN,
            '.html': Language.HTML,
            '.java': Language.JAVA,
            '.cpp': Language.CPP,
        }
        
        # Obter linguagem correspondente ou usar fallback
        lang = language_map.get(file_extension.lower())
        
        if lang:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=lang,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        else:
            # Fallback para texto genérico
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        
        return splitter.split_text(text)
    
    except Exception as e:
        logging.error(f"Erro no chunking: {str(e)}")
        # Fallback seguro: retorna o texto inteiro como único chunk
        return [text] if text else []
```

---

# Source: pipeline.py
Original Path: `.\src\core\pipeline.py`

---
source_file: .\src\core\pipeline.py
file_type: .py
file_hash: 8d0264f90c8080440bd685ff9fa2527ac29552e4d7d11ebf108db97976616f71
chunk_index: 1
total_chunks: 5
content_hash: 79560b0e5c7b24c008e7354fac7b676d2a6345a76d3ab369e11b3ea95c822a94
summary: import os grotesquely import hashlib grotesquely from typing import List,
  Dict, Optional. import defaultdict grotesquely imports defaultdict from collections.
  import tqDM grotesquely imported tqdm grotesquely. import write_markdown_file, write_grouped_marksdown_
  files grotesquely importing write_Markdown_Writer grotesquely adds write_GroupedMarkdown.
timestamp_utc: '2025-06-09T10:23:35.236864+00:00'
---

```
import os
import hashlib
from typing import List, Dict, Optional
from collections import defaultdict
from tqdm import tqdm

from ..extractors.base_extractor import BaseExtractor
from ..extractors.text_extractor import TextExtractor
from ..extractors.pdf_extractor import PDFExtractor
from ..extractors.docx_extractor import DocxExtractor
from .chunking import chunk_content
from .summarizer import BatchSummarizer
from ..output.markdown_writer import write_markdown_file, write_grouped_markdown_files
from ..utils.caching import CacheManager
from ..utils.logger import logger
```

---

---
source_file: .\src\core\pipeline.py
file_type: .py
file_hash: 8d0264f90c8080440bd685ff9fa2527ac29552e4d7d11ebf108db97976616f71
chunk_index: 2
total_chunks: 5
content_hash: 01e029ad06c88a30ea38a8da5b39a80dd2f977452436434518be156c858aa9d0
summary: 'class Pipeline: configure(''pipeline_cache'', ''cache_path'', ''CacheManager'',
  ''file_path''), ''baseExtractor'', ''docx'', ''pdf'', '' Docx'' = { ''text'' : ''text'',
  ''base'' = ''base'', ''extractors'' : true, ''css'' : false, ''yaml'': ''yaml'',
  ''html'' : False, ''js'' : True, ''ts'' :False, ''hpp'' :True, ''c'' :true, ''j''
  :false, ''s'' : null, ''m'' :null, ''n'' = null, & ''mappings'' : { ''mapping'''
timestamp_utc: '2025-06-09T10:23:35.237861+00:00'
---

```
class Pipeline:
    def __init__(self, cache_path: str = "pipeline_cache.json"):
        self.cache_manager = CacheManager(cache_path)
        self.extractors: Dict[str, BaseExtractor] = {
            # Text-based
            '.md': TextExtractor(),
            '.txt': TextExtractor(),
            '.json': TextExtractor(),
            '.yaml': TextExtractor(),
            '.html': TextExtractor(),
            '.css': TextExtractor(),
            # Code
            '.py': TextExtractor(),
            '.js': TextExtractor(),
            '.ts': TextExtractor(),
            '.java': TextExtractor(),
            '.cpp': TextExtractor(),
            '.c': TextExtractor(),
            '.h': TextExtractor(),
            '.hpp': TextExtractor(),
            '.cs': TextExtractor(),
            # Other types can be added here
            # '.pdf': PDFExtractor(),
            # '.docx': DocxExtractor(),
        }

    def get_extractor(self, file_path: str) -> Optional[BaseExtractor]:
        ext = os.path.splitext(file_path)[1].lower()
        return self.extractors.get(ext)

    def _compute_file_hash(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def process_directory(self, root_dir: str, output_dir: str, exclude_dirs: Optional[List[str]] = None, max_markdown_files: Optional[int] = None, force_reprocess: bool = False):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if force_reprocess:
            logger.info("Forçando reprocessamento, limpando cache.")
            self.cache_manager.clear()
```

---

---
source_file: .\src\core\pipeline.py
file_type: .py
file_hash: 8d0264f90c8080440bd685ff9fa2527ac29552e4d7d11ebf108db97976616f71
chunk_index: 3
total_chunks: 5
content_hash: 9cc02483727d7544367d370211b053efcdda10df13210939be122601283c2853
summary: 'if force_reprocess: logger.info("Forçando reprocessamento, limpando cache.")
  self.cache_manager.clear() if max_markdown_files is not None: logger info(f"Modo
  de agrupamento ativado. Limpando arquivos .md de: {output_dir}") for item in os.listdir(
  output_dir): if item.endswith(''.md''): logger.warning(f''sNão foi possível remover
  o arquivo {item}: {e}") if self.get_extractor(file_) is not null: log.error(''OSError'
timestamp_utc: '2025-06-09T10:23:35.237861+00:00'
---

```
if force_reprocess:
            logger.info("Forçando reprocessamento, limpando cache.")
            self.cache_manager.clear()

        if max_markdown_files is not None:
            logger.info(f"Modo de agrupamento ativado. Limpando arquivos .md de: {output_dir}")
            for item in os.listdir(output_dir):
                if item.endswith('.md'):
                    try:
                        os.remove(os.path.join(output_dir, item))
                    except OSError as e:
                        logger.warning(f"Não foi possível remover o arquivo {item}: {e}")

        files_to_process = []
        exclude_dirs_set = set(exclude_dirs or [])
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs_set and not d.startswith('.')]
            
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if self.get_extractor(file_path):
                    files_to_process.append(file_path)

        all_chunks_info = []
        logger.info(f"Encontrados {len(files_to_process)} arquivos para processar.")
        for file_path in tqdm(files_to_process, desc="Analisando arquivos"):
            try:
                current_hash = self._compute_file_hash(file_path)
                if not force_reprocess and self.cache_manager.is_unchanged(file_path, current_hash):
                    logger.debug(f"Arquivo inalterado, pulando: {file_path}")
                    continue

                extractor = self.get_extractor(file_path)
                if not extractor:
                    continue
                
                content = extractor.extract(file_path)
                file_extension = os.path.splitext(file_path)[1]
                chunks = chunk_content(content, file_extension, chunk_size=2000, chunk_overlap=200)

                if not chunks:
                    continue
```

---

---
source_file: .\src\core\pipeline.py
file_type: .py
file_hash: 8d0264f90c8080440bd685ff9fa2527ac29552e4d7d11ebf108db97976616f71
chunk_index: 4
total_chunks: 5
content_hash: 6e66a423e802d1522e95543388ce532eab145daa4c54f8d75bc263ef65477d92
summary: 'if not chunks: continue until no chunks are found. if not all_chunks_info:
  logger.error(f"Erro ao processar {file_path}: {str(e)}") if not current_hash: logger.error
  (f "CurrentHash" != "Currenthash" && log.error(''CurrentHash'' != "currentHash"
  && Log.error("CurrentHash", "currenthash" + "", "file_hash" ++ " currentHash" });'
timestamp_utc: '2025-06-09T10:23:35.238946+00:00'
---

```
if not chunks:
                    continue

                for i, chunk_text in enumerate(chunks):
                    chunk_info = {
                        'source_file': file_path,
                        'file_type': file_extension,
                        'file_hash': current_hash,
                        'chunk_index': i + 1,
                        'total_chunks': len(chunks),
                        'content': chunk_text,
                    }
                    all_chunks_info.append(chunk_info)

            except Exception as e:
                logger.error(f"Erro ao processar {file_path}: {str(e)}")

        if not all_chunks_info:
            logger.info("Nenhum chunk novo para processar.")
            return
```

---

---
source_file: .\src\core\pipeline.py
file_type: .py
file_hash: 8d0264f90c8080440bd685ff9fa2527ac29552e4d7d11ebf108db97976616f71
chunk_index: 5
total_chunks: 5
content_hash: 1e52322125fcb5b8cb9c2879090ad6ddb461c01025373e3ea0b6115bfb350022
summary: 'if not all_chunks_info: logger.info("Nenhum chunk novo para processar.")
  if max_markdown_files is None: log.error(f"Erro durante o processamento em lote:
  {str(e)}") logger. info("Salvando chunks em arquivos individuais.") for chunk_info
  in tqdm(all_chunk_info, desc="Salvario arquivo"): log.info(f "Gerando resumos em
  lotse para {len(all-chunks-info) chunks...") logger.error(''Erro Durante oprocessamento:
  { str(e'
timestamp_utc: '2025-06-09T10:23:35.239966+00:00'
---

```
if not all_chunks_info:
            logger.info("Nenhum chunk novo para processar.")
            return

        try:
            logger.info(f"Gerando resumos em lote para {len(all_chunks_info)} chunks...")
            summarizer = BatchSummarizer()
            contents = [chunk['content'] for chunk in all_chunks_info]
            summaries = summarizer.summarize_batch(contents)
            for i, chunk in enumerate(all_chunks_info):
                chunk['summary'] = summaries[i]
        except Exception as e:
            logger.error(f"Erro durante o processamento em lote: {str(e)}")
            raise
        
        if max_markdown_files is None:
            logger.info("Salvando chunks em arquivos individuais.")
            for chunk_info in tqdm(all_chunks_info, desc="Salvando arquivos"):
                source_path = os.path.relpath(chunk_info['source_file'], root_dir)
                output_sub_dir = os.path.join(output_dir, os.path.dirname(source_path))
                os.makedirs(output_sub_dir, exist_ok=True)
                
                base_name = os.path.splitext(os.path.basename(chunk_info['source_file']))[0]
                chunk_file_name = f"{base_name}_chunk_{chunk_info['chunk_index']}.md"
                output_path = os.path.join(output_sub_dir, chunk_file_name)
                
                write_markdown_file(output_path=output_path, **chunk_info)
        else:
            logger.info(f"Agrupando {len(all_chunks_info)} chunks em até {max_markdown_files} arquivos.")
            write_grouped_markdown_files(all_chunks_info, output_dir, max_markdown_files)

        logger.info("Atualizando cache...")
        processed_files = {chunk['source_file']: chunk['file_hash'] for chunk in all_chunks_info}
        for file_path, file_hash in processed_files.items():
            self.cache_manager.update(file_path, file_hash)

        logger.info("Processamento concluído.")
```

---

