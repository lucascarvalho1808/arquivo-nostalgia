from routes.extensions import supabase

def calcular_estatisticas_usuario(usuario_id):
    """
    Calcula total e porcentagens de filmes/series/jogos do usuário.
    """
    try:
        # busca ids das listas do usuário
        resp = supabase.table("listas").select("id").eq("user_id", usuario_id).execute()
        listas = resp.data or []
        lista_ids = [l["id"] for l in listas]
        if not lista_ids:
            return {
                "total": 0,
                "filmes": {"quantidade": 0, "porcentagem": 0},
                "series": {"quantidade": 0, "porcentagem": 0},
                "jogos": {"quantidade": 0, "porcentagem": 0},
            }

        # buscar itens que pertençam a essas listas
        resp2 = supabase.table("itens_lista").select("tipo").in_("lista_id", lista_ids).execute()
        itens = resp2.data or []

        total = len(itens)
        count_filmes = sum(1 for i in itens if i.get("tipo") == "filme")
        count_series = sum(1 for i in itens if i.get("tipo") == "serie")
        count_jogos = sum(1 for i in itens if i.get("tipo") == "jogo")

        pct = lambda c: round((c / total) * 100) if total > 0 else 0

        return {
            "total": total,
            "filmes": {"quantidade": count_filmes, "porcentagem": pct(count_filmes)},
            "series": {"quantidade": count_series, "porcentagem": pct(count_series)},
            "jogos": {"quantidade": count_jogos, "porcentagem": pct(count_jogos)},
        }
    except Exception as e:
        print("Erro ao calcular estatísticas do usuário:", e)
        return {
            "total": 0,
            "filmes": {"quantidade": 0, "porcentagem": 0},
            "series": {"quantidade": 0, "porcentagem": 0},
            "jogos": {"quantidade": 0, "porcentagem": 0},
        }