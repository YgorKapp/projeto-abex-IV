document.querySelector('.btn_localizacao').addEventListener('click', function() {

    document.querySelector('.localizacao').style.display = 'none';
    document.querySelector('.btn_localizacao').style.display = 'none';
    
    const items = document.querySelectorAll('.items');
    items.forEach(item => {
        item.style.display = 'flex';
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const hamburger = document.querySelector(".hamburger");
    const closeBtn = document.querySelector(".close-btn");

    // Abrir o menu
    hamburger.addEventListener("click", () => {
        sidebar.classList.add("open");
    });

    // Fechar o menu
    closeBtn.addEventListener("click", () => {
        sidebar.classList.remove("open");
    });
});

