// Controle de estado da página e filtros
let paginaAtual = 1;
let generosSelecionados = '';

// Elementos do DOM usados na página de jogos
const botaoVerMais = document.getElementById('botao-ver-mais');
const gradePosters = document.querySelector('.grade-posters');
const btnBuscarFiltro = document.getElementById('btn-buscar-filtro');
const formFiltros = document.getElementById('form-filtros');

/*
 Função de navegação para página de detalhes do jogo.
 Redireciona para a rota de detalhes usando o id e tipo.
 */
function navegarParaDetalhes(id, tipo) {
    const url = `/detalhes/${tipo}/${id}`;
    window.location.href = url;
}

/*
 Detecta se o usuário está em um dispositivo mobile.
 Retorna true para telas pequenas ou user agents de mobile.
 */
function isMobile() {
    return window.innerWidth <= 768 || 
           /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/*
 Adiciona eventos de clique ao card criado dinamicamente.
 No mobile: duplo clique para abrir detalhes.
 No desktop: clique único.
 */
function adicionarEventoCard(card) {
    card.style.cursor = 'pointer';
    
    if (isMobile()) {
        // Mobile: duplo clique para abrir detalhes
        card.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!this.classList.contains('ativo')) {
                document.querySelectorAll('[data-tipo="jogo"]').forEach(c => c.classList.remove('ativo'));
                this.classList.add('ativo');
            } else {
                const id = this.getAttribute('data-id');
                navegarParaDetalhes(id, 'jogo');
            }
        });
    } else {
        // Desktop: clique único para abrir detalhes
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-id');
            navegarParaDetalhes(id, 'jogo');
        });
    }
}

/*
 Cria o HTML de um poster de jogo e adiciona na grade de posters.
 Suporta capas verticais (Steam) e padrão (RAWG).
 */
function criarPoster(jogo) {
    if (!jogo.poster_url) return;
    
    const divPoster = document.createElement('div');
    
    if (jogo.origem_imagem === 'steam') {
        // Steam: capa vertical
        divPoster.className = 'item-poster poster-clean steam-card';
        divPoster.setAttribute('data-id', jogo.id);
        divPoster.setAttribute('data-tipo', 'jogo');
        
        const fallbackAttr = jogo.imagem_fallback 
            ? `onerror="this.onerror=null; this.src='${jogo.imagem_fallback}';"` 
            : '';
            
        divPoster.innerHTML = `
            <div class="poster-wrapper" style="height: 100%; width: 100%;">
                <img src="${jogo.poster_url}" 
                     alt="${jogo.titulo}" 
                     class="poster-jogos" 
                     loading="lazy"
                     style="height: 100%; width: 100%; object-fit: cover;"
                     ${fallbackAttr}>
                
                <div class="game-info-overlay">
                    <h3 class="game-title">${jogo.titulo}</h3>
                </div>
            </div>
        `;
    } else {
        // RAWG: capa vertical (igual Steam)
        divPoster.className = 'item-poster poster-clean steam-card';
        divPoster.setAttribute('data-id', jogo.id);
        divPoster.setAttribute('data-tipo', 'jogo');

        divPoster.innerHTML = `
            <div class="poster-wrapper" style="height: 100%; width: 100%;">
                <img src="${jogo.poster_url}" 
                     alt="${jogo.titulo}" 
                     class="poster-jogos" 
                     loading="lazy"
                     style="height: 100%; width: 100%; object-fit: cover;">
                
                <div class="game-info-overlay">
                    <h3 class="game-title">${jogo.titulo}</h3>
                </div>
            </div>
        `;
    }
    
    gradePosters.appendChild(divPoster);
    adicionarEventoCard(divPoster);
}

/*Limpa todos os posters da grade.*/
function limparGrade() {
    gradePosters.innerHTML = '';
}

// Coleta os IDs dos gêneros selecionados nos checkboxes
function coletarGenerosSelecionados() {
    const checkboxes = formFiltros.querySelectorAll('input[name="genero"]:checked');
    const ids = Array.from(checkboxes).map(cb => cb.value);
    return ids.join(',');
}

// Busca jogos (com ou sem filtro) e atualiza a grade
async function buscarJogos(pagina, generos, substituir = false) {
    try {
        let url = `/api/jogos/filtrar?pagina=${pagina}`;
        if (generos) {
            url += `&generos=${generos}`;
        }

        const response = await fetch(url);
        const jogos = await response.json();

        // Se não houver resultados, exibe mensagem e desativa botão
        if (jogos.length === 0) {
            if (substituir) {
                gradePosters.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">Nenhum jogo encontrado para estes filtros.</p>';
            }
            botaoVerMais.textContent = 'Fim da lista';
            botaoVerMais.disabled = true;
            return;
        }

        // Se for uma nova busca (filtro), limpa a grade primeiro
        if (substituir) {
            limparGrade();
        }

        // Adiciona os jogos na grade
        jogos.forEach(jogo => criarPoster(jogo));

        // Reativa o botão "Ver mais"
        botaoVerMais.disabled = false;
        botaoVerMais.textContent = 'Ver mais';

    } catch (error) {
        // Em caso de erro, exibe mensagem e reativa botão
        console.error('Erro ao carregar jogos:', error);
        botaoVerMais.textContent = 'Erro - Tentar novamente';
        botaoVerMais.disabled = false;
    }
}

// Botão "Ver mais"
if (botaoVerMais) {
    botaoVerMais.addEventListener('click', async function() {
        botaoVerMais.disabled = true;
        botaoVerMais.textContent = 'Carregando...';
        
        paginaAtual++;
        await buscarJogos(paginaAtual, generosSelecionados, false);
    });
}

// Botão "BUSCAR" do filtro - Aplica os filtros selecionados
if (btnBuscarFiltro) {
    btnBuscarFiltro.addEventListener('click', async function() {
        // Reseta para página 1 quando aplica novo filtro
        paginaAtual = 1;
        generosSelecionados = coletarGenerosSelecionados();
        
        // Feedback visual de carregamento
        btnBuscarFiltro.textContent = 'Buscando...';
        btnBuscarFiltro.disabled = true;

        // Busca com os novos filtros 
        await buscarJogos(paginaAtual, generosSelecionados, true);

        // Restaura o botão
        btnBuscarFiltro.textContent = 'BUSCAR';
        btnBuscarFiltro.disabled = false;
    });
}

// Inicializa eventos nos cards já carregados ao carregar a página
document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('[data-tipo="jogo"]');
    
    cards.forEach(card => {
        adicionarEventoCard(card);
    });

    // Remove 'ativo' ao clicar fora de qualquer card de jogo (mobile)
    if (isMobile()) {
        document.addEventListener('click', function(e) {
            if (!e.target.closest('[data-tipo="jogo"]')) {
                document.querySelectorAll('[data-tipo="jogo"]').forEach(c => c.classList.remove('ativo'));
            }
        });
    }

    console.log('Eventos de navegação (jogos) carregados!');
    console.log(`Modo: ${isMobile() ? 'Mobile' : 'Desktop'}`);
});