# main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

# Lista para guardar las conexiones de WebSocket
clients: List[WebSocket] = []

# Servir archivos estáticos (JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    # Devuelve la página HTML con el cliente WebSocket
    html = """
    <html>
        <head>
            <title>FastAPI WebSocket Chat</title>
            <script src="/static/script.js"></script>
        </head>
        <body>
            <h1>FastAPI WebSocket Chat</h1>
            <textarea id="messages" cols="100" rows="20" readonly></textarea><br><br>
            <input type="text" id="message_input" placeholder="Escribe un mensaje..." />
            <button onclick="sendMessage()">Enviar</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Aceptar la conexión WebSocket
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # Recibir los mensajes de los clientes
            data = await websocket.receive_text()
            # Enviar el mensaje a todos los clientes conectados
            for client in clients:
                if client != websocket:  # Evitar enviar al mismo cliente
                    await client.send_text(f"Usuario dijo: {data}")
    except WebSocketDisconnect:
        # Eliminar al cliente desconectado
        clients.remove(websocket)
        print("Un cliente se ha desconectado.")
