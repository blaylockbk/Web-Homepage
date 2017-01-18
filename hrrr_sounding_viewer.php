<!DOCTYPE html>
<!-- 
View HRRR sounding images. 

Created by Brian Blaylock
Date: June 2, 2015

-->
<html>
<head>
<title>HRRR Soundings</title>
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

function change_picture(img_name){
		document.getElementById("sounding_img").src = img_name;
		document.getElementById("sounding_img").style.width= '95%';
	}
function empty_picture(img_name){
	document.getElementById("sounding_img").src = img_name;
	document.getElementById("sounding_img").style.width= '40%';
}

</script>
</head>

<body onload="defult_to_current_date();">
	<script src="./js/site/sitemenu.js"></script>
	<br>

	<h1 align="center"><i class="fa fa-line-chart fa-fw" aria-hidden="true"></i> HRRR BUFR Soundings
      
      <!-- Large modal (the intrusctions help button)-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">HRRR Analysis Soundings</h4><hr>
            <h5>
            <b>Instructions:</b>Select the month, day, year, and station identifier for which you wish
			to display all the available HRRR soundings. Times are in UTC. Then click the "Get Soundings" button.
			If no images show then try a different date or image type. Hover over hour buttons to see the sounding.
			Images exist for green numbered buttons and not for red numbered buttons.
			<br>Rawinsonde observations from the SLC airport are plotted with a thin blue line at 23z, 00z, 11z, and 12z.
			</h5>
            <hr>
			

      </div>
      </div>
      </div>
      </h1>

<div style="background-color:#f5f5f5; width:85%; margin-left:auto; margin-right:auto;">	
	
		<form class="navbar-form" method="post" align="center">
			<table class="center table table-responsive" align="center" cellspacing="10">
			<tr><td>1) Choose Date</td><td>2) Choose Station</td><td> 3) Submit</td></tr>
			<tr>
			<td><input class="form-control" id="date_input" type="date" name="date"></td>
			<td>
				<input type=radio name="station_option" value="KSLC">Salt Lake City (KSLC)<br>
				<input type=radio name="station_option" value="KOGD">Ogden (KOGD)<br>
				<input type=radio name="station_option" value="KPVU">Provo (KPVU)<br></td>
			<td><input class="btn btn-success" type="submit" value="Get Soundings" class="myButton"></td>
			</tr>
			</table>
		</form>
	

<!-- PHP for getting file names in the directory-->
	<?php
			$dir = "/uufs/chpc.utah.edu/common/home/horel-group/archive/";
			
			$date = $_POST['date']; // grab the date value from HTML input
			$date = DateTime::createFromFormat('Y-m-d',$date); // convert date value to PHP date format
			$date = $date->format('Ymd'); // convert date to format usable in retrieving images  
			
			$station = $_POST['station_option']; // grab the image type from selection box


			// open this directory 
			$myDirectory = opendir($dir.$date."/images/models/hrrr/");

			// get each entry, but only if it contains the Station Identifier
			while($entryName = readdir($myDirectory)) {
				if (strpos($entryName,$station) !== false){
					$dirArray[] = $entryName;
				}
				
			}
		
			// close directory
			closedir($myDirectory);
			
			//sort directory array by alphabetical order
			sort($dirArray);					
			
			//	count elements in array
			$indexCount	= count($dirArray);
	?>
			
<!--Area for sounding plot images to appear-->
<div align="center">
		
		<br>
		<!--PHP for creating buttons and image-->
			<?php
			echo $date.' '.$station.'<br><br>';
			echo '<div class="btn-group" role="group" aria-label="...">';
			// loop through the array of files and display a link to the image

							
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				$hour_exists = substr($dirArray[$index],-10,2);
				$hour_exists = (int)$hour_exists;
				if ($extension == 'jpg' or $extension == 'gif'){ // list only jpgs and gif images
					if ($hour_exists==$index+$missed_hours){
						//if sounding exists, then make green button
						$new_image = 'https://api.mesowest.utah.edu/archive/'.$date.'/images/models/hrrr/'. $dirArray[$index].'';
						$anan_hour = substr($dirArray[$index],-10,2);//get the analysis hour
						$anan_hour = (int)$anan_hour;
						echo 
							'
							<input style="color:darkgreen" class="btn btn-default" type=button value='.$anan_hour.' onmouseover=change_picture("'.$new_image.'");>
							';
					}
					else{
						//make red, empty buttons until we reach an hour that exists
						do{
						$absent_hour = $index+$missed_hours;
						echo
						'
						<input style="color:red" class="btn btn-default" type=button value='.$absent_hour.' onmouseover=empty_picture("./images/empty.jpg")>
						';
						$missed_hours++;
						}while($hour_exists>$index+$missed_hours);
						//after making the empty image buttons, make a green button for this index
						$new_image = 'https://api.mesowest.utah.edu/archive/'.$date.'/images/models/hrrr/'. $dirArray[$index].'';
						$anan_hour = substr($dirArray[$index],-10,2);//get the analysis hour
						$anan_hour = (int)$anan_hour;
						echo 
							'
							<input style="color:darkgreen" type=button value='.$anan_hour.' onmouseover=change_picture("'.$new_image.'");>
							';
					}
				}	
			}
			
			?>
		</div>
		<br><br><img id="sounding_img" style="max-width:800px" src="./images/empty.jpg" alt="empty"><br><br>
	<br><br><br><br>
	</div>
</div>
<div>
	<br>
	External Sounding Websites<br>
	<a href="http://weather.uwyo.edu/upperair/sounding.html">Wyoming Sounding Archive</a><br>
	<br>
	</div>

	<br>
	<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>

