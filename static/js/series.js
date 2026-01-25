// Controle de estado da página e filtros
let paginaAtual = 1;
let generosSelecionados = '';

// Elementos do DOM usados na página de séries
const botaoVerMais = document.getElementById('botao-ver-mais');
const gradePosters = document.querySelector('.grade-posters');
const btnBuscarFiltro = document.getElementById('btn-buscar-filtro');
const formFiltros = document.getElementById('form-filtros');

// Cria o HTML de um poster e adiciona na grade 
function criarPoster(serie) {
    if (serie.poster_url) {
        const divPoster = document.createElement('div');
        divPoster.className = 'item-poster';
        divPoster.dataset.id = serie.id;
        divPoster.dataset.tipo = 'serie';
        divPoster.innerHTML = `
            <a href="#">
                <img src="${serie.poster_url}" alt="${serie.titulo}" loading="lazy">
            </a>
        `;
        gradePosters.appendChild(divPoster);
    }
}

// Limpa todos os posters da grade.
function limparGrade() {
    gradePosters.innerHTML = '';
}

// Coleta os IDs dos gêneros selecionados nos checkboxes
function coletarGenerosSelecionados() {
    const checkboxes = formFiltros.querySelectorAll('input[name="genero"]:checked');
    const ids = Array.from(checkboxes).map(cb => cb.value);
    return ids.join(',');
}

// Busca séries (com ou sem filtro) e atualiza a grade
async function buscarSeries(pagina, generos, substituir = false) {
    try {
        let url = `/api/series/filtrar?pagina=${pagina}`;
        if (generos) {
            url += `&generos=${generos}`;
        }

        const response = await fetch(url);
        const series = await response.json();

        // Se não houver resultados, exibe mensagem e desativa botão
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

        // Adiciona os listeners de clique nos novos posters
        adicionarEventListenersSeries();

        // Reativa o botão "Ver mais"
        botaoVerMais.disabled = false;
        botaoVerMais.textContent = 'Ver mais';

    } catch (error) {
        // Em caso de erro, exibe mensagem e reativa botão
        console.error('Erro ao carregar séries:', error);
        botaoVerMais.textContent = 'Erro - Tentar novamente';
        botaoVerMais.disabled = false;
    }
}

/*
 Adiciona event listeners de clique aos posters de séries.
 Remove listeners antigos clonando o elemento antes de adicionar novos.
 */
function adicionarEventListenersSeries() {
    document.querySelectorAll('.item-poster').forEach(item => {
        // Remove listeners duplicados clonando o elemento
        const novoItem = item.cloneNode(true);
        item.parentNode.replaceChild(novoItem, item);
    });
    
    // Adiciona os listeners aos elementos limpos
    document.querySelectorAll('.item-poster').forEach(item => {
        item.style.cursor = 'pointer';
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const id = this.dataset.id;
            const tipo = this.dataset.tipo;
            
            if (id && tipo) {
                window.location.href = `/detalhes/${tipo}/${id}`;
            }
        });
    });
}

// Botão "Ver mais" - Carrega próxima página de séries
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
        // Reseta para página 1 quando aplica novo filtro
        paginaAtual = 1;
        generosSelecionados = coletarGenerosSelecionados();
        
        // Feedback visual de carregamento
        btnBuscarFiltro.textContent = 'Buscando...';
        btnBuscarFiltro.disabled = true;

        // Busca com os novos filtros (substituir = true)
        await buscarSeries(paginaAtual, generosSelecionados, true);

        // Restaura o botão
        btnBuscarFiltro.textContent = 'BUSCAR';
        btnBuscarFiltro.disabled = false;
    });
}

// Chama a função para adicionar listeners nos posters ao carregar a página
document.addEventListener('DOMContentLoaded', adicionarEventListenersSeries);