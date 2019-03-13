$(function() {

	console.log('toto');

var ws = new WebSocket("ws://nepi-vtu19.neuilly.ratp:5678/"),
				messages = document.createElement('ul');
			ws.onmessage = function (event) {
				var messages = document.getElementsByTagName('ul')[0],
					message = document.createElement('li'),
					content = document.createTextNode(event.data);
				message.appendChild(content);
				messages.appendChild(message);
			};
			document.body.appendChild(messages);

});