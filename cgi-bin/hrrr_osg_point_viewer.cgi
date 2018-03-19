#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
February 16, 2018                                  Going to Logan after work :)

Display thumbnail image of OSG Statistics and HRRR model run for a point area.

"""

import sys
import numpy as np
import os
import subprocess
import cgi, cgitb
import time
from datetime import date, datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

try:
    stn = (form['station'].value).upper()
except:
    stn = 'WBB'
try:
    variable = form['variable'].value
except:
    variable = 'TMP_2_m'


print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="../js/site/siteopen.js"></script>
<title>HRRR Percentiles</title>
 
</head>'''


print '''
<script>
hour = '00';
fxx = '00';
AHXX = '00';
AFXX = '00';
function change_pic_h(HXX){
        /*onhover or onclick*/
        hour = HXX;
        var img = 'http://home.chpc.utah.edu/~u0553130/PhD/HRRR/OSG/area_current_HRRR/'''+stn+'/'+variable+'''/h'+hour+'_f'+fxx+'.png';
        document.getElementById("disp_img").src = img;
		document.getElementById("disp_img").style.width= '100%';
        document.getElementById("disp_img").style.maxWidth= '1300px';
        document.getElementById('H'+AHXX).classList.remove('active');
        document.getElementById('H'+HXX).classList.add('active');
        AHXX = HXX;
	}

function change_pic_f(FXX){
        /*onhover or onclick*/
        fxx = FXX;
        var img = 'http://home.chpc.utah.edu/~u0553130/PhD/HRRR/OSG/area_current_HRRR/'''+stn+'/'+variable+'''/h'+hour+'_f'+fxx+'.png';
		document.getElementById("disp_img").src = img;
		document.getElementById("disp_img").style.width= '100%';
        document.getElementById("disp_img").style.maxWidth= '1300px';
        document.getElementById('F'+AFXX).classList.remove('active');
        document.getElementById('F'+FXX).classList.add('active');
        AFXX = FXX;
	}
</script>
'''

print '''
<body>
<script src="js/site/sitemenu.js"></script>
'''

print'''
<div class="container">
    <h1 align="center">
        <i class="fas fa-chart-area" aria-hidden="true"></i> HRRR Percentiles
        <button type="button" class="btn btn-info" data-toggle="modal" data-target="#myModal"><i class="fa fa-info-circle"></i> Info</button>
        <a class="btn btn-info" href="http://dev2.mesowest.net/cgalli/percentiles/radial.html?PSOURCE=PERCENTILES_HRRR"><i class="fa fa-chart-pie"></i> HRRR Percentile Roses</a>
        <a class="btn btn-info" href="http://dev2.mesowest.net/cgalli/percentiles/radial.html?PSOURCE=PERCENTILES2"><i class="fa fa-chart-pie"></i> MesoWest Percentile Roses</a>
    </h1>
    <hr>
</div>
'''

print '''   
<div class="container">
  <form class="form-horizontal" method="GET" action="./cgi-bin/hrrr_osg_point_viewer.cgi">

<!--- Station ---------------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="station">Station:</label>
      <div class="col-md-4">      
         <select class="form-control" id="station" name="station">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['WBB - William Browning Building', 'HWKC1 - Hawkeye CA', 'DBSU1 - Brian Head Burn Scar', 'FAKA-UNION, Florida']
value = ['WBB', 'HWKC1', 'DBSU1', '26.022,-81.512']

for i in range(0,len(value)):
   if stn == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>

      </div>
      
    </div>
<!---(Station) ----------------------->

<!--- Variable ---------------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="variable">Variable:</label>
      <div class="col-md-4">      
         <select class="form-control" id="variable" name="variable">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['2 m Temperature', '2 m Dew Point','10 m Wind Speed', '80 m Wind Speed', 'Composite Reflectivity', 'Surface Gusts', '500 mb Geopotential Height']
value = ['TMP_2_m', 'DPT_2_m', 'UVGRD_10_m', 'UVGRD_80_m', 'REFC_entire', 'GUST_surface', 'HGT_500']

for i in range(0,len(value)):
   if variable == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>

      </div>
      
    </div>
<!---(variable) ----------------------->

    <div class="form-group">        
      <div class="col-md-offset-2 col-md-4">
        <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
      </div>
    </div>
  </form>

</div>
'''

# Create list of images in directory

PATH = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/PhD/HRRR/OSG/area_current_HRRR/%s/%s/' % (stn, variable)

print '<div class="container">'
print '<h4><i class="far fa-hand-point-right" aria-hidden="true"></i> Hover to view image sample. Click to go to image source. <b>'+PATH+'</b></h4>'
print '</div>'


flist = os.listdir(PATH)

# Remove empty elements. There is always one at the end.
flist = np.array(flist)
flist = np.sort(flist)

hours = np.array([int(f.split('_')[0][1:]) for f in flist])
fxxs = np.array([int(f.split('_')[1][1:3]) for f in flist])


# Text on the download button
button_display = np.array(['f%02d' % f for f in fxxs])

# Expected buttons:
expected_buttons = np.array(['f%02d' % f for f in range(0,19)])
 
print '''
<div class='container'>
'''

## Hour Buttons
print '''
<h4>Valid Hours</h4>

<div class="btn-group btn-group-justified">'''
for h in range(24):
    print '''
<a onmouseover=change_pic_h('%02d') id='H%02d' class="btn btn-primary">h%02d</a>''' % (h,h,h)
print '''
</div>
<br>
'''
## Forecast Buttons
print '''
<h4>Forecast Lead Time</h4>
<div class="btn-group btn-group-justified">'''
for f in range(19):
    print '''
<a onmouseover=change_pic_f('%02d') id='F%02d' class="btn btn-warning">f%02d</a>''' % (f,f,f)
print '''
</div>
'''

print '<br>'

print '''

  <center>
    <img id='disp_img' src='./images/empty.jpg' style="width:75%" onclick='window.open(this.src)'>
    
  </center>
  <hr>
  <div align=right>
    <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrr_osg_point_viewer.cgi">
    <i class="fab fa-github" aria-hidden="true"></i> Page</a> | 
    <a href="https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_HRRR/point_area_OSG_vs_current_HRRR_run">
    <i class="fab fa-github" aria-hidden="true"></i> Plot</a>
  </div>
  


</div> <!--End "container"-->
'''




print '''
<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
