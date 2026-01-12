const botoes = document.querySelectorAll('.btn-filtro');
        const cards = document.querySelectorAll('.poster-vazio');

        botoes.forEach(botao => {
            botao.addEventListener('click', () => {
                
                // 1. Muda a cor do botão ativo
                botoes.forEach(b => b.classList.remove('ativo'));
                botao.classList.add('ativo');

                // 2. Pega o texto do botão e força MAIÚSCULO (para evitar erro de digitação)
                const categoria = botao.innerText.toUpperCase().trim();

                // 3. Filtra os cards
                cards.forEach(card => {
                    let deveMostrar = false;

                    if (categoria === 'TODOS') {
                        deveMostrar = true;
                    } 
                    else if (categoria === 'FILMES' && card.classList.contains('tipo-filme')) {
                        deveMostrar = true;
                    } 
                    // O "includes" ajuda a evitar problema com o acento de SÉRIES
                    else if (categoria.includes('SÉRIES') && card.classList.contains('tipo-serie')) {
                        deveMostrar = true;
                    } 
                    else if (categoria === 'JOGOS' && card.classList.contains('tipo-jogo')) {
                        deveMostrar = true;
                    }

                    // Aplica a visibilidade
                    if (deveMostrar) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });