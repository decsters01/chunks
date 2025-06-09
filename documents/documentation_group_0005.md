# Source: relatorio.py
Original Path: `.\relatorio.py`

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 2
total_chunks: 14
content_hash: 68abda0229392942d51b848cac9569f4260bde4badc5c1882540bc7283bdc44b
summary: def analisar_dados_roleta(caminho_arquivo_html, retornar_dataframe=False):.
  Analisa o arquivo HTML de mensagens para extrair dados de roleta e gerar estatísticas.
timestamp_utc: '2025-06-09T10:23:35.227888+00:00'
---

```
def analisar_dados_roleta(caminho_arquivo_html, retornar_dataframe=False):
    """
    Analisa o arquivo HTML de mensagens para extrair dados de roleta e gerar estatísticas.
    """
    try:
        with open(caminho_arquivo_html, 'r', encoding='utf-8') as f:
            conteudo_html = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo_html}' não encontrado.")
        print("Certifique-se de que o arquivo HTML está na mesma pasta que o script,")
        print("ou forneça o caminho completo para o arquivo.")
        return

    soup = BeautifulSoup(conteudo_html, 'html.parser')
    mensagens = soup.find_all('div', class_='message')

    dados_coletados = []
    contexto_usuario = defaultdict(lambda: {'roleta': 'Desconhecida', 'nome': 'Desconhecido'})
    data_atual_str = None

    for msg_div in mensagens:
        # Extrair data do cabeçalho de serviço
        if 'service' in msg_div.get('class', []):
            data_div = msg_div.find('div', class_='body details')
            if data_div:
                data_atual_str = data_div.text.strip() # Ex: "15 May 2025"
            continue # Pula para a próxima mensagem

        # Processar mensagens padrão
        if 'default' in msg_div.get('class', []):
            corpo_msg = msg_div.find('div', class_='body')
            if not corpo_msg:
                continue

            texto_msg_div = corpo_msg.find('div', class_='text')
            if not texto_msg_div:
                continue
            
            texto_msg_completo = texto_msg_div.decode_contents().replace('<br/>', '\n').replace('<br>', '\n')
            texto_msg_limpo = texto_msg_div.get_text(separator='\n', strip=True)
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 3
total_chunks: 14
content_hash: 9e2516ceb6ada2b786eb30aea10c20e6dd45081756cd61eb908f96b9e341c7ab
summary: '# Extrair timestamp = None. # Fallback para data de serviço se o título
  não tiver data completa. # Tentar extrair hora da mensagem se disponível. # Ex:
  "15 May 2025" -> "2025-05-15"'
timestamp_utc: '2025-06-09T10:23:35.227888+00:00'
---

```
# Extrair timestamp
            timestamp = None
            date_details_div = corpo_msg.find("div", class_="pull_right date details")
            if date_details_div and date_details_div.has_attr('title'):
                timestamp = extrair_timestamp_do_titulo(date_details_div['title'])
            
            if not timestamp and data_atual_str: # Fallback para data de serviço se o título não tiver data completa
                # Tentar extrair hora da mensagem se disponível
                hora_match = re.search(r'(\d{2}:\d{2})', date_details_div.text if date_details_div else "")
                if hora_match:
                    hora_str = hora_match.group(1)
                    try:
                        # Tentar converter data_atual_str para um formato que pd.to_datetime entenda
                        # Ex: "15 May 2025" -> "2025-05-15"
                        data_obj_temp = datetime.strptime(data_atual_str, "%d %B %Y")
                        timestamp_completo_str = f"{data_obj_temp.strftime('%Y-%m-%d')} {hora_str}"
                        timestamp = pd.to_datetime(timestamp_completo_str)
                    except ValueError:
                        pass # Não foi possível formar timestamp completo

            if not timestamp: # Se ainda não há timestamp, pula esta mensagem
                 #print(f"Timestamp não encontrado para a mensagem: {texto_msg_limpo[:100]}")
                 continue


            # Verificar se é uma mensagem de início de monitoramento de roleta
            if "INÍCIO DO MONITORAMENTO" in texto_msg_completo:
                match_roleta = re.search(r"🎰 Roleta: ([\w-]+)", texto_msg_completo)
                match_licenca = re.search(r"Licença: (\w+)", texto_msg_completo)
                match_usuario = re.search(r"👤 Usuário: (.+?)(?:\n|<a href=|$)", texto_msg_completo) # Modificado para pegar até \n ou <a
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 4
total_chunks: 14
content_hash: 6b75be404dbe5f15a8d5a5b9911198e4f2ae80358939fb719fd6036ffd5172d6
summary: 'if match_licenca: "Desconhecido" if match_usuario else "Des Conhecidos"
  if "Relatório de Operações" in texto_msg_completo: "Conheção" if ''Relatôrio de
  operaçÝes'' in texta_msg: ''Conceção'' match_placar = re.search(r"🏆 Placar"), match_id_relatorio
  = ''Relatorio'', match_PLACar = ''Placar'' if ''relatôlio'' in Texta_Message: ''Relatsório
  of Operaç'
