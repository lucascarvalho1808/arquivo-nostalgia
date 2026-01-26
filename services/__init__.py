# Importa funções e constantes dos serviços de integração com APIs externas e utilitários do projeto

# Funções relacionadas à API TMDB (filmes e séries)
from .api_tmdb import (
    buscar_filmes_populares, 
    buscar_series_populares, 
    pesquisar_midia, 
    buscar_detalhes_filme
)

# Funções relacionadas à API RAWG (jogos)
from .api_rawg import (
    buscar_jogos_populares,
    pesquisar_jogos,
    buscar_detalhes_jogo,
    buscar_catalogo_jogos,
    buscar_jogos_por_genero
)

# Função para geração de arquivo confidencial via IA 
from .ia_gemini import gerar_arquivo_confidencial

# Função para obter trailer de jogos na Steam
from .api_steam import obter_trailer_steam  

# Funções utilitárias e de manipulação de listas do usuário
from .listas import (
    criar_lista,
    adicionar_item_lista,
    remover_item_lista,
    buscar_itens_lista,
    verificar_item_na_lista,
    obter_cores_disponiveis,
    CORES_DISPONIVEIS
)