#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 6, 2017

Webpage to Download HRRR file from Pando archive. Also display .idx file and sample image.
"""

import sys
import os
import subprocess
import cgi, cgitb
import time
from datetime import date, datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

yesterday = date.today()
max_date = date.today().strftime('%Y-%m-%d')

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
    Date = yesterday.strftime('%Y-%m-%d')
try:
    link2 = cgi.escape(form['link2'].value)
except:
    link2 = 'grib2'

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRR Download Page</title>
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

print '''
<div id="content" class="container">
    <h1 align="center">
    <i class="fa fa-cloud-download-alt" ></i> HRRR Download Page
    <a class='btn btn-default' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=hrrr" title="Alternative HRRR Download Page"><i class="fas fa-list"></i></a>
    </h1>

<script src='./js/pando_status.js'></script>
<script src='./js/HRRR_status.js'></script>

<div class="alert alert-warning">
    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
    <small><p>If you have not already, please 
              <a class='alert-link' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_download_register.html">register</a>
              as a user before downloading data. Citation details can be found at the bottom of this page.
    </small>
</div> 


<div class="row">
      <div class=" col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_download_register.html" class="btn btn-danger btn-block">
            <i class="fa fa-user-plus" ></i> Have you Registered?</a>        
      </div>
      <div class="col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_practices.html" class="btn btn-warning btn-block">
            <i class="far fa-handshake" ></i> Best Practices</a>
      </div>
      <div class="col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" class="btn btn-success btn-block">
            <i class="fa fa-info-circle" ></i> HRRR FAQ</a>
      </div>
      <div class="col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_script_tips.html" class="btn btn-primary btn-block">
            <i class="fa fa-code" ></i> Scripting Tips</a>
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
        <p>The interactive HRRR web download interface displays HRRR files available in the archvie and provides a button to download those files.
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
        fun hours and the subsequent forecasts. 
        If the file is available, the button will be highlighted 
        dark blue. Click the button to retrieve the file.
        <p>Files are named similar to HRRR files named on the NOMADS site. For example,<br>
        <b><span style="color:red">hrrr</span>.<span style="color:blue">t05z</span>.wrf<span style="color:green">sfc</span><span style="color:darkorange">f12</span>.grib2</b><br>
        <b><span style="color:red">[model type]</span>.<span style="color:blue">t[run hour]z</span>.wrf<span style="color:green">[variable field]</span><span style="color:darkorange">f[forecast hour]</span>.grib2
        </b>
        <p>While each file contains additional date information, 
           the <i>file name</i> only contains information about the
           run and forecast hour. Beware of overwriting files if you
           download from multiple days into the same directory.
        <p>Click "Scripting Tips" above for some help scripting the download process.
        <p>Read the HRRR FAQ for a description of what file and dates are available.
      </div>
      <hr>
        <p> Also, check out the <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_custom.html">Custom HRRR Map</a> generator.
      <div class="panel-footer">
        <p> This page is tested in
        <i class="fab fa-edge" ></i> and <i class="fab fa-chrome" ></i>. Why only these two? Because my advisor uses Chrome, and I use Edge.
      </div>
    </div>
  </div>


</div>
    
  <hr> 
<div class="container">

  <form class="form-horizontal" method="GET" action="cgi-bin/hrrr_download.cgi">

<!---Model Type -----------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="model">Model Type:</label>
      <div class="col-md-4">      
         <select class="form-control" id="model" name="model">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['HRRR (operational)', 'HRRR-X (experimental)', 'HRRR Alaska (operational after 12 July 2018)']
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
display = ['Surface (sfc, 2D fields)', 'Pressure (prs, 3D fields)']
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
        <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2016-07-15" max="'''+max_date+'''">
      </div>
    </div>
<!--- (date)----------------------------->
    
<!--- Link Type ----------------------------->
<div class="form-group">
    <label class="control-label col-md-2" for="link2">Get this:</label>
    <div class="col-md-4">
        <div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if link2 == 'grib2':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='grib2' checked> GRIB2
        </label>
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='metadata'> Metadata
        </label>
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='sample'> Sample
        </label>
    '''
elif link2 == 'metadata':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='grib2'> GRIB2
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='metadata' checked> Metadata
        </label>
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='sample'> Sample
        </label>
    '''
elif link2 == 'sample':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='grib2'> GRIB2
        </label>
        <label class="btn btn-default">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='metadata'> Metadata
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="link2" id="link2" autocomplete="off" value='sample' checked> Sample
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
<h3>Tap to download <b>'''+link2+'''</b> from '''+Date+''':</h3>
'''



# Create list of files available
DATE = datetime.strptime(Date, "%Y-%m-%d")
#rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'
rclone = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando_Scripts/rclone-v1.39-linux-386/rclone --config /uufs/chpc.utah.edu/common/home/u0553130/.rclone.conf'
if field not in ['prs', 'sfc', 'nat']:
    ls = ' ls horelS3:%s/%s/%04d%02d%02d | cut -c 11-' \
        % (model, 'nat', DATE.year, DATE.month, DATE.day)
else:
    ls = ' ls horelS3:%s/%s/%04d%02d%02d | cut -c 11-' \
        % (model, field, DATE.year, DATE.month, DATE.day)
rclone_out = subprocess.check_output(rclone + ls, shell=True)
flist = rclone_out.split('\n')


if model == 'hrrr':
    file_model = 'hrrr'
    model_hours = range(0, 24)
    f_hours = range(0, 19)
elif model == 'hrrrX':
    file_model = 'hrrrX'
    model_hours = range(0, 24)
    f_hours = range(0, 19)
elif model == 'hrrrak':
    file_model = 'hrrrak'
    model_hours = range(0, 24, 3)
    f_hours = range(0, 37)

for h in model_hours:
    print '''<div class="form-group">'''
    print '''<div class="col-md-12">'''
    print '''<div class="mybtn-group">'''
    print '''<button name="hour" type="button" class="mybtn hourbtn">Hour %02d</button>''' % (h)
    for f in f_hours:
        if field not in ['prs', 'sfc', 'nat']:
            # Then the request is a for a HRRR native grid file.
            look_for_this_file = '%s.t%02dz.wrfnatf%02d.grib2.%s' % (file_model, h, f, field)
            baseURL = 'https://pando-rgw01.chpc.utah.edu/'
            pathURL = '%s/%s/%s/' % (model, 'nat', DATE.strftime('%Y%m%d'))
            fileURL = look_for_this_file
        else:
            look_for_this_file = '%s.t%02dz.wrf%sf%02d.grib2' % (file_model, h, field, f)
            baseURL = 'https://pando-rgw01.chpc.utah.edu/'
            pathURL = '%s/%s/%s/' % (model, field, DATE.strftime('%Y%m%d'))
            fileURL = look_for_this_file
        if look_for_this_file in flist:
            if link2 == 'grib2':
                download_this = baseURL+pathURL+fileURL
            elif link2 == 'metadata':
                download_this = baseURL+pathURL+fileURL+'.idx'
            elif link2 == 'sample':
                RUN = datetime(DATE.year, DATE.month, DATE.day, h)
                VALID = RUN+timedelta(hours=f)
                download_this = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?model=%s&valid=%s&fxx=%s&location=&plotcode=dBZ_entire_Fill,HGT_500-mb_Contour&dsize=full&background=arcgis' % (file_model, VALID.strftime('%Y-%m-%d_%H00'), f)
            print '''<a href="'''+download_this+'''" target='_blank'><button name="fxx" type="button" class="mybtn unselected">f%02d</button></a>''' % (f)
        else:
            print '''<button name="fxx" type="button" class="mybtn disabled">f%02d</button>''' % (f)
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
'''



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
