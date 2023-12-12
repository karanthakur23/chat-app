console.log("group_chat.js is accessible");

const messageUsername = JSON.parse(document.getElementById('json-message-username').textContent);
    const chatRoomIdElement = document.getElementById('chat_room_id').textContent;

    // const chatRoomIdElement = '"c662a4"';
const regex = /"([^"]*)"/;
const match = chatRoomIdElement.match(regex);
const extractedValue = match[1];
if (match) {
const extractedValue = match[1];
console.log(extractedValue);
} else {
console.log("No match found");
}


console.log("-------",chatRoomIdElement)




console.log(messageUsername, ";;;;;MESSAGE USERNAME;;;;");


const groupChatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/group_chat/'
    + extractedValue
    + '/'
);

groupChatSocket.onopen = function (e) {
    console.log("CONNECTION ESTABLISHED");
}

groupChatSocket.onclose = function (e) {
    console.log("CONNECTION CLOSED");
}

groupChatSocket.onerror = function (e) {
    console.log("ERROR OCCURRED");
}

groupChatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.username == messageUsername) {
        console.log("----->group chat onmessage if");
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                    <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                                                                        <small style="color: white">${data.username}</small><br>
                                                                        ${data.message}
                                                                    </p>
                                                                </td>
                                                            </tr>`;
    } else {
        console.log("------->group chat onmessage else");
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                    <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
                                                                        <small style="color: white">${data.username}</small><br>
                                                                        ${data.message}
                                                                    </p>
                                                                </td>
                                                            </tr>`;
    }
}

document.querySelector('#chat-message-submit').onclick = function (e) {

    let messageInput = document.querySelector('#message_input');

    const message = messageInput.value.trim();

    groupChatSocket.send(JSON.stringify({
        'message': message,
        'username': messageUsername
    }));

    messageInput.value = '';
}

const messageInput = document.querySelector('#message_input');

messageInput.addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {

        event.preventDefault();

        const message = messageInput.value.trim();

        if (message !== '') {
            groupChatSocket.send(JSON.stringify({
                'message': message,
                'username': messageUsername
            }));

            messageInput.value = '';
        }
        messageInput.value = '';
    }
});