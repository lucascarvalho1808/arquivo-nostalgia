def rank_global(qtd):
    if qtd >= 500:
        return ("Lenda do Arquivo", "t-diamante")
    elif qtd >= 250:
        return ("Guardião da Memória", "t-rubi")
    elif qtd >= 100:
        return ("Colecionador Nostálgico", "t-ouro")
    elif qtd >= 20:
        return ("Sócio de Carteirinha", "t-prata")
    else:
        return ("Turista do Passado", "t-bronze")

def rank_filmes(qtd):
    if qtd >= 301:
        return ("Vencedor do Oscar", "t-diamante", "sombra-diamante")
    elif qtd >= 151:
        return ("Diretor Visionário", "t-rubi", "sombra-rubi")
    elif qtd >= 51:
        return ("Cinéfilo voraz", "t-ouro", "sombra-ouro")
    elif qtd >= 11:
        return ("Cliente de Locadora", "t-prata", "sombra-prata")
    else:
        return ("Espectador Casual", "t-bronze", "sombra-bronze")

def rank_series(qtd):
    if qtd >= 61:
        return ("Rei do Streaming", "t-diamante", "sombra-diamante")
    elif qtd >= 31:
        return ("Senhor das Séries", "t-rubi", "sombra-rubi")
    elif qtd >= 16:
        return ("Devorador de Temporadas", "t-ouro", "sombra-ouro")
    elif qtd >= 6:
        return ("Maratonador de Episódios", "t-prata", "sombra-prata")
    else:
        return ("Avaliador de Pilotos", "t-bronze", "sombra-bronze")

def rank_jogos(qtd):
    if qtd >= 101:
        return ("God Mode", "t-diamante", "sombra-diamante")
    elif qtd >= 51:
        return ("Caçador de Platinas", "t-rubi", "sombra-rubi")
    elif qtd >= 21:
        return ("Mestre dos Controles", "t-ouro", "sombra-ouro")
    elif qtd >= 6:
        return ("Leitor de Detonados", "t-prata", "sombra-prata")
    else:
        return ("Player Casual", "t-bronze", "sombra-bronze")