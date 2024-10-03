
// Referencia ao botão e à área onde os inputs serão inseridos
 const addInputButton = document.getElementById('add-input');
const inputArea = document.getElementById('input-area');

// Função para adicionar um novo campo de input
addInputButton.addEventListener('click', () => {
// Cria um novo div que conterá o input
const newInputContainer = document.createElement('div');
newInputContainer.classList.add('input-container');

// Cria o novo campo de input
const newInput = document.createElement('input');
newInput.type = 'text';
newInput.name = 'input[]';  // Nome do input com suporte a múltiplos valores
newInput.placeholder = 'Informe um ponto';

newInput.classList.add('input-cadastrar-ponto');
newInput.classList.add('input-cadastrar-ponto');

// Adiciona o campo de input ao div
newInputContainer.appendChild(newInput);

// Adiciona o novo div à área de inputs
inputArea.appendChild(newInputContainer);
});