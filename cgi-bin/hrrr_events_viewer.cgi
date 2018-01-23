#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
October 12, 2017

Display thumbnail image of HRRR Error statistics from CONUS.

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
    variable = form['variable'].value
except:
    variable = 'THOMAS_FIRE_2017-12-08'


print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRR Events</title>
<style>
      .mybtn {
          border: 1px solid #23415c;
          color: white;
          padding: 5px 7px;
          margin-left: -3px;
          margin-right: -3px;
          margin-bottom:-10px;
          margin-top:-10px;
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
      .hourbtn {
          background-color: #292929  ;
          color: white;
          cursor: not-allowed;
      }
  </style>
  
</head>'''


print '''
<script>
function change_picture(img_name){
        /*onhover or onclick*/
		document.getElementById("sounding_img").src = img_name;
		document.getElementById("sounding_img").style.width= '100%';
        document.getElementById("sounding_img").style.maxWidth= '700px';
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
        <i class="fa fa-globe" aria-hidden="true"></i> HRRR Events
        <button type="button" class="btn btn-info" data-toggle="modal" data-target="#myModal"><i class="fa fa-info-circle" aria-hidden="true"></i> Info</button>
    </h1>
    <hr>
</div>
'''

print '''   
<div class="container">
  <form class="form-horizontal" method="GET" action="./cgi-bin/hrrr_events_viewer.cgi">

<!--- Event ---------------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="variable">Event:</label>
      <div class="col-md-4">      
         <select class="form-control" id="variable" name="variable">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['Thomas Fire 2017-12-08', 'EAST_cyclone_SNOWC_2018-01-04', 'EAST_cyclone_MSLP-WIND_2018-01-04', 'EAST_cyclone_REFC_2018-01-04', 'EAST_cyclone_1hPCP_2018-01-04']
value = ['THOMAS_FIRE_2017-12-08', 'EAST_cyclone_SNOWC_2018-01-04', 'EAST_cyclone_MSLP-WIND_2018-01-04', 'EAST_cyclone_REFC_2018-01-04', 'EAST_cyclone_1hPCP_2018-01-04']

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

PATH = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/PhD/HRRR/Events_Day/%s/' % variable

print '<div class="container">'
print '<h4><i class="far fa-hand-point-right" aria-hidden="true"></i> Hover to view image sample. Click to go to image source. <b>'+PATH+'</b></h4>'
print '</div>'


flist = os.listdir(PATH)

# Remove empty elements. There is always one at the end.
flist = np.array(flist)
flist = np.sort(flist)

hours = np.array([int(f.split('_')[1][1:]) for f in flist])
fxxs = np.array([int(f.split('_')[2][1:3]) for f in flist])
valid = np.unique(np.array([f[0:14] for f in flist]))

# Text on the download button
button_display = np.array(['f%02d' % f for f in fxxs])

# Expected buttons:
expected_buttons = np.array(['f%02d' % f for f in range(0,19)])

print '''
<div class='container' style='width:95%'>
<div class="row">
  <div class="col-md-5">
    <p>Black Date/Time is the valid time. Blue number is the forecast lead time.
    '''

# Loop over each hour of day
for i in range(hours[-1]+1):
    print '''<div class="form-group">'''
    print '''<div class="mybtn-group">'''
    print '''<button name="hour" type="button" class="mybtn hourbtn""><b>%s</b></button>''' % (valid[i])
    # A list of images for the button displays
    buttons = button_display[hours==i]
    # A list of the file names for each button
    imgfiles = flist[hours==i]
    offset = 0
    for j in range(len(expected_buttons)):
        if expected_buttons[j] in buttons:
            image_link = 'http://home.chpc.utah.edu/~u0553130/PhD/HRRR/Events_Day/%s/%s' % (variable, imgfiles[j-offset])
            download_link = 'http://home.chpc.utah.edu/~u0553130/PhD/HRRR/Events_Day/%s/%s' % (variable, imgfiles[j-offset])
            print '''<a href="%s" target="_blank"><button name="fxx" type="button" class="mybtn unselected" onmouseover=change_picture('%s')>%s</button></a>''' % (download_link, image_link, buttons[j-offset])
        else:
            print '''<button name="fxx" type="button" class="mybtn disabled">%s</button>''' % (expected_buttons[j])
            offset += 1

    print '''
    </div></div>'''
print '''
  </div>

  <div class="col-md-7">
  <center><img id='sounding_img' src='./images/empty.jpg' style="width:90%"></center>
  <hr>
  <div align=right><a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrr_events_viewer.cgi">
        <i class="fab fa-github" aria-hidden="true"></i> Page</a>
  <a href="https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_HRRR/plot_HRRR_custom_maps_EVENT.py">
        <i class="fab fa-github" aria-hidden="true"></i> Plot</a>
  </div>
  </div>

</div> <!--End "row"-->
</div> <!--End "container"-->
'''


print '''
<script>
        $(document).ready(function () {
            $('.unselected').click(function () {
                $(this).toggleClass("selected unselected");
            });
            $('.selected').click(function () {
                $(this).toggleClass("selected unselected");
            });
            
            $('.btn').click(function() {
            ;
        });
        });
</script>
'''

print '''
<!-- Modal -->
<div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">&times;</button>
          <h4 class="modal-title">Information</h4>
        </div>
        <div class="modal-body">
          <p>Events of interest as forecasted by the HRRR model.
          <p>Uses the HRRR_custom script to create map.
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
      
    </div>
</div>
'''

print '''
<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''