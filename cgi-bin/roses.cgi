#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
January 17, 2017

To Do List:
[ ] Add back in minimum ozone threshold.
[ ] Add advanced options to modify the plot size, label fonts, dpi, etc. to 
    easily customize plots for publications.
"""

import sys
import cgi, cgitb
import time
from datetime import datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

current = datetime.now()
onedayago = datetime.now()-timedelta(days=1)

try:
      stn = form['stn'].value
except:
      stn = 'WBB'
try:
      start = form['start'].value
except:
      start = onedayago.strftime('%Y-%m-%d %H:%M')
try:
      end = form['end'].value
except:
      end = (current+timedelta(hours=7)).strftime('%Y-%m-%d %H:%M')
try:
      rose_type = form['rose_type'].value
except:
      rose_type = 'wind'
try:
      tz = form['tz'].value   # Time Zone
except:
      tz = 'UTC'
try:
      HI = form['HI'].value   # Hour interval
except:
      HI = 'All Day'
try:
      threshold = form['threshold'].value
except:
      threshold = '00'
try:
      plot_max = form['plot_max'].value
except:
      plot_max = 'auto'

# The issue here is if all the form isn't filled, it defaluts to the peter sinks exception

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>Rose Plots</title>
</head>'''

print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>

      <h1 align="center"><i class="fa fa-pie-chart fa-fw" aria-hidden="true"></i> Rose Plots
      <!-- Large modal (the intrusctions help button)-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">MesoWest Rose Plots</h4><hr>
            <h5 align="left" style="font-size:18px;">
            Input a <a href="http://mesowest.utah.edu/">MesoWest</a> station ID and date range
            Select the rose type, time zone, hour interval, and plot range.
            <ul style="padding-left:10px;">
                  <li>Rose type: color fill by variable name. A traditional 
                  rose uses wind direction the polar coordinate. The clock 
                  rose uses the time of day as the polar coordinate.
                  <li>Time option: UTC or incrament hour by time zone.
                  <li>Hour interval: All day or filter by a three hour chunk.
                  <li>Min Ozone: Filter data by a minimum ozone threshold. Only 
                  useful for the traditional ozone rose.
                  <li>Plot range: modify the plot range (zoom in an out of polar coordinate).
            </ul>
            <hr>
            Note: Not all stations have ozone sensors and will not be able to 
            create a plot. Some station IDs you might like to try are mtmet 
            (University of Utah), naa (Neil Armstrong Academy West Valley), 
            qhw (Hawthorne, Salt Lake City), qnp (Provo Airport), and qsf 
            (Spanish Fork).
            <hr>
            Note: Clock roses are best for long time series. You'll know you have 
            requested enough time if each observation hour averages to 4% of the time.
          
          <hr>

            <p>Example quick plots: Last 31 hours
                  <ul style='padding-left:30px'>
                  <li><a href='#'>
                  Place holder</a>
                  </ul>
            </h5>

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

<form class="form-inline" method="GET" action="cgi-bin/roses.cgi">
	  
<table class="center table table-responsive">
      
<!---STATION ----------------------->	  
      <tr>
            <td><a title="Station ID used by mesowest.utah.edu">
		      Station ID:</a>
            </td>
            <td>
                  <input class="form-control" placeholder="Station ID" type="text" name="stn" value="'''+stn+'''">
            
      
<!---(station) ----------------------->	  
<!---Rose Type ----------------------->  
	
      <span style="padding-left:10px;">Rose Type:</span>
      
         <select class="form-control" name="rose_type">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = ['Wind Speed', 'Wind Clock', 'Ozone', 'Ozone Clock', 'PM 2.5', 'PM Clock']
value = ['wind','wind_clock', 'ozone', 'ozone_clock', 'pm_25', 'pm_clock']

for i in range(0,len(value)):
   if rose_type == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </td>
      </tr>
<!---(rose_type) ----------------------->

	  
<!---TIME OPTION ----------------------->  
	<tr>
            <td><a title="YYYY-MM-DD HH:MM">
                 Time Option (UTC):</a>
            </td>
            <td>
                  Start: <input class="form-control" placeholder="YYYY-MM-DD HH:MM" type="text" name="start" value="'''+start+'''">
                  End: <input class="form-control" placeholder="YYYY-MM-DD HH:MM" type="text" name="end" value="'''+end+'''">
            </td>
	</tr>
<!---(time option) ----------------------->



<!---Time Zone ----------------------->  
	<tr>
      <td>Time Option: *coming soon*</td>
      <td>
         <select class="form-control" name="tz">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = ['UTC', '-7 h', '-6 h', '-5 h', '-4 h']
value = ['0','7', '6', '5', '4']

for i in range(0,len(value)):
   if tz == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      
<!---(time_zone) ----------------------->

<!---Hour Interval ----------------------->  
	<span style="padding-left:10px">Hour Interval: *coming soon*</span>
      
         <select class="form-control" name="HI">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = ['All Day','00-03','03-06','06-09','09-12','12-15','15-18','18-21','21-24']
value = ['All Day','00-03','03-06','06-09','09-12','12-15','15-18','18-21','21-24']

for i in range(0,len(value)):
   if HI == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </td>
      </tr>
<!---(Hour Interval) ----------------------->

<!---THRESHOLD ----------------------->	  	  
	  <tr>
         <td>
		 Min Threshold: *coming soon*
		 </td>
		 
		 <td>
         <input class="form-control" type="text" name="threshold" value="'''+threshold+'''">             
<!---(threshold) ----------------------->

<!---PLOT MAX ----------------------->	  	  
	<span style="padding-left:10px"> Plot Range:</span>
	
		 
         <select class="form-control" name="plot_max">'''
limits = ['auto', '05','10','15','20','25','30','35','40','45','55','55']
for i in limits:
   if plot_max == i:
      print'''<option selected="selected">'''+i+'''</option>'''
   else:
      print'''<option>'''+i+'''</option>'''
print''' </select>
         </td>
      </td>
      </tr>
<!---(plot range) ----------------------->

<!---SUBMIT BUTTON ----------------------->
      <tr>
            <td colspan=5 align="center" style="padding:10px">
                  <input type="submit" value="Make Plot" class="btn btn-primary">
            </td>
      </tr>
<!---(submit button) ----------------------->   

</table>
</form>
</div>
</div>
</div>


<!--Rose Plots-->

<a target="_blank" href="cgi-bin/plot_roses.cgi?''' \
+'''&stn='''+stn \
+'''&rose_type='''+rose_type \
+'''&start='''+start \
+'''&end='''+end \
+'''&tz='''+tz \
+'''&HI='''+HI \
+'''&threshold='''+threshold \
+'''&plot_max='''+plot_max \
+'''">

<img alt="Error: couldn't plot the rose"
class="style1"
src="cgi-bin/plot_roses.cgi?''' \
+'''&stn='''+stn \
+'''&rose_type='''+rose_type \
+'''&start='''+start \
+'''&end='''+end \
+'''&tz='''+tz \
+'''&HI='''+HI \
+'''&threshold='''+threshold \
+'''&plot_max='''+plot_max \
+'''" width=95%>

</a>

<div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
<a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/roses.cgi" target="_blank">
      <i class="fa fa-github fa-fw" aria-hidden="true"></i>Page
</a>
<a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_roses.cgi" target="_blank">
      <i class="fa fa-github fa-fw" aria-hidden="true"></i>Plot
</a>
</div>



<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>


<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
