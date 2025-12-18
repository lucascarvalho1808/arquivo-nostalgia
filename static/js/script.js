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