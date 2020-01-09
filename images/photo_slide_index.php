<!-- 
Photo Viewer
View All Images in a Directory as a slide show

Created by Brian Blaylock
Date: June 2015

Instructions: Drop this script into a directory with jpg or gif images
and when someone enters the directory they will be diverted to a slideshow
of the photos in the directory.
-->

<html >

<body>

	<h1 align="center">Photo Viewer</h1>

	
<div style="background-color:#d6f2ff; width:95%; height:80%; margin-left:auto; margin-right:auto;text-align:center;">	
	<div style="background-color:blue;">
		<br>
	</div>
	<div align="center">
		<br>
		<input type=button value="previous image" onclick="prevImage();">	
		<input type=button value="next image" onclick="nextImage();">
		<br>
	</div>
	<br>
	
			<?php

			
			
			//$date = $_POST['date']; // grab the date value from HTML input
			//$date = DateTime::createFromFormat('Y-m-d',$date); // convert date value to PHP date format
			//$date = $date->format('Ymd'); // convert date to format usable in retrieving images  
			
			$imgtype = $_POST['gallery']; // grab the image type from selection box
			$date = $_POST['date'];
			
			$dir = './';
			// open this directory 
			$myDirectory = opendir($dir);

			// get each entry
			while($entryName = readdir($myDirectory)) {
				$dirArray[] = $entryName;
			}

			// close directory
			closedir($myDirectory);

			//	count elements in array
			$indexCount	= count($dirArray);
			$TrueCount = $indexCount-3;
			
			
			
			
			echo '<span id="pic_count">1 of '.$TrueCount. '</span>;';

			// loop through the array of files and print the javascript index and image source
			echo '<script>';
			echo 'var i = 0;'; 
			echo 'var path = new Array();';
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				
				$js_index = $index-2;//subtract 3 because first index in directory is "parent directory" and second is this script and Javascript first index is zero
				if ($extension == 'jpg' or $extension == 'gif' or $extension == 'png'){ // list only jpg, gif, png
					echo '
					path['.$js_index.']="'.$dir. $dirArray[$index] . '";
					var total_imgs = '.$js_index.';
					';
					
				}
			}
			
			echo'
			function nextImage()
				{
				document.getElementById("photo_showing").src = path[i];
				document.getElementById("pic_text").innerHTML=path[i];
				document.getElementById("pic_count").innerHTML=String(i+1)+" of "+String(total_imgs+1);
				i++;
				if (i > total_imgs){i=0;}
				getEXIF();
				}
			function prevImage()
				{
				document.getElementById("photo_showing").src = path[i];
				document.getElementById("pic_count").innerHTML=String(i+1)+" of "+String(total_imgs+1);
				i = i-1;
				if(i<0){i=total_imgs}
				}
			function getEXIF(){
				var theimg = document.getElementById("photo_showing");
				alert(EXIF.getTag(theimg,"Model"));
				}
				
				
			';
			
			
			echo '</script>
					<a target="_blank"href="'.$dir. $dirArray[$index] . '">
						<span>' . $dirArray[$index] .'</span>
					</a>
					<br>
					<img id="photo_showing" style="max-width:95%; max-height:85%;" src="'.$dir. $dirArray[2] . '" />
					<br><br>';
			echo '<span id="pic_text">'.$dir. $dirArray[2].'</span>';
					
						                         
				
			
			?>
	</div>

	

</div>
</body>

</html>
