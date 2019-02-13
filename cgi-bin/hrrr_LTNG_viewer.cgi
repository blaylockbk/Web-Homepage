#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
November 26, 2018

Custom Photo Viewer for HRRR Lightning statistics

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
PATH = 'PhD/JFSP/'

DIR = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/' + PATH
URL = 'http://home.chpc.utah.edu/~u0553130/' + PATH


# List of the dates in the directory
list_dates = filter(lambda x: os.path.isdir(DIR+x), os.listdir(DIR))
list_dates.sort()

# Get requested date, or get today if the requested date is invalid
try:
    DATE = cgi.escape(form['DATE'].value)
    if DATE not in list_dates:
        DATE = list_dates[0]
except:
    DATE = list_dates[0]

# List the variables in the directory
'''
list_vars = filter(lambda x: os.path.isdir(DIR+'/'+DATE+'/'+x), os.listdir(DIR+'/'+DATE))
list_vars.sort()

try:
    VAR = cgi.escape(form['VAR'].value)
    if VAR not in list_vars:
        VAR = list_vars[-1]
except:
    VAR = list_vars[-1]
'''

short_path = DIR[DIR.find('public_html')+12:]+DATE


print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>HRRR Spread</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>

<script>
function change_picture(img_name, img_id){
    /*On Hover*/
    var URL = img_name;
    document.getElementById(img_id).src = URL;
    document.getElementById(img_id).src = img_name;
    document.getElementById(img_id).style.maxHeight= '80vh';
    document.getElementById(img_id).style.width='auto';
}

function change_picture3() {
        /*Select*/
        var URL = document.getElementById("mySelect").value;
        document.getElementById("hrrr_img").src = URL;
        document.getElementById(img_id).style.maxHeight= '80vh';
        document.getElementById(img_id).style.width='auto';
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
<h2 align="center"><i class="far fa-images"></i> HRRR Lightning Viewer</h2>	
'''


print '''
<form class="form-horizontal" method="GET" action="cgi-bin/hrrr_LTNG_viewer.cgi">

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
    
    for i, name in enumerate(these_buttons):
        img = "%s%s/%s" % (URL, DATE, name)
        print """<option class='btn btn-default' value="%s">%s</option>""" % (img, name)
    


path = DIR+'/'+DATE+'/'

print(path)

print "<select class='form-control'' id='mySelect' style='width:300px' onchange='change_picture3()'>"
add_buttons(os.listdir(path), action='onmouseover', img_id='hrrr_img')
print "</select>"

print '''
</div>
''' 

#else:
#    add_buttons_alt(os.listdir(DIR+DATE+VAR), action='onmouseover', img_id='hrrr_img')

print "<img class='styleT2' id='hrrr_img' src='./images/empty.jpg' alt='empty' onclick='window.open(this.src)'>"

print "<br><br>"


print '''
</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
