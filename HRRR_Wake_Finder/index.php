<!DOCTYPE html>
<!-- 
HRRR Wake Finder

Created by Brian Blaylock
Date: October 23, 2015

perhaps look into WindNinja product for additional data and applications for lakes in 
mountainous regions.

-->
<head>
<title>HRRR Wake Finder</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>

<script>
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


<body>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/sitemenu.js"></script>	
<br>
<h1 align="center" style="font-family:Garamond"><img style="max-width:600px; width:85%;" align=center src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/HRRR_Wake_Finder/lew_ski.png"></h1>


<div style="background-color:#f5f5f5; width:85%; margin-left:auto; margin-right:auto;">	
	<div style="background-color:#d40000;">
<br>
	

	<form action="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/HRRR_Wake_Finder/info.html">
		<input id="waketoolbutton" type="submit" value="More About&#10;This Tool">
	</form>
	<p style="color:white;padding:15px" >Developed with parts and pieces of other stuff I've made, for a friend who loves boating.
	<p style="color:white;padding:15px" >
	<b>Instructions:</b> Select the Water Body for which you wish
	to display a 15 hour wind forecast. Then click the "Get Forecast" button.
	Hover your mouse over each hour button to see the wind forecast. New forecasts (F0) are available
	approximately 32 minutes after the hour. Because my current python plotting script is very slow, F15 is available approx on the hour.
	
	
			<br>
		<div style="width:85%; margin-left:auto; margin-right:auto;">
		<form method="post" align="center">
			<table align="center" style="color:white;" cellspacing="10">
			<tr><td>1) Choose Lake<hr></td><td> 2) Submit<hr></td></tr>
			<tr>
			<td align=right>
			
			
			
			<span style="font-size:25px;padding:15px;">Utah Lake (UT)</span>
			<input  class="FormTouch" type=radio name="lake_option" value="Utah_Lake"><br>
			<span style="font-size:25px;padding:15px;">Bear Lake (UT)</span> discontinued
			<input  class="FormTouch" type=radio name="lake_option" value="Bear_Lake" ><br>
			<span style="font-size:25px;padding:15px;">Moses Lake (WA)</span> discontinued
			<input  class="FormTouch" type=radio name="lake_option" value="Moses_Lake" ><br>
			<td>
			<input style="width:170px;height:120px;" class="FormTouch" id="SUBMIT" type="submit" value="Get&#10;Forecast" class="myButton"></td>
			</tr>
			</table>
			Discontinued maps will be available again when my plotting script becomes faster. If you miss the discontinued maps then contact brian.blaylock@utah.edu.
		</form>
		</div>
		<br>
	</div>
	
<!-- PHP for getting file names in the directory-->
	<?php
			$dir = "/uufs/chpc.utah.edu/common/home/u0553130/public_html/";
			
			
			$station = $_POST['lake_option']; // grab the image type from selection box


			// open this directory 
			$myDirectory = opendir($dir."/oper/current_HRRR/");

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
			echo ' '.$station.'<br><br>';
			// loop through the array of files and display a link to the image

							
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				$hour_exists = substr($dirArray[$index],-10,2);
				$hour_exists = (int)$hour_exists;
				$missed_hour = 0;
				if ($extension == 'jpg' or $extension == 'gif' or $extension == 'png'){ // list only jpg, gif, and png images
					if ($hour_exists==$index+$missed_hours){
						//if sounding exists, then make green button
						$new_image = 'http://home.chpc.utah.edu/~u0553130/oper/current_HRRR/'.$dirArray[$index].'';
						$anan_hour = substr($dirArray[$index],0,2);//get the analysis hour
						$anan_hour = (int)$anan_hour;
						echo 
							'
							<input style="color:darkgreen;height:30px;width:5%;min-width:30px;" type="button" value="F'.$anan_hour.'" onmouseover=change_picture("'.$new_image.'");>
							';
					}
					else{
						//make red, empty buttons until we reach an hour that exists
						do{
						$absent_hour = $index+$missed_hours;
						//echo
						//'
						//<input style="color:red" type=button value='.$absent_hour.' onmouseover=empty_picture("http://ts1.mm.bing.net/th?&id=JN.TuUQe6DpRqXGxmOSnfrHYw&w=300&h=300&c=0&pid=1.9&rs=0&p=0&r=0")>
						//';
						$missed_hours++;
						}while($hour_exists>$index+$missed_hours);
						//after making the empty image buttons, make a green button for this index
						$new_image = 'http://home.chpc.utah.edu/~u0553130/oper/current_HRRR/'.$dirArray[$index].'';
						$anan_hour = substr($dirArray[$index],0,2);//get the analysis hour
						$anan_hour = (int)$anan_hour;
						echo 
							'
							<input style="color:darkgreen;height:30px;width:5%;min-width:30px;" type="button" value="F'.$anan_hour.'" onmouseover=change_picture("'.$new_image.'");>
							';
					}
				}	
			}
			
			?>
		<br><br><img class="style1" id="sounding_img" style="max-width:800px" src="./images/empty.jpg" alt="empty"><br><br>

	</div>
</div>
<br>
<p>Also check out the <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/HRRR_Winds/">HRRR Winds</a> tool for area forecasts.
<p style="color:red;">Note: Use of this webpage/app does not guarantee weather conditions forecasted 
by the HRRR model for any location or any time.
		
	<br>

<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteclose.js"></script>

</body>
</html>
