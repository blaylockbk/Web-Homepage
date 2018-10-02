#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 9, 2018

Custom Photo Viewer for HRRR fire point forecast images
    /public_html/oper/HRRR_fires

Photo Viewer:
View all images in a directory by hovering, clicking, or selecting buttons.
This browser-friendly image viewer allows you to stay on the same page while
flipping through images rather than clicking the back button every time you 
want to see a different image in the directory.

WARNING: Image names in the directory can NOT have any spaces!!

http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html
"""

import os
import cgi, cgitb
from datetime import datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

# Set the directory
PATH = 'oper/HRRR_fires/'

DIR = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/' + PATH
URL = 'http://home.chpc.utah.edu/~u0553130/' + PATH


# List of the dates in the directory
list_dates = filter(lambda x: os.path.isdir(DIR+x), os.listdir(DIR))
list_dates.sort()

# Get requested date, or get today if the requested date is invalid
try:
    DATE = cgi.escape(form['DATE'].value)
    if DATE not in list_dates:
        DATE = list_dates[-1]
except:
    DATE = list_dates[-1]

# List of the available hours for the requested DATE
list_hours = filter(lambda x: os.path.isdir(DIR+DATE+'/'+x), os.listdir(DIR+DATE+'/'))
list_hours.sort()

# Get requested hour, or get latest hour if invalid
try:
    HOUR = cgi.escape(form['HOUR'].value)
    if HOUR not in list_hours:
        HOUR = list_hours[-2]
except:
    HOUR = list_hours[-2]

# List the fires in the directory
list_fires = filter(lambda x: os.path.isdir(DIR+DATE+'/'+HOUR+'/'+x), os.listdir(DIR+DATE+'/'+HOUR+'/'))
list_fires.sort()

try:
    FIRE = cgi.escape(form['FIRE'].value)
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
function change_picture(img_name, img_id){
    /*On Hover*/
    var URL = "'''+URL+'''"+img_name;
    document.getElementById(img_id).src = URL;
    /*document.getElementById(img_id).style.width= '100%';*/
    document.getElementById(img_id).style.maxWidth= '100%';
    document.getElementById(img_id).style.maxHeight= '600px';
}

function empty_picture(img_name){
    /*the empty picture on load*/
    document.getElementById(img_id).src = img_name;
    document.getElementById(img_id).style.width= '30%';
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
'''

print'''
<div class='container'>
<h2 align="center"><i class="fa fa-fire-extinguisher"></i> Fires Viewer
<a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_fires.html" class='btn btn-danger'> Fires Dashboard</a>
<button type="button" class="btn btn-info" data-toggle="modal" data-target="#myModal"><i class="fa fa-info-circle"></i> Info</button>
</h2>	
'''

print '''
<form class="form-horizontal" method="GET" action="cgi-bin/photo_viewer_fire.cgi">

<div class="form-group">
<!-- Select Fire -->
<div class="col-md-3">
    <div class="input-group" title="Select Fire">
    <span class="input-group-addon"><i class="fa fa-fire fa-fw"></i></span>          
    <select class="form-control" id="FIRE" name="FIRE" onchange="this.form.submit()">
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
<!--(Select Fire) -->

<!-- Select Date -->
<div class="col-md-3">
    <div class="input-group" title="Select Date">
    <span class="input-group-addon"><i class="far fa-calendar-alt fa-fw"></i></span>
    <select class="form-control" id="DATE" name="DATE" onchange="this.form.submit()">
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
<!--(Select Date) -->

<!-- Select Hour -->
<div class="col-md-3">
    <div class="input-group" title="HRRR Initialization Hour">
    <span class="input-group-addon"><i class="far fa-clock fa-fw"></i></span>
    <select class="form-control" id="HOUR" name="HOUR" onchange="this.form.submit()">
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
<!--(Select Hour) -->

<!-- Submit Button -->
<div class="form-group">        
    <div class="col-md-3">
        <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
    </div>
</div>
<!-- (Submit Button) -->
</div>
</form>
'''
print "<h3 align='center'><small>%s</small></h3>" % short_path

def add_buttons(these_buttons, action='onclick', img_id='hrrr_img'):
    if action == 'onclick':
        txt_action = 'Click '
    elif action == 'onmouseover':
        txt_action = 'Hover: '
    print txt_action + "<div  class='btn-group btn-group-justified' role='group'>"
    for i in these_buttons:
        img = DATE+'/'+HOUR+'/'+FIRE+'/'+i+'.png'
        if os.path.isfile(DIR+img):
            print """<a class='btn btn-default' %s="change_picture('%s', '%s')">%s</a>""" % (action, img, img_id, i)
        else:
            print "<a class='btn btn-default disabled'>%s</a>" % (i)
    print "</div><br>"

print """
<ul class="nav nav-tabs">
    <li class="active btn-lg"><a data-toggle="tab" href="#pill_1">HRRR</a></li>
    <li class="btn-lg"><a data-toggle="tab" href="#pill_2">GOES</a></li>
