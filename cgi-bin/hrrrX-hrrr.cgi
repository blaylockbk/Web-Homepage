#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
January 30, 2017

HRRR-X versus HRRR (difference)

To Do List:
[X] Add Bootstrap Modals for page instructions. (Jan 17, 2017)
[ ] Add aditional API query that finds the shared variables between the
    requested stations and creates a variable dropdown for the available data.
[ ] Add advanced options to modify the plot size, label fonts, dpi, etc. to 
    easily customize plots for publications.
[ ] Add MesoWest QC checks
"""

import sys
import cgi, cgitb
from datetime import datetime, timedelta
import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
import numpy as np

cgitb.enable()

form = cgi.FieldStorage()

current = datetime.now()
onedayago = datetime.now()-timedelta(days=1)
yesterday = onedayago.strftime('%Y-%m-%d')

try:
      date = form['date'].value
except:
      date = yesterday

try:
      hour = form['hour'].value
except:
      hour = '03'

try:
      domain = form['domain'].value
except:
      domain = 'GSL'

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRRx vs HRRR</title>

<script>

    function GetUserLocation(){
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        } else { 
            alert('geolocation not working for some reason. Sorry :(');
        }
    }

    function showPosition(position) {
        document.getElementById('location').value = position.coords.latitude.toFixed(2) + ',' + position.coords.longitude.toFixed(2);
    }


    function ChangeImage(){
        /*Create HTML string for changing picture*/
        var $loadingmsg = document.getElementById('app-loading')
        $loadingmsg.classList.remove('hidden')

        var URL = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrrX-hrrr.cgi'
        + '?valid=' + document.getElementById('validdate').value + document.getElementById('validhour').value
        + '&location=' + document.getElementById('location').value
        + '&plotcode=' + $('#plotcode').val()
        + '&dsize=' + document.querySelector('input[name="dsize"]:checked').value


        /*Set image as the new picture*/
        document.getElementById('MapLink').href = URL;
        var hrrrimg = document.getElementById('MapImage')
        hrrrimg.src = URL;

        /* We need to find when the image is returned (Thank you Adam Abernathy for this snippet)*/
        var $appLoading = document.getElementById('app-loading');
        $appLoading.classList.remove('hidden');          
        hrrrimg.onload = function () { (this.height && this.width) ? ($appLoading.classList.add('hidden')) : (console.warn('Image load error')) }
    }

</script>

</head>'''


print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>

<h1 align="center"><i class="fa fa-map"></i> HRRRx vs HRRR Maps
<!-- Large modal (the intrusctions help button)-->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

<div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
<div class="modal-dialog modal-lg" role="document">
<div class="modal-content" style="padding:25px">
<button type="button" class="close" data-dismiss="modal">&times;</button>
<h4 style="font-size:22px;">Utah Experimental and Operational HRRR comparison</h4><hr>
<h5 align="left" style="font-size:18px;">
Input the date and hour (UTC) for the model run you wish to see the
comparison between the HRRR and HRRR-X.
<hr>Reasons the images couldn't be plotted
<ol style="paddin-left:30px">
<li>HRRR data isn't available. More likely that the HRRRx isn't available. Try another hour or day.
<li>Browser timed out
</ol>
<br><br>
<div class='alert alert-warning'>
Note: If the requested date was not plotted, there was an error getting
it's data from the archive. There may not be model data for that time.
</div>

</div>


</div>
</div>
</div>
</h1>


<center>
<div class="row" id="content">
<div class=" col-md-1">
</div>
<div class=" col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_golf.html" style="width:100%"> <i class="fa fa-map-marker"></i> Point Forecast</a>      
</div>
<div class="col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_fires.html" style="width:100%"><i class="fa fa-fire-extinguisher"></i> Fires Forecast</a>
</div>
<div class="col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_custom.html" style="width:100%"> <i class="far fa-map"></i> Custom Maps</a>
</div>
<div class="col-md-2">
<a class='btn btn-danger active' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrrX-hrrr.cgi" style="width:100%"> <i class="fa fa-map"></i> Compare Maps</a>
</div>
<div class="col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" style="width:100%"> <i class="fa fa-database"></i> HRRR Archive</a>
</div>
</div>
</center>

<br>

<div class="container">
<div class="col-sm-offset-4 col-sm-4">

<form class="form-horizontal">
    <div class="form-group">    

    <div class="input-group" data-toggle="tooltip" title="Valid Date">
        <span class="input-group-addon"><i class="fa fa-calendar fa-fw"></i></span>
        <input name="date" type="date" required style="width:100%" class="form-control btn btn-default" id="validdate" min="2016-07-15">
    </div>
    <br>
    <div class="input-group" data-toggle="tooltip" title="Run Hour">
            <span class="input-group-addon"><i class="far fa-clock fa-fw"></i></span>
            <select class="form-control" id="validhour">
                    <option value='_0000' selected >00:00 UTC</option>
                    <option value='_0100'>01:00 UTC</option>
                    <option value='_0200'>02:00 UTC</option>
                    <option value='_0300'>03:00 UTC</option>
                    <option value='_0400'>04:00 UTC</option>
                    <option value='_0500'>05:00 UTC</option>
                    <option value='_0600'>06:00 UTC</option>
                    <option value='_0700'>07:00 UTC</option>
                    <option value='_0800'>08:00 UTC</option>
                    <option value='_0900'>09:00 UTC</option>
                    <option value='_1000'>10:00 UTC</option>
                    <option value='_1100'>11:00 UTC</option>
                    <option value='_1200'>12:00 UTC</option>
                    <option value='_1300'>13:00 UTC</option>
                    <option value='_1400'>14:00 UTC</option>
                    <option value='_1500'>15:00 UTC</option>
                    <option value='_1600'>16:00 UTC</option>
                    <option value='_1700'>17:00 UTC</option>
                    <option value='_1800'>18:00 UTC</option>
                    <option value='_1900'>19:00 UTC</option>
                    <option value='_2000'>20:00 UTC</option>
                    <option value='_2100'>21:00 UTC</option>
                    <option value='_2200'>22:00 UTC</option>
                    <option value='_2300'>23:00 UTC</option>
            </select>
    </div>
    <br>
    <div class="input-group" data-toggle="tooltip" title="A MesoWest Station ID or comma separated lat,lon">
            <span class="input-group-addon"><i class="fa fa-map-marker fa-fw"></i></span>
            <div class="col-sm-8">
                <input type="text" required class="form-control" id="location" placeholder="ex: KSLC or 40.8,-111.9">
            </div>
            <div class="col-sm-4">
                <button  data-toggle="tooltip" title='Must be in CONUS' type="button" onclick="GetUserLocation();" class="btn btn-sm btn-default">My Location</button>
            </div>
    </div>
    <br>
    <div class="input-group" data-toggle="tooltip">
            <span class="input-group-addon"><i class="fa fa-map-signs fa-fw"></i></span>
            <select multiple class="form-control" id="plotcode" size=5>
                <optgroup label='Land and Terrain'>
                    <option selected value='LandUse'>Land Use</option>
                    <option value='TerrainWater'>Terrain and Water</option>
                </optgroup>
                <optgroup label="Near Surface Winds">
                    <option value='10mWind_Fill'>10 m Wind: Fill</option>
                    <option value='10mWind_Shade'>10 m Wind: High Winds</option>
                    <option value='10mWind_Barb'>10 m Wind: Barbs</option>
                    <option value='10mWind_Quiver'>10 m Wind: Quiver</option>
                    <option value='80mWind_Fill'>80 m Wind: Fill</option>
                    <option value='80mWind_Shade'>80 m Wind: High Winds</option>
                    <option value='80mWind_Barb'>80 m Wind: Barbs</option>
                    <option value='80mWind_Quiver'>80 m Wind: Quiver</option>
                    <option value='Gust_Hatch'>Surface Gust: Hatch</option>
                </optgroup>
                <optgroup label='Surface Level'>
                    <option value='2mTemp_Fill'>2 m Temperature: Fill</option>
                    <option value='2mTemp_Freeze'>2 m Temperature: 0&degC Line</option>
                    <option value='2mRH_Fill'>2 m Relative Humidity: Fill</option>
                    <option value='SkinTemp_Fill'>Skin Temperature: Fill</option>
                    <option value='2mPOT_Fill'>2 m Potential Temperature: Fill</option>
                <optgroup label='Reflectivity and Precipitation'>
                    <option value='dBZ_Fill'>Radar Simulated: Fill</option>
                    <option value='dBZ_Contour'>Radar Simulated: Contour</option>
                </optgroup>
                </optgroup>
                <optgroup label='Stability'>
                    <option value='CAPE_Fill'>CAPE Surface: Fill</option>
                    <option value='CIN_Fill'>CIN Surface: Fill</option>
                </optgroup>
                <optgroup label='Seal Level'>
                    <option value='MSLP_Contour'>Mean Sea Level: Contour</option>
                    <option value='MSLP_Fill'>Mean Sea Level: Fill</option>
                </optgroup>
                <optgroup label='Red Flag'>
                    <option value='RedFlag_Fill'>Red Flag Criteria: Fill</option>
                    <option value='RedFlag_Contour'>Red Flag Criteria: Contour</option>
                    <option value='RedFlagPot_Fill'>Red Flag Potential: Fill</option>
                </optgroup>
            </select>
    </div>
   
    <label class="control-label">Domain Size</label>
    <div class="form-group">
      <div class="col-sm-12">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
            <label class="btn btn-default" >
                <input type="radio" name="dsize" value='small' > <i class="fa fa-stop fa-xs" data-toggle="tooltip" title="50 km"></i>
            </label>
            <label class="btn btn-default">
                <input type="radio" name="dsize" value='medium'> <i class="fa fa-stop fa-sm" data-toggle="tooltip" title="125km"></i>
            </label>
            <label class="btn btn-default">
                <input type="radio" name="dsize" value='large'> <i class="fa fa-stop" data-toggle="tooltip" title="500 km"></i>
            </label>
            <label class="btn btn-default">
                <input type="radio" name="dsize" value='xlarge'> <i class="fa fa-stop" data-toggle="tooltip" title="1,000 km"></i>
            </label>
            <label class="btn btn-default">
                <input type="radio" name="dsize" value='xxlarge'> <i class="fa fa-stop fa-lg" data-toggle="tooltip" title="2,000 km"></i>
            </label>    
            <label class="btn btn-default">
                    <input type="radio" name="dsize" value='xxxlarge'> <i class="fa fa-stop fa-2x" data-toggle="tooltip" title="3,000 km"></i>
            </label>    
            <label class="btn btn-default active">
                    <input type="radio" name="dsize" value='conus' checked> <i class="fa fa-globe fa-2x" data-toggle="tooltip" title="CONUS"></i>
            </label>
        </div>
      </div>
    </div>
    
</div>


    <div class="form-group">        
        <div class="col-sm-offset-3 col-sm-6">
            <button type="button" onclick="ChangeImage();" class="btn btn-lg btn-success btn-block">Submit</button>
        </div>
    </div>
  </form>

</div>

<div class="col-sm-12">
    
    <div class="row hidden" id="app-loading">
            <div class="col-sm-12">
                <div id="page-is-loading">
                    <div id="loading-progress" class="progress">
                        <div id="progress-bar" class="progress-bar progress-bar-danger progress-bar-striped active" role="progressbar" aria-valuemin="0"
                            aria-valuemax="100" style="width:100%">
                            <p style="font-size:20px">Generating New Image</p>
                        </div>
                    </div>
                </div>
            </div>
    </div>

    <a id='MapLink' href='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/empty.jpg' target='_blank'>
        <img class='style1' id='MapImage' style="width:100%" src='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/empty.jpg'>
    </a>
    <br>
    
    <p>Wind Barbs (if present): half=2.5, full=5, flag=25 m s<sup>-1</sup>
     | <a data-toggle="modal" data-target="#LUmodal">Landuse Legend</a> 
     | <a data-toggle="modal" data-target="#RFmodal">Red Flag Legend</a>
     | <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank"><i class="fab fa-github"></i> Page</a>
     | <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr.cgi" target="_blank"><i class="fab fa-github"></i> Plot</a>
     | 

</div><div class="col-sm-1"></div>
</div>

</center>
<br>

<!-- Landuse Legend Modal -->
<div class="modal fade" id="LUmodal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-body">
          <center><img src="./images/landuse_legend.png"></center>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
      
    </div>
  </div>
<!-- end landuse legend Modal -->

<!-- Red Flag Legend Modal -->
<div class="modal fade" id="RFmodal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-body">
          <center>
              <img src="./images/red_flag_criteria.png">
              <img src="./images/red_flag_potential.png">
          </center>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
      
    </div>
  </div>
<!-- end Red Flag legend Modal -->

</div>


<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<br>
</div>

<script>
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
});
</script>

<script>
    var today = new Date();
    var tomorrow
    var dd = today.getDate();
    var dd1 = today.getDate()+1;
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
    if(dd<10){
            dd='0'+dd
        } 
        if(mm<10){
            mm='0'+mm
        }
    today = yyyy+'-'+mm+'-'+dd;
    tomorrow = yyyy+'-'+mm+'-'+dd1;
    document.getElementById("validdate").setAttribute("max", tomorrow);
    document.getElementById("validdate").setAttribute("value", today);
</script>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
