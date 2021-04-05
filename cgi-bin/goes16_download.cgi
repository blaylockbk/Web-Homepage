#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
October 1, 2017

Interactive web interface for viewing GOES-16/17 files available on the Amazon
noaa-goes16 public bucket. Click button to download files.

Details of GOES-16/17 data
http://www.goes-r.gov/products/images/productFileSize8ColorPng8-1600px.png

"""

import sys
import numpy as np
import os
import subprocess
import cgi, cgitb
import time
from datetime import date, datetime, timedelta

from collections import OrderedDict

cgitb.enable()

form = cgi.FieldStorage()

today = date.today()
max_date = datetime.utcnow().strftime('%Y-%m-%d')

try:
    source = cgi.escape(form['source'].value)
except:
    source = 'aws'    # 'aws' for Amazon or 'occ' for Open Commons Consortium 
try:
    satellite = cgi.escape(form['satellite'].value)
except:
    satellite = 'noaa-goes16'
try:
    domain = cgi.escape(form['domain'].value)
except:
    domain = 'C'    # C for CONUS, F for Full Disk, M for Mesoscale
try:
    product = cgi.escape(form['product'].value)
except:
    product = 'ABI-L2-CMIP' # ABI-L1b-Rad or ABI-L2-CMIP or ABI-L2-MCMIP
try:
    hour = cgi.escape(form['hour'].value)
except:
    hour = '0'
try:
    Date = cgi.escape(form['date'].value)
except:
    Date = today.strftime('%Y-%m-%d')

if source == 'aws':
    sourceURL = 'https://%s.s3.amazonaws.com' % satellite
elif source == 'occ':
    sourceURL = 'https://osdc.rcc.uchicago.edu/%s' % satellite

print "Content-Type: text/html\n"

print'''<!DOCTYPE html>
<html>
<head>
<script src="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>GOES-16/17 on Amazon Download Page</title>
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
    <i class="fa fa-cloud-download-alt"></i> GOES-16/17 on Amazon Download Page
    </h1>
    <center>
    <div class='btn-group'>
    <a class='btn btn-primary active' href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi"><i class="fab fa-aws"></i> GOES on Amazon</a>
    <a class='btn btn-primary' href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_AWS_download.cgi?DATASET=noaa-goes16"><i class="fas fa-list"></i></a>
    </div>
    <div class='btn-group'>
    <a class='btn btn-primary' href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_pando.cgi"><i class="fa fa-database"></i> GOES on Pando</a>
    <a class='btn btn-primary' href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=GOES16"><i class="fas fa-list"></i></a>
    </div>
    <a class='btn btn-warning' target=_blank href="http://rammb-slider.cira.colostate.edu/"><i class="fas fa-external-link-alt"></i> CIRA SLIDER</a>
    <a class='btn btn-warning' target=_blank href="https://geosphere.ssec.wisc.edu/"><i class="fas fa-external-link-alt"></i> SSEC Geosphere</a>
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
            <p>This page makes it easy to explore the GOES dataset on Amazon Web Services (AWS) and download
            files with the click of a mouse.
            <ol style="padding-left:50px">
                <li>Select the desired domain, product, date, and hour for which you want to download.
                    <ul>
                        <li>The "source" option refers to where the data is downloaded from. 
                        AWS is Amazon's cloud.
                        OCC is the 
                        <a href="http://edc.occ-data.org/goes16/">Open Commons Consortium</a>
                        and has GOES files from the last 7-8 months. If you get an XML
                        error when downloading from the Amazon source, try switching to OCC.
                        Check the URL in bold below to confirm the source.</li>
                    </ul>
                <li>Click the submit button.
                <ul style="padding-left:25px">
                    <li> A blue box appears for every file that is available. 
                    <li> The L1b Radiances and L2 Cloud and Moisture Imagery have separate files for each of the 16 bands.
                    <li> All other L2 products have a single file for each observation time.
                    <li> <b>The number on the blue box represents the minute the scan started</b>.
                    <li> Full disk scans are available every 15 minutes,
                    CONUS scans are available every 5 minutes, 
                    and mesoscale scans are available every minute.
                    <li> Some L2 products are not available for all domains.
                </ul>
                <li> Click the desired file and the download will begin.
            </ol>
            <hr>
            <p>Also check out the <a class='btn btn-success' href='https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_AWS_download.cgi?DATASET=noaa-goes16'>
            Alternative Download Page</a>
            <p> For bulk and scripted downloads, consider using 
            <a href="https://rclone.org/">rclone</a>,
            <a href="https://aws.amazon.com/cli/">AWS CLI</a>,
            <a href="https://gist.github.com/blaylockbk/d60f4fce15a7f0475f975fc57da9104d#file-download_goes_aws-py"> Python's s3fs library</a>,
            or <a href="https://www.avl.class.noaa.gov/">NOAA CLASS</a>.
            </a>
            <hr>
            <p>Downloaded files are in NetCDF format. For example:
            <p><kbd>OR_ABI-L1b-RadM1-M3C01_G16_s20172511100550_e20172511101007_c20172511101048.nc</kbd>
            <ul style="padding-left:55px;">
                <li><kbd>OR</kbd> - data is operational and in real-time
                <li><kbd>ABI-L1b-RadM1-</kbd> - is the product, with the mesoscale 1 domain. C is for CONUS, F is for full disk, and M2 is for Mesoscale 2.
                <li><kbd>M3C01</kbd> - Mode is 3 and Channel is 01
                <li><kbd>G16</kbd> - GOES-16 (G17 for GOES-17)
                <li><kbd>s20172511100550</kbd> - scan start time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second
                <li><kbd>e20172511101007</kbd> - scan end time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second
                <li><kbd>c20172511101048</kbd> - scan file creation time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second
                <li><kbd>.nc</kbd> - This is a NetCDF file.
            </ul>
            <p>More details can be found on <a href="https://docs.opendata.aws/noaa-goes16/cics-readme.html">Amazon's page</a>.
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
        <p>Data from the Advanced Baseline Imager (ABI) is downloaded from
          <a href="https://aws.amazon.com/public-datasets/goes/">Amazon S3 <i class="fab fa-aws"></i></a>.
          Read this <a href="https://docs.opendata.aws/noaa-goes16/cics-readme.html#accessing-goes-data-on-aws">
          description about the data</a>.
        <hr>
        <p>The base download URL is <kbd>https://'''+satellite+'''.s3.amazonaws.com</kbd>
        <p>The file path is: <kbd>/product/year/day_of_year/hour/file_name</kbd>
        <hr>
        <p> Usefull Links:                
        <ul style="padding-left:50px">
            <li><a href="http://www.goes-r.gov/" target="blank">GOES-R Homepage</a>
            <li><a href="http://www.goes-r.gov/products/images/productFileSize8ColorPng8-1600px.png" target="blank">Channels Approx. File Sizes</a>            
            <li><a href="http://cimss.ssec.wisc.edu/goes/GOESR_QuickGuides.html" target="blank">ABI Bands Quick Information Guides</a>
            <li><a href="http://www.goes-r.gov/products/docs/PUG-L2+-vol5.pdf" target="blank">GOES-16 User Guide</a>
            <li><a href="https://www.star.nesdis.noaa.gov/goesr/docs/ATBD/Imagery.pdf" target="blank">GOES-R ABI Algorithm Theoretical Basis Document</a>
            <li><a href="https://www.weather.gov/media/crp/GOES_16_Guides_FINALBIS.pdf" target="blank">GOES Band Reference Guide</a>
            <li><a href="http://cimss.ssec.wisc.edu/goes/goesdata.html" target="blank">More GOES-16 Links</a>
            <li><a href="http://www.goes-r.gov/resources/docs.html" target="blank">All the GOES-R Docs</a>
        </ul>
        <hr>
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
        <p>Note: The resolution of the Multi-band files for all channels and other L2 products is 2 km.
        </div>
      </div>
    </div>

<div class="panel panel-default">
      <div class="panel-heading">
        <h4 class="panel-title">
          <a data-toggle="collapse" data-parent="#accordion" href="#collapse3">
          <big><b><i class="fa fa-info-circle" ></i> Other Ways to Download</b></big>
          </a>
        </h4>
      </div>
      <div id="collapse3" class="panel-collapse collapse">
        <div class="panel-body">
        <h3>rclone</h3>
            <a href="https://rclone.org/">rclone</a>
            <p>This page uses <a class='alert-link' href='https://rclone.org/'>rclone</a> to access public GOES-16 files from Amazon Web Services. 
            <a class='btn btn-primary' href='https://github.com/blaylockbk/pyBKB_v3/blob/master/rclone_howto.md'>Brian's rclone Tutorial</a>
        <hr>
        <h3>AWS CLI</h3>
            <a href="https://aws.amazon.com/cli/">AWS CLI</a>
        
        <hr>
        <h3>Python</h3>
            <a href="https://s3fs.readthedocs.io/en/latest/">s3fs</a>
            <p> You can view and download files from public AWS buckets with Python's <code>s3fs</code> library.</p>
            <script src="https://gist.github.com/blaylockbk/d60f4fce15a7f0475f975fc57da9104d.js"></script>
        
        <hr>    
        <h3> NOAA CLASS</h3>
            <a href="https://www.avl.class.noaa.gov/">NOAA CLASS</a>
        
        </div>
      </div>
    </div>

  </div> 
</div>

    <div class='alert alert-warning'>
        Derived (Level 2) products are now available.
    </div>   
    
  <hr> 
<div class="container">
  <form class="form-horizontal" method="GET" action="cgi-bin/goes16_download.cgi">

<!--- Source Type ----------------------------->
<div class="form-group">
    <label class="control-label col-md-2" for="source">Source:</label>
    <div class="col-md-4">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if source == 'aws':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="source" id="source" autocomplete="off" value='aws' checked> AWS
        </label>
        <label class="btn btn-default">
            <input type="radio" name="source" id="source" autocomplete="off" value='occ'> OCC
        </label>
    '''
elif source == 'occ':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="source" id="source" autocomplete="off" value='aws'> AWS
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="source" id="source" autocomplete="off" value='occ' checked> OCC
        </label>
    '''
print '''
        </div>
    </div>
</div>
<!--- (source type)----------------------------->

<!--- Satellite ----------------------------->
<div class="form-group">
    <label class="control-label col-md-2" for="satellite">Satellite:</label>
    <div class="col-md-4">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if satellite == 'noaa-goes16':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="satellite" id="satellite" autocomplete="off" value='noaa-goes16' checked> GOES-16/East
        </label>
        <label class="btn btn-default">
            <input type="radio" name="satellite" id="satellite" autocomplete="off" value='noaa-goes17'> GOES-17/West
        </label>
    '''
elif satellite == 'noaa-goes17':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="satellite" id="satellite" autocomplete="off" value='noaa-goes16'> GOES-16/East
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="satellite" id="satellite" autocomplete="off" value='noaa-goes17' checked> GOES-17/West
        </label>
    '''
print '''
        </div>
    </div>
</div>
<!--- (satellite)----------------------------->

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

pairs = OrderedDict()
pairs['ABI-L1b-Rad'] = 'ABI L1b Radiances'
pairs['ABI-L2-CMIP'] = 'ABI L2 Cloud and Moisture Imagery'
pairs['ABI-L2-MCMIP'] = 'ABI L2 Cloud and Moisture Imagery (Multi-Band Format)'
pairs['GLM-L2-LCFA'] = 'GLM L2 Lightning Detection'
pairs['ABI-L2-ACHA'] = 'ABI L2 Cloud Top Height'
pairs['ABI-L2-ACHT'] = 'ABI L2 Cloud Top Temperature'
pairs['ABI-L2-ACM'] = 'ABI L2 Clear Sky Mask'
pairs['ABI-L2-ACTP'] = 'ABI L2 Cloud Top Phase'
pairs['ABI-L2-ADP'] = 'ABI L2 Aerosol Detection'
pairs['ABI-L2-AOD'] = 'ABI L2 Aerosol Optical Depth'
pairs['ABI-L2-COD'] = 'ABI L2 Cloud Optical Depth'
pairs['ABI-L2-CPS'] = 'ABI L2 Cloud Particle Size'
pairs['ABI-L2-CTP'] = 'ABI L2 Cloud Top Pressure'
pairs['ABI-L2-DMW'] = 'ABI L2 Derived Motion Winds'
pairs['ABI-L2-DSI'] = 'ABI L2 Derived Stability Indices'
pairs['ABI-L2-DSR'] = 'ABI L2 Downward Shortwave Radiation'
pairs['ABI-L2-FDC'] = 'ABI L2 Fire (Hot Spot Characterization)'
pairs['ABI-L2-LST'] = 'ABI L2 Land Surface Temperature'
pairs['ABI-L2-LVMP'] = 'ABI L2 Legacy Vertical Moisture Profile'
pairs['ABI-L2-LVTP'] = 'ABI L2 Legacy Vertical Temperature Profile'
pairs['ABI-L2-RRQPE'] = 'ABI L2 Rainfall Rate (Quantitative Precipitation Estimate)'
pairs['ABI-L2-RSR'] = 'ABI L2 Reflected Shortwave Radiation TOA'
pairs['ABI-L2-SST'] = 'ABI L2 Seas Surface Temperature'
pairs['ABI-L2-TPW'] = 'ABI L2 Total Precipitable Water'
pairs['ABI-L2-VAA'] = 'ABI L2 Volcanic Ash: Detection and Hight'
pairs['SUVI-L1b-Fe093'] = 'Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe093'
pairs['SUVI-L1b-Fe131'] = 'Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe131'
pairs['SUVI-L1b-Fe171'] = 'Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe171'
pairs['SUVI-L1b-Fe195'] = 'Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe195'
pairs['SUVI-L1b-Fe284'] = 'Solar Ultraviolet Imager L1b Extreme Ultraviolet Fe284'
pairs['SUVI-L1b-He303'] = 'Solar Ultraviolet Imager L1b ExtremeUltraviolet He303'

display = pairs.values()
value = list(pairs)

#display = ['ABI L1b Radiances', 'ABI L2 Cloud and Moisture Imagery', 'ABI L2 Cloud and Moisture Imagery: Multi-Band Format', 'Geostationary Lightning Mapper']
#value = ['ABI-L1b-Rad', 'ABI-L2-CMIP', 'ABI-L2-MCMIP', 'GLM-L2-LCFA']

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
if product == 'GLM-L2-LCFA':
    PATH = '/%s/%s/%02d/' % (product, DATE.strftime('%Y/%j'), int(hour))
elif product[:3] == 'SUV':
    PATH = '/%s/%s/%02d/' % (product, DATE.strftime('%Y/%j'), int(hour))
else:    
    PATH = '/%s%s/%s/%02d/' % (product, domain[0], DATE.strftime('%Y/%j'), int(hour))

print '<h4>Click or tap to download from %s S3 bucket: <b>' % satellite, sourceURL+PATH+'</b></h4>'
print "<p>Number represents the scan's start minute for the requested hour"


#rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'
rclone = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando_Scripts/rclone-v1.39-linux-386/rclone --config /uufs/chpc.utah.edu/common/home/u0553130/.rclone.conf'

ls = ' ls AWS:%s%s | cut -c 11-' \
        % (satellite, PATH)

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

if product != 'ABI-L1b-Rad' and product != 'ABI-L2-CMIP':
#if product == 'ABI-L2-MCMIP' or product == 'GLM-L2-LCFA':
    # The multi-band format and GLM doesn't have files separated by band type
    scan_start = np.array([f.split('_')[3][:] for f in flist])
    scan_end = np.array([f.split('_')[4][:] for f in flist])
    scan_save = np.array([f.split('_')[5][:] for f in flist])
    
    # Display the download button start time MINUTE
    button_display = np.array(['%s' % (d[10:12]) for d in scan_start])
    print '''<div class="form-group">'''
    print '''<div class="col-md-12">'''
    print '''<div class="mybtn-group">'''
    #if product == 'ABI-L2-MCMIP':
    #    print '''<button name="hour" type="button" class="mybtn hourbtn"">Multi-band Format:</button>'''
    #elif product == 'GLM-L2-LCFA':
    #    print '''<button name="hour" type="button" class="mybtn hourbtn"">Geostationary Lightning Mapper:</button>'''
    #else:
    btn_text = pairs[product]
    print '''<button name="hour" type="button" class="mybtn hourbtn"">{}:</button>'''.format(btn_text)

    for i in range(len(flist)):
        download_this = '%s%s%s' % (sourceURL, PATH, flist[i])
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
            download_this = '%s%s%s' % (sourceURL, PATH, bfiles[i])
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
<center><a href="https://aws.amazon.com/public-datasets/goes/" class="btn btn-success"><i class="fab fa-aws"></i> Amazon S3</a>
        <a href="http://edc.occ-data.org/goes16/" class="btn btn-success"> Open Commons Consortium</a></center>    
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''

