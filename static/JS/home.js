document.getElementById('hamburger').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');

    if (sidebar.classList.contains('open')) {
        
        sidebar.classList.remove('open');
        sidebar.style.left = '-50%';
    } else {
        
        sidebar.classList.add('open');
        sidebar.style.left = '0'; 
    }
});

document.getElementById('closeBtn').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.remove('open');
    sidebar.style.left = '-50%';
});

document.querySelector('.btn_localizacao').addEventListener('click', function() {

    document.querySelector('.localizacao').style.display = 'none';
    document.querySelector('.btn_localizacao').style.display = 'none';
    
    const items = document.querySelectorAll('.items');
    items.forEach(item => {
        item.style.display = 'flex';
    });
});
