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
PATH = 'PhD/HRRR_RMSE/RMSE_events/'
#PATH = 'oper/HRRR_fires/'

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


short_path = DIR[DIR.find('public_html')+12:]+DATE


print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>HRRR RMSD</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>

<script>
function change_picture(img_name, img_id){
    /*On Hover*/
    var URL = img_name;
    document.getElementById(img_id).src = URL;
    /*document.getElementById(img_id).style.width= '100%';*/
    document.getElementById(img_id).style.maxWidth= '100%';
    document.getElementById(img_id).style.maxHeight= '900px';
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
<h2 align="center"><i class="far fa-images"></i> Directory Photo Viewer</h2>	
'''


print '''
<form class="form-horizontal" method="GET" action="cgi-bin/photo_viewer_RMSD.cgi">

<div class="form-group">

<!-- Select Date -->
<div class="col-md-3">
    <div class="input-group" title="Select Fire">
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
    these_buttons.sort()
    if action == 'onclick':
        txt_action = 'Click '
    elif action == 'onmouseover':
        txt_action = 'Hover: '
    print "<div  class='btn-group btn-group-justified' role='group'>"
    for i, name in enumerate(these_buttons):
        img = "%s%s/%s" % (URL, DATE, name)
        if os.path.isfile("%s/%s/%s" % (DIR, DATE, name)):
            print """<a class='btn btn-default' %s="change_picture('%s', '%s')">%s</a>""" % (action, img, img_id, name.split('-_')[1].split('-')[0])
        else:
            print "<a class='btn btn-default disabled'>%s</a>" % (i)
    print "</div>"

def add_buttons_alt(these_buttons, action='onclick', img_id='hrrr_img'):
    these_buttons.sort()
    if action == 'onclick':
        txt_action = 'Click '
    elif action == 'onmouseover':
        txt_action = 'Hover: '
    print "<div  class='btn-group btn-group-justified' role='group'>"
    for i, name in enumerate(these_buttons):
        img = "%s%s/%s" % (URL, DATE, name)
        if os.path.isfile("%s/%s/%s" % (DIR, DATE, name)):
            print """<a class='btn btn-default' %s="change_picture('%s', '%s')">%s</a>""" % (action, img, img_id, name.split('.')[0])
        else:
            print "<a class='btn btn-default disabled'>%s</a>" % (i)
    print "</div>"


type1 = filter(lambda x: x[:5]=='GLM_A', os.listdir(DIR+DATE))
type2 = filter(lambda x: x[:5]=='GLM_a', os.listdir(DIR+DATE))

if len(type1) > 0:
    # GLM/ABI/RMSD Image
    add_buttons(type1, action='onmouseover', img_id='hrrr_img')

    # GLM/Analysis/RMSD Image
    add_buttons(type2, action='onmouseover', img_id='hrrr_img')
else:
    add_buttons_alt(os.listdir(DIR+DATE), action='onmouseover', img_id='hrrr_img')

print "<img class='styleT2' id='hrrr_img' src='./images/empty.jpg' alt='empty' onclick='window.open(this.src)'>"

print "<br><br><br><br><br><br>"


print '''
</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
