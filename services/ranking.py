def rank_global(qtd):
    if qtd > 500:
        return ("Rank V", "Lenda do Arquivo")
    elif qtd > 250:
        return ("Rank IV", "Guardião da Memória")
    elif qtd > 100:
        return ("Rank III", "Colecionador Nostálgico")
    elif qtd > 20:
        return ("Rank II", "Sócio de Carteirinha")
    else:
        return ("Rank I", "Turista do Passado")

def rank_filmes(qtd):
    if qtd >= 301:
        return ("Rank V", "Vencedor do Oscar")
    elif qtd >= 151:
        return ("Rank IV", "Diretor Visionário")
    elif qtd >= 51:
        return ("Rank III", "Cinéfilo voraz")
    elif qtd >= 11:
        return ("Rank II", "Cliente de Locadora")
    else:
        return ("Rank I", "Espectador Casual")

def rank_series(qtd):
    if qtd >= 61:
        return ("Rank V", "Rei do Streaming")
    elif qtd >= 31:
        return ("Rank IV", "Senhor das Séries")
    elif qtd >= 16:
        return ("Rank III", "Devorador de Temporadas")
    elif qtd >= 6:
        return ("Rank II", "Maratonador de Episódios")
    else:
        return ("Rank I", "Avaliador de Pilotos")

def rank_jogos(qtd):
    if qtd >= 101:
        return ("Rank V", "God Mode")
    elif qtd >= 51:
        return ("Rank IV", "Caçador de Platinas")
    elif qtd >= 21:
        return ("Rank III", "Mestre dos Controles")
    elif qtd >= 6:
        return ("Rank II", "Leitor de Detonados")
    else:
        return ("Rank I", "Player Casual")