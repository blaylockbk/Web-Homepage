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

<div style="width:85%;margin:auto" class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
  
  <div class="panel panel-primary">
    <div class="panel-heading" role="tab" id="headingTwo">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
          <i class="fa fa-info-circle" aria-hidden="true"></i> Instructions and proper use of the HRRR download interface
        </a>
      </h4>
    </div>
    <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
      <div class="panel-body">
        Please review the Terms and Conditions and register before downloading from the archive.
        <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_terms.html" target="_blank" class="btn btn-warning">
        <i class="fa fa-handshake-o" aria-hidden="true"></i> Terms and Conditions</a>
        <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_download_register.html" class="btn btn-danger">
        <i class="fa fa-user-plus" aria-hidden="true"></i> Have you Registered?</a>        
        <br><br>

  <!-- Tabs -->
  <ul class="nav nav-tabs">
    <li class="active"><a data-toggle="tab" href="#tab1">Available Data</a></li>
    <li><a data-toggle="tab" href="#tab2">Data Access: Click to Download</a></li>
    <li><a data-toggle="tab" href="#tab3">Data Access: Script to Download</a></li>
  </ul>

    <div class="tab-content">
        <div id="tab1" class="tab-pane fade in active">
        We provide archived HRRR data for the following:
        <ul style="padding-left:40px">
           <li>NOAA operational HRRR
              <ul style="padding-left:40px">
                  <li>Beginning April 18, 2015
                  <li>sfc and prc analyses
                  <li>sfc forecasts after July 27, 2016
                  <li>All variables
                  <li>Directory name = oper, File name = hrrr
              </ul>
           <li>ESRL experimental HRRR
              <ul style="padding-left:40px">
                  <li>Beginning December 1, 2016
                  <li>sfc analysis
                  <li>All variables
                  <li>Directory name = exp, File name = hrrrX
              </ul>          
           <li>ESRL experimental HRRR Alaska
              <ul style="padding-left:40px">
                  <li>Beginning September 1, 2016
                  <li>sfc and prs analyses
                  <li>sfc forecasts
                  <li>All prs variables, select sfc variables
                  <li>Directory name = alaska, File name = hrrrAK
              </ul>

        </ul>
        <p>For more details about the HRRR archive, check out the Frequently Asked Questions page<br>
        <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" class="btn btn-success">
        <i class="fa fa-info-circle" aria-hidden="true"></i> HRRR FAQ</a>
        </div>

        <div id="tab2" class="tab-pane fade">
        <p>Download grib2 files from this webpage. Select the model type, 
        variable field, and date of interest. Then click <i>Submit</i>.
        <p>After clicking the submit button, a grid of hours and forecasts is 
        displayed. If the file is available, the button will be highlighted 
        dark blue. Click the button to download the file. If the file is not 
        available, the button will be disabled and highlighted light blue.
        <p>Files are named similar to HRRR files named on the nomads site. For example,<br>
        <b><span style="color:red">hrrr</span>.<span style="color:blue">t05z</span>.wrf<span style="color:green">sfc</span><span style="color:darkorange">f12</span>.grib2</b><br>
        <b><span style="color:red">[model type]</span>.<span style="color:blue">t[run hour]z</span>.wrf<span style="color:green">[variable field]</span><span style="color:darkorange">f[forecast hour]</span>.grib2
        </b>
        <p>Note: You will have to keep track of the file date yourself. 
        The file name only contains information about the run and forecast hour,
        so be careful that you don't overwrite files if you are downloading from
        multiple days.
        </div>

        <div id="tab3" class="tab-pane fade">
              <p> Download grib2 files with wget or curl commands. You can write your
        own script to automate the download process, but PLEASE do not download
        an excessive number of files in a short period of time on multiple nodes
        (you agreed to not do this in the terms and conditions).
        <p> Files are downloaded from the URL <span style="font-family:monospace">https://pando-rgw01.chpc.utah.edu/HRRR/[model type]/[variable field]/[YYYYMMDD]/[file name]</span>
        <p> The model type and variable field directory tree options include the following:
        <ul style="padding-left:40px">
            <li><b>oper</b> for the operational HRRR
                  <ul style="padding-left:40px">
                        <li><b>sfc</b>
                        <li><b>prs</b>
                  </ul>
            <li><b>exp</b> for the experimental HRRR
                  <ul style="padding-left:40px">
                        <li><b>sfc</b>
                  </ul>
            <li><b>alaska</b> for HRRR Alaska
                  <ul style="padding-left:40px">
                        <li><b>sfc</b>
                        <li><b>prs</b>
                  </ul>
        </ul>
        <p> [YYYYMMDD] represents the UTC date format.
        <p> [file name] is in the format [hrrr/hrrrX/hrrrAK].t[00-23]z.wrf[sfc/prs]f[00-18 or 0-36].grib2
        
      <div class="panel panel-danger">
            <div class="panel-heading">
                  <h3 class="panel-title">cURL download file</h3>
            </div>
            <div class="panel-body" style="font-family:monospace">
                  curl -O https://pando-rgw01.chpc.utah.edu/HRRR/oper/sfc/20170101/hrrr.t00z.wrfsfcf00.grib2
            </div>
      </div>
      <div class="panel panel-danger">
            <div class="panel-heading">
                  <h3 class="panel-title">cURL download and rename file</h3>
            </div>
            <div class="panel-body" style="font-family:monospace">
                  curl -o hrrr20170101_00zf00.grib2 https://pando-rgw01.chpc.utah.edu/HRRR/oper/sfc/20170101/hrrr.t00z.wrfsfcf00.grib2
            </div>
      </div>
      <div class="panel panel-danger">
            <div class="panel-heading">
                  <h3 class="panel-title">wget download file</h3>
            </div>
            <div class="panel-body" style="font-family:monospace">
                  wget https://pando-rgw01.chpc.utah.edu/HRRR/oper/sfc/20170101/hrrr.t00z.wrfsfcf00.grib2
            </div>
      </div>
        </div>

    </div>


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
        <input name="date" value="'''+Date+'''" type="date" style="width:100%" class="form-control btn btn-default" id="date" min="2015-04-17" max="'''+max_date+'''">
      </div>
    </div>
<!--- (date)----------------------------->
    
    <div class="form-group">        
      <div class="col-md-offset-2 col-md-4">
        <button style="width:100%" type="submit" class="btn btn-success">Submit</button>
      </div>
    </div>
  </form>

</div>
</div>

<div class="container">
<h3>Tap to download '''+Date+''':</h3>
'''

# Create list of files available
DATE = datetime.strptime(Date, "%Y-%m-%d")
rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'
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
    print '''<label class="control-label col-md-2" for="fxx">Hour %02d:</label>''' % (h)
    print '''<div class="col-md-10">'''
    print '''<div class="mybtn-group">'''
    for f in f_hours:
        look_for_this_file = '%s.t%02dz.wrf%sf%02d.grib2' % (file_model, h, field, f)
        if look_for_this_file in flist:
            baseURL = 'https://pando-rgw01.chpc.utah.edu/HRRR'
            pathURL = '/%s/%s/%04d%02d%02d/' % (model, field, DATE.year, DATE.month, DATE.day)
            fileURL = look_for_this_file
            download_this = baseURL+pathURL+fileURL
            print '''<a href="'''+download_this+'''"><button name="fxx" type="button" class="mybtn unselected">f%02d</button></a>''' % (f)
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
