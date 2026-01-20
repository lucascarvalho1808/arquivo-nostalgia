from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.listas import (
    obter_listas_usuario,
    obter_lista_por_id,
    criar_lista,
    atualizar_lista,
    deletar_lista
)
from services.ranking_csv import ler_ranking_comunidade

arquivos_bp = Blueprint('arquivos', __name__, url_prefix='/arquivos')


@arquivos_bp.route('/')
@arquivos_bp.route('/meus-arquivos')
@login_required
def meus_arquivos():
    """
    Página principal com todas as listas (pastas) do usuário.
    Inclui o ranking da comunidade lido do CSV.
    """
    try:
        # Busca todas as listas do usuário logado
        listas = obter_listas_usuario(current_user.id)
        
        # Lê o ranking do CSV 
        ranking = ler_ranking_comunidade()
        
        return render_template(
            'meus_arquivos.html',
            listas=listas,
            ranking=ranking
        )
    except Exception as e:
        print(f"Erro ao carregar meus arquivos: {e}")
        return render_template(
            'meus_arquivos.html', 
            listas=[],
            ranking={'filmes': [], 'series': [], 'jogos': []}
        )


@arquivos_bp.route('/arquivo/<lista_id>')
@login_required
def visualizar_arquivo(lista_id):
    """
    Página de visualização de um arquivo específico (dentro da pasta).
    """
    try:
        # Busca a lista específica
        lista = obter_lista_por_id(lista_id)
        
        if not lista:
            return "Lista não encontrada", 404
        
        # Verifica se a lista pertence ao usuário logado
        if lista.get('usuario_id') != current_user.id:
            return "Acesso negado", 403
        
        return render_template(
            'base_arquivo.html',
            lista=lista
        )
    except Exception as e:
        print(f"Erro ao visualizar arquivo: {e}")
        return "Erro ao carregar arquivo", 500