<!DOCTYPE html>
<html>

<!-- This page is busted-->

<head>
<title>MODIS Satellite Images</title>
<link rel="stylesheet" href="./css/brian_style.css" />
<script src="./js/site/siteopen.js"></script>
<script>
// Change date input to the current date when the page loads
function defult_to_current_date(){
	var currentTime = new Date();
	var month = currentTime.getMonth()+1;
	var day = currentTime.getDate();
	var year = currentTime.getFullYear();
	//Make date-string for HTML date value. Need two digit month and day...
	//    ex: need instead of 2015-5-5, needs to be 2015-05-05
	if (month < 10 && day <10){
		var date_string = String(year)+'-0'+String(month)+'-0'+String(day);	
	}
	else if (month < 10 && day > 9){
		var date_string = String(year)+'-0'+String(month)+'-'+String(day);
	}
	else if (month>9 && day<10){
		var date_string = String(year)+'-'+String(month)+'-0'+String(day);
	}
	else{
		var date_string = String(year)+'-'+String(month)+'-'+String(day);
	}
	document.getElementById("date_input").value = date_string;
}

</script>
</head>

<body onload="defult_to_current_date();">
	<script src="./js/site/sitemenu.js"></script>
	<br>

	<!-- 
	View All Images in the MODIS Directory

	Created by Brian Blaylock
	Date: May 28, 2015

	Displays all the image names and images in a directory. The images 
	must be available in a public html file. In this code the Date
	and Select input determine which day and image type to display.

	I don't know why this code was so hard to find, but I finally found
	a way to display all images in a directory using PHP. This is 
	useful for lots of different applications. Here is the source of where I started:
	http://www.webdeveloper.com/forum/showthread.php?243055-RESOLVED-Display-all-images-in-a-set-directory
	-->


	<h1 align="center">MODIS and SPoRT Image Viewer</h1><br>

	<!-- Instructions and Input -->
	<div style="background-color:#f5f5f5; width:85%; margin-left:auto; margin-right:auto;">	
		<div style="background-color:#d40000;">
			<br>
			<p style="color:white;"> <b>Instructions:</b> Select the year, day, month, and image type for 
			which you wish to display all the available images. Then click the "Get Images" button.
			If no images appear then try a different date or image type.
			</p><br>
			<p style="color:lightgrey;"><b>Note:</b> In Fire Fox or IE you must type the date in the form yyyy-mm-dd (ex. 2015-05-06).
			</p>
			<br>
			<form method="post" align="center" name="php-form">
				<table style="color:White;">
				<tr><td>Date (yyyy-mm-dd)</td><td>Image Type</td></tr>
				<tr>
				<td><input id="date_input" type="date" name="date"></td>
				<td><select name="imgtype_option">
					<option value=""></option>
					<option value="lwir">Infrared</option>
					<option value="ntmicro">Nighttime Microphysics</option>
					<option value="snowcloud">Snow/Cloud</option>
					<option value="specdiff">specdiff (not often available)</option>
					<option value="truecolor">True Color</option>
					<option value="vis">Visible</option>
				</select></td>
				<td><input type="submit" value="Get Images"></td>
				</tr>
				</table>
			</form>
			<br>
	</div>
	<br>
	<br>
	<br>
	<br>
	<!-- PHP for getting input values, opening directory, and reading the number of files-->
		<?php

		$dir = "/uufs/chpc.utah.edu/common/home/horel-group/archive/";
		
		$date = $_POST['date']; // grab the date value from HTML input
		$date = DateTime::createFromFormat('Y-m-d',$date); // convert date value to PHP date format
		$date = $date->format('Ymd'); // convert date to format usable in retrieving images  
		
		$imgtype = $_POST['imgtype_option']; // grab the image type from selection box


		// open this directory 
		$myDirectory = opendir($dir.$date."/modis/".$imgtype);

		// get each entry
		while($entryName = readdir($myDirectory)) {
			$dirArray[] = $entryName;
		}

		// close directory
		closedir($myDirectory);

		//	count elements in array
		$indexCount	= count($dirArray);

		?>
				
	<!-- HTML and PHP for displaying the images from the directory-->
	<div align="center">
		

			<?php
			// loop through the array of files and print them all in a list
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				if ($extension == 'jpg' or $extension == 'gif'){ // list only jpgs and gifs
					echo 
						'
						<a target="_blank"href="https://api.mesowest.utah.edu/archive/'.$date.'/modis/'.$imgtype.'/' . $dirArray[$index] . '">
							<span>' . $dirArray[$index] .'</span>
						</a>
						<br>
						<img width="50%" src="https://api.mesowest.utah.edu/archive/'.$date.'/modis/'.$imgtype.'/' . $dirArray[$index] . '" alt="Image" />
						<br><br>';
				}	
			}
			?>
	</div>


	</div>

	<div>
	<br>
	External Satellite Websites<br>
	<a href="http://lance-modis.eosdis.nasa.gov/imagery/subsets/?subset=GreatSaltLakeBasin">MODIS Archive: GreatSaltLakeBasin Subsets</a><br>
	<a href="http://landsatlook.usgs.gov/">Landsat Viewer</a><br>
	<a href="http://home.chpc.utah.edu/~u0198116/AVHRR/gsltemp.html">GSL temperature from satellite </a><br>
	<a href="https://earthdata.nasa.gov/labs/worldview/">NASA World View</a><br>
	</div>


	<br>
	<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>

