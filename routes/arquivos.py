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
from services.estatisticas_usuario import calcular_estatisticas_usuario

arquivos_bp = Blueprint('arquivos', __name__, url_prefix='/arquivos')


@arquivos_bp.route('/')
@arquivos_bp.route('/meus-arquivos')
@login_required
def meus_arquivos():
    """
    Página principal com todas as listas (pastas) do usuário.
    Inclui o ranking da comunidade lido do CSV e estatísticas pessoais.
    """
    try:
        # Busca todas as listas do usuário logado
        listas = obter_listas_usuario(current_user.id)
        
        # Lê o ranking do CSV 
        ranking = ler_ranking_comunidade()
        
        # Calcula estatísticas pessoais do usuário
        estatisticas = calcular_estatisticas_usuario(current_user.id)
        
        return render_template(
            'meus_arquivos.html',
            listas=listas,
            ranking=ranking,
            estatisticas=estatisticas
        )
    except Exception as e:
        print(f"Erro ao carregar meus arquivos: {e}")
        return render_template(
            'meus_arquivos.html', 
            listas=[],
            ranking={'filmes': [], 'series': [], 'jogos': []},
            estatisticas={'total': 0, 'filmes': {'quantidade': 0, 'porcentagem': 0}, 'series': {'quantidade': 0, 'porcentagem': 0}, 'jogos': {'quantidade': 0, 'porcentagem': 0}}
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