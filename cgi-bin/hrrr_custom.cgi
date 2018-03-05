#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
March 5, 2018
"""

import sys
import os
import subprocess
import cgi, cgitb
import time
from datetime import date, datetime, timedelta
cgitb.enable()
print "Content-Type: text/html\n"

form = cgi.FieldStorage()

today = date.today()
max_date = date.today().strftime('%Y-%m-%d')
min_date = date(2016, 7, 15)

try:
    model = form['model'].value
except:
    model = 'hrrr'

try:
    date = form['valid'].value
    DATE = datetime.strptime(date,'%Y-%m-%d_%H%M') # convert to datetime
    valid_hour = DATE.strftime('_%H%M')
except:
    date = today.strftime('%Y-%m-%d_%H%M')
    DATE = today
    valid_hour = DATE.strftime('_%H%M')

try:
    fxx = int(form['fxx'].value)
except:
    fxx = 0

try:
    location = form['location'].value
except:
    location = ''

try:
    dsize = form['dsize'].value
except:
    dsize = 'conus'

if dsize != 'conus':
    location = form['location'].value
    
    # configure the latitude/longitude based on the location requested
    try:
        if ',' in location:
            # User put inputted a lat/lon point request
            lat, lon = location.split(',')
            lat = float(lat)
            lon = float(lon)
        else:
            # User requested a MesoWest station
            stninfo = get_station_info([location])
            lat = stninfo['LAT']
            lon = stninfo['LON']
    except:
        print ('<script>alert("Error with Location")</script>')

try:
    plotcode = (form['plotcode'].value).split(',')
except:
    plotcode = ['dBZ_Fill']

try:
    background = form['background'].value
except:
    background = 'arcgis'


print '''
<!DOCTYPE html>
<html>

<head>
<title>HRRR Custom</title>
<link rel="stylesheet" href="../css/brian_style.css" />
<script src="../js/site/siteopen.js"></script>


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

        var URL = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi'
        + '?model=' + document.querySelector('input[name="model"]:checked').value
        + '&valid=' + document.getElementById('validdate').value + document.getElementById('validhour').value
        + '&fxx=' + document.getElementById('fxx').value
        + '&location=' + document.getElementById('location').value
        + '&plotcode=' + $('#plotcode').val()
        + '&dsize=' + document.querySelector('input[name="dsize"]:checked').value
        + '&background=' + document.querySelector('input[name="background"]:checked').value;

        var dwnldURL = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi'
        + '?model=oper'
        + '&field=sfc'
        + '&date=' + document.getElementById('validdate').value
        + '&link2=grib2';
        /*
        alert(URL);
        alert(document.querySelector('input[name="background"]:checked').value);
        */

        /*Set image as the new picture*/
        document.getElementById('dwnldGRIB2').href = dwnldURL;
        document.getElementById('MapLink').href = URL;
        var hrrrimg = document.getElementById('MapImage')
        hrrrimg.src = URL;

        /* We need to find when the image is returned (Thank you Adam Abernathy for this snippiet)*/
        var $appLoading = document.getElementById('app-loading');
        $appLoading.classList.remove('hidden');          
        hrrrimg.onload = function () { (this.height && this.width) ? ($appLoading.classList.add('hidden')) : (console.warn('Image load error')) }
    
    }

    function IMG_LOADING(){
        /* We need to find when the image is returned (Thank you Adam Abernathy for this snippiet)*/
        var $appLoading = document.getElementById('app-loading');
        $appLoading.classList.remove('hidden');          
        hrrrimg.onload = function () { (this.height && this.width) ? ($appLoading.classList.add('hidden')) : (console.warn('Image load error')) }
    }

</script>

</head>


<body>

<a name="TOP"></a>
<script src="./js/site/sitemenu.js"></script>	

<h1 align="center"><i class="far fa-map"></i> HRRR Custom Surface Maps</h1>


<center>
<div class="row" id="content">
    <div class=" col-md-1">
    </div>
    <div class=" col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_golf.html" style="width:100%"> <i class="fa fa-map-marker-alt"></i> Point Forecast</a>      
    </div>
    <div class="col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_fires.html" style="width:100%"><i class="fa fa-fire-extinguisher"></i> Fires Forecast</a>
    </div>
    <div class="col-md-2">
<a class='btn btn-danger active' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_custom.html" style="width:100%"> <i class="far fa-map"></i> Custom Maps</a>
    </div>
    <div class="col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrrX-hrrr.cgi" style="width:100%"> <i class="fa fa-map"></i> Compare Maps</a>
    </div>
    <div class="col-md-2">
<a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" style="width:100%"> <i class="fa fa-database"></i> HRRR Archive</a>
    </div>
</div>
</center>



<center>
<div class="row" style="margin:50px"><div class="col-sm-1"></div><div class="col-sm-3" style="min-width:400px">

<div id="container">

<form class="form-horizontal">
    
    <div class="form-group">
      
      <div class="col-sm-12">
'''

# --- Model Type --------------------------------------------------------------
if model == 'hrrr':
    print '''
        <div class="btn-group btn-group-justified" data-toggle="buttons">
            <label class="btn btn-default active">
                <input type="radio" name="model" value='hrrr' checked> HRRR
            </label>
            <label class="btn btn-default">
                <input type="radio" name="model" value='hrrrX'> HRRR-X
            </label>
            <label class="btn btn-default">
                <input type="radio" name="model" value='hrrrAK'> HRRR-Ak
            </label>
        </div>'''
elif model == 'hrrrX':
    print '''
        <div class="btn-group btn-group-justified" data-toggle="buttons">
            <label class="btn btn-default">
                <input type="radio" name="model" value='hrrr' checked> HRRR
            </label>
            <label class="btn btn-default active">
                <input type="radio" name="model" value='hrrrX'> HRRR-X
            </label>
            <label class="btn btn-default">
                <input type="radio" name="model" value='hrrrAK'> HRRR-Ak
            </label>
        </div>'''
elif model == 'hrrrak':
    print '''
        <div class="btn-group btn-group-justified" data-toggle="buttons">
            <label class="btn btn-default">
                <input type="radio" name="model" value='hrrr' checked> HRRR
            </label>
            <label class="btn btn-default">
                <input type="radio" name="model" value='hrrrX'> HRRR-X
            </label>
            <label class="btn btn-default active">
                <input type="radio" name="model" value='hrrrAK'> HRRR-Ak
            </label>
        </div>'''

print '''
      </div>

    </div>
'''

# --- Valid Date --------------------------------------------------------------
print '''
    <div class="input-group" data-toggle="tooltip" title="Valid Date">
            <span class="input-group-addon"><i class="fa fa-calendar fa-fw"></i></span>
            <input name="date" type="date" required style="width:100%" class="form-control btn btn-default" id="validdate" min="'''+min_date.strftime('%Y-%m-%d')+'''">
    </div>
'''

# --- Valid Hour --------------------------------------------------------------
print '''
    <br>
    <div class="input-group" data-toggle="tooltip" title="Valid Hour">
            <span class="input-group-addon"><i class="far fa-clock fa-fw"></i></span>
            <select class="form-control" id="validhour">
'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['%02d:00 UTC' % i for i in range(24)]
value = ['_%02d00' % i for i in range(24)]

for i in range(len(value)):
   if valid_hour == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print'''    </select>

    </div>
'''

# --- Forecast Hour -----------------------------------------------------------
print '''
    <br>
    <div class="input-group" data-toggle="tooltip" title="Forecast Hour">
            <span class="input-group-addon"><i class="fa fa-forward fa-fw"></i></span>
            <select class="form-control" id="fxx">
'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['f%02d' % i for i in range(19)]
value = [str(i) for i in range(19)]

for i in range(len(value)):
   if str(fxx) == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print'''    </select>

    </div>
    <br>
'''

# --- Location ----------------------------------------------------------------
print '''
    <div class="input-group" data-toggle="tooltip" title="A MesoWest Station ID or comma separated lat,lon">
            <span class="input-group-addon"><i class="fa fa-map-marker fa-fw"></i></span>
            <div class="col-sm-8">
                <input type="text" required class="form-control" id="location" placeholder="ex: KSLC or 40.8,-111.9" value='''+location+'''>
            </div>
            <div class="col-sm-4">
                <button  data-toggle="tooltip" title='Must be in CONUS' type="button" onclick="GetUserLocation();" class="btn btn-sm btn-default">My Location</button>
            </div>
    </div>
    <br>
'''

# --- Plot Codes --------------------------------------------------------------
print '''
    <div class="input-group" data-toggle="tooltip" title="Hold ctrl to select multiple layers">
            <span class="input-group-addon"><i class="fa fa-map-signs fa-fw"></i></span>
            <select multiple class="form-control" id="plotcode" size=8>
                <optgroup label="Near Surface Winds">
'''
value_display = [['10mWind_Fill','10 m Wind: Fill'],
                 ['10mWind_Shade','10 m Wind: High Winds'],
                 ['10mWind_Barb','10 m Wind: Barbs'],
                 ['10mWind_Quiver','10 m Wind: Quiver'],
                 ['80mWind_Fill','80 m Wind: Fill'],
                 ['80mWind_Shade','80 m Wind: High Winds'],
                 ['80mWind_Barb','80 m Wind: Barbs'],
                 ['80mWind_Quiver','80 m Wind: Quiver'],
                 ['Gust_Hatch','Surface Gust: Hatch']]

for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
         <optgroup label='Surface Level'>'''

value_display = [['2mTemp_Fill','2 m Temperature: Fill'],
                 ['2mTemp_Freeze','2 m Temperature: 0&degC Line'],
                 ['2mRH_Fill','2 m Relative Humidity: Fill'],
                 ['SkinTemp_Fill','Skin Temperature: Fill'],
                 ['2mPOT_Fill','2 m Potential Temperature: Fill']]

for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
        <optgroup label='Reflectivity and Precipitation'>'''
                    
value_display = [['dBZ_Fill','Radar Simulated: Fill'],
                 ['dBZ_Contour','Radar Simulated: Contour'],
                 ['AccumPrecip_Fill','Precipitation, Accumulated: Fill'],
                 ['1hrPrecip_Fill','Precipitation, 1 Hour: Fill'],
                 ['SnowCover_Fill','Snow Cover: Fill']]
                
for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
         <optgroup label='Stability'>'''

value_display = [['CAPE_Fill','CAPE Surface: Fill'],
                 ['CIN_Fill','CIN Surface: Fill']]
                
for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
         <optgroup label='700 mb'>'''

value_display = [['700Temp_Fill','700 mb Temperature: Fill'],
                 ['700Temp_-12c','700 mb Temperature: -12&degC Line'],
                 ['700RH_Fill','700 mb RH: Fill']]
for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
        <optgroup label='500 mb'>'''

value_display = [['500HGT_Contour','500 mb Height: Contour'],
                 ['500Vort_Fill','500 mb Vorticity: Fill'],
                 ['500Conv_Fill','500 mb Convergence: Fill'],
                 ['500Wind_Fill','500 mb Wind: Fill'],
                 ['500Wind_Barb','500 mb Wind: Barb'],
                 ['500Wind_Quiver','500 mb Wind: Quiver']]
for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
         <optgroup label='Seal Level'>'''
 
value_display= [['MSLP_Contour','Mean Sea Level: Contour'],
                ['MSLP_Fill','Mean Sea Level: Fill']]
for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
         <optgroup label='Red Flag'>'''

value_display = [['RedFlag_Fill','Red Flag Criteria: Fill'],
                 ['RedFlag_Contour','Red Flag Criteria: Contour'],
                 ['RedFlagPot_Fill','Red Flag Potential: Fill']]

for i in range(len(value_display)):
    if value_display[i][0] in plotcode:
        print '''<option selected value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''
    else:
        print '''<option value='''+value_display[i][0]+'''>'''+value_display[i][1]+'''</option>'''

print '''</optgroup>
        </select>
    </div>'''

# --- Domain Size -------------------------------------------------------------
domains = ['small', 'medium', 'large', 'xlarge', 'xxlarge', 'xxxlarge', 'conus']

icons = ['<i class="fa fa-stop fa-xs" data-toggle="tooltip" title="50 km"></i>',
         '<i class="fa fa-stop fa-sm" data-toggle="tooltip" title="125km"></i>',
         '<i class="fa fa-stop" data-toggle="tooltip" title="500 km"></i>',
         '<i class="fa fa-stop" data-toggle="tooltip" title="1,000 km"></i>',
         '<i class="fa fa-stop fa-lg" data-toggle="tooltip" title="2,000 km"></i>',
         '<i class="fa fa-stop fa-2x" data-toggle="tooltip" title="3,000 km"></i>',
         '<i class="fa fa-globe fa-2x" data-toggle="tooltip" title="CONUS"></i>']

checked = map(lambda x: x==dsize, domains)


print '''
    <label class="control-label">Domain Size</label>
    <div class="form-group">

      <div class="col-sm-12">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
'''

for i, d in enumerate(domains):
    if checked[i] == True:
        print '''            
            <label class="btn btn-default active" >
                <input type="radio" name="dsize" value="'''+d+'''" checked>'''+icons[i]+'''
            </label>'''
    else:
        print '''            
            <label class="btn btn-default" >
                <input type="radio" name="dsize" value="'''+d+'''">'''+icons[i]+'''
            </label>'''
print '''
        </div>
      </div>
    </div>
'''

# --- Background --------------------------------------------------------------
backgrounds = ['arcgis', 'arcgisRoad', 'arcgisSat', 'terrain', 'landuse', 'none']

icons = ['<i class="fa fa-globe" data-toggle="tooltip" title="ArcGIS Shaded Relief (not for CONUS)"></i>',
         '<i class="fa fa-road" data-toggle="tooltip" title="ArcGIS Roads (not for CONUS)"></i>',
         '<img src="./images/icon_satellite.svg" width="20px" data-toggle="tooltip" title="ArcGIS Imagery (not for CONUS)">',
         '<i class="fa fa-wifi fa-rotate-180" data-toggle="tooltip" title="Model Terrain (200m Contours)"></i>',
         '<i class="fa fa-tree" data-toggle="tooltip" title="Model Landuse"></i>',
         '<i class="far fa-square"  data-toggle="tooltip" title="I despise background images"></i>']

checked = map(lambda x: x==background, backgrounds)


print '''
    <label class="control-label">Background</label>
    <div class="form-group">

      <div class="col-sm-12">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
'''

for i, b in enumerate(backgrounds):
    if checked[i] == True:
        print '''            
            <label class="btn btn-default active">
                <input type="radio" name="background" value="'''+b+'''" checked>
                '''+icons[i]+'''
            </label>'''
    else:
        print '''            
            <label class="btn btn-default">
                <input type="radio" name="background" value="'''+b+'''">
                '''+icons[i]+'''
            </label>'''


print '''
        </div>
      </div>
    </div>


    <div class="form-group">        
        <div class="col-sm-offset-2 col-sm-9">
            <button type="button" onclick="ChangeImage();" class="btn btn-lg btn-success" style="width:45%;min-width:100px">Submit</button>
        </div>
    </div>
  </form>

</div>



</div>

<div class="col-sm-7">
    
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

    <a id='MapLink' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?plotcode=dBZ_Fill&valid='''+date+'''&dsize='''+dsize+'''&background='''+background+'''" target='_blank'>
        <img class='style1' id='MapImage' style="width:100%;max-width:700px" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?plotcode=dBZ_Fill&valid='''+date+'''&dsize='''+dsize+'''&background='''+background+'''">
    </a>
    <br>
    <p>Wind Barbs (if present): half=2.5, full=5, flag=25 m s<sup>-1</sup>
    <p><a data-toggle="modal" data-target="#LUmodal">Landuse Legend</a>
    <p><a data-toggle="modal" data-target="#RFmodal">Red Flag Legend</a>

    <p><a href="#" id='dwnldGRIB2' class="btn btn-default" role="button"><i class="fa fa-download"></i> GRIB2</a>

    <!-- Accordion Advanced Options-->
    <div class="panel-group">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a data-toggle="collapse" href="#collapse1">Future Features</a>
                </h4>
            </div>
            <div id="collapse1" class="panel-collapse collapse">
                <div class="panel-body">
                <div class="form-group"  style="margin-left:1px;margin-right:1px">
                    <p> Features coming soon, but can't now becuase CHPC doesn't have shapefile installed on this version of Python
                    <p><input type="checkbox" id="outlineFires"> Fire outlines</input>
                    <p><input type="checkbox" id="ScatterMesoWest"> MesoWest Station Locations</input>
                    <p><input type="checkbox" id="ScatterMesoWest"> GOES-16 Background Image</input>
                    <p><input type="checkbox" id="ScatterMesoWest"> User sets alpha image</input>
                    <p><input type="checkbox" id="ScatterMesoWest"> HRRR and HRRRx comparison</input> 
                    <p><input type="checkbox" id="ScatterMesoWest"> Ability to loop through valid time and forecast time</input>                        
                </div>
                </div>
            </div>
        </div>
    </div> 

    <p><a href="https://github.com/blaylockbk/Web-Homepage/blob/master/hrrr_custom.html" target="_blank"><i class="fab fa-github"></i> Page HTML code</a>
    <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrr_custom.cgi" target="_blank"><i class="fab fa-github"></i> Image Python/CGI code</a>
    

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

<script src="./js/site/siteclose.js"></script>
</body>
</html>
'''