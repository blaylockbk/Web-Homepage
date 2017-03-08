<html>

<head>
<title>HRRR Download</title>
<link rel="stylesheet" href="./css/brian_style.css" />
<script src="./js/site/siteopen.js"></script>
  <style>
      .mybtn {
          border: 1px solid #366391;
          color: white;
          padding: 5px 10px;
          margin: -3px;
          outline: none;
      }
      
      .selected {
          background-color: #09437F;
      }
      
      .unselected {
          background-color: #2D71B7;
      }
      .unselected:hover{
          background-color: #2765a3;
      }
      
      .disabled {
          background-color: #c0d5eb  ;
          cursor: not-allowed;
      }
  </style>
  
</head>


<body onload="form.submit()">
<a name="TOP"></a>
<script src="./js/site/sitemenu.js"></script>	

<div id="content">
    <h1 align="center">
    <i class="fa fa-cloud-download" aria-hidden="true"></i> HRRR Download Page
    <!-- Large modal (the intrusctions help button)-->
      <button type="button" name="CB"  class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" name="CB"  class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">How to use this HRRR download interface</h4><hr>
            <h5> Put some stuff here</h5>
      </div>
      </div>
      </div>
    </h1>
  
  <hr>

<div class="container">
  <form class="form-horizontal" method="post">

    <div class="form-group">
      <label class="control-label col-sm-2" for="model">Model Type:</label>
      <div class="col-sm-4">
        <select class="form-control" id="model" name="model">
          <option value="oper">HRRR (operational)</option>
          <option value="alaska">HRRRX (expermental)</option>
          <option value="exp">Alaska (experimental)</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label class="control-label col-sm-2" for="field">Variables Field:</label>
      <div class="col-sm-4">          
        <select class="form-control" id="field" name="field">
          <option value="sfc">Surface (sfc, 2D fields)</option>
          <option value="prs">Pressure (prs, 3D fields)</option>
          <option value="buf">Bufr Soundings</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label class="control-label col-sm-2" for="date">Date:</label>
      <div class="col-sm-4">          
        <input name="date" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2015-04-17">
      </div>
    </div>
    
    <div class="form-group">        
      <div class="col-sm-offset-2 col-sm-4">
        <button type="submit" class="btn btn-success">Submit</button>
      </div>
    </div>
  </form>
</div>


<!-- PHP for getting file names in the directory-->
	<?php
			$dir = "/uufs/chpc.utah.edu/common/home/horel-group/archive/HRRR";
			
			$model = $_POST['model']; // grab the model value from HTML input
      $field = $_POST['field']; // grab the field value from HTML input
      $date = $_POST['date']; // grab the date value from HTML input
			$date = DateTime::createFromFormat('Y-m-d',$date); // convert date value to PHP date format
			$date = $date->format('Ymd'); // convert date to format usable in retrieving images  
			
      echo $dir.'/'.$model.'/'.$field.'/'.$date;

      $myDirectory = opendir($dir.'/'.$model.'/'.$field.'/'.$date.'/');

    // get each entry, but only if it contains the Station Identifier
			while($entryName = readdir($myDirectory)) {
					$dirArray[] = $entryName;
			}
		
			// close directory
			closedir($myDirectory);
			
			//sort directory array by alphabetical order
			sort($dirArray);				
			
			//	count elements in array
			$indexCount	= count($dirArray);
      echo('<br>'.$indexCount);

	?>


<script src="./js/site/siteclose.js"></script>
</body>
</html>