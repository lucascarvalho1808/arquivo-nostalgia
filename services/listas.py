import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def adicionar_item_lista(lista_id, api_id, tipo, titulo, poster_url):
    """
    Adiciona um item (filme/série/jogo) a uma lista específica.
    
    Args:
        lista_id (str): UUID da lista onde o item será adicionado
        api_id (str): ID do item na API externa (TMDB ou RAWG)
        tipo (str): Tipo do conteúdo ('filme', 'serie' ou 'jogo')
        titulo (str): Título do filme/série/jogo
        poster_url (str): URL da imagem do poster
    
    Returns:
        dict: Dados do item adicionado ou None em caso de erro
    
    Exemplo de uso:
         adicionar_item_lista(
             lista_id="uuid-da-lista",
             api_id="550",
             tipo="filme",
             titulo="Clube da Luta",
             poster_url="https://image.tmdb.org/t/p/w300/poster.jpg"
         )
    """
    try:
        # Valida o tipo
        if tipo not in ['filme', 'serie', 'jogo']:
            print(f"Erro: Tipo inválido '{tipo}'. Use 'filme', 'serie' ou 'jogo'.")
            return None
        
        # Dados do item a ser inserido
        dados_item = {
            "lista_id": lista_id,
            "api_id": str(api_id),
            "tipo": tipo,
            "titulo": titulo,
            "poster_url": poster_url
        }
        
        # Insere o item na tabela itens_lista
        response = supabase.table("itens_lista").insert(dados_item).execute()
        
        print(f"Item '{titulo}' adicionado à lista com sucesso!")
        return response.data[0] if response.data else None
        
    except Exception as e:
        # Verifica se é erro de duplicata (item já existe na lista)
        if "duplicate key" in str(e).lower() or "unique" in str(e).lower():
            print(f"Item '{titulo}' já existe nesta lista.")
            return {"erro": "duplicado", "mensagem": "Este item já está na lista."}
        
        print(f"Erro ao adicionar item à lista: {e}")
        return None


def remover_item_lista(item_id):
    """
    Remove um item de uma lista.
    
    Args:
        item_id (str): UUID do item a ser removido
    
    Returns:
        bool: True se removido com sucesso, False caso contrário
    """
    try:
        response = supabase.table("itens_lista").delete().eq("id", item_id).execute()
        
        if response.data:
            print(f"Item removido da lista com sucesso!")
            return True
        else:
            print(f"Item não encontrado.")
            return False
            
    except Exception as e:
        print(f"Erro ao remover item da lista: {e}")
        return False


def buscar_itens_lista(lista_id):
    """
    Busca todos os itens de uma lista específica.
    
    Args:
        lista_id (str): UUID da lista
    
    Returns:
        list: Lista de itens ou lista vazia em caso de erro
    """
    try:
        response = supabase.table("itens_lista")\
            .select("*")\
            .eq("lista_id", lista_id)\
            .order("adicionado_em", desc=True)\
            .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Erro ao buscar itens da lista: {e}")
        return []


def verificar_item_na_lista(lista_id, api_id, tipo):
    """
    Verifica se um item já existe em uma lista específica.
    
    Args:
        lista_id (str): UUID da lista
        api_id (str): ID do item na API externa
        tipo (str): Tipo do conteúdo ('filme', 'serie' ou 'jogo')
    
    Returns:
        bool: True se o item já existe, False caso contrário
    """
    try:
        response = supabase.table("itens_lista")\
            .select("id")\
            .eq("lista_id", lista_id)\
            .eq("api_id", str(api_id))\
            .eq("tipo", tipo)\
            .execute()
        
        return len(response.data) > 0 if response.data else False
        
    except Exception as e:
        print(f"Erro ao verificar item na lista: {e}")
        return False