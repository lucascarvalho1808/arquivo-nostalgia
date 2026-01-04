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
        // Jogo da Steam: poster vertical
        divPoster.className = 'item-poster';
        
        const fallbackAttr = jogo.imagem_fallback 
            ? `onerror="this.onerror=null; this.src='${jogo.imagem_fallback}';"` 
            : '';
        
        divPoster.innerHTML = `
            <a href="#">
                <img src="${jogo.poster_url}" 
                     alt="${jogo.titulo}" 
                     loading="lazy"
                     ${fallbackAttr}>
            </a>
        `;
    } else {
        // Jogo sem Steam: card com imagem horizontal + título
        divPoster.className = 'item-poster game-card';
        divPoster.innerHTML = `
            <a href="#">
                <div class="game-img-container">
                    <img src="${jogo.poster_url}" alt="${jogo.titulo}" loading="lazy">
                </div>
                <h3 class="game-title">${jogo.titulo}</h3>
            </a>
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