$(function() {

	function tick(){
		$('#news-feed div.news-entry:first').slideUp(function () 
			{ 
				$(this).appendTo($('#news-feed'));
				$( '#news-feed div.news-entry:nth-child(1)' ).toggle('slow');
			});
	}
		
	$(document).ready(function() {
		setInterval(function(){ tick() }, 5000);
	});
});