from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, session, send_file, Response
from flask_login import login_required, current_user
from services.listas import (
    obter_listas_usuario,
    obter_lista_por_id,
    criar_lista,
    atualizar_lista,
    deletar_lista,
    CORES_DISPONIVEIS,
    remover_item_lista,
    buscar_itens_lista
)
from services.ranking_csv import ler_ranking_comunidade
from services.estatisticas_usuario import calcular_estatisticas_usuario
import re
from datetime import datetime

# Blueprint para rotas relacionadas a arquivos/listas do usuário
arquivos_bp = Blueprint('arquivos', __name__, url_prefix='/arquivos')


@arquivos_bp.route('/')
@arquivos_bp.route('/meus-arquivos')
@login_required
def meus_arquivos():
    """
    Página principal com todas as listas (pastas) do usuário.
    Inclui o ranking da comunidade lido do CSV e estatísticas pessoais.
    Salva a data/hora do último acesso na sessão.
    """
    try:
        # Salva a data/hora do último acesso na sessão
        session['ultimo_acesso'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

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
            cores_disponiveis=CORES_DISPONIVEIS,
            ultimo_acesso=session.get('ultimo_acesso')  
        )
    except Exception as e:
        print(f"Erro ao carregar meus arquivos: {e}")
        # Em caso de erro, retorna a página com dados vazios
        return render_template(
            'meus_arquivos.html', 
            listas=[],
            ranking={'filmes': [], 'series': [], 'jogos': []},
            estatisticas={'total': 0, 'filmes': {'quantidade': 0, 'porcentagem': 0}, 'series': {'quantidade': 0, 'porcentagem': 0}, 'jogos': {'quantidade': 0, 'porcentagem': 0}},
            cores_disponiveis=CORES_DISPONIVEIS,
            ultimo_acesso=session.get('ultimo_acesso')
        )


def rgb_to_hex(rgb_str):
    """Converte 'rgb(r, g, b)' para '#rrggbb'. Retorna None se não for rgb."""
    m = re.match(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", rgb_str)
    if not m:
        return None
    r, g, b = map(int, m.groups())
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


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
        
        # Converte cor de rgb(...) para hexadecimal, se necessário
        if isinstance(cor, str) and cor.startswith("rgb"):
            hexc = rgb_to_hex(cor)
            if hexc:
                cor = hexc

        print(f"🔍 Nome: {nome}")
        print(f"🔍 Descrição: {descricao}")
        print(f"🔍 Cor: {cor}")
        
        # Validações de entrada
        if not nome:
            print("❌ Nome vazio!")
            return jsonify({'success': False, 'message': 'Nome da pasta é obrigatório'}), 400
        
        if len(nome) > 50:
            print("❌ Nome muito longo!")
            return jsonify({'success': False, 'message': 'Nome muito longo (máximo 50 caracteres)'}), 400
        
        if cor not in CORES_DISPONIVEIS:
            print(f"⚠️ Cor inválida: {cor}, usando padrão")
            cor = '#6366f1'
        
        # Cria a lista no Supabase
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
    Só permite acesso ao dono da lista.
    """
    try:
        # Busca a lista específica pelo ID
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


@arquivos_bp.route('/deletar-pasta/<lista_id>', methods=['DELETE'])
@login_required
def deletar_pasta(lista_id):
    """
    Deleta uma lista (pasta) se pertencer ao usuário logado.
    """
    try:
        lista = obter_lista_por_id(lista_id)
        if not lista:
            return jsonify({'success': False, 'message': 'Lista não encontrada'}), 404

        # Checa se a lista pertence ao usuário autenticado
        if lista.get('user_id') and str(lista.get('user_id')) != str(current_user.id):
            return jsonify({'success': False, 'message': 'Acesso negado'}), 403

        resultado = deletar_lista(lista_id)
        if resultado:
            return jsonify({'success': True, 'message': 'Pasta deletada com sucesso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Erro ao deletar pasta'}), 500
    except Exception as e:
        current_app.logger.exception("Erro ao processar deletar_pasta")
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500


@arquivos_bp.route('/minhas-pastas-json', methods=['GET'])
@login_required
def minhas_pastas_json():
    """
    Retorna todas as pastas/arquivos do usuário autenticado em formato JSON.
    Útil para AJAX no pop-up de seleção.
    """
    try:
        listas = obter_listas_usuario(current_user.id)
        return jsonify({
            "success": True,
            "listas": listas
        }), 200
    except Exception as e:
        print("Erro ao buscar listas do usuário (JSON):", e)
        return jsonify({
            "success": False,
            "listas": []
        }), 500


@arquivos_bp.route('/remover-item/<item_id>', methods=['DELETE'])
@login_required
def remover_item(item_id):
    """
    Remove um item de uma lista do usuário autenticado.
    """
    try:
        sucesso = remover_item_lista(item_id, current_user.id)
        if sucesso:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Item não encontrado ou não pode ser removido."), 404
    except Exception as e:
        print("Erro ao remover item:", e)
        return jsonify(success=False, message="Erro interno ao remover item."), 500


@arquivos_bp.route('/exportar-csv/<lista_id>')
def exportar_csv_lista(lista_id):
    """
    Exporta os itens da lista em formato CSV para download.
    Gera o arquivo manualmente.
    """
    print(f"Exportando CSV para lista_id: {lista_id}")
    lista = obter_lista_por_id(lista_id)
    if not lista:
        print("Lista não encontrada!")
        return "Lista não encontrada", 404

    itens = buscar_itens_lista(lista_id)
    if not itens:
        print("Nenhum item encontrado na lista.")

    # Cabeçalho do CSV
    cabecalho = ['Título', 'Tipo', 'Ano', 'Poster', 'Descrição']
    linhas = []

    # Adiciona o cabeçalho
    linhas.append(';'.join(cabecalho))

    # Função para escapar aspas e ponto e vírgula
    def esc(v):
        v = str(v or '').replace('"', '""')
        if ';' in v or '"' in v or '\n' in v:
            return f'"{v}"'
        return v

    # Função para extrair ano do título, se vier entre parênteses
    def extrair_ano(titulo):
        import re
        m = re.search(r'\((\d{4})\)', titulo or '')
        return m.group(1) if m else ''

    # Adiciona cada item como linha do CSV
    for item in itens:
        titulo = item.get('titulo', '')
        ano = item.get('ano', '') or extrair_ano(titulo)
        linha = [
            esc(titulo),
            esc(item.get('tipo', '').capitalize()),
            esc(ano),
            esc(item.get('poster_url', '')),
            esc(item.get('descricao', '') or '')
        ]
        linhas.append(';'.join(linha))

    # Junta tudo em uma string
    conteudo_csv = '\n'.join(linhas)

    # Adiciona UTF-8 para compatibilidade com excel e outros
    bom = '\ufeff'
    conteudo_csv = bom + conteudo_csv

    # Nome do arquivo
    nome_arquivo = f"{lista['nome'].replace(' ', '_')}_arquivo_nostalgia.csv"

    # Retorna como download
    return Response(
        conteudo_csv,
        mimetype='text/csv; charset=utf-8',
        headers={
            "Content-Disposition": f"attachment; filename={nome_arquivo}"
        }
    )