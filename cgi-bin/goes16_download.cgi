#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
October 1, 2017

Interactive web interface for viewing GOES-16 files available on the Amazon
noaa-goes16 public bucket. Click button to download files.

Details of GOES-16 data
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

today = date.today()
max_date = date.today().strftime('%Y-%m-%d')

try:
    domain = form['domain'].value
except:
    domain = 'C'    # C for CONUS, F for Full Disk, M for Mesoscale
try:
    product = form['product'].value
except:
    product = 'ABI-L2-CMIP' # ABI-L1b-Rad or ABI-L2-CMIP or ABI-L2-MCMIP
try:
    hour = form['hour'].value
except:
    hour = '0'
try:
    Date = form['date'].value
except:
    Date = today.strftime('%Y-%m-%d')

print "Content-Type: text/html\n"

print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>GOES-16 on Amazon Download Page</title>
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
    <i class="fa fa-cloud-download-alt"></i> GOES-16 on Amazon Download Page
    </h1>
    <center>
    <div class='btn-group'>
    <a class='btn btn-primary active' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi"><i class="fab fa-aws"></i> GOES on Amazon</a>
    <a class='btn btn-primary' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_AWS_download.cgi?DATASET=noaa-goes16"><i class="fas fa-list"></i></a>
    </div>
    <div class='btn-group'>
    <a class='btn btn-primary' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_pando.cgi"><i class="fa fa-database"></i> GOES on Pando</a>
    <a class='btn btn-primary' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=GOES16"><i class="fas fa-list"></i></a>
    </div>
    <a class='btn btn-warning' href="http://rammb-slider.cira.colostate.edu/"><i class="fas fa-external-link-alt"></i> CIRA SLIDER</a>
    </center>
<br>

<div class="container">
  <div class="panel-group" id="accordion">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h4 class="panel-title">
          <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
          <big><b><i class="fa fa-info-circle" ></i> Download Instructions</b></big>
          </a>
        </h4>
      </div>
      <div id="collapse1" class="panel-collapse collapse">
        <div class="panel-body">
            <p> This page is tested in
            <i class="fab fa-edge"></i> and <i class="fab fa-chrome"></i> 
            (Why only these two? Because my advisor uses Chrome, and I use Edge.)
            <ol style="padding-left:15px">
            <li>Select the desired domain, product, date, and hour for which you want to download.
            <li>Click the submit button.
            <ul style="padding-left:20px">
                <li>Data is available for 16 different channels or bands. A blue box appears for every file that is available.
                The number on the box represents the minute the scan started. Full disk scans are available every 15 minutes,
                CONUS scans are available every 5 minutes, and mesoscale scans are available every minute.
            </ul>
            <li> Click the desired file and the download will begin.
            </ol>
            <p>Files are downloaded in NetCDF format.
            <p>An example file name:<br> <span style="font-family:monospace">OR_ABI-L1b-RadM1-M3C01_G16_s20172511100550_e20172511101007_c20172511101048.nc</span>
            <ul style="padding-left:35px;">
                <li>OR - data is operational and in real-time
                <li>ABI-L1b-RadM1 - is the product, with the mesoscale 1 domain. C is for CONUS, F is for full disk, and M2 is for Mesoscale 2.
                <li>M3C01 - Mode is 3 and Channel is 01
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
          <big><b><i class="fa fa-info-circle" ></i> Data Details</b></big>
          </a>
        </h4>
      </div>
      <div id="collapse2" class="panel-collapse collapse">
        <div class="panel-body">
        <p>Data from the Advanced Baseline Imager (ABI) is downloaded from  <a href="https://aws.amazon.com/public-datasets/goes/" class="btn btn-success">
            <i class="fab fa-aws"></i> Amazon S3</a>
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
        
        <center><small>
        <div class='table-responsive'>
        <table class='table sortable' style="max-width:650px;text-align:center">
        <tr>
            <th>Band Number</th>
            <th>Resolution (km)</th>
            <th>Wavelength</th>
            <th>Spectrum</th>
            <th>Name</th>
        </tr>
        <tr><td>01</td> <td>1</td> <td>0.47 &microm</td><td>Visible</td><td>Blue Band</td><td></tr>
        <tr><td>02</td> <td>0.5</td> <td>0.64 &microm</td><td> Visible </td><td>Red Band</td><td></tr>
        <tr><td>03</td> <td>1</td> <td>0.86 &microm</td><td> Near-IR </td><td>Veggie Band</td><td></tr>
        <tr><td>04</td> <td>2</td> <td>1.37 &microm</td><td> Near-IR </td><td>Cirrus Band</td><td></tr>
        <tr><td>05</td> <td>1</td> <td>1.60 &microm</td><td> Near-IR </td><td>Snow/Ice Band</td><td></tr>
        <tr><td>06</td> <td>2</td> <td>2.24 &microm</td><td> Near-IR </td><td>Cloud Prticle Size Band</td><td></tr>
        <tr><td>07</td> <td>2</td> <td>3.90 &microm</td><td> IR </td><td>Shortwave Window Band</td><td></tr>
        <tr><td>08</td> <td>2</td> <td>6.20 &microm</td><td> IR </td><td>Upper-Troposphere WV Band</td><td></tr>
        <tr><td>09</td> <td>2</td> <td>6.90 &microm</td><td> IR </td><td>Mid-Level Troposphere WV Band</td><td></tr>
        <tr><td>10</td> <td>2</td> <td>7.30 &microm</td><td> IR </td><td>Low-Level Troposphere WV Band</td><td></tr>
        <tr><td>11</td> <td>2</td> <td>8.40 &microm</td><td> IR </td><td>Cloud-Top Phase Band</td><td></tr>
        <tr><td>12</td> <td>2</td> <td>9.60 &microm</td><td> IR </td><td>Ozone Band</td><td></tr>
        <tr><td>13</td> <td>2</td> <td>10.3 &microm</td><td> IR </td><td>Clean IR Longwave Band</td><td></tr>
        <tr><td>14</td> <td>2</td> <td>11.2 &microm</td><td> IR </td><td>IR Longwave Band</td><td></tr>
        <tr><td>15</td> <td>2</td> <td>12.3 &microm</td><td> IR </td><td>Dirty IR Longwave Band</td><td></tr>
        <tr><td>16</td> <td>2</td> <td>13.3 &microm</td><td> IR </td><td>CO2 Longwave IR Band</td><td></tr>
        </table>
        </div>
        </center></small>
        <p>Note: The resolution of the Multi-band files for all channels is 2 km.
           This file is easiest to work with if you don't <i>need</i> the full
           resolution of the 1 km channels for your images.
        
        </div>
      </div>
    </div>
  </div> 