timestamp_utc: '2025-06-09T10:23:35.228885+00:00'
---

```
if match_licenca:
                    user_id = match_licenca.group(1)
                    nome_usuario_raw = match_usuario.group(1).strip() if match_usuario else "Desconhecido"
                    nome_usuario_limpo = extrair_nome_usuario(nome_usuario_raw)
                    
                    contexto_usuario[user_id]['nome'] = nome_usuario_limpo
                    if match_roleta:
                        contexto_usuario[user_id]['roleta'] = match_roleta.group(1)
                    # Se não encontrar roleta aqui, mantém a anterior ou "Desconhecida"
                continue # Processamos, vamos para a próxima

            # Verificar se é um relatório de operações
            if "📊 Relatório de Operações" in texto_msg_completo:
                match_id_relatorio = re.search(r"🔰 (\w+)", texto_msg_completo)
                match_placar = re.search(r"🏆 Placar Final: ✅ (\d+) x ❌ (\d+)", texto_msg_completo)

                if match_id_relatorio and match_placar:
                    id_usuario_relatorio = match_id_relatorio.group(1)
                    vitorias = int(match_placar.group(1))
                    derrotas = int(match_placar.group(2))
                    
                    # Usa o contexto mais recente para nome e roleta
                    roleta_atual = contexto_usuario[id_usuario_relatorio]['roleta']
                    nome_usuario_atual = contexto_usuario[id_usuario_relatorio]['nome']
                    if nome_usuario_atual == "Desconhecido" and id_usuario_relatorio: # Tenta pegar nome de usuário se não estiver no contexto
                        from_name_div = msg_div.find('div', class_='from_name')
                        if from_name_div and from_name_div.text.strip() != "ProjectB":
                             nome_usuario_atual = from_name_div.text.strip()
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 5
total_chunks: 14
content_hash: d99422bf1d349b92d482f1a8e4040012da4c7be5b63e6897b74930781ec29c58
summary: 'dados_coletados.append({ timestamp: timestamp, userID: id_usuario_relatorio,
  ''Roulette'': roleta_atual, ''Wins'': vitorias, ''Losses'': derrotas, ''Event'':
  event, ''Dashboard'': pd.DataFrame, }); print("Nenhum dado de relatório de operações
  foi encontrado ou extraído.") if not dados_ coletados: print("\n🔰 PAINEL DE ANÁLISE
  DE DADOS DA ROLETA 🔰") print("===========================================\n") print'
timestamp_utc: '2025-06-09T10:23:35.228885+00:00'
---

```
dados_coletados.append({
                        'Timestamp': timestamp,
                        'UserID': id_usuario_relatorio,
                        'UserName': nome_usuario_atual,
                        'Roulette': roleta_atual,
                        'Wins': vitorias,
                        'Losses': derrotas
                    })

    if not dados_coletados:
        print("Nenhum dado de relatório de operações foi encontrado ou extraído.")
        return

    df = pd.DataFrame(dados_coletados)
    df = df.sort_values(by='Timestamp').reset_index(drop=True)

    if retornar_dataframe:
        return df

    # --- Análises e Exibição do Dashboard ---
    print("\n🔰 PAINEL DE ANÁLISE DE DADOS DA ROLETA 🔰")
    print("===========================================\n")

    # 1. Período Analisado
    if not df.empty and pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
        min_date = df['Timestamp'].min()
        max_date = df['Timestamp'].max()
        print(f"🗓️ Período Analisado: de {min_date.strftime('%d/%m/%Y %H:%M')} a {max_date.strftime('%d/%m/%Y %H:%M')}\n")
    else:
        print("🗓️ Período Analisado: Não foi possível determinar (sem dados de timestamp válidos).\n")
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 6
total_chunks: 14
content_hash: 2d097098300584c419a23b237cf259e025bb0f64ed75179a6fd16654da833b5e
summary: '# 2. Listar todos os IDs e suas respectivas listas de placares. print("Histórico
  de Placares por Usuário:") print("---------------------------") # 3. Roleta mais
  usada e contagem. print(''Estatísticas de Roletas:'') print(''Nenhum placar registrado'')'
