document.addEventListener('DOMContentLoaded', function() {
    // Seletores dos elementos da barra de busca e grid de posters
    const inputBusca = document.querySelector('.barra-topo input');
    const iconeBusca = document.querySelector('.barra-topo .icone-lupa');
    const gridPosters = document.querySelector('.grade-posters');
    
    // Guarda o conteúdo original para restaurar se limpar a busca
    let conteudoOriginal = gridPosters ? gridPosters.innerHTML : '';
    
    /*
     Função de navegação para página de detalhes do jogo.
     Redireciona para a rota de detalhes usando o id e tipo.
     */
    function navegarParaDetalhes(id, tipo) {
        const url = `/detalhes/${tipo}/${id}`;
        window.location.href = url;
    }

    /*
     Detecta se o usuário está em um dispositivo mobile.
     Retorna true para telas pequenas ou user agents de mobile.
     */
    function isMobile() {
        return window.innerWidth <= 768 || 
               /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    /*
     Adiciona eventos de clique ao card do jogo.
     No mobile: duplo clique para abrir detalhes.
     No desktop: clique único.
     */
    function adicionarEventoCard(card) {
        card.style.cursor = 'pointer';
        
        if (isMobile()) {
            // Mobile: duplo clique para abrir detalhes
            card.addEventListener('click', function(e) {
                e.preventDefault();
                
                if (!this.classList.contains('ativo')) {
                    document.querySelectorAll('[data-tipo="jogo"]').forEach(c => c.classList.remove('ativo'));
                    this.classList.add('ativo');
                } else {
                    const id = this.getAttribute('data-id');
                    navegarParaDetalhes(id, 'jogo');
                }
            });
        } else {
            // Desktop: clique único para abrir detalhes
            card.addEventListener('click', function(e) {
                e.preventDefault();
                const id = this.getAttribute('data-id');
                navegarParaDetalhes(id, 'jogo');
            });
        }
    }
    
    /*
     Função para buscar jogos pelo termo informado.
     Atualiza o grid de posters com os resultados ou mensagens de erro.
     */
    async function buscarJogos(termo) {
        if (!termo.trim()) {
            restaurarOriginal();
            return;
        }
        
        try {
            // Exibe loading enquanto busca
            gridPosters.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; color: white; padding: 50px;">
                    <i class="fas fa-spinner fa-spin fa-2x"></i>
                    <p style="margin-top: 10px;">Consultando o arquivo...</p>
                </div>
            `;
            
            // Faz requisição para a API de busca de jogos
            const response = await fetch(`/api/busca/jogos?q=${encodeURIComponent(termo)}`);
            const jogos = await response.json();
            
            // Se não houver resultados, exibe mensagem de "sem resultados"
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
            
            // Limpa o grid antes de adicionar os novos cards
            gridPosters.innerHTML = '';
            
            // Cria e adiciona os cards dos jogos encontrados
            jogos.forEach(jogo => {
                const imagemSrc = jogo.poster || jogo.poster_url || 'https://via.placeholder.com/300x450?text=Sem+Imagem';
                
                const divCard = document.createElement('div');
                divCard.className = 'game-card';
                divCard.style.height = '100%';
                divCard.setAttribute('data-id', jogo.id);
                divCard.setAttribute('data-tipo', 'jogo');
                
                divCard.innerHTML = `
                    <div class="item-poster poster-clean" style="height: 100%; width: 100%;">
                        <img src="${imagemSrc}" 
                             alt="${jogo.titulo}" 
                             class="poster-jogos" 
                             loading="lazy"
                             style="height: 100%; width: 100%; object-fit: cover; object-position: center top; display: block;">
                        
                        <div class="game-info-overlay">
                            <h3 class="game-title">${jogo.titulo}</h3>
                        </div>
                    </div>
                `;
                
                gridPosters.appendChild(divCard);
                adicionarEventoCard(divCard);
            });
            
        } catch (error) {
            // Em caso de erro na requisição, exibe mensagem de erro
            console.error('Erro na busca:', error);
            gridPosters.innerHTML = `<p style="color: white; grid-column: 1/-1; text-align: center;">Erro ao conectar com o servidor.</p>`;
        }
    }
    
    /*
     Restaura o grid de posters para o conteúdo original.
     Também readiciona os eventos de clique nos cards originais.
     */
    function restaurarOriginal() {
        gridPosters.innerHTML = conteudoOriginal;
        
        // Adiciona eventos nos cards originais
        const cardsOriginais = gridPosters.querySelectorAll('[data-tipo="jogo"]');
        cardsOriginais.forEach(card => adicionarEventoCard(card));
    }

    // Listener para clique no ícone de busca
    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
        iconeBusca.addEventListener('click', (e) => {
            e.preventDefault();
            buscarJogos(inputBusca.value);
        });
    }
    
    // Listener para pressionar Enter no campo de busca
    if (inputBusca) {
        inputBusca.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarJogos(inputBusca.value);
            }
        });
        
        // Listener para limpar busca ao apagar o campo
        inputBusca.addEventListener('input', (e) => {
            if (e.target.value === '') restaurarOriginal();
        });
    }
    
    /*
     Função global para limpar a busca e restaurar o grid original.
     */
    window.limparBusca = function() {
        if (inputBusca) inputBusca.value = '';
        restaurarOriginal();
    };
});