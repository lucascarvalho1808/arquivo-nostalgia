import os
from datetime import datetime
from routes.extensions import supabase

def gerar_ranking_comunidade():
    """
    Gera o ranking dos itens mais salvos pela comunidade
    e persiste em CSV 
    """
    try:
        # Consulta todos os itens salvos pela comunidade no banco de dados
        response = supabase.table('itens_lista').select('*').execute()
        itens = response.data

        # Inicializa contadores para cada tipo de item
        contadores = {
            'filme': {},
            'serie': {},
            'jogo': {}
        }
        
        # Conta quantas vezes cada item foi salvo, agrupando por tipo e api_id
        for item in itens:
            tipo = (item.get("tipo") or "").strip().lower() 
            api_id = item.get("api_id")
            titulo = item.get("titulo")
            poster_url = item.get("poster_url")
            if tipo in contadores and api_id:
                if api_id not in contadores[tipo]:
                    contadores[tipo][api_id] = {
                        "contagem": 0,
                        "titulo": titulo,
                        "poster_url": poster_url,
                    }
                contadores[tipo][api_id]["contagem"] += 1
        
        # Seleciona os 3 itens mais populares de cada tipo
        top_filmes = sorted(contadores['filme'].items(), key=lambda x: x[1]['contagem'], reverse=True)[:3]
        top_series = sorted(contadores['serie'].items(), key=lambda x: x[1]['contagem'], reverse=True)[:3]
        top_jogos = sorted(contadores['jogo'].items(), key=lambda x: x[1]['contagem'], reverse=True)[:3]
        
        os.makedirs('data', exist_ok=True)
        caminho_csv = 'data/ranking_comunidade.csv'
        
        # Escreve o arquivo CSV manualmente
        with open(caminho_csv, 'w', encoding='utf-8') as arquivo:
            # Cabeçalho do CSV
            arquivo.write('tipo,posicao,api_id,titulo,poster_url,contagem\n')
            # Escreve os filmes
            for idx, (api_id, dados) in enumerate(top_filmes, 1):
                linha = f'filme,{idx},{api_id},"{dados["titulo"]}","{dados["poster_url"]}",{dados["contagem"]}\n'
                arquivo.write(linha)
            # Escreve as séries
            for idx, (api_id, dados) in enumerate(top_series, 1):
                linha = f'serie,{idx},{api_id},"{dados["titulo"]}","{dados["poster_url"]}",{dados["contagem"]}\n'
                arquivo.write(linha)
            # Escreve os jogos
            for idx, (api_id, dados) in enumerate(top_jogos, 1):
                linha = f'jogo,{idx},{api_id},"{dados["titulo"]}","{dados["poster_url"]}",{dados["contagem"]}\n'
                arquivo.write(linha)
        
        # Salva a data/hora da última atualização do ranking
        with open('data/ultima_atualizacao.txt', 'w', encoding='utf-8') as f:
            f.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        print(f"Ranking gerado com sucesso em {caminho_csv}")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar ranking: {e}")
        return False


def ler_ranking_comunidade():
    """
    Lê o ranking do CSV e retorna os dados estruturados.
    """
    try:
        caminho_csv = 'data/ranking_comunidade.csv'
        
        # Se o arquivo não existir, gera o ranking antes de ler
        if not os.path.exists(caminho_csv):
            print("Arquivo CSV não encontrado. O arquivo será gerado.")
            gerar_ranking_comunidade()
        
        # Estrutura para armazenar o ranking lido
        ranking = {
            'filmes': [],
            'series': [],
            'jogos': [],
            'ultima_atualizacao': None
        }
        
        # Lê o arquivo CSV linha a linha, ignorando o cabeçalho
        with open(caminho_csv, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas[1:]:  # pula o cabeçalho
                # Divide a linha, tratando aspas
                partes = []
                atual = ''
                em_aspas = False
                for c in linha.strip():
                    if c == '"':
                        em_aspas = not em_aspas
                    elif c == ',' and not em_aspas:
                        partes.append(atual)
                        atual = ''
                    else:
                        atual += c
                partes.append(atual)
                if len(partes) < 6:
                    continue
                tipo, posicao, api_id, titulo, poster_url, contagem = partes
                item = {
                    'posicao': int(posicao),
                    'api_id': api_id,
                    'titulo': titulo,
                    'poster_url': poster_url,
                    'contagem': int(contagem)
                }
                # Adiciona o item ao tipo correspondente
                if tipo == 'filme':
                    ranking['filmes'].append(item)
                elif tipo == 'serie':
                    ranking['series'].append(item)
                elif tipo == 'jogo':
                    ranking['jogos'].append(item)
        
        # Lê a data/hora da última atualização, se disponível
        try:
            with open('data/ultima_atualizacao.txt', 'r', encoding='utf-8') as f:
                ranking['ultima_atualizacao'] = f.read().strip()
        except:
            ranking['ultima_atualizacao'] = 'Não disponível'
        
        return ranking
        
    except Exception as e:
        print(f"Erro ao ler ranking: {e}")
        return {
            'filmes': [],
            'series': [],
            'jogos': [],
            'ultima_atualizacao': None
        }