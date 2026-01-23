import csv
import os
from datetime import datetime
from routes.extensions import supabase

def gerar_ranking_comunidade():
    """
    Gera o ranking dos itens mais salvos pela comunidade
    e persiste em CSV usando Python
    """
    try:
        # 1. Buscar todos os itens salvos no Supabase
        response = supabase.table('itens_lista').select('*').execute()
        itens = response.data
        print("Itens retornados:", itens)
        # 2. Contar ocorrências por tipo e api_id
        contadores = {
            'filme': {},
            'serie': {},
            'jogo': {}
        }
        
        for item in itens:
            tipo = (item.get("tipo") or "").strip().lower() 
            api_id = item.get("api_id")
            titulo = item.get("titulo")
            poster_url = item.get("poster_url")
            print(f"DEBUG: tipo={repr(tipo)}, api_id={api_id}")
            if tipo in contadores and api_id:
                if api_id not in contadores[tipo]:
                    contadores[tipo][api_id] = {
                        "contagem": 0,
                        "titulo": titulo,
                        "poster_url": poster_url,
                    }
                contadores[tipo][api_id]["contagem"] += 1
        
        print("Contadores:", contadores)
        
        # 3. Pegar Top 3 de cada categoria
        top_filmes = sorted(contadores['filme'].items(), 
                           key=lambda x: x[1]['contagem'], 
                           reverse=True)[:3]
        top_series = sorted(contadores['serie'].items(), 
                           key=lambda x: x[1]['contagem'], 
                           reverse=True)[:3]
        top_jogos = sorted(contadores['jogo'].items(), 
                          key=lambda x: x[1]['contagem'], 
                          reverse=True)[:3]
        
        # 4. Criar diretório data se não existir
        os.makedirs('data', exist_ok=True)
        
        # 5. Escrever no CSV usando Python puro (módulo csv nativo)
        caminho_csv = 'data/ranking_comunidade.csv'
        
        with open(caminho_csv, 'w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            
            # Cabeçalho
            escritor.writerow(['tipo', 'posicao', 'api_id', 'titulo', 'poster_url', 'contagem'])
            
            # Filmes
            for idx, (api_id, dados) in enumerate(top_filmes, 1):
                escritor.writerow([
                    'filme',
                    idx,
                    api_id,
                    dados['titulo'],
                    dados['poster_url'],
                    dados['contagem']
                ])
            
            # Séries
            for idx, (api_id, dados) in enumerate(top_series, 1):
                escritor.writerow([
                    'serie',
                    idx,
                    api_id,
                    dados['titulo'],
                    dados['poster_url'],
                    dados['contagem']
                ])
            
            # Jogos
            for idx, (api_id, dados) in enumerate(top_jogos, 1):
                escritor.writerow([
                    'jogo',
                    idx,
                    api_id,
                    dados['titulo'],
                    dados['poster_url'],
                    dados['contagem']
                ])
        
        # 6. Registrar última atualização
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
    Usa módulo csv nativo.
    """
    try:
        caminho_csv = 'data/ranking_comunidade.csv'
        
        if not os.path.exists(caminho_csv):
            print("Arquivo CSV não encontrado. O arquivo será gerado.")
            gerar_ranking_comunidade()
        
        ranking = {
            'filmes': [],
            'series': [],
            'jogos': [],
            'ultima_atualizacao': None
        }
        
        # Ler CSV com Python 
        with open(caminho_csv, 'r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            
            for linha in leitor:
                item = {
                    'posicao': int(linha['posicao']),
                    'api_id': linha['api_id'],
                    'titulo': linha['titulo'],
                    'poster_url': linha['poster_url'],
                    'contagem': int(linha['contagem'])
                }
                
                if linha['tipo'] == 'filme':
                    ranking['filmes'].append(item)
                elif linha['tipo'] == 'serie':
                    ranking['series'].append(item)
                elif linha['tipo'] == 'jogo':
                    ranking['jogos'].append(item)
        
        # Ler última atualização
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