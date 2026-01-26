import os
from dotenv import load_dotenv
import requests
from flask import session
from routes.extensions import supabase

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Cores pré-definidas disponíveis para as listas
CORES_DISPONIVEIS = [
    '#6366f1',  # Indigo (padrão)
    '#f06292',  # Pink
    '#2d3436',  # black
    '#636e72',  # gray
    '#dfe6e9',  # white
    '#82ccdd',  # blue-light
    '#218c53',  # green-dark
    '#b8e994',  # green-light
    '#f1c40f',  # yellow
    '#e67e22',  # orange
    '#e74c3c',  # red
    '#8d6e63',  # brown
    '#9b59b6',  # purple
]

# Mapeamento de cores hexadecimais para classes CSS
MAPEAMENTO_CORES = {
    '#6366f1': 'indigo',
    '#f06292': 'pink',
    '#2d3436': 'black',
    '#636e72': 'gray',
    '#dfe6e9': 'white',
    '#82ccdd': 'blue-light',
    '#218c53': 'green-dark',
    '#b8e994': 'green-light',
    '#f1c40f': 'yellow',
    '#e67e22': 'orange',
    '#e74c3c': 'red',
    '#8d6e63': 'brown',
    '#9b59b6': 'purple'
}


def _get_supabase_client():
    """
    Retorna o client Supabase configurado em routes.extensions (cliente do servidor).
    """
    try:
        return supabase
    except Exception as e:
        print("Erro ao obter client Supabase:", e)
        return None


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

        # Usa o cliente com o token do usuário
        client = _get_supabase_client()

        # Insere o item na tabela itens_lista
        response = client.table("itens_lista").insert(dados_item).execute()

        print(f"Item '{titulo}' adicionado à lista com sucesso!")
        return response.data[0] if response.data else None

    except Exception as e:
        # Verifica se é erro de duplicata (item já existe na lista)
        if "duplicate key" in str(e).lower() or "unique" in str(e).lower():
            print(f"Item '{titulo}' já existe nesta lista.")
            return {"erro": "duplicado", "mensagem": "Este item já está na lista."}

        print(f"Erro ao adicionar item à lista: {e}")
        return None


def remover_item_lista(item_id, usuario_id):
    """
    Remove um item de uma lista.

    Args:
        item_id (str): UUID do item a ser removido

    Returns:
        bool: True se removido com sucesso, False caso contrário
    """
    try:
        client = _get_supabase_client()
        response = client.table("itens_lista").delete().eq("id", item_id).execute()

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
        client = _get_supabase_client()
        response = client.table("itens_lista")\
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
        client = _get_supabase_client()
        response = client.table("itens_lista")\
            .select("id")\
            .eq("lista_id", lista_id)\
            .eq("api_id", str(api_id))\
            .eq("tipo", tipo)\
            .execute()

        return len(response.data) > 0 if response.data else False

    except Exception as e:
        print(f"Erro ao verificar item na lista: {e}")
        return False


