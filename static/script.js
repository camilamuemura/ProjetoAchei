document.addEventListener('DOMContentLoaded', function () {
    // Código do carrossel
    const carrosselImagens = document.querySelector('.carrossel-imagens');
    if (carrosselImagens) {
        const imagens = document.querySelectorAll('.carrossel-imagens img');
        const prevButton = document.querySelector('.prev');
        const nextButton = document.querySelector('.next');
        
        let currentIndex = 0;

        function showSlide(index) {
            const offset = -index * 100;
            carrosselImagens.style.transform = `translateX(${offset}%)`;
        }

        function nextSlide() {
            currentIndex = (currentIndex + 1) % imagens.length;
            showSlide(currentIndex);
        }

        if (nextButton && prevButton) {
            nextButton.addEventListener('click', function () {
                nextSlide();
            });

            prevButton.addEventListener('click', function () {
                currentIndex = (currentIndex - 1 + imagens.length) % imagens.length;
                showSlide(currentIndex);
            });
        }

        // Muda para a próxima imagem a cada 3 segundos
        setInterval(nextSlide, 3000);

        showSlide(currentIndex);
    }

    // Código do dropdown
    const menu = document.querySelector('.menu img');
    const dropdownContent = document.querySelector('.dropdown-content');

    if (menu && dropdownContent) {
        menu.addEventListener('click', function (event) {
            event.stopPropagation(); // Evita que o clique no ícone feche o dropdown
            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
        });

        // Fechar o dropdown se clicar fora dele
        window.addEventListener('click', function () {
            dropdownContent.style.display = 'none';
        });

        // Evitar fechar o dropdown ao clicar nele
        dropdownContent.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    }
});
