document.addEventListener('DOMContentLoaded', function() {
    const btnsFiltro = document.querySelectorAll('.btn-filtro');
    const posters = document.querySelectorAll('.item-poster');
    const iconeBusca = document.querySelector('.icone-busca');
    
    // Cursor pointer no ícone de busca
    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
    }
    
    // Event listeners de clique nos posters
    function adicionarEventListenersResultados() {
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
    
    // Filtros
    btnsFiltro.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove 'ativo' de todos
            btnsFiltro.forEach(b => b.classList.remove('ativo'));
            // Adiciona 'ativo' no clicado
            this.classList.add('ativo');
            
            const filtro = this.dataset.filtro;
            
            posters.forEach(poster => {
                if (filtro === 'todos') {
                    poster.style.display = '';
                } else {
                    if (poster.dataset.tipo === filtro) {
                        poster.style.display = '';
                    } else {
                        poster.style.display = 'none';
                    }
                }
            });
        });
    });
    
    // Chamar no carregamento inicial
    adicionarEventListenersResultados();
});

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
