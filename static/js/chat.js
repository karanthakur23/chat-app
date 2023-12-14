console.log("chat.js is accessible")

const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('receiver').textContent);
console.log(receiver, ";;;;;;;;;")
console.log(message_username, ";;;;;;;;;")
console.log(id, ";;;;;;;;;")

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + receiver
    + '/'
);

chatSocket.onopen = function(e) {
    console.log("CONNECTION ESTABLISHED")
}

chatSocket.onclose = function(e) {
    console.log("CONNECTION CLOSED")
}

chatSocket.onerror = function(e) {
    console.log("ERROR OCCURED")
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    if(data.username == message_username){
        console.log("----->chat onmessage if")
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }else{
        console.log("------->chat onmessage else")
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){

    let message_input = document.querySelector('#message_input');

    const message = message_input.value.trim();
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': message_username,
        'receiver': receiver
    }))

    message_input.value = '';
}

const message_input = document.querySelector('#message_input');

message_input.addEventListener('keyup', function(event) {

    if (event.key === 'Enter') {

       event.preventDefault();

       const message = message_input.value.trim();

       if(message !== ''){
            chatSocket.send(JSON.stringify({
                'message' : message,
                'username' : message_username,
                'receiver':receiver
            }))

            message_input.value = '';
       }
    message_input.value = '';
    }
});