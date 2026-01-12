document.addEventListener('DOMContentLoaded', function() {
    const btnsFiltro = document.querySelectorAll('.btn-filtro');
    const posters = document.querySelectorAll('.item-poster');
    const iconeBusca = document.querySelector('.icone-busca');
    
    // Cursor pointer no ícone de busca
    if (iconeBusca) {
        iconeBusca.style.cursor = 'pointer';
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
});