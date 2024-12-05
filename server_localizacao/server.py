import asyncio
import json
from aiohttp import web
import websockets

# Dicionário para armazenar informações dos clientes
clients = {}

# Rota para servir a página administrativa
async def admin_page(request):
    return web.FileResponse('./static/admin.html')

# Rota para servir o cliente HTML
async def client_page(request):
    return web.FileResponse('./static/index.html')

# WebSocket Handler
async def websocket_handler(websocket, path):
    client_id = None  # Inicializa client_id com None
    try:
        # Recebe o nome do usuário como a primeira mensagem
        name_message = await websocket.recv()
        name_data = json.loads(name_message)
        user_name = name_data.get("name")

        if not user_name:
            await websocket.send(json.dumps({"error": "Nome de usuário não fornecido."}))
            await websocket.close()
            return

        # Atribui um ID único para o cliente
        client_id = id(websocket)
        clients[client_id] = {
            "websocket": websocket,
            "name": user_name,
            "location": None,
            "history": []
        }
        print(f"Conexão estabelecida com {user_name} (ID: {client_id})")

        # Envia uma mensagem de confirmação ao cliente
        await websocket.send(json.dumps({"status": "Conectado", "client_id": client_id}))

        async for message in websocket:
            data = json.loads(message)
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude is not None and longitude is not None:
                clients[client_id]["location"] = {"latitude": latitude, "longitude": longitude}
                clients[client_id]["history"].append({"latitude": latitude, "longitude": longitude})

                print(f"Localização recebida de {clients[client_id]['name']} (ID: {client_id}): Latitude {latitude}, Longitude {longitude}")

                # Broadcast das localizações para todos os clientes
                await broadcast_locations()
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Conexão com cliente encerrada: {e}")
    finally:
        # Remove o cliente da lista ao desconectar, se client_id foi definido
        if client_id is not None and client_id in clients:
            print(f"Cliente {clients[client_id]['name']} (ID: {client_id}) desconectado.")
            del clients[client_id]
            await broadcast_locations()

# Função para broadcast das localizações
async def broadcast_locations():
    # Prepara os dados de todas as localizações
    locations = {
        client["name"]: {
            "latitude": client["location"]["latitude"],
            "longitude": client["location"]["longitude"],
            "history": client["history"]
        }
        for client in clients.values()
        if client["location"] is not None
    }

    # Se não houver clientes com localização, envia uma mensagem vazia
    if locations:
        message = json.dumps(locations)
    else:
        message = json.dumps({})

    # Envia a mensagem para todos os clientes conectados
    if clients:
        await asyncio.gather(*[client["websocket"].send(message) for client in clients.values()])

# Função para inicializar o servidor WebSocket e HTTP
async def init_servers():
    # Configura o servidor WebSocket
    websocket_server = await websockets.serve(websocket_handler, "127.0.0.1", 5001)

    # Configura o servidor HTTP com aiohttp
    app = web.Application()
    app.router.add_get('/admin', admin_page)
    app.router.add_get('/client', client_page)
    app.router.add_static('/static/', path='./static', name='static')

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()

    print("Servidor WebSocket ouvindo em ws://127.0.0.1:5001")
    print("Servidor HTTP ouvindo em http://127.0.0.1:8080")

    # Mantém o servidor em execução
    await asyncio.Future()

# Executa os servidores
if __name__ == '__main__':
    asyncio.run(init_servers())
