<!DOCTYPE html>
<!-- 
Photo Viewer
View all images in a directory by clicking buttons.
This allows you to stay on the same page rather than clicking the back button every time you want to see a different image.
Image name can not have any spaces!!

Created by Brian Blaylock
Date: November 30, 2015
Updated with bootstrap style: February 10, 2017

http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html
-->
<head>
<title>Image Viewer - Click</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>

<script>
function change_picture(img_name){
		document.getElementById("sounding_img").src = img_name;
		document.getElementById("sounding_img").style.width= '100%';
		document.getElementById("sounding_img").style.max-height= '80vh';
	}
function empty_picture(img_name){
	document.getElementById("sounding_img").src = img_name;
	document.getElementById("sounding_img").style.width= '30%';
}

/* For the button group on resize */
var wideScreen = 900; // for example beyond 640 is considered wide
var toggleBtnGroup = function() {
    var windowWidth = $(window).width();
  if(windowWidth >= wideScreen) {
    $('#btn-group-toggle').addClass('btn-group-vertical').removeClass('btn-group');
  } else {
    $('#btn-group-toggle').addClass('btn-group').removeClass('btn-group-vertical');
  }
}
toggleBtnGroup(); // trigger on load
window.addEventListener('resize',toggleBtnGroup); // change on resize
/* (for the button group on resize) */

</script>
</head>


<body>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/sitemenu.js"></script>	
<h2 align="center"><i class="fa fa-picture-o" aria-hidden="true"></i> Image Viewer
<div class="btn-group">
	<button type="button" class="btn btn-primary" onclick=window.location.href="./photo_viewer_v1.php">Hover</button>
	<button type="button" class="btn btn-primary active">Click</button>
	<button type="button" class="btn btn-primary" onclick=window.location.href="./photo_viewer_v3.php">Select</button>
</div></h2>

<div class="jumbotron" style="width:95vw; padding-top:15px; margin-left:auto; margin-right:auto;">	
	
	
<!-- PHP for getting file names in the directory-->
	<?php
			$dir =  getcwd();

			// open this directory 
			$myDirectory = opendir($dir);

			// get each entry, but only if it contains the Station Identifier
			while($entryName = readdir($myDirectory)) {
				if (strpos($entryName,".png") !== false or strpos($entryName,".jpg") !== false or strpos($entryName,".gif") !== false or strpos($entryName,".GIF") !== false or strpos($entryName,".PNG") !== false or strpos($entryName,".JPG") !== false){
					$dirArray[] = $entryName;
				}
				
			}
		
			// close directory
			closedir($myDirectory);
			
			//sort directory array by alphabetical order
			sort($dirArray);					
			
			//	count elements in array
			$indexCount	= count($dirArray);
			//echo $dir;
			//echo "<br>";
			// The server path to public_html directory
			//echo substr($dir,0,53);
			// The path after public_html. Will use this for creating the URL path to the image
			echo "<p>Path: ", substr($dir,53);
			$img_URL_dir = substr($dir,53);

	?>
			
<!--Area for sounding plot images to appear-->
<div class="row" style="padding-left:15px;">
    <div class="col-md-2">
	<div  class="btn-group" id="btn-group-toggle" align="center">
		
		<!--PHP for creating buttons and image-->
			<?php
			// loop through the array of files and display a link to the image

							
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				if ($extension == 'jpg' or $extension == 'gif' or $extension == 'png'){ // list only jpg, gif, and png images
					
						//if sounding exists, then make green button
						$new_image = 'http://home.chpc.utah.edu/~u0553130/'.$img_URL_dir.'/'.$dirArray[$index].'';
						$anan_hour = substr($dirArray[$index],0,2);//get the analysis hour
						$anan_hour = (int)$anan_hour;
						echo '<button type="button" class="btn btn-default" onclick=change_picture("'.$new_image.'")>'.$dirArray[$index].'</button>';				
				}	
			}
			
			?>
	</div>
	</div>
	<div class="col-md-10">
	<img class="style1" id="sounding_img" style="width:30%" src="./images/empty.jpg" alt="empty">
	</div>

</div> <!--row-->

</div> <!--Jumbotron-->


<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteclose.js"></script>

</body>
</html>
