#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
January 17, 2017

To Do List:
[X] Add Bootstrap Modals for page instructions. (Jan 17, 2017)
[ ] Add aditional API query that finds the shared variables between the
    requested stations and creates a variable dropdown for the available data.
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
      stn1 = form['stn1'].value
except:
      stn1 = 'PSRIM'
try:
      stn2 = form['stn2'].value
except:
      stn2 = 'PSINK'
try:
      stn3 = form['stn3'].value
except:
      stn3 = ''
try:
      stn4 = form['stn4'].value
except:
      stn4 = ''
try:
      start = form['start'].value
except:
      start = onedayago.strftime('%Y-%m-%d %H:%M')
try:
      end = form['end'].value
except:
      end = (current+timedelta(hours=7)).strftime('%Y-%m-%d %H:%M')
try:
      units = form['units'].value
except:
      units = 'C'

# The issue here is if all the form isn't filled, it defaluts to the peter sinks exception

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>Multi-station Time Series</title>
</head>'''

print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>

      <h1 align="center"><i class="fa fa-chart-line fa-fw"></i> Multi-station Time Series
      <!-- Large modal (the intrusctions help button)-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-lg">Instructions</button>

      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="padding:25px">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 style="font-size:22px;">MesoWest Multi-Station Time Series Plots</h4><hr>
            <h5 align="left" style="font-size:18px;">
            <ol style="padding-left:10px;">
            <li>Input up to 4 <a href="http://mesowest.utah.edu/">MesoWest</a> station IDs to plot each time series on 
            the same graph. 
                  <ul style="padding-left:10px">
                  <li>Requires at least 2 stations. (You can cheat the system
                  for a single station time series by requesting the same ID twice).
                  <li> Fill station input in order (i.e. Don't leave Station 2 blank if 1 and 3 are filled).
                  </ul>
            <li>Input the UTC dates in the format <font color="red">YYYY-MM-DD HH:MM</font>. 
                  <ul style="padding-left:10px">
                  <li>If you leave the end date blank, it will use the current time (hard coded to be +7 hours of local time).
                  </ul>
            <li>Choose the units (only for temperature).
            <li>Select the variable.
            </ol>
            <hr>
            <p>Note: If the requested station was not plotted, there was an error getting
            it's data from the MesoWest API. The station ID may be incorrect 
            or not availalbe for the request variable or time.
            <p>Hack! If you want more than four stations, add more station IDs in
            the last station input field, each separated by a comma (e.g. kslc,naa,wbb,mtmet).
          
          <hr>

            <p>Example quick plots: Last 31 hours
                  <ul style='padding-left:30px'>
                  <li><a href='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ts_multistations.cgi?stn1=UT20&stn2=UT23&stn3=UT12&stn4=UT11'>
                  Salt Lake County 1-15 UDOT</a>
                  <li><a href='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ts_multistations.cgi'>
                  Peter Sinks, UT</a>
                  <li><a href='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ts_multistations.cgi?stn1=MTMET&stn2=WBB&stn3=KSLTC&stn4=KSLC'>
                  University of Utah to Airport</a>
                  <li><a href='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ts_multistations.cgi?stn1=KSLC&stn2=FPS&stn3=KPVU&stn4=UKBKB'>
                  Salt Lake to Spanish Fork</a>
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

<form class="form-inline" method="GET" action="cgi-bin/ts_multistations.cgi">
	  
<table class="center table table-responsive">
      
<!---STATION ----------------------->	  
      <tr>
            <td><a title="Station ID used by mesowest.utah.edu">
		      Station ID:</a>
            </td>
            <td>
                  <input class="form-control" placeholder="Station 1" type="text" name="stn1" value="'''+stn1+'''">
                  <input class="form-control" placeholder="Station 2" type="text" name="stn2" value="'''+stn2+'''">
                  <input class="form-control" placeholder="Station 3" type="text" name="stn3" value="'''+stn3+'''">
                  <input class="form-control" placeholder="Station 4" type="text" name="stn4" value="'''+stn4+'''">
            </td>
      </tr>
<!---(station) ----------------------->	  
	    
	  
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

<!---Units ----------------------------->	  
      <tr>
            <td>Units:</td>
            <td>'''