timestamp_utc: '2025-06-09T10:23:35.229882+00:00'
---

```
# 2. Listar todos os IDs e suas respectivas listas de placares
    print("📊 Histórico de Placares por Usuário:")
    print("------------------------------------")
    unique_ids = df['UserID'].unique()
    for user_id in unique_ids:
        df_usuario = df[df['UserID'] == user_id]
        nome_usuario = str(df_usuario['UserName'].iloc[0]).strip()
        if nome_usuario.endswith('('):
            nome_usuario = nome_usuario[:-1].strip()
        print(f"\n👤 Usuário: {nome_usuario}")
        if df_usuario.empty:
            print("   Nenhum placar registrado.")
            continue
        for _, row in df_usuario.iterrows():
            print(f"   - {row['Timestamp'].strftime('%d/%m/%Y %H:%M')}: 🏆 Placar: ✅ {row['Wins']} x ❌ {row['Losses']} (Roleta: {row['Roulette']})")
    print("\n===========================================\n")

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
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 7
total_chunks: 14
content_hash: 04609555aa743aac7221ecf973df905faf84af133d491a677974a3873b530026
summary: '# 4. Usuário com melhor placar total (Saldo de Vitórias) print("🏆 Usuério
  com Melhor Saldo of Vitória:") if not df.empty: print(f""), print("Não há dados
  de placar para determinar o melhor usuário.") print("\n===========================================\n")
  print("Â£££", true, true, false, false)'
timestamp_utc: '2025-06-09T10:23:35.230880+00:00'
---

```
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
chunk_index: 8
total_chunks: 14
content_hash: f468d9f4e70ebcd9af4874c78acf52ef55d0ff38f7e66e070c3e48cf87b79900
summary: '# 5. Quantas entradas (relatórios) cada usuário fez. print("📊 Entradas de
  Placar) por Usuário:") print("---------------------------------------------") if
  not df.empty: entries_per_user = df.groupby([''UserID'', ''UserName'']).size().reset_index(name=''Entries'')
  print("Nenhum usUário comEntradas.") print("\n===========================================\n")'
timestamp_utc: '2025-06-09T10:23:35.230880+00:00'
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
chunk_index: 9
total_chunks: 14
content_hash: 3e0337f4071a86dc4924ef74c528e0b1b0a2c814244a9791631420c424c7b88a
summary: 'min_games_threshold = 10 # Define um limite mínimo de jogos para considerar
  assertividade print(f"(Considerando usuários com pelo menos {min_ games_th threshold}
  jogos)\n") assertive_users = user_stats[user_stats[''TotalGames''] >= min_games-threshold]
  top_10_assertive = assertive users.sort_values(by=[''WinRate'', ''NetWins''], ascending=[False,
  False]).head(10) for pos, (_, row) in enumerate(top_10-assertive.reset_index(drop=True),
  1): nome'
