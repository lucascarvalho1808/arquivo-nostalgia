// Função para rolar o slider para a esquerda (com loop)
function sliderScrollLeft(id) {
    const slider = document.getElementById(id);
    
    // Se estiver no início, volta para o final 
    if (slider.scrollLeft === 0) {
        slider.scrollTo({
            left: slider.scrollWidth,
            behavior: 'smooth'
        });
    } else {
        // Caso contrário, rola 320px para a esquerda
        slider.scrollBy({
            left: -320,
            behavior: 'smooth'
        });
    }
}

// Função para rolar o slider para a direita (com loop)
function sliderScrollRight(id) {
    const slider = document.getElementById(id);
    
    // Se estiver no final, volta para o início 
    if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) {
        slider.scrollTo({
            left: 0,
            behavior: 'smooth'
        });
    } else {
        // Caso contrário, rola 320px para a direita
        slider.scrollBy({
            left: 320,
            behavior: 'smooth'
        });
    }
}

// Sistema de navegação para páginas de detalhes
function navegarParaDetalhes(id, tipo) {
    // Monta a URL de detalhes e redireciona
    const url = `/detalhes/${tipo}/${id}`;
    window.location.href = url;
}

// Detecta se o usuário está em um dispositivo móvel
function isMobile() {
    return window.innerWidth <= 768 || 
           /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Adiciona eventos de clique nos cards ao carregar a página
document.addEventListener("DOMContentLoaded", function() {
    
    // Seleciona todos os cards de filmes e séries
    const filmesCards = document.querySelectorAll('[data-tipo="filme"], [data-tipo="serie"]');
    
    filmesCards.forEach(card => {
        card.style.cursor = 'pointer';
        
        // Clique único para navegar para detalhes (desktop e mobile)
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-id');
            const tipo = this.getAttribute('data-tipo');
            navegarParaDetalhes(id, tipo);
        });
    });

    // Seleciona todos os cards de jogos
    const jogosCards = document.querySelectorAll('[data-tipo="jogo"]');
    
    jogosCards.forEach(card => {
        card.style.cursor = 'pointer';
        
        if (isMobile()) {
            // Mobile: duplo clique para abrir detalhes
            card.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Primeiro clique: ativa hover visual
                if (!this.classList.contains('ativo')) {
                    jogosCards.forEach(c => c.classList.remove('ativo'));
                    this.classList.add('ativo');
                } else {
                    // Segundo clique: navega para detalhes
                    const id = this.getAttribute('data-id');
                    navegarParaDetalhes(id, 'jogo');
                }
            });
            
            // Remove 'ativo' ao clicar fora de qualquer card de jogo
            document.addEventListener('click', function(e) {
                if (!e.target.closest('[data-tipo="jogo"]')) {
                    jogosCards.forEach(c => c.classList.remove('ativo'));
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
    });

    // Mensagens de debug no console
    console.log(' Eventos de navegação carregados!');
    console.log(` Modo: ${isMobile() ? 'Mobile' : 'Desktop'}`);
});