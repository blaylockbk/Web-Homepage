#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

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
      variable = form['variable'].value
except:
      units = 'C'
      variable = 'air_temp'

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
<h1 align="center">Multi-station Time Series</h1>
<br>

<div style="background-color:#f5f5f5; width:85%; max-width:1000px; margin-left:auto; margin-right:auto;">	
	<div style="background-color:#d40000;">
		<br><p style="color:white;"> <font size="4"><b>Instructions:</b></font>
		  Input up to 4 MesoWest station IDs to plot each time series on 
              the same graph. You must have at least 2 station IDs 
              (if you really only want to plot one station, you can cheet the 
              system by inputing the same ID in two boxes).
              Fill in the boxes in the order you want to plot them. If you have a 
              station in box (1) and (3), don't leave (2) blank.
              Input the UTC dates in the format YYYY-MM-DD HH:MM. If 
              you leave the end date blank, it will use the current time
              (hard coded to be +7 hours of local time).
              If the requested station was not plotted, there was error getting
              it's data from the MesoWest API. The station ID may be incorrect 
              it that variable isn't availalbe at that station for that time.
		<br><br>  
	</div>			
	
       
<div>
<div>
   <br>

<div class="contentText">
<form method="GET" action="cgi-bin/ts_multistations.cgi">
	  
<table class="center">
      
<!---STATION ----------------------->	  
      <tr>
            <td><a title="Station ID used by mesowest.utah.edu">
		      Station ID:</a>
            </td>
            <td>
                  1:<input style="width:75px" type="text" name="stn1" value="'''+stn1+'''">
                  2:<input style="width:75px" type="text" name="stn2" value="'''+stn2+'''">
                  3:<input style="width:75px" type="text" name="stn3" value="'''+stn3+'''">
                  4:<input style="width:75px" type="text" name="stn4" value="'''+stn4+'''">
            </td>
      </tr>
<!---(station) ----------------------->	  
	    
	  
<!---TIME OPTION ----------------------->  
	<tr>
            <td><a title="YYYY-MM-DD HH:MM">
                 Time Option (UTC):</a>
            </td>
            <td>
                  Start:<input type="text" style="width:200px" name="start" value="'''+start+'''">
                  End:<input type="text" style="width:200px" name="end" value="'''+end+'''">
            </td>
	</tr>
<!---(time option) ----------------------->

<!---Units ----------------------------->	  
      <tr>
            <td>Units:</td>
            <td>'''
if units=='C':
      print '''<input type='radio' name='units' value='C' checked> C
               <input type='radio' name='units' value='F'> F'''
else:
      print '''<input type='radio' name='units' value='C'> C
               <input type='radio' name='units' value='F' checked> F'''
print '''
            </td>
	</tr>
<!---(units) ---------------------------->

<!---Variables ----------------------->  
	<tr>
      <td>Variables:</td>
      <td>
         <select name="variable" style="width:200px">'''
# display is the variable name as it will display on the webpage
# value is the value used in the MesoWest API call
display = ['Air Temperature', 'Relative Humidity', 'Wind Speed', 'Wind Direction', 'Wind Barbs']
value = ['air_temp','relative_humidity', 'wind_speed', 'wind_direction', 'wind_direction,wind_speed']

for i in range(0,len(value)):
   if variable == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
      </td>
      </tr>
<!---(variables) ----------------------->

<!---SUBMIT BUTTON ----------------------->
      <tr>
            <td colspan=5 align="center">
                  <input type="submit" value="Make Plot" class="myButton">
            </td>
      </tr>
<!---(submit button) ----------------------->   

</table>
</form>
</div>
</div>
</div>


<!--Multistation Graph-->

<a target="_blank" href="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
+'''&stn2='''+stn2 \
+'''&stn3='''+stn3 \
+'''&stn4='''+stn4 \
+'''&start='''+start \
+'''&end='''+end \
+'''&units='''+units \
+'''&variable='''+variable \
+'''">

<img alt="Error: Temp/RH graph not available for some reason"
class="style1"
src="cgi-bin/plot_ts_multistations.cgi?stn1='''+stn1 \
+'''&stn2='''+stn2 \
+'''&stn3='''+stn3 \
+'''&stn4='''+stn4 \
+'''&start='''+start \
+'''&end='''+end \
+'''&units='''+units \
+'''&variable='''+variable \
+'''" width=95%>

</a>
<div style='padding:50px'>
      <h3>Quick Plots: Last 31 hours</h3>
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
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''

"""
Someday, add in options to modify the plot size, label fonts, dpi, etc. to 
easily customize plots for publications.

"""

