// Controle da página atual
let paginaAtual = 1;
const botaoVerMais = document.getElementById('botao-ver-mais');
const gradePosters = document.querySelector('.grade-posters');

// Só executa se o botão existir na página
if (botaoVerMais) {
    botaoVerMais.addEventListener('click', async function() {
        // Desabilita o botão enquanto carrega
        botaoVerMais.disabled = true;
        botaoVerMais.textContent = 'Carregando...';

        try {
            // Incrementa a página e busca as novas séries
            paginaAtual++;
            const response = await fetch(`/api/series?pagina=${paginaAtual}`);
            const series = await response.json();

            // Se não houver mais séries, esconde o botão
            if (series.length === 0) {
                botaoVerMais.textContent = 'Fim da lista';
                botaoVerMais.disabled = true;
                return;
            }

            // Adiciona cada série na grade
            series.forEach(serie => {
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
            });

            // Reativa o botão
            botaoVerMais.disabled = false;
            botaoVerMais.textContent = 'Ver mais';

        } catch (error) {
            console.error('Erro ao carregar séries:', error);
            botaoVerMais.textContent = 'Erro - Tentar novamente';
            botaoVerMais.disabled = false;
        }
    });
}