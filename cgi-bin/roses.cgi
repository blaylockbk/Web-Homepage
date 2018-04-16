#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
January 17, 2017

To Do List:
[ ] Put "advanced options" in a dropdown bootstrap accordian menu
[ ] Add back in minimum ozone threshold.
[ ] Add advanced plot options to modify the plot size, label fonts, dpi, etc. to 
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
      tz = '0'
try:
      HI = form['HI'].value   # Hour interval
except:
      HI = 'All Day'
try:
      units = form['units'].value   # Units, english or metric
except:
      units = 'metric'
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
<body>
<script src="js/site/sitemenu.js"></script>
'''

print''' 
<h1 align="center"><i class="fa fa-chart-pie fa-fw"></i> Rose Plots
      <!-- Large modal (the intsructions help button)-->
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

<div class='container'>
<hr>
<div class="contentText form-group">
<form class="form-horizontal" method="GET" action="cgi-bin/roses.cgi">

<!-- Station ID and Rose Type ------------------------------------------------>
<div class="form-group">
      <label class="control-label col-sm-2" for="station">Station ID:</label>
      <div class="col-sm-3">
            <input type="text" class="form-control" id="stn" placeholder="Station ID" name="stn" value="'''+stn+'''">
      </div>
      <label class="control-label col-sm-2" for="email">Rose Type:</label>
      <div class="col-sm-3">
            <select class="form-control" name="rose_type">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = ['Wind Speed', 'Wind Clock', 'Gust', 'Ozone', 'Ozone Clock', 'PM 2.5', 'PM Clock']
value = ['wind','wind_clock', 'gust', 'ozone', 'ozone_clock', 'pm_25', 'pm_clock']

for i in range(0,len(value)):
   if rose_type == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </div>
</div>
<!-- (Station ID and Rose Type) ---------------------------------------------->


<!-- Date Range and Plot Max ------------------------------------------------->
<div class="form-group">
      <label class="control-label col-sm-2" for="pwd">Date Range:</label>
      <div class="col-sm-3">          
            Start: <input class="form-control" placeholder="YYYY-MM-DD HH:MM" type="text" name="start" value="'''+start+'''">
            End: <input class="form-control" placeholder="YYYY-MM-DD HH:MM" type="text" name="end" value="'''+end+'''">
      </div>
      <label class="control-label col-sm-2" for="pwd">Plot Max:</label>
      <div class="col-sm-3">
      <select class="form-control" name="plot_max">'''

limits = ['auto', '05','10','15','20','25','30','35','40','45','55','55']
for i in limits:
   if plot_max == i:
      print'''<option selected="selected">'''+i+'''</option>'''
   else:
      print'''<option>'''+i+'''</option>'''
print''' </select>
      </div>
</div>
<!-- (Date Range and Plot Max) ----------------------------------------------->


<!-- Time Zone and Hour Interval ---------------------------------------------->
<div class="form-group">
      <label class="control-label col-sm-2" for="station">Time Zone:</label>
      <div class="col-sm-3">
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
      </div>

      <label class="control-label col-sm-2" for="email">Hour Interval:</label>
      <div class="col-sm-3">
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
      </div>
</div>
<!-- (Time Zone and Hour Interval) ------------------------------------------->


<!-- Units and Threshold ------------------------------------------------------>
<div class="form-group">
      <label class="control-label col-sm-2" for="pwd">Units:</label>
      <div class="col-sm-3 btn-group" data-toggle="buttons">
'''
if units == 'metric':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="units" id="units" autocomplete="off" value='metric' checked> Metric
        </label>
        <label class="btn btn-default">
            <input type="radio" name="units" id="units" autocomplete="off" value='english'> English
        </label>
    '''
elif units == 'english':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="units" id="units" autocomplete="off" value='metric'> Metric
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="units" id="units" autocomplete="off" value='english' checked> English
        </label>'''
print '''
      </div>

      <label class="control-label col-sm-2" for="pwd">Minimum Threshold:</label>
      <div class="col-sm-3 btn-group" data-toggle="buttons">
            <input class="form-control" type="number" placeholder="Only show data greater than this number" name="threshold" value="'''+threshold+'''" disabled>             
      </div>
</div>
<!-- (Units and threshold) --------------------------------------------------->


<!-- Submit Button ----------------------------------------------------------->
<div class="form-group">        
      <div class="col-sm-offset-5 col-sm-10">
            <button type="submit" class="btn btn-success">Make Plot</button>
      </div>
</div>
<!-- (Submit Button) ----------------------------------------------------------->

</form>
</div>
<hr>

	
<!--Rose Plots-->

<a target="_blank" href="cgi-bin/plot_roses.cgi?''' \
+'''&stn='''+stn \
+'''&rose_type='''+rose_type \
+'''&start='''+start \
+'''&end='''+end \
+'''&tz='''+tz \
+'''&HI='''+HI \
+'''&units='''+units \
+'''&threshold='''+threshold \
+'''&plot_max='''+plot_max \
+'''">

<img alt="Error: couldn't plot the rose"
class="style11"
style='max-width:800px;width:90%'
src="cgi-bin/plot_roses.cgi?''' \
+'''&stn='''+stn \
+'''&rose_type='''+rose_type \
+'''&start='''+start \
+'''&end='''+end \
+'''&tz='''+tz \
+'''&HI='''+HI \
+'''&units='''+units \
+'''&threshold='''+threshold \
+'''&plot_max='''+plot_max \
+'''">
</a>


<br>
      <div align='right' style="width:90%;max-width:900px">
            <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/roses.cgi" target="_blank">
                  <i class="fab fa-github fa-fw"></i>Page
            </a>
            <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_roses.cgi" target="_blank">
                  <i class="fab fa-github fa-fw"></i>Plot
            </a>
      </div>


<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank">
      <img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px">
</a>

</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
