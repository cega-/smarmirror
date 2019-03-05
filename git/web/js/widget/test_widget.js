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

/*
	  var client = mqtt.connect("ws://nepi-vtu19.neuilly.ratp/mqtt", [{ port: 9001 }]) // you add a ws:// url here

  client.subscribe("sensor/temperature")

  client.on("message", function (topic, payload) {
	alert([topic, payload].join(": "))
	client.end()
  })

  client.publish("sensor/temperature", "hello world!")
  */

/*
	// Create a client instance
	client = new Paho.MQTT.Client("nepi-vtu19.neuilly.ratp", 9001, "clientId");
	console.log('titi');

	// set callback handlers
//	client.onConnectionLost = onConnectionLost;
//	client.onMessageArrived = onMessageArrived;

	// connect the client
	client.connect();

	// called when the client loses its connection
	function onConnectionLost(responseObject) {
		if (responseObject.errorCode !== 0) {
			console.log("onConnectionLost:"+responseObject.errorMessage);
		}
	}

	// called when the client connects
	function onConnect() {
		// Once a connection has been made, make a subscription and send a message.
		console.log("onConnect");
		client.subscribe("#");
		message = new Paho.MQTT.Message("Hello");
		message.destinationName = "World";
		client.send(message);
	}

	// called when a message arrives
	function onMessageArrived(message) {
		console.log("onMessageArrived:"+message.payloadString);
	}
*/
});