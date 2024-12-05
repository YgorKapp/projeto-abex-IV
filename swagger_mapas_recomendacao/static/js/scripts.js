document.addEventListener("DOMContentLoaded", () => {
    const mapSelector = document.getElementById("mapa");
    const addPointForm = document.getElementById("form-ponto");
    const createMapForm = document.getElementById("form-mapa");
    let currentMap = null;
    let map = L.map('map').setView([-23.550520, -46.633308], 13); // Coordenadas iniciais (São Paulo)

    // Adicionar camada de mapa base
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Variável para armazenar os marcadores
    let markers = {};

    // Função para buscar e popular a lista de mapas
    const fetchMapas = async () => {
        try {
            const response = await fetch('/mapas');
            if (!response.ok) {
                throw new Error('Erro ao buscar mapas.');
            }
            const mapas = await response.json();
            populateMapSelector(mapas);
        } catch (error) {
            console.error(error);
            alert('Não foi possível carregar a lista de mapas.');
        }
    };

    // Função para popular o select de mapas
    const populateMapSelector = (mapas) => {
        // Limpar opções existentes, exceto a primeira
        while (mapSelector.options.length > 1) {
            mapSelector.remove(1);
        }

        mapas.forEach(mapa => {
            const option = document.createElement("option");
            option.value = mapa.id;
            option.textContent = mapa.nome;
            mapSelector.appendChild(option);
        });
    };

    // Função para carregar um mapa específico
    const loadMapa = async (mapaId) => {
        try {
            const response = await fetch(`/mapas/${mapaId}`);
            if (!response.ok) {
                throw new Error('Erro ao carregar o mapa selecionado.');
            }
            const mapa = await response.json();
            displayMapa(mapa);
        } catch (error) {
            console.error(error);
            alert('Não foi possível carregar o mapa selecionado.');
        }
    };

    // Função para exibir o mapa no Leaflet
    const displayMapa = (mapa) => {
        // Limpar camadas anteriores
        map.eachLayer((layer) => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        markers = {}; // Resetar os marcadores

        // Ajustar a visualização do mapa
        if (mapa.pontos.length > 0) {
            const bounds = [];
            mapa.pontos.forEach(ponto => {
                const marker = L.marker([ponto.latitude, ponto.longitude]).addTo(map)
                    .bindPopup(`<b>${ponto.nome}</b><br>${ponto.descricao || ''}`);
                markers[ponto.id] = marker;
                bounds.push([ponto.latitude, ponto.longitude]);
            });
            map.fitBounds(bounds);
        } else {
            map.setView([-23.550520, -46.633308], 13); // Coordenadas padrão
        }
    };

    // Evento de seleção de mapa
    mapSelector.addEventListener("change", (event) => {
        const mapaId = event.target.value;
        if (mapaId) {
            currentMap = mapaId;
            loadMapa(mapaId);
        } else {
            // Limpar o mapa se nenhuma seleção for feita
            map.setView([-23.550520, -46.633308], 13);
            // Remover todos os marcadores
            for (let id in markers) {
                map.removeLayer(markers[id]);
            }
            markers = {};
            currentMap = null;
        }
    });

    // Evento de submissão do formulário para adicionar ponto
    addPointForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!currentMap) {
            alert('Por favor, selecione um mapa antes de adicionar um ponto.');
            return;
        }

        const nome = document.getElementById('nome').value;
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);
        const descricao = document.getElementById('descricao').value;

        const ponto = {
            nome: nome,
            latitude: latitude,
            longitude: longitude,
            descricao: descricao
        };

        try {
            const response = await fetch(`/mapas/${currentMap}/pontos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ponto)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro ao adicionar ponto.');
            }

            const novoPonto = await response.json();
            alert('Ponto adicionado com sucesso!');

            // Adicionar o marcador no mapa
            const marker = L.marker([novoPonto.latitude, novoPonto.longitude]).addTo(map)
                .bindPopup(`<b>${novoPonto.nome}</b><br>${novoPonto.descricao || ''}`);
            markers[novoPonto.id] = marker;

            // Ajustar os limites do mapa para incluir o novo marcador
            const latLng = [novoPonto.latitude, novoPonto.longitude];
            const currentBounds = map.getBounds();
            if (currentBounds.contains(latLng)) {
                // Já está dentro dos limites
            } else {
                map.setView(latLng, map.getZoom());
            }

            // Limpar o formulário
            addPointForm.reset();

        } catch (error) {
            console.error('Erro ao adicionar ponto:', error);
            alert(`Erro ao adicionar ponto: ${error.message}`);
        }
    });

    // Evento de submissão do formulário para criar mapa
    createMapForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const nome_mapa = document.getElementById("nome_mapa").value;
        const descricao_mapa = document.getElementById("descricao_mapa").value;

        const mapa = { nome: nome_mapa, descricao: descricao_mapa, pontos: [] };

        try {
            const response = await fetch(`/mapas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(mapa)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro ao criar mapa.');
            }

            const novoMapa = await response.json();
            alert('Mapa criado com sucesso!');
            // Atualizar a lista de mapas
            fetchMapas();
            // Limpar o formulário
            createMapForm.reset();
        } catch (error) {
            console.error('Erro ao criar mapa:', error);
            alert(`Erro ao criar mapa: ${error.message}`);
        }
    });

    // Inicialização: buscar mapas e configurar eventos
    fetchMapas();
});
