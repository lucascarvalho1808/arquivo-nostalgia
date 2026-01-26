from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.estatisticas_usuario import calcular_estatisticas_usuario
from services.ranking import rank_global, rank_filmes, rank_series, rank_jogos
from datetime import datetime
from routes.extensions import supabase

# Blueprint da página de perfil do usuário
perfil_bp = Blueprint('perfil', __name__, url_prefix='/perfil')

@perfil_bp.route('/')
@login_required
def perfil():
    """
    Página de perfil do usuário autenticado.
    """
    # Busca estatísticas do usuário (filmes, séries, jogos)
    stats = calcular_estatisticas_usuario(current_user.id)
    # Garante que created_at é datetime
    data_cadastro = getattr(current_user, 'created_at', None)
    print("Criado em: ", repr(data_cadastro))
    if data_cadastro:
        if isinstance(data_cadastro, str):
            try:
                # Tenta ISO
                data_cadastro = datetime.fromisoformat(data_cadastro)
            except Exception:
                try:
                    # Tenta formato comum de datetime do banco
                    data_cadastro = datetime.strptime(data_cadastro, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    data_cadastro = None
    elif not data_cadastro:
        data_cadastro = None

    # Calcula os ranks
    rank_geral = rank_global(stats["total"])
    rank_filme = rank_filmes(stats["filmes"]["quantidade"])
    rank_serie = rank_series(stats["series"]["quantidade"])
    rank_jogo = rank_jogos(stats["jogos"]["quantidade"])

    return render_template(
        'usuario/perfil.html',
        usuario=current_user,
        stats=stats,
        data_cadastro=data_cadastro,
        rank_geral=rank_geral,
        rank_filme=rank_filme,
        rank_serie=rank_serie,
        rank_jogo=rank_jogo
    )

@perfil_bp.route('/atualizar-nome', methods=['POST'])
@login_required
def atualizar_nome():
    novo_nome = request.json.get('nome')
    if not novo_nome or not novo_nome.strip():
        return jsonify({'success': False, 'mensagem': 'Nome inválido.'}), 400

    # Atualiza no Supabase
    try:
        resp = supabase.table("usuarios").update({"username": novo_nome.strip()}).eq("id", current_user.id).execute()
        if resp.data:
            # Atualiza o current_user em tempo real (opcional)
            current_user.username = novo_nome.strip()
            return jsonify({'success': True, 'nome': novo_nome.strip()})
        else:
            return jsonify({'success': False, 'mensagem': 'Erro ao atualizar nome.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'mensagem': str(e)}), 500