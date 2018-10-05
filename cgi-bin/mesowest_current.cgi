#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 16, 2018

Display table of current MesoWest observations for any station
"""

import os
import cgi, cgitb
from datetime import datetime, timedelta
import time
cgitb.enable()

form = cgi.FieldStorage()
print "Content-Type: text/html\n"

try:
    STN = cgi.escape(form['STN'].value)
except:
    STN = 'UKBKB'
try:
    UNITS = cgi.escape(form['UNITS'].value)
except:
    UNITS = 'English'
try:
    TZ = cgi.escape(form['TZ'].value)
except:
    TZ = 'Local'

# Get nearest station data
import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
from BB_MesoWest.MesoWest_latest import *
from BB_wx_calcs.humidity import Tempdwpt_to_RH

a = get_mesowest_latest(STN, tz=TZ, units=UNITS)

sectors = np.arange(22.5, 361, 45)
Wdir = a['wind_direction']['value']
if np.isnan(Wdir):
    WDR = "no wind direction"
elif Wdir <= sectors[0] or Wdir > sectors[-1]:
    WDR = 'North'
elif Wdir >= sectors[0] and Wdir < sectors[1]:
    WDR = 'Northeast'
elif Wdir >= sectors[1] and Wdir < sectors[2]:
    WDR = 'East'
elif Wdir >= sectors[2] and Wdir < sectors[3]:
    WDR = 'Southeast'
elif Wdir >= sectors[3] and Wdir < sectors[4]:
    WDR = 'South'
elif Wdir >= sectors[4] and Wdir < sectors[5]:
    WDR = 'Southwest'
elif Wdir >= sectors[5] and Wdir < sectors[6]:
    WDR = 'West'
elif Wdir >= sectors[6] and Wdir < sectors[7]:
    WDR = 'Northwest'

if TZ.upper() == 'LOCAL':
    minutes_ago =  (datetime.now()-a['DATE']).seconds/60+(datetime.now()-a['DATE']).days*1440
else:
    minutes_ago =  (datetime.utcnow()-a['DATE']).seconds/60+(datetime.utcnow()-a['DATE']).days*1440

print '''
<!DOCTYPE html>
<html>

<head>
<title>MesoWest Current Conditions</title>
<script src="../js/site/siteopen.js"></script>
</head>


<body>
<a name="TOP"></a>
<script src="./js/site/sitemenu.js"></script>	

<div class="container">
<h1 align="center"><i class="fa fa-sun" aria-hidden="true"></i> MesoWest Current Conditions - %s</h1>
''' % (STN)

print '''
<center>
<form class="form-horizontal" method="GET" action="cgi-bin/mesowest_current.cgi">
<div class="col-sm-1"></div>      
<!---STATION ----------------------->	  
<div class="form-group">
      <label class="control-label col-sm-2" for="station"><a style='color:black' title="Station ID used by mesowest.utah.edu">Station ID</a>:</label>
      <div class="col-sm-2">
            <input type="text" class="form-control" id="STN" placeholder="MesoWest ID" name="STN" value="'''+STN+'''">
      </div>
              
<!---(station) ----------------------->	  

<!---Time Zone ----------------------------->	  
<div class="col-sm-2">
<div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if TZ.upper() == 'UTC':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="TZ" id="TZ" autocomplete="off" value='UTC' checked> UTC
        </label>
        <label class="btn btn-default">
            <input type="radio" name="TZ" id="TZ" autocomplete="off" value='Local'> Local
        </label>
    '''
elif TZ.upper() == 'LOCAL':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="TZ" id="TZ" autocomplete="off" value='UTC'> UTC
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="TZ" id="TZ" autocomplete="off" value='Local' checked> Local
        </label>'''
print '''
</div>
</div>
<!---(units) ---------------------------->	    
	  
<!---Units ----------------------------->	  
<div class="col-sm-2">
<div class="btn-group btn-group-justified" data-toggle="buttons">
'''
if UNITS.upper() == 'METRIC':
    print '''
        <label class="btn btn-default active">
            <input type="radio" name="UNITS" id="UNITS" autocomplete="off" value='metric' checked> Metric
        </label>
        <label class="btn btn-default">
            <input type="radio" name="UNITS" id="UNITS" autocomplete="off" value='english'> English
        </label>
    '''
elif UNITS.upper() == 'ENGLISH':
    print '''
        <label class="btn btn-default">
            <input type="radio" name="UNITS" id="UNITS" autocomplete="off" value='metric'> Metric
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="UNITS" id="UNITS" autocomplete="off" value='english' checked> English
        </label>'''
print '''
</div>
</div>
<!---(units) ---------------------------->


<!-- Submit Button ----------------------------------------------------------->
<div class="col-sm-2">
<button type="submit" class="btn btn-success btn-block">Get Data</button>
</div>
</div>
<!-- (Submit Button) -----------------------------------------------------------> 
</form>
</center>
'''

print '''
<br>
<table class="table table-hover">
<tr><td align="right">Station Name</td><td>%s</td></tr>
<tr><td align="right">Observation Time</td><td>%s %s (%s minutes ago)</td></tr>
'''  % (a['NAME'], 
        a['DATE'].strftime('%B %d, %Y %I:%M %p %A'), TZ, minutes_ago)

keys = a.keys()
keys.sort()
for i in keys:
    if i not in ['DATE', 'NAME', 'URL', 'STID', 'qc']:
        print """<tr><td align="right">%s</td><td>%s %s</td></tr>""" % (i.replace('_', ' ').upper(), a[i]['value'], a[i]['unit'])


print '''
<tr><td align="right">Wind Direction</td><td>%s (%s degrees)</td></tr>
</table>
'''% (WDR, a['wind_direction']['value'])

print '''
<center>
<a class='btn btn-default' href="http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=%s">MesoWest Table</a>
<a class='btn btn-default' href="%s">Raw Data</a>
<p><a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/mesowest_current.cgi" target="_blank"><i class="fab fa-github"></i> Page HTML code</a>
</center>
''' % (STN, a['URL'])

print '''
<hr>

<h3>Temperature, Dew Point, Relative Humidity</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=TTD&level=">

<h3>Temperature, Wet Bulb</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=TWB&level=">

<h3>Wind</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=WND&level=">

<h3>Pressure</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=PRES&level=">

<h3>24-hr Precipitation</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=P24I&level=">

<h3>5-min Precipitation</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=P05I&level=">

<h3>1-min Precipitation</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=P1MI&level=">

<h3>Accumulated Precipitation</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='''+STN+'''&unit=0&hours=25&past=0&day1=0&month1=&year1=&hour1=00&time=LOCAL&var=PREC&level=">

<h3> Radar</h3>
<img class="img-rounded" width="100%" onclick='window.open(this.src)' src="https://radar.weather.gov/Conus/RadarImg/latest.gif">
'''

print '''
</div>

<script src="./js/site/siteclose.js"></script>
</body>
</html>
'''
