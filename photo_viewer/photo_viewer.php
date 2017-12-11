<!DOCTYPE html>
<!-- 
Photo Viewer:
View all images in a directory by hovering, clicking, or selecting buttons.
Simply dump this script into any public_html directory with images.
This browser-friendly image viewer allows you to stay on the same page while
flipping through images rather than clicking the back button every time you 
want to see a different image in the directory.

WARNING: Image names in the directory can NOT have any spaces!!

Created by Brian Blaylock
Date: November 30, 2015
Updated with bootstrap style: February 13, 2017

http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html
-->

<head>
<title>Image Viewer - Hover</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>

<script>
function change_picture(img_name){
        /*On Hover*/
		document.getElementById("sounding_img").src = img_name;
		document.getElementById("sounding_img").style.width= '100%';
		document.getElementById("sounding_img").style.maxHeight= '80vh';
	}
function change_picture2(img_name){
        /*On Click*/
		document.getElementById("sounding_img2").src = img_name;
		document.getElementById("sounding_img2").style.width= '100%';
		document.getElementById("sounding_img2").style.maxHeight= '80vh';
	}
function change_picture3() {
        /*Select*/
        var x = document.getElementById("mySelect").value;
        document.getElementById("sounding_img3").src = x;
        document.getElementById("sounding_img3").style.width= '98%';
        document.getElementById("sounding_img3").style.maxHeight= '80vh';
}
function empty_picture(img_name){
        /*the empty picture on load*/
        document.getElementById("sounding_img").src = img_name;
        document.getElementById("sounding_img").style.width= '30%';
}

/* For the button group on resize 
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
 (for the button group on resize) */

</script>
</head>


<body>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/sitemenu.js"></script>	
<h2 align="center"><i class="far fa-image"></i> Image Viewer

<!-- PHP for getting file names in the current working directory-->
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
        // The server path to public_html directory
        //echo substr($dir,0,53);
        // The path after public_html. Will use this for creating the URL path to the image
        echo "<small>", substr($dir,53);
        $img_URL_dir = substr($dir,53);
	?>

</small>

<!-- Large modal (the intrusctions help button)-->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

<div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
<div class="modal-dialog modal-lg" role="document">
<div class="modal-content" style="padding:25px">
    <button type="button" class="close" data-dismiss="modal">&times;</button>
    <h4 style="font-size:22px;"><i class="far fa-image"></i> Image Viewer Instructions</h4><hr>
    <h5 align="left" style="font-size:18px;">
    <p>There are three options for looking at the images:
        <ol style="padding-left:60px">
            <li> Hover - Picture changes when mouse hovers over image name.
            <li> Click - Picture changes when you click the image name.
            <li> Select - Click an option in the select box to change image.
        </ol>
        <hr>
        <p>Dump this image viewer PHP script into any public_html 
        directory and the viewer will display the images in that 
        directory in a browser-friendly display.
            <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">On the CHPC system? Link this script 
                to your directory</h3>
            </div>
            <div class="panel-body">
                <p style="font-family:courier; font-size:12px">ln /uufs/chpc.utah.edu/common/home/u0553130/public_html/Brian_Blaylock/photo_viewer/photo_viewer.php
            </div>
            </div>
        <hr>
        <p>Tips:
            <ul style="padding-left:60px">
                <li>Make window wide enough so buttons are on side.
                <li>Image names in directory must not contain spaces.
                <li>In the "Select" tab, use up/down arrow keys to change picture.
            </ul>
            <div class="panel panel-default">
    </h5>

</div>
</div>
</div>
</h1><!-- Large modal (the intrusctions help button)-->
      
</h2>	


<div class="container-fluid" style="width:1500px;max-width:90%">		

<!-- Tabs -->
  <ul class="nav nav-tabs">
    <li class="active"><a data-toggle="tab" href="#tab1">Hover</a></li>
    <li><a data-toggle="tab" href="#tab2">Click</a></li>
    <li><a data-toggle="tab" href="#tab3">Select</a></li>
  </ul>

    <div class="tab-content">
        <div id="tab1" class="tab-pane fade in active">
			<!--Area for images to appear-->
            <div class="row" style="padding-left:15px;">
                <div class="col-md-2">
                <br>
                    <div  class="btn-group-vertical"  role="group" align="center">
                        
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
                        echo '<button type="button" class="btn btn-default" onmouseover=change_picture("'.$new_image.'")>'.$dirArray[$index].'</button>';					
                        }	
                        }

                        ?>
                    
                    </div>
                </div>
                <div class="col-md-10">
                <img class="style1" id="sounding_img" style="width:30%;" src="./images/empty.jpg" alt="empty" onclick="window.open(this.src)">
                </div>

            </div> <!--row-->
        </div><!--(Tab1)-->

        <div id="tab2" class="tab-pane fade">
            <!--Area for images to appear-->
            <div class="row" style="padding-left:15px;">
                <div class="col-md-2">
                <br>
                <div  class="btn-group-vertical" id="btn-group-toggle" align="center">
                    
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
        echo '<button type="button" class="btn btn-default" onclick=change_picture2("'.$new_image.'")>'.$dirArray[$index].'</button>';				
        }	
        }

        ?>
                </div>
                </div>
                <div class="col-md-10">
                <img class="style1" id="sounding_img2" style="width:30%" src="./images/empty.jpg" alt="empty" onclick="window.open(this.src)">
                </div>

            </div> <!--row-->
        </div> <!--(Tab2)-->

        <div id="tab3" class="tab-pane fade">
        <!--Area for sounding plot images to appear-->
            <div align="center">
                    <br>
            <!--PHP for creating buttons and image-->
            <?php
            // loop through the array of files and display a link to the image
            echo "<select class='form-control'' id='mySelect' style='width:300px' onchange='change_picture3()'>";			

            for($index=0; $index < $indexCount; $index++) {
            $extension = substr($dirArray[$index], -3);
            if ($extension == 'jpg' or $extension == 'gif' or $extension == 'png'){ // list only jpg, gif, and png images

            //if sounding exists, then make green button
            $new_image = 'http://home.chpc.utah.edu/~u0553130/'.$img_URL_dir.'/'.$dirArray[$index].'';
            $anan_hour = substr($dirArray[$index],0,2);//get the analysis hour
            $anan_hour = (int)$anan_hour;
            echo 
            '
            <option style="height:25px;" value="'.$new_image.'" >'.$dirArray[$index].'<br>
            ';

            }	
            }
            echo "</select></td></tr></table>";
            ?>
                    <img class="style1" style="width:500px" id="sounding_img3" src="./images/empty.jpg" alt="empty" onclick="window.open(this.src)">

                </div>

        </div>

    </div>
<!--(Tabs)-->
</div> <!--(container))-->


<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteclose.js"></script>
</body>
</html>
