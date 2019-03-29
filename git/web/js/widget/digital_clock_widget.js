$(function() {

	function clock(){ 
		var Maintenant = new Date();
		var heures = Maintenant.getHours();
		var minutes = Maintenant.getMinutes();
		var secondes = Maintenant.getSeconds();

		heures = ((heures < 10) ? " 0" : " ") + heures;
		minutes = ((minutes < 10) ? ":0" : ":") + minutes;
		secondes = ((secondes < 10) ? ":0" : ":") + secondes;

		$('#digital_clock').text(heures + minutes);
	}

	clock();
	setInterval(clock,60000);

});