#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
January 30, 2017

HRRR-X versus HRRR (difference)

To Do List:
[X] Add Bootstrap Modals for page instructions. (Jan 17, 2017)
[ ] Add aditional API query that finds the shared variables between the
    requested stations and creates a variable dropdown for the available data.
[ ] Add advanced options to modify the plot size, label fonts, dpi, etc. to 
    easily customize plots for publications.
[ ] Add MesoWest QC checks
"""

import sys
import cgi, cgitb
from datetime import datetime, timedelta
import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
import numpy as np

cgitb.enable()

form = cgi.FieldStorage()

current = datetime.now()
onedayago = datetime.now()-timedelta(days=1)
yesterday = onedayago.strftime('%Y-%m-%d')

try:
      date = form['date'].value
except:
      date = yesterday

try:
      hour = form['hour'].value
except:
      hour = '03'

try:
      domain = form['domain'].value
except:
      domain = 'GSL'

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRRX versus HRRR</title>
</head>'''


print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>

      <h1 align="center"><i class="fa fa-map" aria-hidden="true"></i> HRRR Maps
      <!-- Large modal (the intrusctions help button)-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">Utah Experimental and Operational HRRR comparison</h4><hr>
            <h5 align="left" style="font-size:18px;">
            Input the date and hour (UTC) for the model run you wish to see the
            comparison between the HRRR and HRRR-X.
            <hr>Reasons the images couldn't be plotted
            <ol style="paddin-left:30px">
            <li>HRRR data isn't available. More likely that the HRRRx isn't available. Try another hour or day.
            <li>Browser timed out
            </ol>
            <br><br>
            <div class='alert alert-warning'>
            Note: If the requested date was not plotted, there was an error getting
            it's data from the archive. There may not be model data for that time.
            </div>
            <div class='alert alert-info'>
            Because of timeout issues, I can't show the CONUS, west, or east domains
            on this page. You can look at those domains. Just right click the 
            image and copy URL, paste URL in a new browser window, 
            and change the 'domain' argument
            to 'CONUS', 'west', or 'east' i.e. domain=west.
            </div>
            

      </div>
      </div>
      </div>
      </h1>

<br>

<div style="background-color:#f5f5f5; width:85%; max-width:1000px; margin-left:auto; margin-right:auto;">	
		
	
       
<div>
<div>
   <br>

<div class="contentText form-group">

<form class="form-inline" method="GET" action="cgi-bin/hrrrX-hrrr.cgi">
	  
<table class="center table table-responsive">
      
<!---Date ----------------------->	  
      <tr>
            <td><a title="YYYY-MM-DD">
		      Date:</a>
            </td>
            <td>
                  <input class="form-control" placeholder="YYYY-MM-DD" type="date" name="date" value="'''+date+'''">
            </td>
      </tr>
<!---(date) ----------------------->	  

<!---HOUR ----------------------->	  
      <tr>
            <td><a title="YYYY-MM-DD">
		      Hour:</a>
            </td>
            <td>
                  <select class="form-control" name="hour">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = range(0,25)
value = ['%02d' % (i) for i in display]

for i in range(0,len(value)):
   if hour == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+str(display[i])+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+str(display[i])+'''</option>'''
print''' </select>
            </td>
      </tr>
<!---(Hour) ----------------------->

<!---Domain ----------------------->	  
      <tr>
            <td><a title="YYYY-MM-DD">
		      Domain:</a>
            </td>
            <td>
                  <select class="form-control" name="domain">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = ['Utah', 'Great Salt Lake', 'Utah Lake', 'Uintah Basin','West US (this will timeout)', 'CONUS (this will timeout)']
value = ['Utah','GSL', 'UtahLake', 'Uintah', 'west', 'CONUS']

for i in range(0,len(value)):
   if domain == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
            </td>
      </tr>
<!---(Domain) ----------------------->

<!---SUBMIT BUTTON ----------------------->
      <tr>
            <td colspan=5 align="center" style="padding:10px">
                  <input type="submit" value="Submit" class="btn btn-primary">
            </td>
      </tr>
<!---(submit button) ----------------------->   

</table>
</form>
</div>
</div>
</div>

<h3 align="center">'''

print '''</h3>

  <!-- Tabs -->
  <ul class="nav nav-tabs">
    <li class="active"><a data-toggle="tab" href="#tab1">Skin Temp</a></li>
    <li><a data-toggle="tab" href="#tab2">2-m Temp</a></li>
    <li><a data-toggle="tab" href="#tab3">2-m DWPT</a></li>
    <li><a data-toggle="tab" href="#tab4">10-m Wind Speed</a></li>
    <li><a data-toggle="tab" href="#tab5">Terrain and Water</a></li>
    <li><a data-toggle="tab" href="#tab6">Vegetation</a></li>
    <li><a data-toggle="tab" href="#tab7">Other</a></li>
  </ul>

    <div class="tab-content">
        <div id="tab1" class="tab-pane fade in active">
            <img alt="Error: Whoops. Something is wrong."
                        class="style1"
                        src="cgi-bin/plot_hrrrX-hrrr_skin.cgi?date='''+date \
                              +'''&hour='''+hour \
                              +'''&domain='''+domain \
                              +'''" width="95%">
            <div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page</a>
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr_skin.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot</a>
            </div>
        </div>
        

        <div id="tab2" class="tab-pane fade">
            <img alt="Error: Whoops. Something is wrong."
                        class="style1"
                        src="cgi-bin/plot_hrrrX-hrrr_2mTemp.cgi?date='''+date \
                              +'''&hour='''+hour \
                              +'''&domain='''+domain \
                              +'''" width="95%">
            <div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page</a>
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr_2mTemp.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot</a>
            </div>        
        </div>

        <div id="tab3" class="tab-pane fade">
            <img alt="Error: Whoops. Something is wrong."
                        class="style1"
                        src="cgi-bin/plot_hrrrX-hrrr_2mDwpt.cgi?date='''+date \
                              +'''&hour='''+hour \
                              +'''&domain='''+domain \
                              +'''" width="95%"> 
            <div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page</a>
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr_2mDwpt.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot</a>
            </div>             
        </div>

        <div id="tab4" class="tab-pane fade">
            <img alt="Error: Whoops. Something is wrong."
                        class="style1"
                        src="cgi-bin/plot_hrrrX-hrrr_WSPD.cgi?date='''+date \
                              +'''&hour='''+hour \
                              +'''&domain='''+domain \
                              +'''" width="95%">
            <div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page</a>
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr_WSPD.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot</a>
            </div>            
        </div>

        <div id="tab5" class="tab-pane fade">
            <img alt="Error: Whoops. Something is wrong."
                        class="style1"
                        src="cgi-bin/plot_hrrrX-hrrr_Terrain.cgi?date='''+date \
                              +'''&hour='''+hour \
                              +'''&domain='''+domain \
                              +'''" width="95%">
            <div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page</a>
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr_Terrain.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot</a>
            </div>              
        </div>

        <div id="tab6" class="tab-pane fade">
            <img alt="Error: Whoops. Something is wrong."
                        class="style1"
                        src="cgi-bin/plot_hrrrX-hrrr_LandUse.cgi?date='''+date \
                              +'''&hour='''+hour \
                              +'''&domain='''+domain \
                              +'''" width="95%">
            <div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrrX-hrrr.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page</a>
                  <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_hrrrX-hrrr_LandUse.cgi" target="_blank">
                        <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot</a>
            </div>        
        </div>

        <div id="tab7" class="tab-pane fade">
            <h3>Other variable names shared by HRRR and HRRRx file</h3>
            <ul style="padding-left:60px">
            '''
var_list = ['Vertically-integrated liquid',
'Vertically-integrated liquid',
'Visibility',
'Wind speed (gust)',
'Surface pressure',
'Total snowfall',
'Plant canopy surface water',
'Water equivalent of accumulated snow depth',
'Snow cover',
'Snow depth',
'Potential temperature',
'Specific humidity',
'Relative humidity',
'Percent frozen precipitation',
'Precipitation rate',
'Water equivalent of accumulated snow depth',
'Storm surface runoff',
'Baseflow-groundwater runoff',
'Water equivalent of accumulated snow depth',
'Categorical snow',
'Categorical ice pellets',
'Categorical freezing rain',
'Categorical rain',
'Surface roughness',
'Frictional velocity',
'Sensible heat net flux',
'Latent heat net flux',
'Ground heat flux',
'Surface lifted index',
'Precipitable water',
'Pressure',
'Geopotential Height',
'Geopotential Height',
'Pressure',
'Geopotential Height',
'Upward long-wave radiation flux',
'Downward short-wave radiation flux',
'Downward long-wave radiation flux',
'Upward short-wave radiation flux',
'Upward long-wave radiation flux',
'Storm relative helicity',
'Storm relative helicity',
'U-component storm motion',
'V-component storm motion',
'Geopotential Height',
'Relative humidity',
'Pressure',
'Geopotential Height',
'Relative humidity',
'Pressure',
'Geopotential Height',
'Geopotential Height',
'Planetary boundary layer height',
'Geopotential Height',
'Geopotential Height',
'Land-sea mask',
'Sea-ice cover']
for i in var_list:
      print '''<li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrrX-hrrr_other.cgi?date='''+date+'''&hour='''+hour+'''&domain='''+domain+'''&other='''+i+'''" target="_blank">'''+i+'''</a>'''
print '''      
            </ul>
        </div>

    </div>
</div>




<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<br>
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
