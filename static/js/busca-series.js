document.addEventListener('DOMContentLoaded', function() {
    const inputBusca = document.querySelector('.barra-topo input');
    const iconeBusca = document.querySelector('.barra-topo .icone-lupa');
    const gridPosters = document.querySelector('.grade-posters');
    
    let conteudoOriginal = gridPosters ? gridPosters.innerHTML : '';
    
    // Função para buscar séries
    async function buscarSeries(termo) {
        if (!termo.trim()) {
            gridPosters.innerHTML = conteudoOriginal;
            return;
        }
        
        try {
            // Loading estilizado
            gridPosters.innerHTML = `
                <div class="loading-busca">
                    <div class="spinner"></div>
                    <p>Buscando séries...</p>
                </div>
            `;
            
            const response = await fetch(`/api/busca/series?q=${encodeURIComponent(termo)}`);
            const series = await response.json();
            
            if (series.length === 0) {
                gridPosters.innerHTML = `
                    <div class="sem-resultados">
                        <i class="fa-solid fa-tv"></i>
                        <p>Nenhuma série encontrada para "${termo}"</p>
                        <button class="btn-limpar-busca" onclick="limparBusca()">Voltar ao catálogo</button>
                    </div>
                `;
                return;
            }
            
            gridPosters.innerHTML = series.map(serie => `
                <div class="item-poster" data-id="${serie.id}" data-tipo="serie">
                    <a href="#">
                        ${serie.poster 
                            ? `<img src="${serie.poster}" alt="${serie.titulo}" loading="lazy">`
                            : '<div class="poster-placeholder">Sem Imagem</div>'
                        }
                    </a>
                </div>
            `).join('');
            
            // Adicionar listeners de clique
            adicionarEventListenersBusca();
            
        } catch (error) {
            console.error('Erro ao buscar séries:', error);
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
            buscarSeries(inputBusca.value);
        });
    }
    
    if (inputBusca) {
        inputBusca.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarSeries(inputBusca.value);
            }
        });
    }
    
    window.limparBusca = function() {
        if (inputBusca) inputBusca.value = '';
        gridPosters.innerHTML = conteudoOriginal;
        adicionarEventListenersBusca();
    };
    
    // Função para adicionar event listeners
    function adicionarEventListenersBusca() {
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
    
    // Chamar no carregamento inicial
    adicionarEventListenersBusca();
});