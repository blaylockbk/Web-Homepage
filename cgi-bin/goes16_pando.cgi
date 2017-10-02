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
try:
    link2 = form['link2'].value
except:
    link2 = 'png'


print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>GOES-16 on Pando</title>
<style>
      .mybtn {
          border: 2px solid #23415c;
          color: white;
          padding: 5px 10px;
          margin: -3px;
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
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print'''
<div id="content" class="container">
    <h1 align="center">
    <i class="fa fa-globe" aria-hidden="true"></i> GOES-16 on Pando
    </h1>

<br>

<div class="container">
  <div class="panel-group" id="accordion">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h4 class="panel-title">
          <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
          <big><b><i class="fa fa-info-circle" aria-hidden="true" ></i> Download Instructions</b></big>
          </a>
        </h4>
      </div>
      <div id="collapse1" class="panel-collapse collapse">
        <div class="panel-body">
            <p> This page is tested in
            <i class="fa fa-edge" aria-hidden="true"></i> and <i class="fa fa-chrome" aria-hidden="true"></i> 
            (Why only these two? Because my advisor uses Chrome, and I use Edge.)
            <p> The Pando GOES-16 archive contains the 2 meter resolution, mutli-band formatted
                cloud and moisture product files, for the CONUS domain 
                downloaded from the Amazon noaa-goes16 bucket.
                We started downloading the files begining August 3rd 
                and storing them in our own archive because files older than
                60 days are placed in the Glacier storage on Amazon (i.e. it's 
                difficult to grab files when they are in the Glacier storage class).
            <ol style="padding-left:15px">
            <li>Select the desired domain and date for which you want to download.
            <li>Click the submit button.
            <ul style="padding-left:20px">
                <li>A blue box appears for every file that is available.
                The number on the box represents the minute the scan started.
            </ul>
            <li> Click the desired file and the download will begin.
            </ol>
            <p>Files are downloaded in NetCDF format.
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
        </div>
      </div>
    </div>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h4 class="panel-title">
          <a data-toggle="collapse" data-parent="#accordion" href="#collapse2">
          <big><b><i class="fa fa-info-circle" aria-hidden="true" ></i> Data Details</b></big>
          </a>
        </h4>
      </div>
      <div id="collapse2" class="panel-collapse collapse">
        <div class="panel-body">
        <p>Data from the Advanced Baseline Imager (ABI) is downloaded from  <a href="https://aws.amazon.com/public-datasets/goes/" class="btn btn-success">
            <i class="fa fa-amazon" aria-hidden="true"></i> Amazon S3</a>
        <p>The base download URL is https://noaa-goes16.s3.amazonaws.com
        <p>The file path is: <span style='font-family:monospace'>/product/year/day_of_year/hour/file_name</span>
        <p> Usefull Links:                
        <ul style="padding-left:60px">
            <li><a href="http://www.goes-r.gov/" target="blank">GOES-R Homepage</a>
            <li><a href="http://www.goes-r.gov/products/images/productFileSize8ColorPng8-1600px.png" target="blank">Channels Approx. File Sizes</a>            
            <li><a href="http://www.goes-r.gov/education/ABI-bands-quick-info.html" target="blank">ABI Bands Quick Information Guides</a>
            <li><a href="http://www.goes-r.gov/products/docs/PUG-L2+-vol5.pdf" target="blank">GOES-16 User Guide</a>
            <li><a href="http://www.goes-r.gov/products/ATBDs/baseline/Imagery_v2.0_no_color.pdf" target="blank">Another ABI Document</a>
            <li><a href="https://www.weather.gov/media/crp/GOES_16_Guides_FINALBIS.pdf" target="blank">NOAA GOES Guide</a>
            <li><a href="http://cimss.ssec.wisc.edu/goes/goesdata.html" target="blank">More GOES-16 Links</a>
            <li><a href="http://www.goes-r.gov/resources/docs.html" target="blank">All the GOES-R Docs</a>
        </ul>
        
        <p>Note: The resolution of the Multi-band files for all channels is 2 km.
           This file is easiest to work with if you don't <i>need</i> the full
           resolution of the 1 km channels for your images.
        
        </div>
      </div>
    </div>
  </div> 
</div>

  <hr> 
<div class="container">
  <form class="form-horizontal" method="GET" action="cgi-bin/goes16_pando.cgi">

<!---domain Type -----------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="model">Domain:</label>
      <div class="col-md-4">      
         <select class="form-control" id="model" name="domain">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['CONUS', 'Utah']
value = ['', 'UTAH']

for i in range(0,len(value)):
   if domain == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>

      </div>
      
    </div>
<!---(domain_type) ----------------------->

<!--- Date ------------------------------>
    <div class="form-group">
      <label class="control-label col-md-2" for="date">Date:</label>
      <div class="col-md-4">          
        <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2017-07-10" max="'''+max_date+'''">
      </div>
    </div>
<!--- (date)----------------------------->

<!--- Link Type ----------------------------->
<div class="form-group">
    <label class="control-label col-md-2" for="link2">Get this:</label>
    <div class="col-md-4">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if link2 == 'nc':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='nc' checked> NetCDF
        </label>
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='png'> Image
        </label>
    '''
elif link2 == 'png':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='nc'> NetCDF
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='png' checked> Image
        </label>
    '''
print '''
        </div>
    </div>
</div>
<!--- (link type)----------------------------->


    <div class="form-group">        
      <div class="col-md-offset-2 col-md-4">
        <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
      </div>
    </div>
  </form>

</div>
</div>

<div class="container">
'''


# Create list of image files available for the requested date
DATE = datetime.strptime(Date, "%Y-%m-%d")
PATH = '/ABI-L2-MCMIPC/%s/' % (DATE.strftime('%Y%m%d'))

print '<h4>Tap to view images from: <b>'+PATH+'</b></h4>'
print "<p>Number represents the scan's start minute for the requested hour"


rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'

ls = ' ls horelS3:GOES16%s | cut -c 11-' \
        % (PATH)

rclone_out = subprocess.check_output(rclone + ls, shell=True)
flist = rclone_out.split('\n')

# Remove empty elements. There is always one at the end.
flist.remove('')

# Order the files
flist.sort() 

# Only get Utah .png files
if domain == 'UTAH':
    flist = np.array([f for f in flist if 'UTAH.png' in f])
else:
    flist = np.array([f for f in flist if '.png' in f and 'UTAH.png' not in f])


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Need to do some special things for Utah domain or IR or water vapor images
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



scan_start = np.array([datetime.strptime(f.split('_')[3][:], 's%Y%j%H%M%S%f') for f in flist])

scan_start_hours = np.array([a.hour for a in scan_start])

# Text on the download button
button_display = scan_start

for i in range(24):
    print '''<div class="form-group">'''
    print '''<div class="col-md-12">'''
    print '''<div class="mybtn-group">'''
    print '''<p><button name="hour" type="button" class="mybtn hourbtn""><b>Hour %02d</b></button>''' % (i)
    # A list of images for the button displays
    buttons = scan_start[scan_start_hours==i]
    # A list of the file names for each button
    bfiles = flist[scan_start_hours==i]
    for j in range(len(bfiles)):
        if link2 == 'png':
            link_to_this = 'https://pando-rgw01.chpc.utah.edu/GOES16/ABI-L2-MCMIPC/%s/%s' % (DATE.strftime('%Y%m%d'), bfiles[j])
        elif link2 == 'nc':
            link_to_this = 'https://pando-rgw01.chpc.utah.edu/GOES16/ABI-L2-MCMIPC/%s/%s' % (DATE.strftime('%Y%m%d'), bfiles[j][:-3]+'nc')
        print '''<a href="'''+link_to_this+'''" target='_blank'><button name="fxx" type="button" class="mybtn unselected">%02d</button></a>''' % (buttons[j].minute)
    print "<hr style='margin-top:.3em;margin-bottom:.3em'></div></div></div>"

print '''</div>'''

# Page Bottom
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


<br><br>
<p align=center>Powered By:<br>
<center><a href="https://aws.amazon.com/public-datasets/goes/" class="btn btn-success"><i class="fa fa-amazon" aria-hidden="true"></i> Amazon S3</a></center>    
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
