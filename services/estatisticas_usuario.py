from routes.extensions import supabase

def calcular_estatisticas_usuario(usuario_id):
    """
    Calcula as estatísticas pessoais do usuário:
    - Total de itens salvos
    - Porcentagem de Filmes, Séries e Jogos
    
    Retorna um dicionário com os dados.
    """
    try:
        # Busca todos os itens do usuário
        response = supabase.table('itens_lista').select('tipo').eq('usuario_id', usuario_id).execute()
        itens = response.data
        
        if not itens:
            return {
                'total': 0,
                'filmes': {'quantidade': 0, 'porcentagem': 0},
                'series': {'quantidade': 0, 'porcentagem': 0},
                'jogos': {'quantidade': 0, 'porcentagem': 0}
            }
        
        # Conta por tipo
        total = len(itens)
        count_filmes = sum(1 for item in itens if item.get('tipo') == 'filme')
        count_series = sum(1 for item in itens if item.get('tipo') == 'serie')
        count_jogos = sum(1 for item in itens if item.get('tipo') == 'jogo')
        
        # Calcula porcentagens
        porc_filmes = round((count_filmes / total) * 100) if total > 0 else 0
        porc_series = round((count_series / total) * 100) if total > 0 else 0
        porc_jogos = round((count_jogos / total) * 100) if total > 0 else 0
        
        return {
            'total': total,
            'filmes': {
                'quantidade': count_filmes,
                'porcentagem': porc_filmes
            },
            'series': {
                'quantidade': count_series,
                'porcentagem': porc_series
            },
            'jogos': {
                'quantidade': count_jogos,
                'porcentagem': porc_jogos
            }
        }
        
    except Exception as e:
        print(f"Erro ao calcular estatísticas do usuário: {e}")
        return {
            'total': 0,
            'filmes': {'quantidade': 0, 'porcentagem': 0},
            'series': {'quantidade': 0, 'porcentagem': 0},
            'jogos': {'quantidade': 0, 'porcentagem': 0}
        }