timestamp_utc: '2025-06-09T10:23:35.231877+00:00'
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
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 10
total_chunks: 14
content_hash: 29ac0e4829db3f5d12c2bdb1a54c123ba02d73005c6bb77981856d4b46bcba4a
summary: 'def coletar_arquivos_html_em_todos_chat_exports(diretorio_base=''.''): """Busca
  todos os arquvos .html dentro de pastas que começam com ChatExport_ no diretório
  base.""" arquivo_html = [] for nome_pasta in os.listdir(''ChatExport_''): if nome.startswith(''Chat
  Export''): return arquivo_html.append(os.path.join(caminho_pastA, nome_.arquivo),
  ''html'') return arqivo.html. append(os'
timestamp_utc: '2025-06-09T10:23:35.231877+00:00'
---

```
def coletar_arquivos_html_em_todos_chat_exports(diretorio_base='.'):
    """Busca todos os arquivos .html dentro de pastas que começam com ChatExport_ no diretório base."""
    arquivos_html = []
    for nome_pasta in os.listdir(diretorio_base):
        caminho_pasta = os.path.join(diretorio_base, nome_pasta)
        if os.path.isdir(caminho_pasta) and nome_pasta.startswith('ChatExport_'):
            for nome_arquivo in os.listdir(caminho_pasta):
                if nome_arquivo.endswith('.html'):
                    arquivos_html.append(os.path.join(caminho_pasta, nome_arquivo))
    return arquivos_html

def salvar_relatorio_em_log(funcao_dashboard, df, nome_arquivo_log="relatorio_dashboard.log"):
    # Salva stdout original
    stdout_original = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        funcao_dashboard(df)
    finally:
        sys.stdout = stdout_original
    conteudo = buffer.getvalue()
    with open(nome_arquivo_log, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"\n[Relatório salvo em: {nome_arquivo_log}]")

def analisar_varios_arquivos_html():
    arquivos_html = coletar_arquivos_html_em_todos_chat_exports()
    if not arquivos_html:
        print("Nenhum arquivo HTML encontrado nas pastas ChatExport_*")
        return

    todos_dados = []
    for caminho_arquivo in arquivos_html:
        print(f"Processando: {caminho_arquivo}")
        dados = analisar_dados_roleta(caminho_arquivo, retornar_dataframe=True)
        if dados is not None:
            todos_dados.append(dados)
    
    if not todos_dados:
        print("Nenhum dado extraído dos arquivos.")
        return

    df_geral = pd.concat(todos_dados, ignore_index=True)
    exibir_dashboard(df_geral)
    salvar_relatorio_em_log(exibir_dashboard, df_geral)
```

---

---
source_file: .\relatorio.py
file_type: .py
file_hash: 429b310bac1e3d6fc71880958eade8928d7c086893d3911ad87769db22ea7f12
chunk_index: 11
total_chunks: 14
content_hash: 318a64f87032cf5000c1b17e9aca7f6db783727e0d47f86b6412dcc09bbc2ae9
summary: 'def exibir_dashboard(df): print("PAINEL DE ANÁLISE DE DADOS DA ROLETA")
  # 1. Listar todos os IDs e suas respectivas listas de placares. If not df.empty
  and pd.api.types.is_datetime64_any_dtype(df[''Timestamp'']): print(f"Período Analisado:
  de {min_date.strftime(''%d/%m/%Y %H:%M'')} a {max_ date. strftime(''%.d/%.m/%,%Y%,%H:%.M'')")
  # 2. listar to'
timestamp_utc: '2025-06-09T10:23:35.232874+00:00'
---

```
def exibir_dashboard(df):
    print("\n🔰 PAINEL DE ANÁLISE DE DADOS DA ROLETA 🔰")
    print("===========================================\n")

    # 1. Período Analisado
    if not df.empty and pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
        min_date = df['Timestamp'].min()
        max_date = df['Timestamp'].max()
        print(f"🗓️ Período Analisado: de {min_date.strftime('%d/%m/%Y %H:%M')} a {max_date.strftime('%d/%m/%Y %H:%M')}\n")
    else:
        print("🗓️ Período Analisado: Não foi possível determinar (sem dados de timestamp válidos).\n")

    # 2. Listar todos os IDs e suas respectivas listas de placares
    print("📊 Histórico de Placares por Usuário:")
    print("------------------------------------")
    unique_ids = df['UserID'].unique()
    for user_id in unique_ids:
        df_usuario = df[df['UserID'] == user_id]
        nome_usuario = str(df_usuario['UserName'].iloc[0]).strip()
        if nome_usuario.endswith('('):
            nome_usuario = nome_usuario[:-1].strip()
        print(f"\n👤 Usuário: {nome_usuario}")
        if df_usuario.empty:
            print("   Nenhum placar registrado.")
            continue
        for _, row in df_usuario.iterrows():
            print(f"   - {row['Timestamp'].strftime('%d/%m/%Y %H:%M')}: 🏆 Placar: ✅ {row['Wins']} x ❌ {row['Losses']} (Roleta: {row['Roulette']})")
    print("\n===========================================\n")
```

---

