document.addEventListener('DOMContentLoaded', function() {
    const inputBusca = document.querySelector('.barra-topo input');
    const iconeBusca = document.querySelector('.barra-topo .icone-lupa');
    const gridPosters = document.querySelector('.grade-posters');
    
    let conteudoOriginal = gridPosters ? gridPosters.innerHTML : '';
    
    async function buscarJogos(termo) {
        if (!termo.trim()) {
            gridPosters.innerHTML = conteudoOriginal;
            return;
        }
        
        try {
            // Loading estilizado
            gridPosters.innerHTML = `
                <div class="loading-busca">
                    <div class="spinner"></div>
                    <p>Buscando jogos...</p>
                </div>
            `;
            
            const response = await fetch(`/api/busca/jogos?q=${encodeURIComponent(termo)}`);
            const jogos = await response.json();
            
            if (jogos.length === 0) {
                gridPosters.innerHTML = `
                    <div class="sem-resultados">
                        <i class="fa-solid fa-gamepad"></i>
                        <p>Nenhum jogo encontrado para "${termo}"</p>
                        <button class="btn-limpar-busca" onclick="limparBusca()">Voltar ao catálogo</button>
                    </div>
                `;
                return;
            }
            
            gridPosters.innerHTML = jogos.map(jogo => `
                <div class="item-poster">
                    <a href="#">
                        ${jogo.poster 
                            ? `<img src="${jogo.poster}" alt="${jogo.titulo}" loading="lazy">`
                            : '<div class="poster-placeholder">Sem Imagem</div>'
                        }
                    </a>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Erro ao buscar jogos:', error);
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
            buscarJogos(inputBusca.value);
        });
    }
    
    if (inputBusca) {
        inputBusca.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarJogos(inputBusca.value);
            }
        });
    }
    
    window.limparBusca = function() {
        if (inputBusca) inputBusca.value = '';
        gridPosters.innerHTML = conteudoOriginal;
    };
});