</div>
   
    <div class='alert alert-warning'>
    GOES-16 will not be available between November 30 and December 20, 2017
    when it will be moved to it's operational location at 75.2 degrees west.
    <a href="http://www.goes-r.gov/users/transitiontToOperations.html">More Info</a>
    </div>
    
  <hr> 
<div class="container">
  <form class="form-horizontal" method="GET" action="cgi-bin/goes16_download.cgi">

<!---domain Type -----------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="model">Domain:</label>
      <div class="col-md-4">      
         <select class="form-control" id="model" name="domain">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['CONUS', 'Full Disk', 'Mesoscale 1', 'Mesoscale 2']
value = ['C', 'F', 'M1', 'M2']

for i in range(0,len(value)):
   if domain == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>

      </div>
      
    </div>
<!---(domain_type) ----------------------->

<!---Product type-------------------------->
    <div class="form-group">
      <label class="control-label col-md-2" for="product">Product:</label>
      <div class="col-md-4">          
        <select class="form-control" id="product" name="product">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['ABI L1b Radiances', 'ABI L2 Cloud and Moisture Imagery', 'ABI L2 Cloud and Moisture Imagery: Multi-Band Format']
value = ['ABI-L1b-Rad', 'ABI-L2-CMIP', 'ABI-L2-MCMIP']

for i in range(0,len(value)):
   if product == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </div>
    </div>
<!---(Product_type) ----------------------->

<!--- Date ------------------------------>
    <div class="form-group">
      <label class="control-label col-md-2" for="date">Date:</label>
      <div class="col-md-4">          
        <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2017-07-10" max="'''+max_date+'''">
      </div>
    </div>
<!--- (date)----------------------------->

<!---hour type-------------------------->
    <div class="form-group">
      <label class="control-label col-md-2" for="hour">Hour (UTC):</label>
      <div class="col-md-4">          
        <select class="form-control" id="hour" name="hour">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = range(0, 24)
value = range(0, 24)

for i in range(0,len(value)):
   if hour == str(value[i]):
      print'''<option selected="selected" value="'''+str(value[i])+'''">'''+str(display[i])+'''</option>'''
   else:
      print'''<option value="'''+str(value[i])+'''">'''+str(display[i])+'''</option>'''
