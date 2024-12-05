// static/js/app.js

document.addEventListener('DOMContentLoaded', () => {
    // Manipulação de 'button' e 'animação' com verificação
    setTimeout(function() {
        const container1 = document.getElementById('button');
        const container2 = document.getElementById('animação');

        if (container1) {
            container1.classList.remove('hidden');
            container1.classList.add('show');
        }

        if (container2) {
            container2.classList.remove('animação');
        }
    }, 1500);

    // Manipulação do 'backButton' com verificação
    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.onclick = function(event) {
            event.preventDefault(); // Evita comportamento padrão
            window.history.back();
        };
    }
});
