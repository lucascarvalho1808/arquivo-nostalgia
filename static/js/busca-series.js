document.addEventListener('DOMContentLoaded', function() {
    // Seletores dos elementos da barra de busca e grid de posters
    const inputBusca = document.querySelector('.barra-topo input');
    const iconeBusca = document.querySelector('.barra-topo .icone-lupa');
    const gridPosters = document.querySelector('.grade-posters');
    
    // Salva o conteúdo original do grid para restaurar depois
    let conteudoOriginal = gridPosters ? gridPosters.innerHTML : '';
    
    /*
     Função assíncrona para buscar séries pelo termo informado.
     Atualiza o grid de posters com os resultados ou mensagens de erro.
     */
    async function buscarSeries(termo) {
        if (!termo.trim()) {
            gridPosters.innerHTML = conteudoOriginal;
            return;
        }
        
        try {
            // Exibe loading estilizado enquanto busca
            gridPosters.innerHTML = `
                <div class="loading-busca">
                    <div class="spinner"></div>
                    <p>Buscando séries...</p>
                </div>
            `;
            
            // Faz requisição para a API de busca de séries
            const response = await fetch(`/api/busca/series?q=${encodeURIComponent(termo)}`);
            const series = await response.json();
            
            // Se não houver resultados, exibe mensagem de "sem resultados"
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
            
            // Monta o HTML dos posters das séries encontradas
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
            
            // Adiciona listeners de clique nos novos elementos
            adicionarEventListenersBusca();
            
        } catch (error) {
            // Em caso de erro na requisição, exibe mensagem de erro
            console.error('Erro ao buscar séries:', error);
            gridPosters.innerHTML = `
                <div class="mensagem-erro">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <p>Erro ao buscar. Tente novamente.</p>
                </div>
            `;
        }
    }
    
    // Listener para clique no ícone de busca
    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
        iconeBusca.addEventListener('click', function() {
            buscarSeries(inputBusca.value);
        });
    }
    
    // Listener para pressionar Enter no campo de busca
    if (inputBusca) {
        inputBusca.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarSeries(inputBusca.value);
            }
        });
    }
    
    /*
     Função global para limpar a busca e restaurar o grid original.
     */
    window.limparBusca = function() {
        if (inputBusca) inputBusca.value = '';
        gridPosters.innerHTML = conteudoOriginal;
        adicionarEventListenersBusca();
    };
    
    /*
     Adiciona event listeners de clique nos posters para redirecionar para a página de detalhes.
     */
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
    
    // Chama a função para adicionar listeners no carregamento inicial
    adicionarEventListenersBusca();
});