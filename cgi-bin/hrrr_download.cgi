#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 6, 2017

Webpage to Display HRRR files on Pando. 
Click button to download GRIB2 file, .idx file, or view a sample image.
"""

import sys
import os
import subprocess
import cgi, cgitb
from datetime import date, datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

try:
    model = cgi.escape(form['model'].value)
except:
    model = 'hrrr'
try:
    field = cgi.escape(form['field'].value)
except:
    field = 'sfc'
try:
    Date = cgi.escape(form['date'].value)
except:
    Date = datetime.now().strftime('%Y-%m-%d')
try:
    link2 = cgi.escape(form['link2'].value)
except:
    link2 = 'grib2'


###############################################################################
# Rados Gateway
# Set to 1 or 2. This is an option if the certificate for the gateway URL 
# expires as it happened on September 8th, 2019.
# Rados Gateway 1 is the default and downloads from https://pando-rgw01.chpc.utah.edu
# Rados Gateway 2 is the alternative and downloads from https://pando-rgw02.chpc.utah.edu

rados_gateway = 1

###############################################################################

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRR Download Page</title>
<style>
      .mybtn {
          border: 2px solid #23415c;
          color: white;
          padding: 5px 5px;
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
'''

# Title, menu buttons, and page instructions
print '''
<div id="content" class="container">
    <h1 align="center">
    <i class="fa fa-cloud-download-alt" ></i> HRRR Download Page
    <a class='btn btn-default' href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=hrrr" title="Alternative HRRR Download Page"><i class="fas fa-list"></i></a>
    </h1>

    <script src='./js/pando_status.js'></script>
    <script src='./js/HRRR_status.js'></script>

	<br>
	<div id="content" class="container">
	<div class="alert alert-warning">
		<p style='font-size:15px'>Thank you for visiting this resource.  With the expanded availability of archived HRRR grib2-formatted data now courtesy of <a href="https://registry.opendata.aws/noaa-hrrr-pds/" target="_blank">NOAA and the Registry of Open Data on AWS</a>, this archive hosted at the University of Utah is now being reduced.  Users interested in the grib2 format are encouraged to switch to using the AWS archive, or a similar archive operated within the <a href="https://console.cloud.google.com/marketplace/product/noaa-public/hrrr?project=python-232920&pli=1" target="_blank">Google Cloud</a>.<br><br>For users interested in subsets of HRRR data, our research group is now supporting a parallel archive in <a href="https://mesowest.utah.edu/html/hrrr/" target="_blank">Zarr format</a>.  This new Zarr archive is also hosted by the <a href="https://hrrrzarr.s3.amazonaws.com/index.html" target="_blank">Registry of Open Data on AWS</a>.
	</div>
	</div>
	<br>

	<div class="row" id="content">
		<div class="col-md-3">
			<a href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html"
				class="btn btn-success btn-block active">
				<i class="fa fa-info-circle"></i> HRRR FAQ</a>
		</div>
		<div class="col-md-3">
			<a href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_practices.html"
				class="btn btn-warning btn-block">
				<i class="far fa-handshake"></i> Best Practices</a>
		</div>
		<div class="col-md-3">
			<a href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi"
				class="btn btn-primary btn-block">
				<i class="fa fa-cloud-download-alt"></i>Pando Web Download Page</a>
		</div>
		<div class=" col-md-3">
			<a href="https://registry.opendata.aws/noaa-hrrr-pds/"
				class="btn btn-danger btn-block" target="_blank">
				<i class="fa fa-cloud-download-alt"></i> AWS HRRR Archive</a>
		</div>
	</div>

    <br>
    <div style="width:100%" class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="headingTwo">
        <h4 class="panel-title">
            <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
            <big><b><i class="fa fa-info-circle"></i> Web Download Instructions</b></big>
            </a>
        </h4>
        </div>
                
        <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
            <div class="panel-body">
                <p>This HRRR download interface displays HRRR files available in the Pando archvie.
                <p>The blue buttons can perform three different actions:
                <ol style="padding-left:60px">
                    <li>Download the GRIB2 file directly to your computer.
                    <li>View the metadata (.idx) for the file.
                    <li>Produce a sample image of simulated reflectivity and 500 hPa contours for the file.
                </ol>
                <p>Select the model type, variable field, and date of interest. Toggle the
                buttons for what you want to do.
                <p>Then click <b><i>Submit</i></b>. <b>You must click 'submit' after
                you make a change</b>.
                <p>The grid of hours and forecasts displayed represent the HRRR model
                run hours and the subsequent forecasts. 
                If the file is available, the button will be highlighted 
                dark blue. Click the button to retrieve the file.
                <p>Files are named similar to HRRR files named on the NOMADS site. For example,<br>
                <b><span style="color:red">hrrr</span>.<span style="color:blue">t05z</span>.wrf<span style="color:green">sfc</span><span style="color:darkorange">f12</span>.grib2</b><br>
                <b><span style="color:red">[model type]</span>.<span style="color:blue">t[run hour]z</span>.wrf<span style="color:green">[variable field]</span><span style="color:darkorange">f[forecast hour]</span>.grib2
                </b>
                    <div class="alert alert-info">
                    <p>Note: While each file contains additional date information, 
                        the <i>file name</i> only contains information about the
                        run and forecast hour. Beware of overwriting files if you
                        download from multiple days into the same directory.
                    </div>
                <p>Click "Scripting Tips" above for some help scripting the download process.
                <p>Read the HRRR FAQ for a description of what file and dates are available.
                <p> Check out the <a href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_custom.html">Custom HRRR Map</a> generator.
            </div>            
            <div class="panel-footer">
                <p> This page is tested in
                <i class="fab fa-edge" ></i> and <i class="fab fa-chrome" ></i>. Why only these two? Because my advisor uses Chrome, and I use Edge.
            </div>
        </div>
    </div>
    </div>
</div>
'''


# Form inputs
print '''
<div class="container">

    <form class="form-horizontal" method="GET" action="cgi-bin/hrrr_download.cgi">

<!---Model Type -----------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="model">Model Type:</label>
      <div class="col-md-4">      
         <select class="form-control" id="model" name="model">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['HRRR (operational)', 'HRRR-X (experimental)', 'HRRR Alaska']
value = ['hrrr', 'hrrrX','hrrrak']
for i in range(0,len(value)):
   if model == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </div> 
    </div>
<!---(model_type) ----------------------->

<!---Field type-------------------------->
    <div class="form-group">
      <label class="control-label col-md-2" for="field">Variable Fields:</label>
      <div class="col-md-4">          
        <select class="form-control" id="field" name="field">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['SFC (Surface, 2D fields)', 'PRS (Pressure, 3D fields)']
value = ['sfc', 'prs']
for i in range(0,len(value)):
   if field == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </div>
    </div>
<!---(field_type) ----------------------->

<!--- Date ------------------------------>
    <div class="form-group">
      <label class="control-label col-md-2" for="date">Date:</label>
      <div class="col-md-4">          
        <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2018-07-13" max="'''+datetime.now().strftime('%Y-%m-%d')+'''">
      </div>
    </div>
<!--- (date)----------------------------->'''
    
print'''<!--- Link Type ----------------------------->'''
# Order of buttons is [grib2, metadata, sample]
if link2 == 'grib2':
    active = ['active', '', '']
    radio = ['checked', '', '']
elif link2 == 'metadata':
    active = ['', 'active', '']
    radio = ['', 'checked', '']
elif link2 == 'sample':
    active = ['', '', 'active']
    radio = ['', '', 'checked']

print '''
        <div class="form-group">
            <label class="control-label col-md-2" for="link2">Get this:</label>
            <div class="col-md-4">
                <div class="btn-group btn-group-justified" data-toggle="buttons">
                    <label class="btn btn-default %s">
                        <input type="radio" name="link2" id="link2" autocomplete="off" value='grib2' %s> GRIB2
                    </label>
                    <label class="btn btn-default %s">
                        <input type="radio" name="link2" id="link2" autocomplete="off" value='metadata' %s> Metadata
                    </label>
                    <label class="btn btn-default %s">
                        <input type="radio" name="link2" id="link2" autocomplete="off" value='sample' %s> Sample
                    </label>
                </div>
            </div>
        </div>
<!--- (link type)----------------------------->
''' % (active[0], radio[0], active[1], radio[1], active[2], radio[2])


print '''
<!--- Submit Button ----------------------------->
        <div class="form-group">        
        <div class="col-md-offset-2 col-md-4">
            <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
        </div>
        </div>
<!--- (submit button) --------------------------->
    
    </form>
</div>
'''

# Create list of files available on Pando for the requested date/model/field
DATE = datetime.strptime(Date, "%Y-%m-%d")
rclone = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando_Scripts/rclone-v1.39-linux-386/rclone --config /uufs/chpc.utah.edu/common/home/u0553130/.rclone.conf'


if rados_gateway == 1:
    ls = ' ls horelS3:%s/%s/%04d%02d%02d | cut -c 11-' % (model, field, DATE.year, DATE.month, DATE.day)
elif rados_gateway == 2:
    ls = ' ls horelS3_rgw02:%s/%s/%04d%02d%02d | cut -c 11-' % (model, field, DATE.year, DATE.month, DATE.day)


rclone_out = subprocess.check_output(rclone + ls, shell=True)
flist = rclone_out.split('\n')


# Model version dates
if model == 'hrrr':
    if DATE >= datetime(2020,12,2):
        version = 'HRRRv4'
    elif DATE >= datetime(2018,7,12):
        version = 'HRRRv3'
    elif DATE >= datetime(2016,8,23):
        version = 'HRRRv2'
    else:
        version = 'HRRRv1'
if model == 'hrrrak':
    if DATE >= datetime(2018,7,12):
        version = 'HRRR-AK'
    else:
        version = 'HRRR-AK (experimental)'
if model == 'hrrrX':
    version = 'HRRR-X'

print '''<div class="container" style='width:100%;max-width:1400px'>'''
print '''<h3>Tap to download %s <b>%s</b> from %s:</h3>''' % (version, link2, Date)


# Make a button for each file that should be available
# Define fxx buttons needed for each hour.
#   HRRR    : runs every hour, 36 hr forecasts every 6 hours, 18 forecasts all others
#                  every hour, 48 hr after May 26th 2020 (every 6 hours)
#   HRRR-AK : runs every 3 hours, 36 hr forecasts every 6 hours, 18 forecasts all others
#   HRRR-X  : runs every hour, 32 hr forecasts every hour

# Define forecast length for each hour of the day.
# (Each key is an hour (UTC). The key item is the range of forecasts hours.)
hour_fxx_buttons = {}

if model == 'hrrr':
    for HOUR in range(24):
        # After the HRRRv4 update, forecasts go out to 48 hours every 6 hours.
        if HOUR in range(0,24,6) and DATE >= datetime(2020, 7, 1):
            hour_fxx_buttons[HOUR] = range(49)
        # After the HRRRv3 update, forecasts go out to 36 hours every 6 hours.
        elif HOUR in range(0,24,6) and DATE >= datetime(2018, 7, 12):
            hour_fxx_buttons[HOUR] = range(37)
        else:
            hour_fxx_buttons[HOUR] = range(19)
elif model == 'hrrrX':
    for HOUR in range(24):
        hour_fxx_buttons[HOUR] = range(33)
elif model == 'hrrrak':
    for HOUR in range(0,24,3):
        # After the HRRRv4 update, forecasts go out to 48 hours every 6 hours.
        ## When the upgrade takes place, change this date...for now, set to July 1
        if HOUR in range(0,24,6) and DATE >= datetime(2020, 7, 1):
            hour_fxx_buttons[HOUR] = range(49)
        # After the HRRRv3 update, forecasts go out to 36 hours every 6 hours.
        elif HOUR in range(0,24,6) and DATE >= datetime(2018, 7, 12):
            hour_fxx_buttons[HOUR] = range(37)
        # HRRRv1 and HRRRv2 only go out to F00-F18 for all hours.
        else:
            hour_fxx_buttons[HOUR] = range(19)

# Make buttons
for hr, fxxs in hour_fxx_buttons.items():
    print '''<div class="form-group">'''
    print '''<div class="col-md-12">'''
    print '''<div class="mybtn-group">'''
    print '''<button name="hour" type="button" class="mybtn hourbtn">Hour %02d</button>''' % (hr)
    for f in fxxs:
        look_for_this_file = '%s.t%02dz.wrf%sf%02d.grib2' % (model, hr, field, f)
        if rados_gateway == 1:
            baseURL = 'https://pando-rgw01.chpc.utah.edu/'
        elif rados_gateway == 2:
            baseURL = 'https://pando-rgw02.chpc.utah.edu/'
        pathURL = '%s/%s/%s/' % (model, field, DATE.strftime('%Y%m%d'))
        fileURL = look_for_this_file
        if look_for_this_file in flist:
            if link2 == 'grib2':
                download_this = baseURL+pathURL+fileURL
            elif link2 == 'metadata':
                download_this = baseURL+pathURL+fileURL+'.idx'
            elif link2 == 'sample':
                RUN = datetime(DATE.year, DATE.month, DATE.day, hr)
                VALID = RUN+timedelta(hours=f)
                download_this = 'https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?model=%s&valid=%s&fxx=%s&location=&plotcode=dBZ_entire_Fill,HGT_500-mb_Contour&dsize=full&background=arcgis' % (model, VALID.strftime('%Y-%m-%d_%H00'), f)
            print '''<a href="'''+download_this+'''" target='_blank'><button name="fxx" type="button" class="mybtn unselected">F%02d</button></a>''' % (f)
        else:
            print '''<button name="fxx" type="button" class="mybtn disabled">F%02d</button>''' % (f)
    print "<hr style='margin-top:.3em;margin-bottom:.3em'></div></div></div>"
print '''</div>'''


# Page Bottom
# Toggle button color if button has been clicked
print '''
<script>
// Toggle button color if button has been clicked
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

# Credits and Citation info. Site close.
print '''
<div class='container'>
    <script src='./js/pando_citation.js'></script>
</div>

<div class='row'>
    <div class='col-md-3  col-md-offset-3'>
        <script src='./js/climate_acknowledgement.js'></script>
    </div>
    <div class='col-md-3'>
        <script src='./js/powered_by_mesowest.js'></script>
    </div>
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