</ul>
"""

print """
<div class="tab-content">
    <div id="pill_1" class="tab-pane fade in active">
"""
# F00-F18
add_buttons(['f%02d' % i for i in range(19)], action='onmouseover', img_id='hrrr_img')
    
# Hovemollers
add_buttons(['TMP', 'DPT', 'RH', 'WIND', 'RedFlag', 'REF', 'Landuse'], action='onclick', img_id='hrrr_img')

print "<img class='styleT2' id='hrrr_img' src='./images/empty.jpg' alt='empty' onclick='window.open(this.src)'>"

print """
    </div>
    <div id="pill_2" class="tab-pane fade">
"""
# GOES-16 images
add_buttons(['G%02d' % i for i in range(2,60,5)], action='onmouseover', img_id='goes_img')

# GLM Histograms
add_buttons(['GLM_map', 'GLM_histogram', 'GLM_proximity', 'GLM_rose30', 'GLM_rose60', 'GLM_rose90'], action='onclick', img_id='goes_img')

print "<img class='styleT2' id='goes_img' src='./images/empty.jpg' alt='empty' onclick='window.open(this.src)'>"

print """
    </div>
</div>
"""




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
          <p> The figures are generated every hour. The inputs row lets you 
              change images for each fire, date, and hour. You change the
              images by hovering your mouse over the buttons.
          <p style="font-weight:bold">Hover Button Rows  
            <ol>
            <li>Images from GOES-16 for the hour selected. There are images 
                every 5 minutes. The image is a blended "TrueColor" and 
                "FireTemperature" product, with GLM lightning data showing 
                flashes indicated by small yellow crosshairs. Be aware of 
                <a href="http://cimss.ssec.wisc.edu/goes/blog/archives/217" target='_blank'>"parallax"</a>
                which makes tall clouds appear larger and lightning point data
                to appear skewed. The GLM data is parallax corrected with an
                assumed cloud height.
            <li>Lightning data from the Geostationary Lightning Mapper: note, 
                the lightning mapper "measures" total lightning 
                (intracloud+cloud-to-ground) simply by identifying "bright" 
                regions in the near IR channel and interprets those flashes as 
                lightning. You will notice some parallax in the GOES-16 images 
                (flash are shifted slightly south of the cloud's convective 
                center) which I haven't solved yet. The idea with these plots 
                is to show where the lightning has been observed and how it has
                moved in the last 90 minutes. 
                <a href="https://www.goes-r.gov/products/ATBDs/baseline/Lightning_v2.0_no_color.pdf" target='_blank'>GLM Documentation</a>.
                <ul>
                    <li>GLM_map - map centered on fire start location, a 300 
                        mile radius is shown in red, and the accumulated 
                        flashes for the previous 0-30 minutes (black), 
                        30-60 minutes (grey), and 60-90 minutes (white). 
                        The HRRR 500 mb wind barbs are plotted using HRRR data 
                        from that hour. 
                    <li>GLM_histogram - a histogram describing the distance of 
                        the flashes relative to the fire.
                    <li>GLM_proximity - a scatter plot showing flashes by 
                        distance and direction from the fire.
                    <li>GLM_rose30 - a "lightning rose" showing how many 
                        flashes are in each direction and how close they are 
                        relative to the fire for the previous 0-30 minutes. The
                        length of a rose petal is the count of lighting 
                        flashes in that direction. The color represents the 
                        relative distance from the fire where yellow is closer 
                        to the fire than purple.
                    <li>GLM_rose60 - same as GLM_rose30, except showing 
                        lightning for previous 30-60 minutes.
                    <li>GLM_rose90 - same, but for previous 60-90 minutes.
                </ul>
            <li>HRRR point-forecast initialized at the hour. Forecast image for each 18 forecast hours.
            <li>HRRR forecast hovmoller to show how HRRR forecasts have changed.
            </ol>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
      
    </div>
</div>
'''


print '''
</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
