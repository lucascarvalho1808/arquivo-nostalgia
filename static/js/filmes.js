// Controle da página atual
let paginaAtual = 1;
const botaoVerMais = document.getElementById('botao-ver-mais');
const gradePosters = document.querySelector('.grade-posters');

// Executa se o botão existir na página
if (botaoVerMais) {
    botaoVerMais.addEventListener('click', async function() {
        // Desabilita o botão enquanto carrega
        botaoVerMais.disabled = true;
        botaoVerMais.textContent = 'Carregando...';

        try {
            // Incrementa a página e busca os novos filmes
            paginaAtual++;
            const response = await fetch(`/api/filmes?pagina=${paginaAtual}`);
            const filmes = await response.json();

            // Se não houver mais filmes, esconde o botão
            if (filmes.length === 0) {
                botaoVerMais.textContent = 'Fim da lista';
                botaoVerMais.disabled = true;
                return;
            }

            // Adiciona cada filme na grade
            filmes.forEach(filme => {
                if (filme.poster_url) {
                    const divPoster = document.createElement('div');
                    divPoster.className = 'item-poster';
                    divPoster.innerHTML = `
                        <a href="#">
                            <img src="${filme.poster_url}" alt="${filme.titulo}" loading="lazy">
                        </a>
                    `;
                    gradePosters.appendChild(divPoster);
                }
            });

            // Reativa o botão
            botaoVerMais.disabled = false;
            botaoVerMais.textContent = 'Ver mais';

        } catch (error) {
            console.error('Erro ao carregar filmes:', error);
            botaoVerMais.textContent = 'Erro - Tentar novamente';
            botaoVerMais.disabled = false;
        }
    });
}