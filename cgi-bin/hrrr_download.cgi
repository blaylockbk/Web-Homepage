#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
March 6, 2017
"""

import sys
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
    model = form['model'].value
except:
    model = 'oper'
try:
    field = form['field'].value
except:
    field = 'sfc'
try:
    Date = form['date'].value
except:
    Date = yesterday.strftime('%Y-%m-%d')
try:
    link2 = form['link2'].value
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

print'''
<div id="content" class="container">
    <h1 align="center">
    <i class="fa fa-cloud-download" aria-hidden="true"></i> HRRR Download Page
    </h1>

<div class="alert alert-warning">
    <small><p>Reminder: Please register as a user before downloading data and 
           reference this <a href="https://doi.org/10.1016/j.cageo.2017.08.005" target="_blank">
           <b>paper</b> <i class="fa fa-book" aria-hidden="true"></i></a>
    </small>
</div> 


<div class="row">
      <div class=" col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_download_register.html" class="btn btn-danger btn-block">
            <i class="fa fa-user-plus" aria-hidden="true"></i> Have you Registered?</a>        
      </div>
      <div class="col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_practices.html" class="btn btn-warning btn-block">
            <i class="fa fa-handshake-o" aria-hidden="true"></i> Best Practices</a>
      </div>
      <div class="col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" class="btn btn-success btn-block">
            <i class="fa fa-info-circle" aria-hidden="true"></i> HRRR FAQ</a>
      </div>
      <div class="col-md-3">
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_script_tips.html" class="btn btn-primary btn-block">
            <i class="fa fa-code" aria-hidden="true"></i> Scripting Tips</a>
      </div>
</div>

<br>
<div style="width:100%" class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="headingTwo">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
          <big><b><i class="fa fa-info-circle" aria-hidden="true" ></i> Web Download Instructions</b></big>
        </a>
      </h4>
    </div>
            

    <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
      <div class="panel-body">
        <p> This page is tested in
        <i class="fa fa-edge" aria-hidden="true"></i> and <i class="fa fa-chrome" aria-hidden="true"></i> 
        (Why only these two? Because my advisor uses Chrome, and I use Edge.)
        <p>You may do three things here: 
        <ol style="padding-left:60px">
            <li>Download grib2 files
            <li>View metadata files
            <li>View a sample image of simulated reflectivity for each file (takes some time to generate).
        </ol>
        <p>Select the model type, variable field, and date of interest. Toggle the
        buttons for what you want to do.
        <p>Then click <b><i>Submit</i></b>. <b>You must click 'submit' after
        you make a change</b>.
        <p>After clicking the submit button, a grid of hours and forecasts is 
        displayed. If the file is available, the button will be highlighted 
        dark blue. Click the button to retrive what you requested.
        <p>Files are named similar to HRRR files named on the NOMADS site. For example,<br>
        <b><span style="color:red">hrrr</span>.<span style="color:blue">t05z</span>.wrf<span style="color:green">sfc</span><span style="color:darkorange">f12</span>.grib2</b><br>
        <b><span style="color:red">[model type]</span>.<span style="color:blue">t[run hour]z</span>.wrf<span style="color:green">[variable field]</span><span style="color:darkorange">f[forecast hour]</span>.grib2
        </b>
        <p>Note: You will have to keep track of the file date yourself. 
        The file name only contains information about the run and forecast hour,
        so be careful that you don't overwrite files if you are downloading from
        multiple days into the same directory.
        <p>You may script the download process. Click the "Scripting Tips"
        button above for some help.
        <p>Read the HRRR FAQ for a description of what file and dates are available.
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
display = ['HRRR (operational)', 'HRRRx (experimental)', 'Alaska (experimental)']
value = ['oper', 'exp','alaska']

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
      <label class="control-label col-md-2" for="field">Variables Field:</label>
      <div class="col-md-4">          
        <select class="form-control" id="field" name="field">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = ['Surface (sfc, 2D fields)', 'Pressure (prs, 3D fields)', 'Sub-hourly (HRRR only)', 'HRRR Native Grid - BrianHead Fire 2017, June 25-July 18']
value = ['sfc', 'prs', 'subh', 'BRIANHEAD']

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
        <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2015-04-17" max="'''+max_date+'''">
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
rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'
if field not in ['prs', 'sfc', 'subh']:
    ls = ' ls horelS3:HRRR/%s/%s/%04d%02d%02d | cut -c 11-' \
        % (model, 'nat', DATE.year, DATE.month, DATE.day)
else:
    ls = ' ls horelS3:HRRR/%s/%s/%04d%02d%02d | cut -c 11-' \
        % (model, field, DATE.year, DATE.month, DATE.day)
rclone_out = subprocess.check_output(rclone + ls, shell=True)
flist = rclone_out.split('\n')

if model == 'oper':
    file_model = 'hrrr'
    model_hours = range(0, 24)
    f_hours = range(0, 19)
elif model == 'exp':
    file_model = 'hrrrX'
    model_hours = range(0, 24)
    f_hours = range(0, 19)
elif model == 'alaska':
    file_model = 'hrrrAK'
    model_hours = range(0, 24, 3)
    f_hours = range(0, 37)

for h in model_hours:
    print '''<div class="form-group">'''
    print '''<div class="col-md-12">'''
    print '''<div class="mybtn-group">'''
    print '''<button name="hour" type="button" class="mybtn hourbtn">Hour %02d</button>''' % (h)
    for f in f_hours:
        if field not in ['prs', 'sfc', 'subh']:
            # Then the request is a for a HRRR native grid file.
            # These are subregional native files, with the field defining the name of the subregion
            look_for_this_file = '%s.t%02dz.wrfnatf%02d.grib2.%s' % (file_model, h, f, field)
            baseURL = 'https://pando-rgw01.chpc.utah.edu/HRRR'
            pathURL = '/%s/%s/%04d%02d%02d/' % (model, 'nat', DATE.year, DATE.month, DATE.day)
            fileURL = look_for_this_file
        else:
            look_for_this_file = '%s.t%02dz.wrf%sf%02d.grib2' % (file_model, h, field, f)
            baseURL = 'https://pando-rgw01.chpc.utah.edu/HRRR'
            pathURL = '/%s/%s/%04d%02d%02d/' % (model, field, DATE.year, DATE.month, DATE.day)
            fileURL = look_for_this_file
        if look_for_this_file in flist:
            if link2 == 'grib2':
                download_this = baseURL+pathURL+fileURL
            elif link2 == 'metadata':
                download_this = 'https://api.mesowest.utah.edu/archive/HRRR/'+pathURL+fileURL+'.idx'
            elif link2 == 'sample':
                download_this = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_sample.cgi?model=%s&date=%s&hour=%s&fxx=%s' % (file_model, Date, h, f)
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


<br><br>
<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
