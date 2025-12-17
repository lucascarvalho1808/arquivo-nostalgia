// Controle de estado
let paginaAtual = 1;
let generosSelecionados = '';

// Elementos do DOM
const botaoVerMais = document.getElementById('botao-ver-mais');
const gradePosters = document.querySelector('.grade-posters');
const btnBuscarFiltro = document.getElementById('btn-buscar-filtro');
const formFiltros = document.getElementById('form-filtros');

/**
 * Cria o HTML de um poster e adiciona na grade
 */
function criarPoster(serie) {
    if (serie.poster_url) {
        const divPoster = document.createElement('div');
        divPoster.className = 'item-poster';
        divPoster.innerHTML = `
            <a href="#">
                <img src="${serie.poster_url}" alt="${serie.titulo}" loading="lazy">
            </a>
        `;
        gradePosters.appendChild(divPoster);
    }
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
 * Busca séries (com ou sem filtro) e atualiza a grade
 */
async function buscarSeries(pagina, generos, substituir = false) {
    try {
        let url = `/api/series/filtrar?pagina=${pagina}`;
        if (generos) {
            url += `&generos=${generos}`;
        }

        const response = await fetch(url);
        const series = await response.json();

        if (series.length === 0) {
            if (substituir) {
                gradePosters.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">Nenhuma série encontrada para estes filtros.</p>';
            }
            botaoVerMais.textContent = 'Fim da lista';
            botaoVerMais.disabled = true;
            return;
        }

        // Se for uma nova busca (filtro), limpa a grade primeiro
        if (substituir) {
            limparGrade();
        }

        // Adiciona as séries na grade
        series.forEach(serie => criarPoster(serie));

        // Reativa o botão
        botaoVerMais.disabled = false;
        botaoVerMais.textContent = 'Ver mais';

    } catch (error) {
        console.error('Erro ao carregar séries:', error);
        botaoVerMais.textContent = 'Erro - Tentar novamente';
        botaoVerMais.disabled = false;
    }
}

// --- EVENT LISTENERS ---

// Botão "Ver mais" - Carrega próxima página
if (botaoVerMais) {
    botaoVerMais.addEventListener('click', async function() {
        botaoVerMais.disabled = true;
        botaoVerMais.textContent = 'Carregando...';
        
        paginaAtual++;
        await buscarSeries(paginaAtual, generosSelecionados, false);
    });
}

// Botão "BUSCAR" do filtro - Aplica os filtros selecionados
if (btnBuscarFiltro) {
    btnBuscarFiltro.addEventListener('click', async function() {
        paginaAtual = 1;
        generosSelecionados = coletarGenerosSelecionados();
        
        btnBuscarFiltro.textContent = 'Buscando...';
        btnBuscarFiltro.disabled = true;

        await buscarSeries(paginaAtual, generosSelecionados, true);

        btnBuscarFiltro.textContent = 'BUSCAR';
        btnBuscarFiltro.disabled = false;
    });
}