#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 9, 2018

Custom Photo Viewer for HRRR point forecast (HRRR_golf) images
    /public_html/oper/HRRR_golf

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

try:
    LOC = cgi.escape(form['LOC'].value)
except:
    LOC = 'UKBKB'

# Get Contents of the current diretory 
PATH = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/oper/HRRR_golf/%s/' % LOC
URL = 'http://home.chpc.utah.edu/~u0553130/oper/HRRR_golf/%s/' % LOC
imgs = os.listdir(PATH)
imgs = filter(lambda x: x[-4:]=='.png' or x[-4:]=='.jpg', imgs)
imgs.sort()
short_path = PATH[PATH.find('public_html')+12:]

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>HRRR Golf</title>
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
<h2 align="center"><i class="far fa-image"></i> Image Viewer <small>%s</small>
<button type="button" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>
<br>
<a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_golf.html" class='btn btn-danger'><i class="fa fa-map-marker-alt"></i> More Locations</a>
''' % short_path
if LOC not in ['Oaks', 'SND', 'Orderville', 'UtahLake']:
    print '''
    <a href="http://home.chpc.utah.edu/~u0553130/oper/HRRR_anlys/%s/photo_viewer2.php" class='btn btn-primary'><i class="far fa-clock"></i> f00</a>
    <a href="http://home.chpc.utah.edu/~u0553130/oper/HRRR_f06/%s/photo_viewer2.php" class='btn btn-primary'><i class="far fa-clock"></i> f06</a>
    <a href="http://home.chpc.utah.edu/~u0553130/oper/HRRR_f12/%s/photo_viewer2.php" class='btn btn-primary'><i class="far fa-clock"></i> f12</a>
    <a href="http://home.chpc.utah.edu/~u0553130/oper/HRRR_f18/%s/photo_viewer2.php" class='btn btn-primary'><i class="far fa-clock"></i> f18</a>
    <a href="http://home.chpc.utah.edu/~u0553130/oper/HRRR_hovmoller/%s/photo_viewer.php" class='btn btn-primary'><i class="far fa-clock"></i> Hovm&oumlller</a>
    ''' % (LOC, LOC, LOC, LOC, LOC)
print "</h2>"

# Hovemoller and other plots
print "<div  class='btn-group btn-group-justified' role='group'>"
for i in imgs:
    if i not in ['f%02d.png' % I for I in range(19)]:
        print "<a class='btn btn-default' onmouseover=change_picture('%s')>%s</a>" % (i,i.split('.')[0])
print "</div>"

# Forecasts I expect to have a file for each of the forecast hours
print "<div  class='btn-group btn-group-justified' role='group'>"
for f in range(19):
    if os.path.isfile("%s/f%02d.png" % (PATH,f)):
        print "<a class='btn btn-default' onmouseover=change_picture('f%02d.png')>f%02d</a>" % (f,f)
    else:
        print "<a class='btn btn-default disabled' onmouseover=change_picture('f%02d.png')>f%02d</a>" % (f,f)
print "</div>"


print "<img class='styleT2' id='sounding_img' style='width:30%;' src='./images/empty.jpg' alt='empty' onclick='window.open(this.src)'>"

print '''
<!-- Large modal (the instructions help button)-->
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
                <p style="font-family:courier; font-size:12px">ln /uufs/chpc.utah.edu/common/home/u0553130/public_html/Brian_Blaylock/photo_viewer/photo_viewer_fire.php
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

</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
