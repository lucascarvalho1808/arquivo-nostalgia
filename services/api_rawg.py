import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

RAWG_API_KEY = os.environ.get('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"

def _extrair_steam_id(stores):
    """
    Tenta encontrar o ID da Steam dentro da lista de lojas da RAWG.
    """
    if not stores:
        return None
        
    for loja_item in stores:
        store_info = loja_item.get('store', {})
        if store_info.get('slug') == 'steam':
            url_loja = loja_item.get('url', '') or loja_item.get('url_en', '')
            
            match = re.search(r'/app/(\d+)', str(url_loja))
            if match:
                return match.group(1)
    return None

def _gerar_capa_steam(steam_id):
    """
    Gera a URL da capa vertical (library_600x900) da Steam sem precisar chamar a API.
    """
    if not steam_id:
        return None
    return f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{steam_id}/library_600x900.jpg"

def _buscar_dados_steam_detalhes(app_id):
    """
    Busca dados ricos (Preço, PT-BR, Requisitos) na API pública da Steam.
    """
    url_steam = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=brazilian"
    try:
        response = requests.get(url_steam, timeout=3) # Timeout curto para não travar
        dados = response.json()
        
        if dados and str(app_id) in dados and dados[str(app_id)]['success']:
            return dados[str(app_id)]['data']
    except Exception as e:
        print(f"Erro ao conectar na Steam: {e}")
    
    return None

def _formatar_jogos_lista(resultados):
    """
    Formata a lista de jogos, tentando substituir a imagem da RAWG pela capa da Steam.
    """
    jogos_formatados = []
    for jogo in resultados:
        # Tenta achar o ID da Steam
        steam_id = _extrair_steam_id(jogo.get('stores', []))
        
        # Se tiver Steam ID, usa a capa vertical da Steam. Se não, usa o wallpaper da RAWG.
        poster = _gerar_capa_steam(steam_id)
        if not poster:
            poster = jogo.get('background_image')

        jogos_formatados.append({
            'id': jogo['id'],
            'titulo': jogo['name'],
            'slug': jogo.get('slug'),
            'poster_url': poster, # Aqui vai a capa da Steam se existir
            'nota': jogo.get('metacritic'),
            'tipo': 'game'
        })
    return jogos_formatados

def buscar_jogos_populares(pagina=1, page_size=12):
    """
    Busca jogos populares e tenta usar capas da Steam.
    """
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

def buscar_detalhes_jogo(game_id_ou_slug):
    """
    Busca detalhada HÍBRIDA: RAWG + Steam (se disponível).
    """
    # 1. Busca na RAWG
    url_rawg = f"{BASE_URL}/games/{game_id_ou_slug}?key={RAWG_API_KEY}"
    
    try:
        response = requests.get(url_rawg)
        dados_rawg = response.json()
        
        # 2. Prepara objeto base com dados da RAWG
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

        # 3. Tenta colcoar dados da Steam
        steam_id = _extrair_steam_id(dados_rawg.get('stores', []))
        
        if steam_id:
            # Tenta usar a capa vertical da Steam também nos detalhes
            capa_steam = _gerar_capa_steam(steam_id)
            if capa_steam:
                jogo_final['poster_url'] = capa_steam

            # Busca dados extras (Preço, Requisitos)
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

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes do jogo {game_id_ou_slug}: {e}")
        return None

# Testes comentados para evitar chamadas desnecessárias na API durante o desenvolvimento
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