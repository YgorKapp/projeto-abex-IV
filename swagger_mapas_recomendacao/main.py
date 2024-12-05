from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import requests
import math

app = FastAPI(
    title="API de Localização OneBus",
    description="API para obter coordenadas, endereços e encontrar pontos próximos.",
    version="1.0.0"
)

# Modelo de Dados
class Endereco(BaseModel):
    nome_exibicao: str
    latitude: float
    longitude: float

class Coordenada(BaseModel):
    latitude: float
    longitude: float

# Lista estática de pontos. Em produção, considere usar um banco de dados.
LISTA_PONTOS: List[Endereco] = [
    Endereco(nome_exibicao="Ponto A", latitude=-23.550520, longitude=-46.633308),
    Endereco(nome_exibicao="Ponto B", latitude=-22.906847, longitude=-43.172897),
    Endereco(nome_exibicao="Ponto C", latitude=-19.916681, longitude=-43.934493),
    Endereco(nome_exibicao="Ponto D", latitude=-3.7319, longitude=-38.5267),
    Endereco(nome_exibicao="Ponto E", latitude=-30.0346, longitude=-51.2177),
    Endereco(nome_exibicao="Ponto F", latitude=-15.7942, longitude=-47.8822),
    # Adicione mais pontos conforme necessário
]

# Função para converter graus em radianos
def graus_para_radianos(graus: float) -> float:
    return graus * math.pi / 180

