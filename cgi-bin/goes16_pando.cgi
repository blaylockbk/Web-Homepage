#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
September 25, 2017

Display thumbnail image of GOES-16 true color for every time. Image on Pando.

Details of GOES-16 data:
http://www.goes-r.gov/products/images/productFileSize8ColorPng8-1600px.png

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

yesterday = date.today() - timedelta(days=1)
max_date = date.today().strftime('%Y-%m-%d')

try:
    domain = form['domain'].value
except:
    domain = 'CONUS'    # CONUS or UTAH
try:
    Date = form['date'].value
except:
    Date = date.today().strftime('%Y-%m-%d')


print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>GOES-16 on Pando</title>
<style>
      .mybtn {
          border: 1px solid #23415c;
          color: white;
          padding: 5px 8px;
          margin: -3px;
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
        document.getElementById("sounding_img").style.maxWidth= '1000px';
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
        <i class="fa fa-globe"></i> GOES-16 on Pando
        <button type="button" class="btn btn-info" data-toggle="modal" data-target="#myModal"><i class="fa fa-info-circle"></i> Info</button>
    </h1>
    <center>
    <div class='btn-group'>
    <a class='btn btn-primary' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi"><i class="fab fa-aws"></i> GOES on Amazon</a>
    <a class='btn btn-primary' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_AWS_download.cgi?DATASET=noaa-goes16"><i class="fas fa-list"></i></a>
    </div>
    <div class='btn-group'>
    <a class='btn btn-primary active' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_pando.cgi"><i class="fa fa-database"></i> GOES on Pando</a>
    <a class='btn btn-primary' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=GOES16"><i class="fas fa-list"></i></a>
    </div>
    <a class='btn btn-warning' href="http://rammb-slider.cira.colostate.edu/"><i class="fas fa-external-link-alt"></i> CIRA SLIDER</a>
    </center>
    <br>

    <div class='alert alert-warning'>
    GOES-16 was moved to it's east position and turned back on December 14, 2017.
    <a href="http://www.goes-r.gov/users/transitiontToOperations.html">More Info</a>
    </div>

    <hr>
</div>
'''

print '''   
<div class="container">
  <form class="form-horizontal" method="GET" action="./cgi-bin/goes16_pando.cgi">

<!--- Date ------------------------------>
    <div class="form-group">
        <label class="control-label col-md-2" for="date">Date:</label>
        <div class="col-md-4">          
            <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2017-08-03" max="'''+max_date+'''">
        </div>
    </div>
<!--- (date)----------------------------->

<!--- Domain Type ----------------------------->
    <div class="form-group">
        <label class="control-label col-md-2" for="domain">Image Sample:</label>
        <div class="col-md-4">
            <div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if domain == 'CONUS':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="domain" id="domain" autocomplete="off" value='CONUS' checked> CONUS
        </label>
        <label class="btn btn-default">
            <input type="radio" name="domain" id="domain" autocomplete="off" value='UTAH'> Utah
        </label>
    '''
elif domain == 'UTAH':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="domain" id="domain" autocomplete="off" value='CONUS'> CONUS
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="domain" id="domain" autocomplete="off" value='UTAH' checked> Utah
        </label>
    '''
print '''
            </div>
        </div>
    </div>
<!--- (domain type)----------------------------->

    <div class="form-group">        
      <div class="col-md-offset-2 col-md-4">
        <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
      </div>
    </div>
  </form>

</div>
'''

# Create list of image files available for the requested date
DATE = datetime.strptime(Date, "%Y-%m-%d")
PATH = '/ABI-L2-MCMIPC/%s/' % (DATE.strftime('%Y%m%d'))

print '<div class="container">'
print '<h4><i class="far fa-hand-point-right"></i> Hover to view image sample. Click to download CONUS .nc file. <b>'+DATE.strftime('%Y %B %d')+'</b></h4>'
print '</div>'
rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'

ls = ' ls horelS3:GOES16%s | cut -c 11-' \
        % (PATH)

rclone_out = subprocess.check_output(rclone + ls, shell=True)
flist = rclone_out.split('\n')

# Remove empty elements. There is always one at the end.
flist.remove('')

# Order the files
flist.sort() 

# List of .nc files to download
dwnldlist = np.array([f for f in flist if '.nc' in f])

# Only get Utah .png files
if domain == 'UTAH':
    figlist = np.array([f for f in flist if 'UTAH.png' in f])
else:
    figlist = np.array([f for f in flist if '.png' in f and 'UTAH.png' not in f])

scan_start = np.array([datetime.strptime(f.split('_')[3][:], 's%Y%j%H%M%S%f') for f in figlist])

scan_start_hours = np.array([a.hour for a in scan_start])
scan_start_mins = np.array([a.minute for a in scan_start])

# Text on the download button
button_display = scan_start

# Expected buttons:
expected_buttons = np.arange(2, 58, 5)

print '''
<div class='container' style='width:90%'>
<div class="row">
  <div class="col-md-4">
    <p>Number represents the scan's start minute for the hour.
    '''

# Loop over each hour of day
for i in range(24):
    print '''<div class="form-group">'''
    print '''<div class="mybtn-group">'''
    print '''<button name="hour" type="button" class="mybtn hourbtn""><b>Hour %02d</b></button>''' % (i)
    # A list of images for the button displays
    buttons = scan_start_mins[scan_start_hours==i]
    # A list of the file names for each button
    bfiles = figlist[scan_start_hours==i]
    dfiles = dwnldlist[scan_start_hours==i]
    offset = 0
    for j in range(len(expected_buttons)):
        if expected_buttons[j] in buttons:
            image_link = 'https://pando-rgw01.chpc.utah.edu/GOES16/ABI-L2-MCMIPC/%s/%s' % (DATE.strftime('%Y%m%d'), bfiles[j-offset])
            download_link = 'https://pando-rgw01.chpc.utah.edu/GOES16/ABI-L2-MCMIPC/%s/%s' % (DATE.strftime('%Y%m%d'), dfiles[j-offset])
            print '''<a href="%s"><button name="fxx" type="button" class="mybtn unselected" onmouseover=change_picture('%s')>%02d</button></a>''' % (download_link, image_link, buttons[j-offset])
        else:
            print '''<button name="fxx" type="button" class="mybtn disabled">%02d</button>''' % (expected_buttons[j])
            offset += 1

    print '''
    </div></div>'''
print '''
  </div>

  <div class="col-md-8">
  <center><img id='sounding_img' src='./images/empty.jpg' width=60%></center>
  <hr>
  <div align=right><a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/goes16_pando.cgi"><i class="fab fa-github"></i> Page</a>
  <a href="https://github.com/blaylockbk/HorelS3-Archive/blob/master/GOES_downloads/download_GOES16.py"><i class="fab fa-github"></i> Plot</a>
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
          <p>This GOES-16 archive is hosted on the Pando archive system at 
             <a href="https://www.chpc.utah.edu/" target="_blank">Utah's
             Center for High Performance Computing</a>. It contains the <b>ABI-L2-MCMIPC</b>
             (level 2, 2 km, multi-band) data files from the noaa-goes16 bucket hosted on
             Amazaon AWS. We began downloading these when we realized that AWS
             only contains data from the last 60 days. The earliest date in 
             this archive is August 3, 2017.
          
          <h5><b>Using this page</b></h5>
          <p>Select a <i>Date</i> and an <i>Image Sample</i>, and click <i>Submit</i>.
          <p>Hover your mouse over the buttons to see a sample true-color image
             with nighttime IR band. I like to hover from top to bottom to get 
             a general idea of the day, and I hover from left to right when I want
             to look at a particular fine-scale feature.
          <p>Click the button to download the NetCDF file from the Pando archive. 
          
          <h5><b>File Name Details</b></h5>
          <p>An example file name:<br> <span style="font-family:monospace">OR_ABI-L2-MCMIPC-M3_G16_s20172330202189_e20172330204562_c20172330205056.nc</span>
            <ul style="padding-left:35px;">
                <li>OR - data is operational and in real-time
                <li>ABI-L2-MCMIPC-M3 - is the product. C is for CONUS. M3 is for mode 3.
                <li>G16 - GOES-16
                <li>s20172511100550 - scan start time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second
                <li>e20172511101007 - scan end time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second
                <li>c20172511101048 - scan file creation time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second
            </ul>
            <p>More details can be found on <a href="https://aws.amazon.com/public-datasets/goes/">Amazon's page</a>.
            
            <h5><b>Other details that may answer your questions.</b></h5>
            <p>I created a companion webpage,
               <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi" target="_blank">
               GOES-16 on Amazon</a>, to help you
               explore the additional files available on the Amazon AWS archive.
            <p>Presently, this page is the only way to explore the files in the Pando archive.
               This isn't helpful if you want to download lots of data with a script,
               becuase the file names are unpredictable.
            <p>If you want data from the last 60 days, I suggest grabbing it
               directly from Amazon AWS where you can use rclone or similar 
               command line software that can list files in the buckets and 
               download directly.
            <p><a href="http://www.goes-r.gov/resources/docs.html" target="_blank">Additional GOES-16 Documents</a>
            <p><a href="http://rammb-slider.cira.colostate.edu/" target="_blank">CIRA GOES-16 Viewer</a>
            <p><a href="http://www.sciencedirect.com/science/article/pii/S0098300417305083?via%3Dihub" target="_blank">Details on Pando Archive</a>
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
