from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from services.listas import (
    obter_listas_usuario,
    obter_lista_por_id,
    criar_lista,
    atualizar_lista,
    deletar_lista,
    CORES_DISPONIVEIS
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
            estatisticas=estatisticas,
            cores_disponiveis=CORES_DISPONIVEIS
        )
    except Exception as e:
        print(f"Erro ao carregar meus arquivos: {e}")
        return render_template(
            'meus_arquivos.html', 
            listas=[],
            ranking={'filmes': [], 'series': [], 'jogos': []},
            estatisticas={'total': 0, 'filmes': {'quantidade': 0, 'porcentagem': 0}, 'series': {'quantidade': 0, 'porcentagem': 0}, 'jogos': {'quantidade': 0, 'porcentagem': 0}},
            cores_disponiveis=CORES_DISPONIVEIS
        )


@arquivos_bp.route('/criar-pasta', methods=['POST'])
@login_required
def criar_pasta():
    """
    Cria uma nova pasta (lista) para o usuário.
    """
    try:
        data = request.get_json()
        
        print(f"🔍 Dados recebidos do frontend: {data}")
        print(f"🔍 Usuário atual: {current_user.id}")
        
        nome = data.get('nome', '').strip()
        descricao = data.get('descricao', '').strip()
        cor = data.get('cor', '#6366f1')
        
        print(f"🔍 Nome: {nome}")
        print(f"🔍 Descrição: {descricao}")
        print(f"🔍 Cor: {cor}")
        
        # Validações
        if not nome:
            print("❌ Nome vazio!")
            return jsonify({'success': False, 'message': 'Nome da pasta é obrigatório'}), 400
        
        if len(nome) > 50:
            print("❌ Nome muito longo!")
            return jsonify({'success': False, 'message': 'Nome muito longo (máximo 50 caracteres)'}), 400
        
        if cor not in CORES_DISPONIVEIS:
            print(f"⚠️ Cor inválida: {cor}, usando padrão")
            cor = '#6366f1'
        
        # Criar a lista no Supabase
        print(f"🔍 Chamando criar_lista...")
        nova_lista = criar_lista(
            usuario_id=current_user.id,
            nome=nome,
            descricao=descricao,
            cor=cor
        )
        
        print(f"🔍 Resultado criar_lista: {nova_lista}")
        
        if nova_lista:
            print("✅ Lista criada com sucesso!")
            return jsonify({
                'success': True,
                'message': 'Pasta criada com sucesso!',
                'lista': nova_lista
            }), 201
        else:
            print("❌ criar_lista retornou None")
            return jsonify({'success': False, 'message': 'Erro ao criar pasta no banco de dados'}), 500
            
    except Exception as e:
        print(f"❌ Erro na rota criar_pasta: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'}), 500


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
        if lista.get('user_id') != current_user.id:
            return "Acesso negado", 403
        
        # Busca os itens salvos nesta lista
        from services.listas import obter_itens_lista
        itens = obter_itens_lista(lista_id)
        
        return render_template(
            'base_arquivo.html',
            lista=lista,
            itens=itens
        )
    except Exception as e:
        print(f"Erro ao visualizar arquivo: {e}")
        return "Erro ao carregar arquivo", 500