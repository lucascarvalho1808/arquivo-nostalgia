from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.listas import (
    criar_lista,
    adicionar_item_lista,
    remover_item_lista,
    buscar_itens_lista,
    verificar_item_na_lista,
    obter_cores_disponiveis,
    CORES_DISPONIVEIS
)

# Cria o Blueprint para rotas relacionadas a listas personalizadas do usuário
listas_bp = Blueprint('listas', __name__)

@listas_bp.route('/cores-disponiveis', methods=['GET'])
def cores_disponiveis():
    """
    Retorna as cores disponíveis para personalização das listas.

    Retorna:
    {
        "success": true,
        "cores": ["#6366f1", "#ec4899", ...]
    }
    """
    return jsonify({
        "success": True,
        "cores": obter_cores_disponiveis()
    }), 200

@listas_bp.route('/criar-lista', methods=['POST'])
@login_required
def criar_lista_route():
    """
    Rota para criar uma nova lista.
    """
    try:
        # Recebe os dados do request
        dados = request.get_json()
        
        # Validação do campo obrigatório
        nome = dados.get('nome', '').strip()
        if not nome:
            return jsonify({
                "success": False,
                "erro": "O nome da lista é obrigatório."
            }), 400
        
        # Validação do tamanho do nome
        if len(nome) < 3:
            return jsonify({
                "success": False,
                "erro": "O nome da lista deve ter pelo menos 3 caracteres."
            }), 400
        
        if len(nome) > 100:
            return jsonify({
                "success": False,
                "erro": "O nome da lista deve ter no máximo 100 caracteres."
            }), 400
        
        # Descrição é opcional
        descricao = dados.get('descricao', '').strip()
        
        # Cor é opcional, mas se informada deve ser válida
        cor = dados.get('cor')
        if cor and cor not in CORES_DISPONIVEIS:
            return jsonify({
                "success": False,
                "erro": "Cor inválida. Use uma das cores disponíveis.",
                "cores_disponiveis": CORES_DISPONIVEIS
            }), 400
        
        # Cria a lista
        resultado = criar_lista(nome=nome, descricao=descricao, cor=cor)
        
        if resultado and not resultado.get('erro'):
            return jsonify({
                "success": True,
                "mensagem": f"Lista '{nome}' criada com sucesso!",
                "lista": resultado
            }), 201  # 201 Created
        elif resultado and resultado.get('erro') == 'cor_invalida':
            return jsonify({
                "success": False,
                "erro": resultado.get('mensagem'),
                "cores_disponiveis": CORES_DISPONIVEIS
            }), 400
        else:
            return jsonify({
                "success": False,
                "erro": "Erro ao criar lista."
            }), 500
            
    except Exception as e:
        print(f"Erro na rota /criar-lista: {e}")
        return jsonify({
            "success": False,
            "erro": "Erro interno do servidor."
        }), 500

@listas_bp.route('/adicionar-item', methods=['POST'])
@login_required
def adicionar_item():
    """
    Rota para adicionar um item (filme/série/jogo) a uma lista.

    Esperado no body (JSON):
    {
        "lista_id": "uuid-da-lista",
        "api_id": "550",
        "tipo": "filme",
        "titulo": "Clube da Luta",
        "poster_url": "https://image.tmdb.org/t/p/w300/poster.jpg"
    }

    Retorna:
    {
        "success": true,
        "mensagem": "Item adicionado com sucesso!",
        "item": {...}
    }
    """
    try:
        # Recebe os dados do request
        dados = request.get_json()
        
        # Validação dos campos obrigatórios
        campos_obrigatorios = ['lista_id', 'api_id', 'tipo', 'titulo']
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({
                    "success": False,
                    "erro": f"Campo '{campo}' é obrigatório."
                }), 400
        
        lista_id = dados.get('lista_id')
        api_id = dados.get('api_id')
        tipo = dados.get('tipo')
        titulo = dados.get('titulo')
        poster_url = dados.get('poster_url', '')
        
        # Validação do tipo
        if tipo not in ['filme', 'serie', 'jogo']:
            return jsonify({
                "success": False,
                "erro": "Tipo inválido. Use 'filme', 'serie' ou 'jogo'."
            }), 400
        
        # Verifica se o item já existe na lista
        if verificar_item_na_lista(lista_id, api_id, tipo):
            return jsonify({
                "success": False,
                "erro": "Este item já está na lista."
            }), 409  # 409 Conflict
        
        # Adiciona o item à lista
        resultado = adicionar_item_lista(
            lista_id=lista_id,
            api_id=api_id,
            tipo=tipo,
            titulo=titulo,
            poster_url=poster_url
        )
        
        if resultado and "erro" not in resultado:
            return jsonify({
                "success": True,
                "mensagem": f"'{titulo}' adicionado à lista com sucesso!",
                "item": resultado
            }), 201  # 201 Created
        else:
            return jsonify({
                "success": False,
                "erro": resultado.get("mensagem") if resultado else "Erro ao adicionar item."
            }), 500
            
    except Exception as e:
        print(f"Erro na rota /adicionar-item: {e}")
        return jsonify({
            "success": False,
            "erro": "Erro interno do servidor."
        }), 500

@listas_bp.route('/remover-item/<item_id>', methods=['DELETE'])
@login_required
def remover_item(item_id):
    """
    Rota para remover um item de uma lista.

    Parâmetro na URL:
        item_id (str): UUID do item a ser removido

    Retorna:
    {
        "success": true,
        "mensagem": "Item removido com sucesso!"
    }
    """
    try:
        resultado = remover_item_lista(item_id)
        
        if resultado:
            return jsonify({
                "success": True,
                "mensagem": "Item removido com sucesso!"
            }), 200
        else:
            return jsonify({
                "success": False,
                "erro": "Item não encontrado."
            }), 404
            
    except Exception as e:
        print(f"Erro na rota /remover-item: {e}")
        return jsonify({
            "success": False,
            "erro": "Erro interno do servidor."
        }), 500

@listas_bp.route('/lista/<lista_id>/itens', methods=['GET'])
@login_required
def listar_itens(lista_id):
    """
    Rota para buscar todos os itens de uma lista.

    Parâmetro na URL:
        lista_id (str): UUID da lista

    Retorna:
    {
        "success": true,
        "itens": [...]
    }
    """
    try:
        itens = buscar_itens_lista(lista_id)
        
        return jsonify({
            "success": True,
            "itens": itens,
            "total": len(itens)
        }), 200
            
    except Exception as e:
        print(f"Erro na rota /lista/itens: {e}")
        return jsonify({
            "success": False,
            "erro": "Erro interno do servidor."
        }), 500

@listas_bp.route('/verificar-item', methods=['POST'])
@login_required
def verificar_item():
    """
    Rota para verificar se um item já existe em uma lista.

    Esperado no body (JSON):
    {
        "lista_id": "uuid-da-lista",
        "api_id": "550",
        "tipo": "filme"
    }

    Retorna:
    {
        "existe": true/false
    }
    """
    try:
        dados = request.get_json()
        
        lista_id = dados.get('lista_id')
        api_id = dados.get('api_id')
        tipo = dados.get('tipo')
        
        if not all([lista_id, api_id, tipo]):
            return jsonify({
                "success": False,
                "erro": "Parâmetros incompletos."
            }), 400
        
        existe = verificar_item_na_lista(lista_id, api_id, tipo)
        
        return jsonify({
            "success": True,
            "existe": existe
        }), 200
            
    except Exception as e:
        print(f"Erro na rota /verificar-item: {e}")
        return jsonify({
            "success": False,
            "erro": "Erro interno do servidor."
        }), 500


