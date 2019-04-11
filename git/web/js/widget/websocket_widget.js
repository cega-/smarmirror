$(function() {

	console.log('toto');
	var ws = null;

	function initWebsocket() {
		try
		{
			if (ws == null || ws.readyState == 3) {}
			ws = new WebSocket("ws://nepi-vtu19.neuilly.ratp:5678/server");
			var widget_content = null

			ws.onmessage = function (event) {
				console.log('Event receive');
				widget_content = JSON.parse(event.data);
				//console.log(JSON.parse(event.data));
				div_widget_name = widget_content['topic'].split('/')[1];
				console.log(JSON.parse(widget_content['content']));
				var d_content = JSON.parse(widget_content['content']);
				Object.entries(d_content).forEach(entry => {
					$('#'+entry[0]).html(entry[1]);
				});
				//$('#'+div_widget_name).html(widget_content['content']);
			};

			ws.onclose = function(error){
				ws.close();
				console.log('error');
				console.log(error);
			};
		}
		catch (exception)
		{
			ws.close();
			console.log('Connection Error');
			console.error(exception);
		}
	}

	initWebsocket();

	setInterval(function() {
		try 
		{
			console.log('Send Keep-Alive');
			if (ws.readyState == 1)
			{
				ws.send('WS Client keep-alive request');
			}
			else
			{
				console.log('WS ERROR');
				console.log(ws.readyState);
				if (ws.readyState == 3)
				{
					initWebsocket();
				}
				if (ws.readyState > 1)
				{
					ws.close();
				}
			}	
		}
		catch (exception)
		{
			console.log('Send Error');
			console.error(exception);
		}
	},8000);

});
