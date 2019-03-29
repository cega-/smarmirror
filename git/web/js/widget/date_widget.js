$(function() {

	function capitalizeFirstLetter(string) {
		return string.charAt(0).toUpperCase() + string.slice(1);
	}

	function refresh_current_date() {
		var midnight = new Date();
		midnight.setHours(24, 0, 0, 0);
		var timeUntilMidnight = midnight.getTime() - Date.now();

		var today = new Date();
		var weekday = capitalizeFirstLetter(new Intl.DateTimeFormat('fr-FR', {weekday: 'long'}).format(today));
		var day = new Intl.DateTimeFormat('fr-FR', {day: 'numeric'}).format(today);
		var month = capitalizeFirstLetter(new Intl.DateTimeFormat('fr-FR', {month: 'long'}).format(today));

		var date_string_iso = weekday +"<br>"+ day +' '+ month;
		
		var date_num_iso = today.toLocaleDateString();

		$('#current_date').html(date_string_iso);

		setTimeout(function () {
			refresh_current_date();
		}, timeUntilMidnight);
	}

	refresh_current_date();
});