if units=='C':
      print '''<div class='radio'>
               <label><input type='radio' name='units' value='C' checked> C</label>
               <label><input type='radio' name='units' value='F'> F</label>
               </div>
               '''
else:
      print '''<div class='radio'>
               <label><input type='radio' name='units' value='C'> C</label>
               <label><input type='radio' name='units' value='F' checked> F</label>
               </div>'''
print '''
            </td>
	</tr>
<!---(units) ---------------------------->


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


<!--Multistation Graph, one for each variable-->
'''
# I tried printing this html in a loop, but it rendered all the images stacked
# in the first tab, until another tab was selected. This method is repetative, 
# but it works.
print '''
<!-- Individual Plot Tabs-->
<ul class="nav nav-tabs">
    <li class="active"><a data-toggle="tab" href="#tab1">Air Temperature</a></li>
    <li><a data-toggle="tab" href="#tab2">Relative Humidity</a></li>
    <li><a data-toggle="tab" href="#tab3">Wind Speed</a></li>
    <li><a data-toggle="tab" href="#tab4">Wind Direction</a></li>
    <li><a data-toggle="tab" href="#tab5">Wind Barb</a></li>
    <li><a data-toggle="tab" href="#tab6">Other</a></li>
  </ul>

  <div class="tab-content">
    <div id="tab1" class="tab-pane fade in active">
      <a target="_blank" href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=air_temp">

                              <img alt="Error: Temp/RH graph not available for some reason"
                              class="style1"
                              src="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=air_temp" width=95%>
                              </a>
    </div>
    <div id="tab2" class="tab-pane fade">
      <a target="_blank" href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=relative_humidity">

                              <img alt="Error: Temp/RH graph not available for some reason"
                              class="style1"
                              src="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=relative_humidity" width=95%>
                              </a>
    </div>
    <div id="tab3" class="tab-pane fade">
      <a target="_blank" href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=wind_speed">

                              <img alt="Error: Temp/RH graph not available for some reason"
                              class="style1"
                              src="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=wind_speed" width=95%>
                              </a>
    </div>
    <div id="tab4" class="tab-pane fade">
      <a target="_blank" href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=wind_direction">

                              <img alt="Error: Temp/RH graph not available for some reason"
                              class="style1"
                              src="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=wind_direction" width=95%>
                              </a>
    </div>
    <div id="tab5" class="tab-pane fade">
      <a target="_blank" href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=wind_direction,wind_speed">

                              <img alt="Error: Temp/RH graph not available for some reason"
                              class="style1"
                              src="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=wind_direction,wind_speed" width=95%>
                              </a>
    </div>
    <div id="tab6" class="tab-pane fade">
      <h3>Other Possible Variables, if available</h3>
      <ul style="padding-left:60px">
            <li><a href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=PM_25_concentration" target="_blank">PM 25 Concentration
            <li><a href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=ozone_concentration" target="_blank">Ozone Concentration
            <li><a href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
                              +'''&stn2='''+stn2 \
                              +'''&stn3='''+stn3 \
                              +'''&stn4='''+stn4 \
                              +'''&start='''+start \
                              +'''&end='''+end \
                              +'''&units='''+units \
                              +'''&variable=pressure" target="_blank">Pressure
      </ul>
    </div>
  </div>



<div class="github_link" align='right' style="padding-top:10px;padding-right:20px;">
<a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/ts_multistations.cgi" target="_blank">
      <i class="fab fa-github fa-fw"></i>Page
</a>
<a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/plot_ts_multistations.cgi" target="_blank">
      <i class="fab fa-github fa-fw"></i>Plot
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
