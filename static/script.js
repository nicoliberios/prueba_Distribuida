// static/script.js

const ws = new WebSocket("ws://localhost:8000/ws");

// Enviar mensajes cuando se recibe uno
ws.onmessage = function(event) {
    const messages = document.getElementById("messages");
    messages.value += event.data + "\n"; // Mostrar los mensajes recibidos
};

function sendMessage() {
    const messageInput = document.getElementById("message_input");
    const message = messageInput.value;
    ws.send(message); // Enviar el mensaje al servidor WebSocket
    messageInput.value = ''; // Limpiar el campo de entrada
}
