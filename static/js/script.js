// Função para rolar para a esquerda (com loop)
function sliderScrollLeft(id) {
    const slider = document.getElementById(id);
    
    if (slider.scrollLeft === 0) {
        slider.scrollTo({
            left: slider.scrollWidth,
            behavior: 'smooth'
        });
    } else {
        slider.scrollBy({
            left: -320,
            behavior: 'smooth'
        });
    }
}

// Função para rolar para a direita (com loop)
function sliderScrollRight(id) {
    const slider = document.getElementById(id);
    
    if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) {
        slider.scrollTo({
            left: 0,
            behavior: 'smooth'
        });
    } else {
        slider.scrollBy({
            left: 320,
            behavior: 'smooth'
        });
    }
}

// Sistema de navegação para páginas de detalhes
function navegarParaDetalhes(id, tipo) {
    const url = `/detalhes/${tipo}/${id}`;
    window.location.href = url;
}

// Detecta se é dispositivo móvel
function isMobile() {
    return window.innerWidth <= 768 || 
           /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Adiciona eventos de clique nos cards
document.addEventListener("DOMContentLoaded", function() {
    
    // Filmes e Séries: clique único (desktop e mobile)
    const filmesCards = document.querySelectorAll('[data-tipo="filme"], [data-tipo="serie"]');
    
    filmesCards.forEach(card => {
        card.style.cursor = 'pointer';
        
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-id');
            const tipo = this.getAttribute('data-tipo');
            navegarParaDetalhes(id, tipo);
        });
    });

    // Jogos: comportamento especial no mobile
    const jogosCards = document.querySelectorAll('[data-tipo="jogo"]');
    
    jogosCards.forEach(card => {
        card.style.cursor = 'pointer';
        
        if (isMobile()) {
            // Mobile: duplo clique
            card.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Primeiro clique: ativa hover
                if (!this.classList.contains('ativo')) {
                    jogosCards.forEach(c => c.classList.remove('ativo'));
                    this.classList.add('ativo');
                } else {
                    // Segundo clique: navega
                    const id = this.getAttribute('data-id');
                    navegarParaDetalhes(id, 'jogo');
                }
            });
            
            // Remove 'ativo' ao clicar fora
            document.addEventListener('click', function(e) {
                if (!e.target.closest('[data-tipo="jogo"]')) {
                    jogosCards.forEach(c => c.classList.remove('ativo'));
                }
            });
            
        } else {
            // Desktop: clique único
            card.addEventListener('click', function(e) {
                e.preventDefault();
                const id = this.getAttribute('data-id');
                navegarParaDetalhes(id, 'jogo');
            });
        }
    });

    console.log('✅ Eventos de navegação carregados!');
    console.log(`📱 Modo: ${isMobile() ? 'Mobile' : 'Desktop'}`);
});