def criar_lista(usuario_id, nome, descricao, cor):
    """
    Cria uma nova lista usando o access_token do usuário (session['supabase_access_token']).
    Retorna o objeto criado ou None.
    """
    try:
        token = session.get('supabase_access_token')
        if not token:
            print("Token do Supabase não encontrado na sessão. Salve o token no login.")
            return None

        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/listas"
        headers = {
            "Content-Type": "application/json",
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
            "Prefer": "return=representation"
        }
        payload = {
            "user_id": usuario_id,
            "nome_lista": nome,
            "descricao": descricao,
            "cor": cor
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code in (200, 201):
            data = resp.json()
            return data[0] if isinstance(data, list) and data else data
        else:
            print("Erro ao criar lista (Supabase REST):", resp.status_code, resp.text)
            return None

    except Exception as e:
        print("Erro detalhado ao criar lista:", e)
        import traceback
        traceback.print_exc()
        return None


def atualizar_lista(lista_id, nome=None, descricao=None, cor=None):
    """
    Atualiza campos de uma lista (nome_lista, descricao, cor).
    Retorna o registro atualizado ou None em caso de erro.
    """
    try:
        token = session.get('supabase_access_token')
        if not token:
            print("Token do Supabase não encontrado na sessão.")
            return None

        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/listas?id=eq.{lista_id}"
        headers = {
            "Content-Type": "application/json",
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
            "Prefer": "return=representation"
        }

        payload = {}
        if nome is not None:
            payload["nome_lista"] = nome
        if descricao is not None:
            payload["descricao"] = descricao
        if cor is not None:
            payload["cor"] = cor

        if not payload:
            return None

        resp = requests.patch(url, headers=headers, json=payload, timeout=10)
        if resp.status_code in (200, 201):
            data = resp.json()
            return data[0] if isinstance(data, list) and data else data
        else:
            print("Erro ao atualizar lista (Supabase REST):", resp.status_code, resp.text)
            return None

    except Exception as e:
        print("Erro ao atualizar lista:", e)
        import traceback
        traceback.print_exc()
        return None


def obter_cores_disponiveis():
    """
    Retorna a lista de cores disponíveis para personalização.

    Returns:
        list: Lista de códigos hexadecimais das cores disponíveis
    """
    return CORES_DISPONIVEIS.copy()


def obter_listas_usuario(usuario_id):
    """
    Busca todas as listas do usuário autenticado, normalizando campos para o template.

    Args:
        usuario_id (str): ID do usuário

    Returns:
        list: Listas do usuário com campos de cor e nome normalizados
    """
    try:
        response = supabase.table("listas").select("*").eq("user_id", usuario_id).execute()
        listas = response.data or []
        for l in listas:
            # normaliza cor e garante campo para o template
            cor = (l.get("cor") or "#6366f1").strip().lower()
            l["cor"] = cor
            l["cor_classe"] = MAPEAMENTO_CORES.get(cor, "")
            # mantém compatibilidade com templates que usam 'nome'
            l["nome"] = l.get("nome_lista") or l.get("nome")
        return listas
    except Exception as e:
        print("Erro ao buscar listas do usuário:", e)
        return []


def obter_lista_por_id(lista_id):
    """
    Busca uma lista específica pelo ID, normalizando campos para o template.

    Args:
        lista_id (str): UUID da lista

    Returns:
        dict: Dados da lista ou None em caso de erro
    """
    try:
        response = supabase.table("listas").select("*").eq("id", lista_id).single().execute()
        lista = response.data
        if lista:
            cor = (lista.get("cor") or "#6366f1").strip().lower()
            lista["cor"] = cor
            lista["cor_classe"] = MAPEAMENTO_CORES.get(cor, "")
            lista["nome"] = lista.get("nome_lista") or lista.get("nome")
        return lista
    except Exception as e:
        print("Erro ao buscar lista por ID:", e)
        return None


def obter_itens_lista(lista_id):
    """
    Busca todos os itens de uma lista específica para uso em templates.

    Args:
        lista_id (str): UUID da lista

    Returns:
        list: Lista de itens com campos normalizados
    """
    try:
        response = supabase.table("itens_lista").select("*").eq("lista_id", lista_id).execute()
        itens = response.data or []
        # garantir chaves usadas no template
        for it in itens:
            it["titulo"] = it.get("titulo")
        return itens
    except Exception as e:
        print("Erro ao buscar itens da lista:", e)
        return []


def deletar_lista(lista_id):
    """
    Deleta uma lista pelo ID (usa token do usuário salvo na sessão).
    Retorna True se deletado com sucesso, False caso contrário.
    """
    try:
        token = session.get('supabase_access_token')
        if not token:
            print("Token do Supabase não encontrado na sessão.")
            return False

        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/listas?id=eq.{lista_id}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
            "Prefer": "return=representation"
        }

        resp = requests.delete(url, headers=headers, timeout=10)
        if resp.status_code in (200, 204):
            return True

        print("Erro ao deletar lista (Supabase REST):", resp.status_code, resp.text)
        return False

    except Exception as e:
        print("Erro ao deletar lista:", e)
        import traceback
        traceback.print_exc()
        return False


# Função auxiliar para testes (opcional)
if __name__ == "__main__":
    # Exemplo de teste (quando suas tabelas estiverem prontas)
    print("Módulo de gerenciamento de listas carregado!")
    print("Funções disponíveis:")
    print("  - adicionar_item_lista()")
    print("  - remover_item_lista()")
    print("  - buscar_itens_lista()")
    print("  - verificar_item_na_lista()")
    print("  - criar_lista()")