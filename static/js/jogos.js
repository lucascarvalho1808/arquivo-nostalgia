// Controle de estado
let paginaAtual = 1;
let generosSelecionados = '';

const botaoVerMais = document.getElementById('botao-ver-mais');
const gradePosters = document.querySelector('.grade-posters');
const btnBuscarFiltro = document.getElementById('btn-buscar-filtro');
const formFiltros = document.getElementById('form-filtros');

/**
 * Cria o HTML de um poster e adiciona na grade.
 * Jogos da Steam: capa vertical (poster)
 * Jogos sem Steam: imagem horizontal do RAWG (card com título)
 */
function criarPoster(jogo) {
    if (!jogo.poster_url) return;
    
    const divPoster = document.createElement('div');
    
    if (jogo.origem_imagem === 'steam') {
        // --- ESTILO 1: STEAM (Vertical) ---
        divPoster.className = 'item-poster poster-clean steam-card';
        
        const fallbackAttr = jogo.imagem_fallback 
            ? `onerror="this.onerror=null; this.src='${jogo.imagem_fallback}';"` 
            : '';
            
        divPoster.innerHTML = `
            <a href="#" style="display: block; position: relative; height: 100%;">
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
            </a>
        `;
    } else {
        // --- ESTILO 2: RAWG (Horizontal forçado a preencher) ---
        // Aqui está o segredo: adicionei os styles inline igual fizemos no HTML
        divPoster.className = 'game-card';
        divPoster.style.height = '100%'; // Garante altura total

        divPoster.innerHTML = `
            <div class="item-poster poster-clean" style="height: 100%; width: 100%;">
                <a href="#" style="display: block; height: 100%; width: 100%; position: relative;">
                    <img src="${jogo.poster_url}" 
                         alt="${jogo.titulo}" 
                         class="poster-jogos" 
                         loading="lazy"
                         style="height: 100%; width: 100%; object-fit: cover; object-position: center top; display: block;">
                    
                    <div class="game-info-overlay">
                        <h3 class="game-title">${jogo.titulo}</h3>
                    </div>
                </a>
            </div>
        `;
    }
    
    gradePosters.appendChild(divPoster);
}

/**
 * Limpa a grade de posters
 */
function limparGrade() {
    gradePosters.innerHTML = '';
}

/**
 * Coleta os IDs dos gêneros selecionados nos checkboxes
 */
function coletarGenerosSelecionados() {
    const checkboxes = formFiltros.querySelectorAll('input[name="genero"]:checked');
    const ids = Array.from(checkboxes).map(cb => cb.value);
    return ids.join(',');
}

/**
 * Busca jogos (com ou sem filtro) e atualiza a grade
 */
async function buscarJogos(pagina, generos, substituir = false) {
    try {
        let url = `/api/jogos/filtrar?pagina=${pagina}`;
        if (generos) {
            url += `&generos=${generos}`;
        }

        const response = await fetch(url);
        const jogos = await response.json();

        if (jogos.length === 0) {
            if (substituir) {
                gradePosters.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">Nenhum jogo encontrado para estes filtros.</p>';
            }
            botaoVerMais.textContent = 'Fim da lista';
            botaoVerMais.disabled = true;
            return;
        }

        if (substituir) {
            limparGrade();
        }

        jogos.forEach(jogo => criarPoster(jogo));

        botaoVerMais.disabled = false;
        botaoVerMais.textContent = 'Ver mais';

    } catch (error) {
        console.error('Erro ao carregar jogos:', error);
        botaoVerMais.textContent = 'Erro - Tentar novamente';
        botaoVerMais.disabled = false;
    }
}


if (botaoVerMais) {
    botaoVerMais.addEventListener('click', async function() {
        botaoVerMais.disabled = true;
        botaoVerMais.textContent = 'Carregando...';
        
        paginaAtual++;
        await buscarJogos(paginaAtual, generosSelecionados, false);
    });
}

if (btnBuscarFiltro) {
    btnBuscarFiltro.addEventListener('click', async function() {
        paginaAtual = 1;
        generosSelecionados = coletarGenerosSelecionados();
        
        btnBuscarFiltro.textContent = 'Buscando...';
        btnBuscarFiltro.disabled = true;

        await buscarJogos(paginaAtual, generosSelecionados, true);

        btnBuscarFiltro.textContent = 'BUSCAR';
        btnBuscarFiltro.disabled = false;
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os wrappers de jogos (Steam e RAWG)
    const cards = document.querySelectorAll('.poster-wrapper, .game-card');

    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Verifica se é um dispositivo touch ou tela pequena (opcional, mas recomendado)
            // Se quiser que funcione assim no PC também, pode remover o 'if'
            const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);

            if (isTouch) {
                // Se o card JÁ tem a classe ativo...
                if (card.classList.contains('ativo')) {
                    // ...Deixa o navegador seguir o link normalmente (2º clique)
                    return true; 
                } else {
                    // ...Se NÃO tem a classe ativo (1º clique)
                    e.preventDefault(); // Impede de entrar no link
                    
                    // Remove a classe 'ativo' de todos os outros jogos abertos
                    cards.forEach(c => c.classList.remove('ativo'));
                    
                    // Adiciona a classe 'ativo' neste jogo
                    card.classList.add('ativo');
                }
            }
        });
    });

    // Lógica para "Limpar a tela" ao clicar fora
    document.addEventListener('click', function(e) {
        // Se o clique NÃO foi dentro de nenhum card de jogo
        if (!e.target.closest('.poster-wrapper') && !e.target.closest('.game-card')) {
            // Remove o ativo de todo mundo
            cards.forEach(c => c.classList.remove('ativo'));
        }
    });
});