document.addEventListener('DOMContentLoaded', function() {
    const inputBusca = document.querySelector('.barra-topo input');
    const iconeBusca = document.querySelector('.barra-topo .icone-lupa');
    const gridPosters = document.querySelector('.grade-posters');
    // Removi a seleção do botão pois não vamos mais mexer nele
    
    // Guarda o conteúdo original para restaurar se limpar a busca
    let conteudoOriginal = gridPosters ? gridPosters.innerHTML : '';
    
    async function buscarJogos(termo) {
        if (!termo.trim()) {
            restaurarOriginal();
            return;
        }
        
        try {
            gridPosters.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; color: white; padding: 50px;">
                    <i class="fas fa-spinner fa-spin fa-2x"></i>
                    <p style="margin-top: 10px;">Consultando o arquivo...</p>
                </div>
            `;
            
            // REMOVIDO: O código que escondia o botão "Ver Mais"
            
            const response = await fetch(`/api/busca/jogos?q=${encodeURIComponent(termo)}`);
            const jogos = await response.json();
            
            if (jogos.length === 0) {
                gridPosters.innerHTML = `
                    <div style="grid-column: 1/-1; text-align: center; color: white; padding: 40px;">
                        <i class="fas fa-ghost fa-3x" style="margin-bottom: 15px; opacity: 0.5;"></i>
                        <p>Nenhum jogo encontrado para "<strong>${termo}</strong>".</p>
                        <button onclick="limparBusca()" style="margin-top: 15px; padding: 8px 16px; cursor: pointer; background: #ff4757; border: none; color: white; border-radius: 4px;">Limpar Busca</button>
                    </div>
                `;
                return;
            }
            
            gridPosters.innerHTML = jogos.map(jogo => {
                const imagemSrc = jogo.poster || jogo.poster_url || 'https://via.placeholder.com/300x450?text=Sem+Imagem';
                
                return `
                <div class="game-card" style="height: 100%;">
                    <div class="item-poster poster-clean" style="height: 100%; width: 100%;">
                        
                        <a href="#" onclick="return false;" style="display: block; height: 100%; width: 100%; position: relative; cursor: default;">
                            
                            <img src="${imagemSrc}" 
                                 alt="${jogo.titulo}" 
                                 class="poster-jogos" 
                                 loading="lazy"
                                 style="height: 100%; width: 100%; object-fit: cover; object-position: center top; display: block;">
                            
                            <div class="game-info-overlay">
                                <h3 class="game-title">${jogo.titulo}</h3>
                            </div>
                            
                        </a>
                    </div>
                </div>
                `;
            }).join('');
            
        } catch (error) {
            console.error('Erro na busca:', error);
            gridPosters.innerHTML = `<p style="color: white; grid-column: 1/-1; text-align: center;">Erro ao conectar com o servidor.</p>`;
        }
    }
    
    function restaurarOriginal() {
        gridPosters.innerHTML = conteudoOriginal;
        // Não precisa mais restaurar o botão, pois ele nunca sumiu
    }

    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
        iconeBusca.addEventListener('click', (e) => {
            e.preventDefault();
            buscarJogos(inputBusca.value);
        });
    }
    
    if (inputBusca) {
        inputBusca.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarJogos(inputBusca.value);
            }
        });
        
        inputBusca.addEventListener('input', (e) => {
            if (e.target.value === '') restaurarOriginal();
        });
    }
    
    window.limparBusca = function() {
        if (inputBusca) inputBusca.value = '';
        restaurarOriginal();
    };
});