print''' </select>
      </div>
    </div>
<!---(hour_type) ----------------------->


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




# Names of the 16 bands
band_num = range(1,17)
band = ['0.47 &microm: Visible "Blue Band"',\
        '0.64 &microm: Visible "Red Band"',\
        '0.86 &microm: Near-IR "Veggie Band"',\
        '1.37 &microm: Near-IR "Cirrus Band"',\
        '1.60 &microm: Near-IR "Snow/Ice Band"',\
        '2.24 &microm: Near-IR "Cloud Prticle Size Band"',\
        '3.90 &microm: IR "Shortwave Window Band"',\
        '6.20 &microm: IR "Upper-Troposphere WV Band"',\
        '6.90 &microm: IR "Mid-Level Troposphere WV Band"',\
        '7.30 &microm: IR "Low-Level Troposphere WV Band"',\
        '8.40 &microm: IR "Cloud-Top Phase Band"',\
        '9.60 &microm: IR "Ozone Band"',\
        '10.3 &microm: IR "Clean IR Longwave Band"',\
        '11.2 &microm: IR "IR Longwave Band"',\
        '12.3 &microm: IR "Dirty IR Longwave Band"',\
        '13.3 &microm: IR "CO2 Longwave IR Band"']

# Create list of files available for the requested hour
DATE = datetime.strptime(Date, "%Y-%m-%d")
PATH = '/%s%s/%s/%02d/' % (product, domain[0], DATE.strftime('%Y/%j'), int(hour))

print '<h4>Tap to download from noaa-goes16 S3 bucket: <b>'+PATH+'</b></h4>'
print "<p>Number represents the scan's start minute for the requested hour"


rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'

ls = ' ls goes16:noaa-goes16%s | cut -c 11-' \
        % (PATH)

rclone_out = subprocess.check_output(rclone + ls, shell=True)
flist = rclone_out.split('\n')

# Remove empty elements. There is always one at the end.
flist.remove('')

# Order the files
flist.sort() 

# if we are requesting a mesoscale file, remove the ones we didn't request
if domain == 'M1':
    flist = [f for f in flist if product+'M1' in f.split('_')[1]]
if domain == 'M2':
    flist = [f for f in flist if product+'M2' in f.split('_')[1]]

# Convert to numpy array
flist = np.array(flist)

if product == 'ABI-L2-MCMIP':
    # The multi-band format doesn't have files separated by band type
    scan_end = np.array([f.split('_')[4][:] for f in flist])
    button_display = np.array(['%s' % (d[10:12]) for d in scan_end])
    print '''<div class="form-group">'''
    print '''<div class="col-md-12">'''
    print '''<div class="mybtn-group">'''
    print '''<button name="hour" type="button" class="mybtn hourbtn"">Multi-band Format:</button>'''
    for i in range(len(flist)):
        download_this = 'https://noaa-goes16.s3.amazonaws.com%s%s' % (PATH, flist[i])
        print '''<a href="'''+download_this+'''" target='_blank'><button name="fxx" type="button" class="mybtn unselected">%s</button></a>''' % (button_display[i])
    print "<hr style='margin-top:.3em;margin-bottom:.3em'></div></div></div>"  
else:
    channels = np.array([int(f.split('_')[1][-2:]) for f in flist])
    scan_start = np.array([f.split('_')[3][:] for f in flist])
    scan_end = np.array([f.split('_')[4][:] for f in flist])
    scan_save = np.array([f.split('_')[5][:] for f in flist])

    # Display the download button by the scan's start time MINUTE (don't include second or fractional second)
    button_display = np.array(['%s' % (d[10:12]) for d in scan_start])

    for i in range(len(band)):
        print '''<div class="form-group">'''
        print '''<div class="col-md-12">'''
        print '''<div class="mybtn-group">'''
        print '''<p><button name="hour" type="button" class="mybtn hourbtn""><b>Band %02d</b></button>''' % (band_num[i])
        # A list of names for the button displays
        blist = button_display[channels==band_num[i]]
        # A list of the file names for each button
        bfiles = flist[channels==band_num[i]]
        for i in range(len(blist)):
            download_this = 'https://noaa-goes16.s3.amazonaws.com%s%s' % (PATH, bfiles[i])
            print '''<a href="'''+download_this+'''" target='_blank'><button name="fxx" type="button" class="mybtn unselected">%s</button></a>''' % (blist[i])
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
<center><a href="https://aws.amazon.com/public-datasets/goes/" class="btn btn-success"><i class="fab fa-aws"></i> Amazon S3</a></center>    
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''

