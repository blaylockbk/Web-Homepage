#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
March 9, 2018

New Photo Viewer built with Python instead of PHP

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
Updated with new date selector: May 21, 2017

http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html
"""

import os
import cgi, cgitb
from datetime import datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

# Set the directory
DIR = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/oper/HRRR_fires/'
URL = 'http://home.chpc.utah.edu/~u0553130/oper/HRRR_fires/'

# List of the dates in the directory
list_dates = filter(lambda x: os.path.isdir(DIR+x), os.listdir(DIR))
list_dates.sort()

# Get requested date, or get today if the requested date is invalid
try:
    DATE = form['DATE'].value
    if DATE not in list_dates:
        DATE = list_dates[-1]
except:
    DATE = list_dates[-1]

# List of the available hours for the requested DATE
list_hours = filter(lambda x: os.path.isdir(DIR+DATE+'/'+x), os.listdir(DIR+DATE+'/'))
list_hours.sort()

# Get requested hour, or get latest hour if invalid
try:
    HOUR = form['HOUR'].value
    if HOUR not in list_hours:
        HOUR = list_hours[-2]
except:
    HOUR = list_hours[-2]

# List the fires in the directory
list_fires = filter(lambda x: os.path.isdir(DIR+DATE+'/'+HOUR+'/'+x), os.listdir(DIR+DATE+'/'+HOUR+'/'))
list_fires.sort()

try:
    FIRE = form['FIRE'].value
    if FIRE not in list_fires:
        FIRE = list_fires[0]
except:
    FIRE = list_fires[0]

short_path = DIR[DIR.find('public_html')+12:]+DATE+'/'+HOUR+'/'+FIRE

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>HRRR Fires</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>

<script>
function change_picture(img_name){
    /*On Hover*/
    var URL = "'''+URL+'''"+img_name;
    document.getElementById("sounding_img").src = URL;
    document.getElementById("sounding_img").style.width= '100%';
    document.getElementById("sounding_img").style.maxWidth= '1300px';
    document.getElementById("sounding_img").style.maxHeight= '600px';
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
</head>'''



print '''
<body>

<script src="js/site/sitemenu.js"></script>
</div>'''

print'''
<div class='container'>
<h2 align="center"><i class="fa fa-fire-extinguisher"></i> Fires Viewer
<a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_fires.html" class='btn btn-danger'> Fires Dashboard</a>
</h2>	
'''

print '''
<form class="form-horizontal" method="GET" action="cgi-bin/photo_viewer_fire.cgi">

<div class="form-group">
<!--- Select Fire -------------------------->
<div class="col-md-3">
    <div class="input-group" title="Select Fire">
    <span class="input-group-addon"><i class="fa fa-fire fa-fw"></i></span>          
    <select class="form-control" id="FIRE" name="FIRE">
    '''
display = list_fires
value = list_fires
for i in range(0,len(value)):
   if FIRE == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print'''
    </select>
    </div>
</div>
<!---(Select Fire) ----------------------->

<!--- Select Date -------------------------->
<div class="col-md-3">
    <div class="input-group" title="Select Date">
    <span class="input-group-addon"><i class="far fa-calendar-alt fa-fw"></i></span>
    <select class="form-control" id="DATE" name="DATE">
    '''
display = list_dates
value = list_dates
for i in range(0,len(value)):
   if DATE == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print'''
    </select>
    </div>
</div>
<!---(Select Date) ----------------------->

<!--- Select Hour -------------------------->
<div class="col-md-3">
    <div class="input-group" title="HRRR Initialization Hour">
    <span class="input-group-addon"><i class="far fa-clock fa-fw"></i></span>
    <select class="form-control" id="HOUR" name="HOUR">
    '''
display = ['%02d:00' % i for i in range(24)]
value = ['%02d00' % i for i in range(24)]
for i, value in enumerate(value):
   if HOUR == value:       
      print'''<option selected="selected" value="'''+value+'''">'''+display[i]+'''</option>'''
   elif value in list_hours:
      print'''<option value="'''+value+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option disabled style='background-color:lightgrey;' value="'''+value+'''">'''+display[i]+'''</option>'''
print'''
    </select>
    </div>
</div>
<!---(Select Hour) ----------------------->

<!--- Submit Button ---------------------->
<div class="form-group">        
    <div class="col-md-3">
        <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
    </div>
</div>
<!--- (Submit Button)--------------------->
</div>
</form>
'''
print "<h3 align='center'><small>%s</small></h3>" % short_path

# Land use and GOES-16 image
print "<div  class='btn-group btn-group-justified' role='group'>"
for i in ['G%02d' % i for i in range(2,60,5)]:
    print "<a class='btn btn-default' onmouseover=change_picture('%s')>%s</a>" % (DATE+'/'+HOUR+'/'+FIRE+'/'+i+'.png', i)
print "</div><br>"

# Hovemollers
print "<div  class='btn-group btn-group-justified' role='group'>"
for i in ['TMP', 'DPT', 'RH', 'WIND', 'RedFlag', 'REF', 'Landuse']:
    print "<a class='btn btn-default' onmouseover=change_picture('%s')>%s</a>" % (DATE+'/'+HOUR+'/'+FIRE+'/'+i+'.png', i)
print "</div><br>"

# F00-F18
print "<div  class='btn-group btn-group-justified' role='group'>"
for i in ['f%02d' % i for i in range(19)]:
    print "<a class='btn btn-default' onmouseover=change_picture('%s')>%s</a>" % (DATE+'/'+HOUR+'/'+FIRE+'/'+i+'.png', i)
print "</div>"

print "<img class='styleT2' id='sounding_img' style='width:30%;' src='./images/empty.jpg' alt='empty' onclick='window.open(this.src)'>"

print '''
</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
