import random
from datetime import datetime
from services.api_tmdb import buscar_filmes_populares
from services.ia_gemini import gerar_arquivo_confidencial

_cache_curiosidade = None
_data_ultima_atualizacao = None

def get_curiosidade_diaria():
    """
    Retorna a curiosidade do dia.
    Se já tiver gerado hoje, retorna a mesma.
    Se mudou o dia (ou é a primeira vez), gera uma nova.
    """
    global _cache_curiosidade, _data_ultima_atualizacao
    
    hoje = datetime.now().date()

    # Se já temos uma curiosidade e a data é de hoje, retorna a que está na memória
    if _cache_curiosidade and _data_ultima_atualizacao == hoje:
        return _cache_curiosidade

    print("Gerando nova curiosidade do dia...")

    try:
        # Busca lista de filmes populares
        filmes = buscar_filmes_populares(pagina=1)
        
        if not filmes:
            return None

        # Escolhe um filme aleatório da lista
        filme_escolhido = random.choice(filmes)
        
        # Chama o Gemini para gerar o texto
        texto_curiosidade = gerar_arquivo_confidencial(filme_escolhido['titulo'], "filme")

        # 4. Monta o objeto final
        nova_curiosidade = {
            'titulo': filme_escolhido['titulo'],
            'data_lancamento': filme_escolhido['data_lancamento'],
            'poster_url': filme_escolhido['poster_url'],
            'texto': texto_curiosidade,
            'tipo': 'filme'
        }

        # Salva no cache
        _cache_curiosidade = nova_curiosidade
        _data_ultima_atualizacao = hoje
        
        return nova_curiosidade

    except Exception as e:
        print(f"Erro ao gerar curiosidade diária: {e}")
        return None