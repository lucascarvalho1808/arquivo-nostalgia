document.addEventListener('DOMContentLoaded', function() {
    const inputBusca = document.querySelector('.barra-topo input');
    const iconeBusca = document.querySelector('.barra-topo .icone-lupa');
    const gridPosters = document.querySelector('.grade-posters');
    
    let conteudoOriginal = gridPosters ? gridPosters.innerHTML : '';
    
    async function buscarFilmes(termo) {
        if (!termo.trim()) {
            gridPosters.innerHTML = conteudoOriginal;
            return;
        }
        
        try {
            // Loading estilizado
            gridPosters.innerHTML = `
                <div class="loading-busca">
                    <div class="spinner"></div>
                    <p>Buscando filmes...</p>
                </div>
            `;
            
            const response = await fetch(`/api/busca/filmes?q=${encodeURIComponent(termo)}`);
            const filmes = await response.json();
            
            if (filmes.length === 0) {
                gridPosters.innerHTML = `
                    <div class="sem-resultados">
                        <i class="fa-solid fa-film"></i>
                        <p>Nenhum filme encontrado para "${termo}"</p>
                        <button class="btn-limpar-busca" onclick="limparBusca()">Voltar ao catálogo</button>
                    </div>
                `;
                return;
            }
            
            gridPosters.innerHTML = filmes.map(filme => `
                <div class="item-poster">
                    <a href="#">
                        ${filme.poster 
                            ? `<img src="${filme.poster}" alt="${filme.titulo}" loading="lazy">`
                            : '<div class="poster-placeholder">Sem Imagem</div>'
                        }
                    </a>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Erro ao buscar filmes:', error);
            gridPosters.innerHTML = `
                <div class="mensagem-erro">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <p>Erro ao buscar. Tente novamente.</p>
                </div>
            `;
        }
    }
    
    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
        iconeBusca.addEventListener('click', function() {
            buscarFilmes(inputBusca.value);
        });
    }
    
    if (inputBusca) {
        inputBusca.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarFilmes(inputBusca.value);
            }
        });
    }
    
    window.limparBusca = function() {
        if (inputBusca) inputBusca.value = '';
        gridPosters.innerHTML = conteudoOriginal;
    };
});