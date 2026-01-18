import requests
import re

def buscar_app_id_steam(nome_jogo):
    """
    Busca o App ID de um jogo na Steam através da store search.
    
    Args:
        nome_jogo (str): Nome do jogo
    
    Returns:
        int: App ID do jogo ou None
    """
    try:
        url = "https://store.steampowered.com/api/storesearch/"
        
        params = {
            'term': nome_jogo,
            'l': 'brazilian',
            'cc': 'BR'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            print(f"❌ Jogo não encontrado na Steam: {nome_jogo}")
            return None
        
        primeiro_resultado = items[0]
        app_id = primeiro_resultado.get('id')
        nome_encontrado = primeiro_resultado.get('name')
        
        print(f"✅ Jogo encontrado na Steam: {nome_encontrado} (ID: {app_id})")
        return app_id
        
    except Exception as e:
        print(f"⚠️ Erro ao buscar App ID na Steam: {e}")
        return None


def buscar_trailer_steam(app_id):
    """
    Busca o trailer de um jogo na Steam pelo App ID.
    
    Args:
        app_id (int): App ID do jogo na Steam
    
    Returns:
        str: URL da página do jogo na Steam com foco no vídeo
    """
    try:
        url = f"https://store.steampowered.com/api/appdetails"
        
        params = {
            'appids': app_id,
            'l': 'brazilian'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get(str(app_id), {}).get('success'):
            print(f"❌ App ID {app_id} não retornou dados válidos")
            return None
        
        game_data = data[str(app_id)]['data']
        movies = game_data.get('movies', [])
        
        if not movies:
            print(f"❌ Nenhum trailer encontrado para App ID {app_id}")
            return None
        
        primeiro_trailer = movies[0]
        nome_trailer = primeiro_trailer.get('name', 'Trailer')
        
        print(f"🎬 Trailer encontrado: {nome_trailer}")
        
        steam_page_url = f"https://store.steampowered.com/app/{app_id}#app_videos"
        
        print(f"✅ URL com foco em vídeos: {steam_page_url}")
        return steam_page_url
        
    except Exception as e:
        print(f"⚠️ Erro ao buscar trailer na Steam: {e}")
        return None


def obter_trailer_steam(nome_jogo):
    """
    Função principal que busca o App ID e retorna a URL da Steam.
    
    Args:
        nome_jogo (str): Nome do jogo
    
    Returns:
        str: URL da página do jogo na Steam
    """
    print(f"🔍 Iniciando busca na Steam para: {nome_jogo}")
    
    app_id = buscar_app_id_steam(nome_jogo)
    
    if not app_id:
        return None
    
    trailer_url = buscar_trailer_steam(app_id)
    
    return trailer_url


# Teste
if __name__ == "__main__":
    testes = [
        "Red Dead Redemption 2",
        "The Witcher 3",
        "Portal 2",
        "Cyberpunk 2077"
    ]
    
    for jogo in testes:
        print(f"\n{'='*60}")
        print(f"🎮 TESTANDO: {jogo}")
        print(f"{'='*60}")
        url = obter_trailer_steam(jogo)
        print(f"✅ RESULTADO: {url if url else 'Não encontrado'}")
        print()