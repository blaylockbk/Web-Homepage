<!DOCTYPE html>
<html>
<head>
<title>KSL Flights</title>
<link rel="stylesheet" href="./css/brian_style.css" />
<script src="./js/site/siteopen.js"></script>
<script>
// Change date input to yesterdays date when the page loads


function defult_to_current_date(){
	var currentTime = new Date();
	var month = currentTime.getMonth()+1;
	var day = currentTime.getDate()-1;
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

function pad(number, length) {
   
    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }
   
    return str;

}

function next_day(){
    //                    dec   jan   feb   mar   arp   may   jun   jul   aug   set   oct   nov   dec   jan
    var days_per_month = ["31", "31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31", "31"];
    
    year = parseInt(document.getElementById('dateinput').value.slice(0,4));
    month = parseInt(document.getElementById('dateinput').value.slice(5,7));
    day = parseInt(document.getElementById('dateinput').value.slice(8,10));
        
    if (day < parseInt(days_per_month[month])){
       day = day+1; 
       day = pad(day,2);
       month = pad(month,2);
        }
    else{
        day = '01';
         if (month==12){
            month = '01';
            year = year +1
            year = pad(year,4)
         }
         else{
            month = month + 1;
            month = pad(month,2);     
         }
        
    }
    
    
    document.getElementById('dateinput').value = year+'-'+month+'-'+day
}

function previous_day(){
    //                    dec   jan   feb   mar   arp   may   jun   jul   aug   set   oct   nov   dec
    var days_per_month = ["31", "31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"];
    
    year = parseInt(document.getElementById('dateinput').value.slice(0,4));
    month = parseInt(document.getElementById('dateinput').value.slice(5,7));
    day = parseInt(document.getElementById('dateinput').value.slice(8,10));
    
    if (day == 1){
       day = days_per_month[month-1];
        if (month==1){
            month = '12';
            year = year -1
            year = pad(year,4)
        }
        else{
          month = month-1;
           month = pad(month,2);     
        }
       
    }
    else{
        day = day-1;
        day = pad(day,2);
        month = pad(month,2);
    }
    
    
    document.getElementById('dateinput').value = year+'-'+month+'-'+day;

}



</script>
</head>

<body onload="set_to_input_date()">
	<script src="./js/site/sitemenu.js"></script>
	<br>

	<!-- 
	View All Images for the date in the KSL_daily Directory

	Created by Brian Blaylock
	Date: May 10, 2016

	Displays all the image names and images in a directory. The images 
	must be available in a public html file. In this code the Date
	and Select input determine which day and image type to display.

	I don't know why this code was so hard to find, but I finally found
	a way to display all images in a directory using PHP. This is 
	useful for lots of different applications. Here is the source of where I started:
	http://www.webdeveloper.com/forum/showthread.php?243055-RESOLVED-Display-all-images-in-a-set-directory
	-->

<?php
// define variables and set to empty values
$name = date ( "Y-m-d", time() - 86400 );

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  if (empty($_POST["name"])) {
    $nameErr = "Name is required";
  } else {
    $name = test_input($_POST["name"]);
  }

}

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}
?>
    
    
	<!-- Instructions and Input -->

<br>

      <h1 align="center"><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> KSL Flights
      
      <!-- Large modal (the intrusctions help button)-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">KSL Chopper Plots</h4><hr>
            <h5>
			<img align=right style="width:100px;" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/ksl_logo.png">
            <b>Instructions:</b> Select the year, day, month, and image type for 
			which you wish to display all the available images. Then click the "Get Images" button.
			If no images appear then try a different date or image type.
			</h5>
            <hr>
            <h5><b>Note:</b> File name date/time is saved -6 H from UTC so the PHP script can find the flights before local midnight.</h5>
			<h5><b>Note:</b> In Fire Fox or IE you must type the date in the form yyyy-mm-dd (ex. 2015-05-06).</h5>
			

      </div>
      </div>
      </div>
      </h1>

	<div style="background-color:#f5f5f5; width:85%; margin-left:auto; margin-right:auto;">	
		<div class="jumbotron;">
			
                <form class="navbar-form" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">  
                    <table>
                    <tr><td>
                    <p><b>Date:<br></b> <input class="form-control" type="date" id='dateinput' name="name" min="2015-06-01" value="<?php echo $name;?>" style='width:200px'>
                    </td>
                    <td>
                    <button class="btn btn-success" type="submit" name="submit">Get Images</button>
                    </td>
                    </tr>
                    <tr>
                    <td>
                    <div class="btn-group" role="group" aria-label="...">
                        <input class="btn btn-default" type='button' value="-1 Day" onclick="previous_day();">
                        <input class="btn btn-default" type='button' value="+1 Day" onclick="next_day();">
                    </div>
                    </td>
                    <td>
                    </td>
                    </tr>
                    </table>
                    <br>
                </form>
	</div>