# Função para calcular a distância usando a Fórmula de Haversine
def calcular_distancia(coord1: Coordenada, coord2: Coordenada) -> float:
    R = 6371  # Raio da Terra em km
    lat1_rad = graus_para_radianos(coord1.latitude)
    lat2_rad = graus_para_radianos(coord2.latitude)
    delta_lat = graus_para_radianos(coord2.latitude - coord1.latitude)
    delta_lon = graus_para_radianos(coord2.longitude - coord1.longitude)

    a = math.sin(delta_lat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * \
        math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia = R * c
    return distancia

# Endpoint para obter coordenadas a partir de um endereço
@app.get("/obter_coordenadas", response_model=Coordenada, summary="Obter Coordenadas")
def obter_coordenadas(endereco: str = Query(..., description="Endereço para obter as coordenadas")):
    if not endereco.strip():
        raise HTTPException(status_code=400, detail="O parâmetro 'endereco' é obrigatório.")

    url_base = "https://nominatim.openstreetmap.org/search"
    parametros = {
        'q': endereco,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'ProjetoOneBus/1.0'
    }

    resposta = requests.get(url_base, params=parametros, headers=headers)
    if resposta.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao se comunicar com o serviço de geocodificação.")

    dados = resposta.json()
    if not dados:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado para o endereço fornecido.")

    primeiro_endereco = dados[0]
    coordenadas = Coordenada(
        latitude=float(primeiro_endereco['lat']),
        longitude=float(primeiro_endereco['lon'])
    )
    return coordenadas

# Endpoint para obter endereço a partir de coordenadas
@app.post("/obter_endereco_por_coordenadas", summary="Obter Endereço por Coordenadas")
def obter_endereco_por_coordenadas(coordenada: Coordenada):
    url_base = "https://nominatim.openstreetmap.org/reverse"
    parametros = {
        'lat': coordenada.latitude,
        'lon': coordenada.longitude,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'ProjetoOneBus/1.0'
    }

    resposta = requests.get(url_base, params=parametros, headers=headers)
    if resposta.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao se comunicar com o serviço de geocodificação.")

    dados = resposta.json()
    if 'display_name' not in dados:
        raise HTTPException(status_code=404, detail="Nenhum endereço encontrado para as coordenadas fornecidas.")

    endereco = dados['display_name']
    return {"endereco": endereco}

# Endpoint para obter pontos próximos a um endereço
@app.get("/obter_pontos_proximos", summary="Obter Pontos Próximos")
def obter_pontos_proximos(
    endereco: str = Query(..., description="Endereço para encontrar pontos próximos"),
    quantidade: int = Query(5, ge=1, description="Número de pontos próximos a retornar")
):
    if not endereco.strip():
        raise HTTPException(status_code=400, detail="O parâmetro 'endereco' é obrigatório.")

    # Obter coordenadas do endereço
    url_base = "https://nominatim.openstreetmap.org/search"
    parametros = {
        'q': endereco,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'ProjetoOneBus/1.0'
    }

    resposta = requests.get(url_base, params=parametros, headers=headers)
    if resposta.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao se comunicar com o serviço de geocodificação.")

    dados = resposta.json()
    if not dados:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado para o endereço fornecido.")

    primeiro_endereco = dados[0]
    coordenada_atual = Coordenada(
        latitude=float(primeiro_endereco['lat']),
        longitude=float(primeiro_endereco['lon'])
    )

    # Calcular distância para cada ponto na lista
    lista_com_distancias = []
    for ponto in LISTA_PONTOS:
        distancia = calcular_distancia(coordenada_atual, Coordenada(latitude=ponto.latitude, longitude=ponto.longitude))
        lista_com_distancias.append({
            'nome': ponto.nome_exibicao,
            'latitude': ponto.latitude,
            'longitude': ponto.longitude,
            'distancia_em_km': round(distancia, 2)
        })

    # Ordenar pela distância e selecionar os N mais próximos
    lista_com_distancias.sort(key=lambda x: x['distancia_em_km'])
    proximos = lista_com_distancias[:quantidade]

    return {
        "endereco_original": primeiro_endereco.get('display_name', endereco),
        "coordenadas": coordenada_atual,
        "pontos_proximos": proximos
    }

# Modelo para adicionar um novo ponto
class NovoEndereco(BaseModel):
    nome_exibicao: str
    latitude: float
    longitude: float

# Endpoint para adicionar um novo ponto com validação de distância
@app.post("/adicionar_ponto", summary="Adicionar Novo Ponto de Localização")
def adicionar_ponto(
    novo_ponto: NovoEndereco,
    distancia_minima_km: float = Query(1.0, ge=0.0, description="Distância mínima em km em relação aos pontos existentes")
):
    nova_coordenada = Coordenada(latitude=novo_ponto.latitude, longitude=novo_ponto.longitude)

    # Verificar a distância em relação aos pontos existentes
    for ponto in LISTA_PONTOS:
        coordenada_existente = Coordenada(latitude=ponto.latitude, longitude=ponto.longitude)
        distancia = calcular_distancia(nova_coordenada, coordenada_existente)
        if distancia < distancia_minima_km:
            raise HTTPException(
                status_code=400,
                detail=f"A distância entre '{novo_ponto.nome_exibicao}' e '{ponto.nome_exibicao}' é {distancia:.2f} km, que é menor que a distância mínima requerida de {distancia_minima_km} km."
            )

    # Se todas as validações passarem, adicionar o ponto
    novo_endereco = Endereco(
        nome_exibicao=novo_ponto.nome_exibicao,
        latitude=novo_ponto.latitude,
        longitude=novo_ponto.longitude
    )
    LISTA_PONTOS.append(novo_endereco)
    return {"mensagem": "Ponto adicionado com sucesso.", "ponto": novo_endereco}

# Endpoint adicional para validar a distância entre dois pontos específicos
@app.get("/validar_distancia", summary="Validar Distância entre Dois Pontos")
def validar_distancia(
    ponto1: str = Query(..., description="Nome do primeiro ponto"),
    ponto2: str = Query(..., description="Nome do segundo ponto"),
    distancia_minima_km: float = Query(1.0, ge=0.0, description="Distância mínima em km")
):
    # Encontrar os pontos na lista
    ponto_a = next((p for p in LISTA_PONTOS if p.nome_exibicao.lower() == ponto1.lower()), None)
    ponto_b = next((p for p in LISTA_PONTOS if p.nome_exibicao.lower() == ponto2.lower()), None)

    if not ponto_a:
        raise HTTPException(status_code=404, detail=f"Ponto '{ponto1}' não encontrado.")
    if not ponto_b:
        raise HTTPException(status_code=404, detail=f"Ponto '{ponto2}' não encontrado.")

    coord_a = Coordenada(latitude=ponto_a.latitude, longitude=ponto_a.longitude)
    coord_b = Coordenada(latitude=ponto_b.latitude, longitude=ponto_b.longitude)
    distancia = calcular_distancia(coord_a, coord_b)

    if distancia < distancia_minima_km:
        return {
            "valido": False,
            "mensagem": f"A distância entre '{ponto1}' e '{ponto2}' é {distancia:.2f} km, que é menor que a distância mínima requerida de {distancia_minima_km} km."
        }
    else:
        return {
            "valido": True,
            "distancia_em_km": round(distancia, 2),
            "mensagem": f"A distância entre '{ponto1}' e '{ponto2}' é {distancia:.2f} km, atendendo à distância mínima requerida de {distancia_minima_km} km."
        }

# Opcional: Endpoint para remover um ponto existente
@app.delete("/remover_ponto", summary="Remover Ponto de Localização")
def remover_ponto(nome_exibicao: str = Query(..., description="Nome do ponto a ser removido")):
    global LISTA_PONTOS
    ponto_existente = next((p for p in LISTA_PONTOS if p.nome_exibicao.lower() == nome_exibicao.lower()), None)
    if not ponto_existente:
        raise HTTPException(status_code=404, detail=f"Ponto '{nome_exibicao}' não encontrado.")

    LISTA_PONTOS = [p for p in LISTA_PONTOS if p.nome_exibicao.lower() != nome_exibicao.lower()]
    return {"mensagem": f"Ponto '{nome_exibicao}' removido com sucesso."}

# Opcional: Endpoint para listar todos os pontos
@app.get("/listar_pontos", summary="Listar Todos os Pontos de Localização", response_model=List[Endereco])
def listar_pontos():
    return LISTA_PONTOS
