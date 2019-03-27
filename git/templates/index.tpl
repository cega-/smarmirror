<!DOCTYPE html>

<html lang="fr">
	<head>

		<title>{{ page_title }}</title>

		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link href="web/css/bootstrap.min.css" rel="stylesheet">
		<link href="web/css/weather-icons.css" rel="stylesheet">
		<link href="web/css/weather-icons-wind.css" rel="stylesheet">

		<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
		<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
		<!--[if lt IE 9]>
		<script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
		<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->

	</head>

	<body>

		<h1>Hello, world!</h1>

		<div id="weather">
			<div id="current_temp">
				
			</div>
			<div id="forecast_temp">
				
			</div>
			<div id="logo_weather">
				<i class="wi wi-owm-904"></i>
			</div>
			<div id="string_weather">
				
			</div>
		</div>

		<div id="news-feed">
			<div class="news-entry">
				<div class="news-entry-title">
					British nurse Pauline Cafferkey, who recovered from Ebola, back in hospital again
				</div>
				<div class="news-entry-summary">
					A Scottish nurse, who recovered from Ebola but then suffered life-threatening complications from the virus persisting in her brain, has been admitted to hospital for a third time, a hospital in Scotland said on Tuesday.
				</div>
			</div>
			<div class="news-entry" style="display:none">
				<div class="news-entry-title">
					Invercargill 11-year-old runaway heads towards Dunedin on his motorbike
				</div>
				<div class="news-entry-summary">
					An 11-year-old Invercargill boy has been found after taking off from the city on his motorbike and heading towards Dunedin.
				</div>
			</div>
			<div class="news-entry" style="display:none">
				<div class="news-entry-title">
					One dead, several injured after Dutch passenger train derails
				</div>
				<div class="news-entry-summary">
					A passenger train in the Netherlands has derailed after hitting a maintenance crane during rush hour, killing one person and injuring several others.
				</div>
			</div>		
		</div>


		<script src="web/js/jquery.js"></script>
		<script src="web/js/bootstrap.js"></script>
		<script src="web/js/widget/websocket_widget.js"></script>
		<script src="web/js/widget/test_slide_widget.js"></script>

	</body>

</html>