import math

def haversine(coord1, coord2):
    R = 6371  # Raio da Terra em km

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Converter graus para radianos
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Fórmula de Haversine
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia = R * c
    return distancia

def encontrar_pontos_proximos(pontos, ponto_atual, quantidade=5):
    distancia_pontos = []
    coord_atual = (ponto_atual['latitude'], ponto_atual['longitude'])

    for ponto in pontos:
        coord_ponto = (ponto['latitude'], ponto['longitude'])
        distancia = haversine(coord_atual, coord_ponto)
        distancia_pontos.append((ponto, distancia))

    # Ordenar pela distância
    distancia_pontos.sort(key=lambda x: x[1])

    # Retornar os N pontos mais próximos
    proximos = distancia_pontos[:quantidade]
    return proximos

# Exemplo de uso
if __name__ == "__main__":
    lista_pontos = [
        {'nome': 'Ponto A', 'latitude': -23.550520, 'longitude': -46.633308},
        {'nome': 'Ponto B', 'latitude': -22.906847, 'longitude': -43.172897},
        {'nome': 'Ponto C', 'latitude': -19.916681, 'longitude': -43.934493},
        {'nome': 'Ponto D', 'latitude': -3.7319, 'longitude': -38.5267},
        {'nome': 'Ponto E', 'latitude': -30.0346, 'longitude': -51.2177},
        {'nome': 'Ponto F', 'latitude': -15.7942, 'longitude': -47.8822},
    ]

    ponto_atual = {'nome': 'Ponto Atual', 'latitude': -23.550520, 'longitude': -46.633308}

    proximos = encontrar_pontos_proximos(lista_pontos, ponto_atual, quantidade=3)

    print(f"Pontos mais próximos de {ponto_atual['nome']}:")
    for ponto, distancia in proximos:
        print(f"{ponto['nome']}: {distancia:.2f} km")
