from .api_tmdb import (
    buscar_filmes_populares, 
    buscar_series_populares, 
    pesquisar_midia, 
    buscar_detalhes_filme
)

from .api_rawg import (
   buscar_jogos_populares,
    pesquisar_jogos,
    buscar_detalhes_jogo,
    buscar_catalogo_jogos,
    buscar_jogos_por_genero
)

from .ia_gemini import gerar_arquivo_confidencial
from .api_steam import obter_trailer_steam  # ← NOVO

from .listas import (
    criar_lista,
    adicionar_item_lista,
    remover_item_lista,
    buscar_itens_lista,
    verificar_item_na_lista,
    obter_cores_disponiveis,
    CORES_DISPONIVEIS
)