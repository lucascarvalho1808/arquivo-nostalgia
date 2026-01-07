// Função para rolar para a esquerda (com loop)
function sliderScrollLeft(id) {
    const slider = document.getElementById(id);
    
    if (slider.scrollLeft === 0) {
        slider.scrollTo({ left: slider.scrollWidth, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -300, behavior: 'smooth' });
    }
}

// Função para rolar para a direita (com loop)
function sliderScrollRight(id) {
    const slider = document.getElementById(id);
    
    if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) {
        slider.scrollTo({ left: 0, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: 300, behavior: 'smooth' });
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os wrappers de jogos (Steam e RAWG)
    const cards = document.querySelectorAll('.poster-wrapper, .game-card');

    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Verifica se é um dispositivo touch ou tela pequena (opcional, mas recomendado)
            // Se quiser que funcione assim no PC também, pode remover o 'if'
            const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);

            if (isTouch) {
                // Se o card JÁ tem a classe ativo...
                if (card.classList.contains('ativo')) {
                    // ...Deixa o navegador seguir o link normalmente (2º clique)
                    return true; 
                } else {
                    // ...Se NÃO tem a classe ativo (1º clique)
                    e.preventDefault(); // Impede de entrar no link
                    
                    // Remove a classe 'ativo' de todos os outros jogos abertos
                    cards.forEach(c => c.classList.remove('ativo'));
                    
                    // Adiciona a classe 'ativo' neste jogo
                    card.classList.add('ativo');
                }
            }
        });
    });

    // Lógica para "Limpar a tela" ao clicar fora
    document.addEventListener('click', function(e) {
        // Se o clique NÃO foi dentro de nenhum card de jogo
        if (!e.target.closest('.poster-wrapper') && !e.target.closest('.game-card')) {
            // Remove o ativo de todo mundo
            cards.forEach(c => c.classList.remove('ativo'));
        }
    });
});