<?php
echo "<h4>Requested Date:</h4>";
echo $name;
echo "<br>";
echo "<br>";
?>

	<!-- PHP for getting input values, opening directory, and reading the number of files-->
		<?php

		$dir = "/uufs/chpc.utah.edu/common/home/u0553130/public_html/oper/KSL_daily/";
		
		$dateHTML = $_POST['name']; // grab the date value from HTML input
		$datePHP = DateTime::createFromFormat('Y-m-d',$dateHTML); // convert date value to PHP date format
		$date = $datePHP->format('Ymd'); // convert date to format usable in retrieving images


		// open this directory 
		$myDirectory = opendir($dir);
        

		// get each entry
		while($entryName = readdir($myDirectory)) {
			$dirArray[] = $entryName;
		}
        
        // sort the array
        array_multisort($dirArray);

		// close directory
		closedir($myDirectory);

		//	count elements in array
		$indexCount	= count($dirArray);
        
        echo $datePHP->format('d M Y');
        echo '<hr size=10 noshade><br>';
        
		?>

        <!-- HTML and PHP for displaying the images from the directory-->
	<div align="center">
		

			<?php
			// loop through the array of files and print them all in a list
			for($index=0; $index < $indexCount; $index++) {
                
				$day = substr($dirArray[$index], 0,8);
				if ($day == $date){ // list only files for the date we requested
                    // Put those times into an array, getting the hour and minute
                    $dirDay[] = substr($dirArray[$index],0,12);
                    }
                        
				}	
		
            
            //now with our dirDay array (a litst of dates) we will grab the three plots and show them in the same order
            echo '<p>'.(count($dirDay)/3).' Flights on '.$datePHP->format('d M Y').'<br>';
            foreach (array_unique($dirDay) as $datei){
                
                echo '<a target="_blank"href="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_map_ozone.png">'.$datei.'</a><br>';
                echo '<br><img class="style1" width="60%" src="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_map_ozone.png" alt="no ozone map"><br><br>';

                echo '<a target="_blank"href="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_scatter_ozone-theta.png">'.$datei.'</a><br>';
                echo '<br><img class="style1" width="60%" src="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_scatter_ozone-theta.png" alt="no ozone scatter"><br><br>';
                
                echo '<a target="_blank"href="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_timeseries_ozone-elevation.png">'.$datei.'</a><br>';
                echo '<br><img class="style1" width="60%" src="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_timeseries_ozone-elevation.png" alt="no ozone timeseries"><br><br>';
                
                echo '<a target="_blank"href="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_map.png">'.$datei.'</a><br>';
                echo '<br><img class="style1" width="60%" src="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_map_pm25.png" alt="no pm25 map"><br><br>';

                echo '<a target="_blank"href="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_scatter_pm25-theta.png">'.$datei.'</a><br>';
                echo '<br><img class="style1" width="60%" src="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_scatter_pm25-theta.png" alt="no pm25 scatter"><br><br>';
                
                echo '<a target="_blank"href="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_timeseries_pm25-elevation.png">'.$datei.'</a><br>';
                echo '<br><img class="style1" width="60%" src="http://home.chpc.utah.edu/~u0553130/oper/KSL_daily/'.$datei.'_KSL5_timeseries_pm25-elevation.png" alt="no pm25 timeseries"><br><br>';
                echo '<hr size=10 noshade><br>';
            }
                           
			
            
			?>
	</div>

				



	<br>
	<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>

