let chatId = 0
console.log('Hello')

let ws = new WebSocket(`ws://localhost:8000/chat_ws/${chatId}`)
document.getElementById('chat_id_text').innerHTML = chatId

ws.onmessage = function(event) {
    let messages = document.getElementById('messages')
    let message = document.createElement('li')
    let content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};

function sendMessage(event) {
    let input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}

function connectToChat(){
    chatId = document.getElementById('chat_id').value
    ws = new WebSocket(`ws://localhost:8000/chat_ws/${chatId}`)
    document.getElementById('chat_id_text').innerHTML = chatId
}