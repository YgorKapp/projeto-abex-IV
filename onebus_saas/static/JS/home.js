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

