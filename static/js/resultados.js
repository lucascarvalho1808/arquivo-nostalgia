document.addEventListener('DOMContentLoaded', function() {
    // Seletores dos botões de filtro, posters e ícone de busca
    const btnsFiltro = document.querySelectorAll('.btn-filtro');
    const posters = document.querySelectorAll('.item-poster');
    const iconeBusca = document.querySelector('.icone-busca');
    
    // Define cursor pointer no ícone de busca para indicar interatividade
    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
    }
    
    /*
     * Adiciona event listeners de clique nos posters da página de resultados.
     Ao clicar, redireciona para a página de detalhes do item (filme, série ou jogo).
     */
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
    
    /*
     Event listeners para os botões de filtro (filmes, séries, jogos, todos).
     Mostra ou esconde posters conforme o filtro selecionado.
     */
    btnsFiltro.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove a classe 'ativo' de todos os botões
            btnsFiltro.forEach(b => b.classList.remove('ativo'));
            // Adiciona a classe 'ativo' no botão clicado
            this.classList.add('ativo');
            
            const filtro = this.dataset.filtro;
            
            // Mostra ou esconde posters conforme o filtro selecionado
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
    
    // Chama a função para adicionar listeners nos posters ao carregar a página
    adicionarEventListenersResultados();
});

/*
 Cria e adiciona um poster de jogo na grade de posters.
 Suporta dois estilos: Steam (vertical) e RAWG (horizontal).
 */
function criarPoster(jogo) {
    if (!jogo.poster_url) return;
    
    const divPoster = document.createElement('div');
    
    if (jogo.origem_imagem === 'steam') {
        // ESTILO 1: STEAM (Vertical) 
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
        // ESTILO 2: RAWG (Horizontal forçado a preencher) 
        // Usa estilos inline para garantir o layout correto
        divPoster.className = 'game-card';
        divPoster.style.height = '100%'; 

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
