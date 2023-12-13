// document.addEventListener("DOMContentLoaded", function() {
//     const notify_socket = new WebSocket(
//         'ws://' + window.location.host + '/ws/notify/'
//     );

//     notify_socket.onopen = function(e) {
//         console.log("CONNECTED TO NOTIFICATION");
//     };

//     var notificationTag = document.getElementById('noti_message');
//     var notiCountTag = document.getElementById('noti_count');

//     notify_socket.onmessage = function(e) {
//         const data = JSON.parse(e.data);
//         notiCountTag.innerHTML = data.count;
//         notificationTag.innerHTML = data.notifications.join('<br>');
//     };

//     notify_socket.onclose = function(e) {
//         console.log("DISCONNECTED FROM NOTIFICATION");
//     };
// });


    document.addEventListener("DOMContentLoaded", function() {
        const notify_socket = new WebSocket(
            'ws://' + window.location.host + '/ws/notify/'
        );

        notify_socket.onopen = function(e) {
            console.log("CONNECTED TO NOTIFICATION");
        };

        var notificationList = document.getElementById('notificationList');
        var noNotificationMessage = document.getElementById('noNotificationMessage');

        notify_socket.onmessage = function(e) {
            const data = JSON.parse(e.data);

            console.log(data.notifications)

            // Check if the notificationList element is found
            if (notificationList) {
                // Clear existing content
                notificationList.innerHTML = '';

                if (data.notifications.length > 0) {
                    noNotificationMessage.style.display = 'none';

                    // Create and append new <li> elements for each notification
                    data.notifications.forEach(function(notification) {
                        const liElement = document.createElement('li');
                        const pElement = document.createElement('p');
                        const strongElement = document.createElement('strong');
                        strongElement.textContent = notification.message;
                        pElement.appendChild(strongElement);

                        const smallElement = document.createElement('small');
                        smallElement.textContent = notification.timestamp;
                        pElement.appendChild(smallElement);

                        liElement.appendChild(pElement);
                        notificationList.appendChild(liElement);
                    });
                } else {
                    noNotificationMessage.style.display = 'block';
                }
            } else {
                console.error("Element with ID 'notificationList' not found in the DOM.");
            }
        };

        notify_socket.onclose = function(e) {
            console.log("DISCONNECTED FROM NOTIFICATION");
        };
    });
