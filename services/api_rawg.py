import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

RAWG_API_KEY = os.environ.get('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"

_steam_id_cache = {}

def _buscar_id_steam_por_nome(nome_jogo):
    """
    Busca o AppID da Steam usando o nome do jogo na API de busca da Steam.
    """
    # Verifica cache primeiro
    if nome_jogo in _steam_id_cache:
        return _steam_id_cache[nome_jogo]

    try:
        # API de busca da Steam 
        url = f"https://store.steampowered.com/api/storesearch/?term={nome_jogo}&l=english&cc=US"
        response = requests.get(url, timeout=1) # Timeout curto
        data = response.json()
        
        if data and data.get('total') > 0:
            items = data.get('items', [])
            if items:
                # Pega o primeiro resultado
                steam_id = str(items[0]['id'])
                _steam_id_cache[nome_jogo] = steam_id
                return steam_id
    except:
        pass # Se falhar, usa a capa da RAWG
    
    return None

def _extrair_steam_id(stores, nome_jogo):
    """
    Tenta encontrar o ID da Steam.
    1. Tenta pela URL da RAWG (se disponível).
    2. Se tiver loja Steam mas sem URL, busca pelo nome na Steam.
    """
    tem_steam = False
    
    if stores:
        for loja_item in stores:
            store_info = loja_item.get('store', {})
            if store_info.get('slug') == 'steam':
                tem_steam = True
                # Tenta pegar URL direta se existir
                url_loja = loja_item.get('url', '') or loja_item.get('url_en', '')
                match = re.search(r'/app/(\d+)', str(url_loja))
                if match:
                    return match.group(1)
                break
    
    
    if tem_steam and nome_jogo:
        return _buscar_id_steam_por_nome(nome_jogo)
        
    return None

def _gerar_capa_steam(steam_id):
    """Gera a URL da capa vertical da Steam."""
    if not steam_id:
        return None
    return f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{steam_id}/library_600x900.jpg"

def _buscar_dados_steam_detalhes(app_id):
    """Busca dados ricos na API pública da Steam."""
    url_steam = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=brazilian"
    try:
        response = requests.get(url_steam, timeout=3)
        dados = response.json()
        if dados and str(app_id) in dados and dados[str(app_id)]['success']:
            return dados[str(app_id)]['data']
    except Exception as e:
        print(f"Erro ao conectar na Steam: {e}")
    return None

def _formatar_jogos_lista(resultados):
    """Formata a lista. Define se usa estilo Steam ou RAWG."""
    jogos_formatados = []
    for jogo in resultados:
        # 1. Tenta achar ID e Capa Steam
        steam_id = _extrair_steam_id(jogo.get('stores', []), jogo.get('name'))
        capa_steam = _gerar_capa_steam(steam_id)
        
        # 2. Define a imagem principal e o estilo
        if capa_steam:
            poster_principal = capa_steam
            origem = 'steam' # Estilo Limpo (Só imagem)
        else:
            poster_principal = jogo.get('background_image')
            origem = 'rawg'  # Estilo Card (Com título)

        jogos_formatados.append({
            'id': jogo['id'],
            'titulo': jogo['name'],
            'slug': jogo.get('slug'),
            'poster_url': poster_principal,
            'imagem_rawg': jogo.get('background_image'), 
            'origem_imagem': origem, # Para o HTML saber qual layout usar
            'nota': jogo.get('metacritic'),
            'tipo': 'game'
        })
    return jogos_formatados

def buscar_jogos_populares(pagina=1, page_size=25):
    """Busca jogos populares."""
    endpoint = f"{BASE_URL}/games"
    params = {
        'key': RAWG_API_KEY,
        'ordering': '-added',
        'page_size': page_size,
        'page': pagina
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_jogos_lista(response.json().get('results', []))

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos na RAWG: {e}")
        return []

def pesquisar_jogos(query):
    """Pesquisa jogos por nome."""
    endpoint = f"{BASE_URL}/games"
    params = {
        'key': RAWG_API_KEY,
        'search': query,
        'page_size': 12
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_jogos_lista(response.json().get('results', []))

    except requests.exceptions.RequestException as e:
        print(f"Erro ao pesquisar jogos: {e}")
        return []

def buscar_detalhes_jogo(game_id_ou_slug):
    """Busca detalhada HÍBRIDA."""
    url_rawg = f"{BASE_URL}/games/{game_id_ou_slug}?key={RAWG_API_KEY}"
    
    try:
        response = requests.get(url_rawg)
        dados_rawg = response.json()
        
        descricao_limpa = re.sub('<[^<]+?>', '', dados_rawg.get('description', ''))
        
        jogo_final = {
            'id': dados_rawg['id'],
            'titulo': dados_rawg['name'],
            'sinopse': descricao_limpa,
            'data_lancamento': dados_rawg.get('released'),
            'poster_url': dados_rawg.get('background_image'),
            'nota': dados_rawg.get('metacritic'),
            'generos': [g['name'] for g in dados_rawg.get('genres', [])],
            'plataformas': [p['platform']['name'] for p in dados_rawg.get('platforms', [])],
            'preco': 'Não informado',
            'requisitos': None,
            'tipo': 'game'
        }

        steam_id = _extrair_steam_id(dados_rawg.get('stores', []), dados_rawg.get('name'))
        
        if steam_id:
            capa_steam = _gerar_capa_steam(steam_id)
            if capa_steam:
                jogo_final['poster_url'] = capa_steam

            dados_steam = _buscar_dados_steam_detalhes(steam_id)
            if dados_steam:
                if 'short_description' in dados_steam:
                    jogo_final['sinopse'] = dados_steam['short_description']
                if 'price_overview' in dados_steam:
                    jogo_final['preco'] = dados_steam['price_overview'].get('final_formatted', 'Grátis')
                elif dados_steam.get('is_free'):
                    jogo_final['preco'] = 'Gratuito'
                if 'pc_requirements' in dados_steam and 'minimum' in dados_steam['pc_requirements']:
                    jogo_final['requisitos'] = dados_steam['pc_requirements']['minimum']
            
        return jogo_final

    except Exception as e:
        print(f"Erro ao buscar detalhes do jogo {game_id_ou_slug}: {e}")
        return None

# Testes
if __name__ == "__main__":
    print("--- Testando Jogos Populares ---")
    jogos = buscar_jogos_populares()
    if jogos:
        print(f"Jogo mais popular: {jogos[0]['titulo']} (Nota: {jogos[0]['nota']})")
        print(f"Imagem: {jogos[0]['poster_url']}")
    else:
        print("Nenhum jogo encontrado.")

    print("\n--- Testando Pesquisa (Mario) ---")
    busca = pesquisar_jogos("Mario")
    if busca:
        print(f"Primeiro resultado: {busca[0]['titulo']}")