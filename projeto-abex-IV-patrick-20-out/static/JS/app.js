setTimeout(function() {
    const container1 = document.getElementById('button');
    const container2 = document.getElementById('animação');

    container1.classList.remove('hidden');
    container1.classList.add('show');
    container2.classList.remove('animação');
}, 1500);

document.getElementById('backButton').onclick = function() {
    window.history.back();
    return false; // Evita que o link siga a URL "#"
};