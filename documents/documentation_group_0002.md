# Source: chunkv3.py
Original Path: `.\chunkv3.py`

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 8
total_chunks: 24
content_hash: 505eaf58df02bb0414a55df9400d1c58e1156cc9e698f174fd7124d57180ee0f
summary: '# Control patterns (prioritize those that clearly start a new visual block)
  # C# specific # Python specific # Common specific. # Common common patterns are:
  "catch", "switch", "default", "if", "else", "catch"'
timestamp_utc: '2025-06-09T10:23:35.209936+00:00'
---

```
# Control patterns (prioritize those that clearly start a new visual block)
    control_patterns = [
        # Common
        r"^\\s*if\\s*\\(.*\\)\\s*\\{?", r"^\\s*if\\s+.*:",
        r"^\\s*else\\s*if\\s*\\(.*\\)\\s*\\{?", r"^\\s*elif\\s+.*:",
        r"^\\s*else\\s*\\{?", r"^\\s*else:",
        r"^\\s*for\\s*\\(.*\\)\\s*\\{?", r"^\\s*for\\s+.*:",
        r"^\\s*while\\s*\\(.*\\)\\s*\\{?", r"^\\s*while\\s+.*:",
        r"^\\s*do\\s*\\{?", # often followed by while at the end
        r"^\\s*switch\\s*\\(.*\\)\\s*\\{?",
        r"^\\s*case\\s+.*:", r"^\\s*default\\s*:",
        r"^\\s*try\\s*\\{?", r"^\\s*try:",
        r"^\\s*catch\\s*\\(.*\\)\\s*\\{?",
        r"^\\s*finally\\s*\\{?", r"^\\s*finally:",
        # Python specific
        r"^\\s*with\\s+.*:", r"^\\s*async\\s+with\\s+.*:",
        r"^\\s*async\\s+for\\s+.*:",
        # C# specific
        r"^\\s*using\\s*\\(.*\\)\\s*\\{?", r"^\\s*lock\\s*\\(.*\\)\\s*\\{?",
        # Java specific
        # try-with-resources often looks like "try (ResourceType r = ...)"
    ]

    closing_patterns = [
        r"^\\s*\\}",                            # C-style, JS, Java, C#, MQL
        r"^\\s*\\}\\s*while\\s*\\(.*\\)\\s*;", # do-while loop end
    ]
    
    in_multiline_python = False
    python_multi_start_char = ''
    in_multiline_c = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 9
total_chunks: 24
content_hash: f32c60bde2c3c0108c50047b3e2f5ccab2ebc388efa03d68f8e17f8d62fae8fd
summary: 'for i, line in enumerate(lines): stripped_line = line.strip() # Python multiline
  comments. char_to_check = ''''''"'' if ''"""'' in stripped_ line or "''''''" in
  stripped line. in_multiline_python = True. python_multi_start_char = char_ to_check.
  marcadores.add(i) # Start of comment block.'
timestamp_utc: '2025-06-09T10:23:35.209936+00:00'
---

```
for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Python multiline comments """ or '''
        if '"""' in stripped_line or "'''" in stripped_line:
            char_to_check = '"""' if '"""' in stripped_line else "'''"
            if stripped_line.count(char_to_check) % 2 == 1:
                if not in_multiline_python:
                    in_multiline_python = True
                    python_multi_start_char = char_to_check
                    marcadores.add(i) # Start of comment block
                elif python_multi_start_char == char_to_check :
                    in_multiline_python = False
                    if i + 1 < num_lines: marcadores.add(i + 1) # Line after comment block
            elif in_multiline_python and python_multi_start_char in stripped_line : 
                 in_multiline_python = False
                 if i + 1 < num_lines: marcadores.add(i + 1) 
        if in_multiline_python:
            continue

        # C-style multiline comments /* ... */
        if '/*' in stripped_line:
            if '*/' not in stripped_line :
                in_multiline_c = True
                marcadores.add(i) 
                continue
            else: 
                if stripped_line.startswith("/*") and stripped_line.endswith("*/"):
                    marcadores.add(i)
                    if i + 1 < num_lines: marcadores.add(i + 1)
                    continue
        if '*/' in stripped_line and in_multiline_c:
            in_multiline_c = False
            if i + 1 < num_lines: marcadores.add(i + 1) 
            continue
        if in_multiline_c:
            continue
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 10
total_chunks: 24
content_hash: 3c1a5f8900847a4d0fd7579a5c72dfdb1efb69f81d883603b6e4a914ac49f90f
summary: '# Single line comments: stripped_line.startswith(''#'') or stripped_ line.start
  swith(''//''): is_block_start = True. # Line after this comment block: marcadores.add(i+1)
  # Comment block continues: is_marker = False.'
timestamp_utc: '2025-06-09T10:23:35.210933+00:00'
---

```
# Single line comments
        if stripped_line.startswith('#') or stripped_line.startswith('//'):
            is_block_start = True
            if i > 0:
                prev_stripped = lines[i-1].strip()
                if prev_stripped.startswith('#') or prev_stripped.startswith('//'):
                    is_block_start = False # Part of an existing comment block
            
            if is_block_start:
                 marcadores.add(i) # Start of a new comment block

            is_block_end = True
            if i + 1 < num_lines:
                next_stripped = lines[i+1].strip()
                if next_stripped.startswith('#') or next_stripped.startswith('//'):
                    is_block_end = False # Comment block continues
            
            if is_block_end:
                if i + 1 < num_lines: marcadores.add(i+1) # Line after this comment block
            continue

        is_marker = False
        for pattern in definition_patterns:
            if re.match(pattern, stripped_line):
                marcadores.add(i)
                is_marker = True
                break
        if is_marker: continue
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 11
total_chunks: 24
content_hash: 2eeb2a1ef48a225867c87c4bbe23ca80b0a1cfe7546c6468ce4c9cb0145ea0ee
summary: 'for pattern in control_patterns: if re.match(pattern, stripped_line): marcadores.add(i)
  is_marker = True. If i + 1 < num_lines, add ''i+1'' instead of ''i'' as a separator.'
timestamp_utc: '2025-06-09T10:23:35.210933+00:00'
---

```
for pattern in control_patterns:
            if re.match(pattern, stripped_line):
                marcadores.add(i)
                is_marker = True
                break
        if is_marker: continue
        
        for pattern in closing_patterns:
            if re.match(pattern, stripped_line):
                if i + 1 < num_lines: marcadores.add(i+1)
                break
        
        if not stripped_line:
            if i > 0 and i + 1 < num_lines:
                prev_line_stripped = lines[i-1].strip()
                next_line_stripped = lines[i+1].strip()
                # Only add blank line as separator if it's between meaningful content lines
                if prev_line_stripped and not prev_line_stripped.startswith(('#', '//')) and \
                   next_line_stripped and not next_line_stripped.startswith(('#', '//')):
                    # Avoid adding 'i' if 'i+1' is already a strong marker or if prev line ended a block
                    # This logic can be complex; for now, simpler:
                    if (i not in marcadores and (i-1 not in marcadores or not lines[i-1].strip().endswith(('{',':','}')) ) ) :
                         marcadores.add(i) # Blank line itself if it's a true separator
                    marcadores.add(i+1) # Start of the next block
            continue
            
    marcadores.add(num_lines)
    
    # Post-processing (similar to before, MIN_LINES_PER_CODE_BLOCK will be key)
    sorted_marcadores = sorted(list(set(marcadores))) # Ensure uniqueness and order
    
    if not sorted_marcadores: return [0, num_lines] if num_lines > 0 else [0]
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 12
total_chunks: 24
content_hash: ef9a92c89cb93a2cac140d82c05ecb949708deb09f5bf41f4a579523cf8a9d38
summary: 'final_marcadores = [sorted_marCadores[0] for k in range(1, len(sorted marcAdores)):
  final_mar cadores.append(s sorted_marAdores[k], num_lines) if len(final_ MarcAdore)
  != 1: final_Marcadore.insert(0,0) elif not final_ marcadors and num_ lines > 0:
   final_MarCAdores. append(num_lines),  num_line.insert() elif num_line is not in
  final_ MarAdores: final MarAdores = sorted(list('
timestamp_utc: '2025-06-09T10:23:35.211930+00:00'
---

```
final_marcadores = [sorted_marcadores[0]]
    for k in range(1, len(sorted_marcadores)):
        if (sorted_marcadores[k] - final_marcadores[-1] >= MIN_LINES_PER_CODE_BLOCK) or \
           (sorted_marcadores[k] == num_lines and final_marcadores[-1] != num_lines) :
            final_marcadores.append(sorted_marcadores[k])
    
    if num_lines not in final_marcadores and num_lines in sorted_marcadores and final_marcadores[-极] < num_lines :
        if num_lines - final_marcadores[-1] < MIN_LINES_PER_CODE_BLOCK and len(final_marcadores) > 1:
            final_marcadores[-1] = num_lines
        elif final_marcadores[-1] != num_lines: # only add if not already the last one
            final_marcadores.append(num_lines)

    final_marcadores = sorted(list(set(final_marcadores)))

    if len(final_marcadores) == 1 and num_lines > 0:
        if final_marcadores[0] == 0: final_marcadores.append(num_lines)
        elif final_marcadores[0] == num_lines: final_marcadores.insert(0,0)
    elif not final_marcadores and num_lines > 0: 
        final_marcadores = [0, num_lines]
    elif num_lines == 0: # Handles empty file
         return [0] 

    if num_lines > 0 and len(final_marcadores) < 2: # Ensure at least [0, num_lines] for non-empty
        final_marcadores = sorted(list(set([0] + final_marcadores + [num_lines])))
        # Filter again if introducing 0 or num_lines made segments too small, except for the end itself
        temp_marcadores = [final_marcadores[0]]
        for k_idx in range(1,len(final_marcadores)):
            if (final_marcadores[k_idx] - temp_marcadores[-1] >=1) or final_marcadores[k_idx] == num_lines:
                 if final_marcadores[k_idx] == num_lines and temp_marcadores[-1] == num_lines: continue # Avoid [..., N, N]
                 temp_marcadores.append(final_marcadores[k_idx])
        final_marcadores = temp_marcadores
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 13
total_chunks: 24
content_hash: 526b04d713bc5d09bd74b93cf53e39ec956ac44a4aacb81373261dbefa4462bb
summary: '# Ensure first marker is 0 and last is num_lines if content exists. # Check
  for empty files or files that result in only [0,0] # Keep the marker if it''s the
  end of the file or if it respects MIN_LINES_PER_CODE_BLOCK.'
timestamp_utc: '2025-06-09T10:23:35.211930+00:00'
---

```
# Ensure first marker is 0 and last is num_lines if content exists
    if num_lines > 0:
        if not final_marcadores or final_marcadores[0] != 0:
            final_marcadores.insert(0,0)
        if final_marcadores[-1] != num_lines:
            final_marcadores.append(num_lines)
        final_marcadores = sorted(list(set(final_marcadores)))


    # Final check for empty files or files that result in only [0,0]
    if not final_marcadores or (len(final_marcadores) == 1 and final_marcadores[0] == 0 and num_lines == 0):
        return [0]
    if len(final_marcadores) >=2 and final_marcadores[0]==0 and final_marcadores[1]==0 and num_lines==0: # e.g. from [0,0]
        return [0]
        
    # Remove redundant markers if they are too close to each other after all adjustments
    # This is a simplified re-application of the MIN_LINES_PER_CODE_BLOCK logic
    if len(final_marcadores) > 1:
        current_marcadores = [final_marcadores[0]]
        for mk_idx in range(1, len(final_marcadores)):
            # Keep the marker if it's the end of the file or if it respects MIN_LINES_PER_CODE_BLOCK
            if final_marcadores[mk_idx] == num_lines or \
               (final_marcadores[mk_idx] - current_marcadores[-1] >= MIN_LINES_PER_CODE_BLOCK):
                current_marcadores.append(final_marcadores[mk_idx])
            elif mk_idx == len(final_marcadores) - 1 : # If it's the last potential marker and too close, replace previous to extend to end
                current_marcadores[-1] = final_marcadores[mk_idx]
        final_marcadores = current_marcadores
        final_marcadores = sorted(list(set(final_marcadores))) # cleanup duplicates

    return final_marcadores
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 14
total_chunks: 24
content_hash: acd7914edb85a47f81ef89743a32a006563a97cb7fd4f95ff81e39553881cd8a
summary: 'def dividir_em_chunks_por_marcadores(conteudo, marcadore): linhas = conteudo.splitlines()
  chunks = ["], marcadores = sorted(list(set(marcore), m) if len(linhas) > 0: return
  []; else: return ["], marcore.append("\n".join(lin has), ""; });'
timestamp_utc: '2025-06-09T10:23:35.212928+00:00'
---

```
def dividir_em_chunks_por_marcadores(conteudo, marcadores):
    linhas = conteudo.splitlines()
    chunks = []
    
    # Validate marcadores: must be sorted, unique, and contain at least 0 and len(lines) if content exists
    if not marcadores or (len(linhas) > 0 and (marcadores[0] != 0 or marcadores[-1] != len(linhas))):
        # Basic fallback or error, here we attempt a sane default
        if len(linhas) > 0:
            marcadores = sorted(list(set([0] + marcadores + [len(linhas)])))
            # Remove markers outside the valid range, if any crept in
            marcadores = [m for m in marcadores if 0 <= m <= len(linhas)]
            marcadores = sorted(list(set(marcadores))) # re-sort and unique
            if not marcadores or marcadores[0] != 0: marcadores.insert(0,0)
            if marcadores[-1] != len(linhas): marcadores.append(len(linhas))
            marcadores = sorted(list(set(marcadores))) # final cleanup
        else: # No lines
            return []


    if len(marcadores) < 2: # Needs at least a start and end
        if "".join(linhas).strip(): # If there's actual content
            chunks.append("\n".join(linhas))
        return chunks

    for i in range(len(marcadores) - 1):
        inicio = marcadores[i]
        fim = marcadores[i+1]
        
        if inicio < fim: # Ensure there's a valid range
            chunk_linhas = linhas[inicio:fim]
            # Add chunk only if it contains non-whitespace characters
            if any(line.strip() for line in chunk_linhas):
                chunks.append('\n'.join(chunk_linhas))
    return chunks

nlp = spacy.load("pt_core_news_sm")  # Modelo pequeno e local para português
nlp.max_length = 2000000  # Aumenta o limite para 2 milhões de caracteres
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 15
total_chunks: 24
content_hash: 559ec0a4bbbf4a3706a0bad44eac99d25359319413fd8edb574659ff969abeeb
summary: 'def resumir_chunk(chunk): # Bem abaixo do limite de 1.000.000 para ter margem
  de segurança. # Se o texto for muito grande, truncar por caracteres. # Pega as 2
  frases mais longas como "resumo" simples.'
timestamp_utc: '2025-06-09T10:23:35.212928+00:00'
---

```
def resumir_chunk(chunk):
    # Definir o limite máximo de caracteres para processar
    max_chars = 500000  # Bem abaixo do limite de 1.000.000 para ter margem de segurança
    
    # Se o texto for muito grande, truncar
    if len(chunk) > max_chars:
        # Opção 1: pegar as primeiras N linhas
        linhas = chunk.splitlines()
        if len(linhas) > 50:
            texto_para_processar = '\n'.join(linhas[:50])
        else:
            # Opção 2: se tiver poucas linhas mas muito longas, truncar por caracteres
            texto_para_processar = chunk[:max_chars]
    else:
        texto_para_processar = chunk
    
    try:
        doc = nlp(texto_para_processar)
        sentencas = list(doc.sents)
        # Pega as 2 frases mais longas como "resumo" simples
        if sentencas:
            sentencas_ordenadas = sorted(sentencas, key=lambda s: -len(s.text))
            resumo = " ".join([s.text for s in sentencas_ordenadas[:2]])
        else:
            # Fallback se não conseguir extrair frases
            palavras = texto_para_processar.split()
            resumo = " ".join(palavras[:20]) + "..." if len(palavras) > 20 else texto_para_processar
        return resumo
    except Exception as e:
        # Fallback se ocorrer qualquer erro no processamento
        print(f"Erro ao resumir chunk: {e}")
        return "Não foi possível gerar resumo automático."
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 16
total_chunks: 24
content_hash: aa78cd72593178791096ef6f7ca925340e4d53a362354f45baba91d9ebdb5314
summary: 'def process_file(file_path): """Processa um arquivo individual e retorna
  seus chunks" # Registrar erro de conversão se houver. If not content, conversion_error
  = convert_to_text( file_path) return [{''origem'': file_Path, ''texto'': chunk for
  chunk in chunks] except Exception as e: return traceback.format_exc()'
timestamp_utc: '2025-06-09T10:23:35.213925+00:00'
---

```
def process_file(file_path):
    """Processa um arquivo individual e retorna seus chunks"""
    try:
        content, conversion_error = convert_to_text(file_path)
        
        # Registrar erro de conversão se houver
        if conversion_error:
            error_msg, tb = conversion_error
            full_error = f"Erro na conversão de {file_path}: {error_msg}\n{tb}"
            with open("erros_paralelos.log", "a") as log_file:
                log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {full_error}\n")
            return []
        
        if not content:
            return []
        
        file_ext = os.path.splitext(file_path)[1]
        marcadores = detect_code_blocks(content, file_ext)
        chunks = dividir_em_chunks_por_marcadores(content, marcadores)
        
        return [{'origem': file_path, 'texto': chunk} for chunk in chunks]
    except Exception as e:
        import traceback
        error_msg = f"Erro ao processar {file_path}: {str(e)}\n"
        error_msg += traceback.format_exc()
        print(error_msg)
        # Registrar em log estruturado para ambiente paralelo
        with open("erros_paralelos.log", "a") as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}\n")
        return []
```

---

---
source_file: .\chunkv3.py
file_type: .py
file_hash: 2bc6983f82da799f73258a45b83d6a6d80adc3abab811e6df699bdb79ef26d14
chunk_index: 17
total_chunks: 24
content_hash: 5762b72b421b1ffc2d3b734501cac0f6f6f9637d1c2f9cf5f3d8bc87fde5fc7f
summary: 'def salvar_chunks_em_markdown (nome_arquivo, chunks, pasta_destino, indice_arqivo=None,
  total_arQUIVos=MAX_ARQUIVOS_MARKDOWN): """ Salva chunks em arquivos markdown. Se
  indice _arquiva for fornecido, salva no arquivo específico dentro do limite total_
  Arquivo. Agora inclui um resumo automático do chunk usando spaCy"'
timestamp_utc: '2025-06-09T10:23:35.213925+00:00'
---

```
def salvar_chunks_em_markdown(nome_arquivo, chunks, pasta_destino, indice_arquivo=None, total_arquivos=MAX_ARQUIVOS_MARKDOWN):
    """
    Salva chunks em arquivos markdown.
    Se indice_arquivo for fornecido, salva no arquivo específico dentro do limite total_arquivos.
    Agora inclui um resumo automático do chunk usando spaCy.
    """
    base = os.path.splitext(os.path.basename(nome_arquivo))[0]
    _, ext = os.path.splitext(nome_arquivo)
    lang_ext = ext.lstrip('.').lower() if ext else 'text'
    
    if indice_arquivo is not None:
        # Modo de agrupamento: salvar múltiplos chunks em um único arquivo
        nome_md = f"documentacao_{indice_arquivo:04d}.md"
        caminho_md = os.path.join(pasta_destino, nome_md)
        
        # Verificar se o arquivo já existe para adicionar conteúdo
        modo = 'a' if os.path.exists(caminho_md) else 'w'
        
        with open(caminho_md, modo, encoding='utf-8') as f:
            for idx, chunk in enumerate(chunks, 1):
                resumo = resumir_chunk(chunk)
                # Adicionar cabeçalho para cada chunk com resumo
                f.write(f'# {base} (chunk {idx})\n\n**Resumo:** {resumo}\n\n```{lang_ext}\n{chunk}\n```\n\n')
    else:
        # Modo original: um arquivo por chunk (usado apenas para testes ou quando MAX_ARQUIVOS_MARKDOWN é muito grande)
        for idx, chunk in enumerate(chunks, 1):
            resumo = resumir_chunk(chunk)
            nome_md = f"{base}_chunk{idx}.md"
            caminho_md = os.path.join(pasta_destino, nome_md)
            markdown_content = f'# {base} (chunk {idx})\n\n**Resumo:** {resumo}\n\n```{lang_ext}\n{chunk}\n```\n'
            with open(caminho_md, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

# Função removida (substituída por implementação direta com langchain)
```

---

