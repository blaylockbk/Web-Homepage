#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
January 27, 2017

MesoWest Station Climatology

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
import time
from datetime import datetime, timedelta
import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
from BB_MesoWest.MesoWest_climo import get_mesowest_climatology
import numpy as np

cgitb.enable()

form = cgi.FieldStorage()

current = datetime.now()
onedayago = datetime.now()-timedelta(days=1)

try:
      stn1 = form['stn1'].value
except:
      stn1 = 'UKBKB'

Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTH = np.array([])
AVG_Temp = np.array([])
MAX_Temp = np.array([])
MIN_Temp = np.array([])

station = stn1

months = np.arange(1, 13)
for m in months:
      start = '%02d010000' % (m)
      if m != 12:
            end = '%02d010000' % (m+1)
      else:
            end = '12312359'

      a = get_mesowest_climatology(station, start, end)

      MONTH = np.append(MONTH, m)

      avg_temp = np.nanmean(a['air_temp'])
      AVG_Temp = np.append(AVG_Temp, avg_temp)
      MAX_Temp = np.append(MAX_Temp, np.nanmax(a['air_temp']))
      MIN_Temp = np.append(MIN_Temp, np.nanmin(a['air_temp']))

# The issue here is if all the form isn't filled, it defaluts to the peter sinks exception

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>Station Climatology</title>
</head>'''


print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>

      <h1 align="center"><i class="fa fa-sun-o" aria-hidden="true"></i> Station Climatology
      <!-- Large modal (the intrusctions help button)-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">MesoWest Station Climatology</h4><hr>
            <h5 align="left" style="font-size:18px;">
            Input a MesoWest Sation ID and see statistics for that station.
            This tool severly needs QC checks.<h/5>
            <br><br>
            <div class="alert alert-info">As you noticed, this page can take a long time to load.
            Load time is a function of number of observations the station made.</div>            
            <div class='alert alert-warning'>
            Note: If the requested station was not plotted, there was an error getting
            it's data from the MesoWest API. The station ID may be incorrect.
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

<form class="form-inline" method="GET" action="cgi-bin/stn_climo.cgi">
	  
<table class="center table table-responsive">
      
<!---STATION ----------------------->	  
      <tr>
            <td><a title="Station ID used by mesowest.utah.edu">
		      Station ID:</a>
            </td>
            <td>
                  <input class="form-control" placeholder="Station 1" type="text" name="stn1" value="'''+stn1+'''">
            </td>
      </tr>
<!---(station) ----------------------->	  


<!---SUBMIT BUTTON ----------------------->
      <tr>
            <td colspan=5 align="center" style="padding:10px">
                  <input type="submit" value="Get Climatology" class="btn btn-primary">
            </td>
      </tr>
<!---(submit button) ----------------------->   

</table>
</form>
</div>
</div>
</div>

<h3 align="center">'''
print a['NAME'][0]
print '''</h3>

  <!-- Tabs -->
  <ul class="nav nav-tabs">
    <li class="active"><a data-toggle="tab" href="#tab1">Table</a></li>
    <li><a data-toggle="tab" href="#tab2">Plot</a></li>
    <li><a data-toggle="tab" href="#tab3">Details</a></li>
  </ul>

    <div class="tab-content">
        <div id="tab1" class="tab-pane fade in active">'''
print '''
<table class="table sortable">
<th>&#35</th><th>Month</th><th>Average (&degC)</th><th>Max (&degC)</th><th>Min (&degC)</th></th>
'''
for i in range(0,len(MONTH)):
      print '''<tr>'''
      print '<td>%d</td><td>%s</td><td>%.2f</td><td>%.2f</td><td>%.2f</td>' % (MONTH[i],Month[i], AVG_Temp[i], MAX_Temp[i], MIN_Temp[i])
      print '''</tr>'''
print '''</table>
        </div>

        <div id="tab2" class="tab-pane fade">
        <img alt="Error: Temp/RH graph not available for some reason"
                              class="style1"
                              src="cgi-bin/plot_stn_climo.cgi?stn1='''+stn1+'''" width=95%>
                              </a>
        <br><br><p>(Be patient, this takes some time to load. I'm really calling the 
        get_mesowest_climatology function twice on this page, which is 
        horribly inefficient)
        </div>

        <div id="tab3" class="tab-pane fade">
        <p>Details coming soon
        <p>Station name:
        <p>Date Range:
        <p>Number of Observations:
        </div>

    </div>
</div>



<div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
<a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/stn_climo.cgi" target="_blank">
      <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page
</a>
<a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_stn_climo.cgi" target="_blank">
      <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot
</a>
</div>

<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<br>
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
