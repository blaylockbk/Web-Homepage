#!/uufs/chpc.utah.edu/common/home/u0553130/anaconda3/bin/python

"""
Brian Blaylock
February 12, 2019

Generate custom figure of time series for multiple station locations from
MesoWest API for /test_python3.cgi

(A rewrite for pyBKB_v3)
"""

import matplotlib as mpl 
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator
from datetime import datetime, timedelta
from collections import OrderedDict

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/anaconda3/lib/python3.6/site-packages/')
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v3/')
from BB_MesoWest.get_MesoWest import get_mesowest_ts
from BB_wx_calcs.wind import wind_spddir_to_uv

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.
form = cgi.FieldStorage()	# CGI function takes in web arguments

print("Content-Type: text/html\n")
#print("Content-Type: image/png\n")

## Reset figure defaults (http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = np.array([16,9])*.8
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['axes.labelsize'] = 17
mpl.rcParams['axes.titlesize'] =20
mpl.rcParams['grid.linewidth'] = .25
mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.loc'] = 'best'
mpl.rcParams['savefig.bbox'] = 'tight'
#mpl.rcParams['savefig.dpi'] = 1000     # For publication purposes

#== Input from the URL form ===================================================
#==============================================================================

# MesoWest Station IDs
# NOTE: Users can request more than one station in a box by separating the
#       Station IDs with a comma.
try:
    stn1 = cgi.escape(form['stn1'].value)
except:
    stn1 = 'PSRIM'
try:
    stn2 = cgi.escape(form['stn2'].value)
except:
    stn2 = 'PSINK'
try:
    stn3 = cgi.escape(form['stn3'].value)
except:
    stn3 = ''
try:
    stn4 = cgi.escape(form['stn4'].value)
except:
    stn4 = ''

# Start and End Date: In the form 'YYYY-MM-DD HH:MM'
try:
    start = cgi.escape(form['start'].value)
    sDATE = datetime.strptime(start, '%Y-%m-%d %H:%M')
except:
    # if no start input, then default to 24 hours ago (UTC).
    sDATE = datetime.utcnow()-timedelta(days=1)
    start = sDATE.strftime('%Y-%m-%d %H:%M')
try:
    end = cgi.escape(form['end'].value)
    eDATE = datetime.strptime(end, '%Y-%m-%d %H:%M')
except:
    # if no end input, then default to right now, plus three hours
    eDATE = datetime.utcnow()+timedelta(hours=1)
    end = eDATE.strftime('%Y-%m-%d %H:%M')

# Desired Units: 'metric' or 'english'
try:
    units = cgi.escape(form['units'].value)
except:
    units = 'metric'

# Desired Variable:
# https://developers.synopticdata.com/mesonet/v2/api-variables/
try:
    variable = cgi.escape(form['variable'].value)
except:
    variable = 'air_temp'

#==============================================================================
#==============================================================================

## List of station IDs 
# Note: A user may request more than one station per entry if the ID is
# separated by a comman (,).
stations = []
for i in [stn1, stn2, stn3, stn4]:
    if i != '':
        stations += i.split(',')

## Preserve the requested order of the stations
data = OrderedDict()

## Get the data from MesoWest for each station
for s in stations:
    a = get_mesowest_ts(s, sDATE, eDATE, variables=variable, verbose=False)
    if a != 'ERROR':
        data[s] = a
    # Debug API Request
    #print(a['URL'])

## Create the Figure
fig, ax = plt.subplots(1, 1)

# Store the station that was plotted without errors
plotted_stations = [] 

for n, s in enumerate(data.keys()):   
    if variable == 'air_temp':
        if units == 'english':
            plot_this = data[s][variable]*9/5.+32
            unit = 'F'
        else:
            plot_this = data[s][variable]
            unit = 'C'
        ax.plot(data[s]['DATETIME'], plot_this, label=s.upper())
        plt.title('Air Temperature')
        plt.ylabel('Temperature (%s)' % unit)

    elif variable == 'relative_humidity':
        ax.plot(data[s]['DATETIME'], data[s][variable], label=s.upper())
        ax.set_ylim([0, 100])
        plt.title('Relative Humidity')
        plt.ylabel('Relative Humidity (%)')

    elif variable == 'wind_direction':
        ax.scatter(data[s]['DATETIME'], data[s][variable], label=s.upper())
        plt.ylim([0,360])
        plt.yticks(range(0,361,45), ['N','NE','E','SE','S','SW','W','NW','N',])
        plt.title('Wind Direction')
        plt.ylabel('Wind Direction')

    elif variable == 'wind_speed':
        if units == 'english':
            plot_this = data[s][variable]*2.2369
            unit = 'MPH'
        else:
            plot_this = data[s][variable]
            unit = r'ms$\mathregular{^{-1}}$'
        ax.plot(data[s]['DATETIME'], plot_this, label=s.upper())
        ax.set_ylim(ymin=0)
        plt.title('Wind Speed')
        plt.ylabel('Wind Speed (%s)' % unit) 

    elif variable == 'wind_direction,wind_speed':
        if 'wind_speed' in data[s].keys() and 'wind_direction' in data[s].keys():
            # Make a wind barb.
            u, v = wind_spddir_to_uv(data[s]['wind_speed'], data[s]['wind_direction'])
            # plt.barbs can not take a datetime, so find the date indexes:
            idx = mpl.dates.date2num(data[s]['DATETIME'])
            size = len(idx)
            ys = np.ones(size)*n
            ax.barbs(idx, ys, u, v, length=7, linewidth=.5, pivot='middle',
                    barb_increments=dict(half=2.5, full=5, flag=25))
            plt.title('Wind Barbs')
            plt.ylabel(r'Half=2.5, Full=5, Flag=25 (ms$\mathregular{^{-1}}$)')    
        
    else:
        ax.plot(data[s]['DATETIME'], data[s][variable], label=s.upper())
        plt.title(variable)
        plt.ylabel(variable)
    
    plotted_stations.append(s.upper())

plt.grid()
plt.xlabel('Date/Time (UTC)')
plt.xlim([sDATE, eDATE])

if variable == 'wind_direction,wind_speed':
  plt.yticks(range(0,n+1), plotted_stations)
  plt.ylim([-1, len(data.keys())])
else:
  plt.legend()


if (eDATE-sDATE).days == 0: # Less than one Day
    if (eDATE-sDATE).seconds <= 3600: # 1 hour
        ax.xaxis.set_major_locator(MinuteLocator(byminute=range(0,60,10)))
        ax.xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
    elif (eDATE-sDATE).seconds <= 10800: # 3 hours
        ax.xaxis.set_major_locator(MinuteLocator(byminute=[0,30]))
        ax.xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
    elif (eDATE-sDATE).seconds <= 43200: # 12 hours
        ax.xaxis.set_major_locator(HourLocator(byhour=range(24)))
        ax.xaxis.set_minor_locator(MinuteLocator(byminute=[0,30]))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
    else:
        ax.xaxis.set_major_locator(HourLocator(byhour=[0,3,6,9,12,15,18,21]))
        ax.xaxis.set_minor_locator(HourLocator(byhour=range(24)))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
else: # More than one day
    if (eDATE-sDATE).days < 2:
        ax.xaxis.set_major_locator(HourLocator(byhour=[0,3,6,9,12,15,18,21]))
        ax.xaxis.set_minor_locator(HourLocator(byhour=range(24)))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
    elif (eDATE-sDATE).days < 3:
        ax.xaxis.set_major_locator(HourLocator(byhour=[0,6,12,18]))
        ax.xaxis.set_minor_locator(HourLocator(byhour=range(24)))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
    elif (eDATE-sDATE).days < 6:
        ax.xaxis.set_major_locator(HourLocator(byhour=[0,12]))
        dateFmt = DateFormatter('%b %d\n%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
    else:
        dateFmt = DateFormatter('%b %d\n%Y')
        ax.xaxis.set_major_formatter(dateFmt)

DIR = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/Brian_Blaylock/cgi-bin/temp/'
NAME = 'web_temp_ts_multistation_%s' % variable
plt.savefig(DIR+NAME)	# Save with a figure name

#==============================================================================
# Web Page
#==============================================================================

print('''<!DOCTYPE html>
<html>
<head>
<script src="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>Multi-station Time Series</title>
</head>''')

print('''
<body>
<script src="js/site/sitemenu.js"></script>
''')


print(''' 
<h1 align="center"><i class="fa fa-chart-line fa-fw"></i> Multi-station Time Series
      <!-- Large modal (the instructions help button)-->
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
                  <li><a href='https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/test_python3.cgi?stn1=UT20&stn2=UT23&stn3=UT12&stn4=UT11'>
                  Salt Lake County 1-15 UDOT</a>
                  <li><a href='https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/test_python3.cgi'>
                  Peter Sinks, UT</a>
                  <li><a href='https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/test_python3.cgi?stn1=MTMET&stn2=WBB&stn3=KSLTC&stn4=KSLC'>
                  University of Utah to Airport</a>
                  <li><a href='https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/test_python3.cgi?stn1=KSLC&stn2=FPS&stn3=KPVU&stn4=UKBKB'>
                  Salt Lake to Spanish Fork</a>
                  </ul>
            </h5>

      </div>
      </div>
      </div>
      </h1>

<div class='container'>
<hr>
<div class="contentText form-group">
<form class="form-horizontal" method="GET" action="cgi-bin/test_python3.cgi">
      
<!---STATION ----------------------->	  
<div class="form-group">
      <label class="control-label col-sm-2" for="station"><a style='color:black' title="Station ID used by mesowest.utah.edu">Station IDs</a>:</label>
      <div class="col-sm-2">
            <input type="text" class="form-control" id="stn" placeholder="Station 1" name="stn1" value="'''+stn1+'''">
      </div>
      <div class="col-sm-2">
            <input type="text" class="form-control" id="stn" placeholder="Station 2" name="stn2" value="'''+stn2+'''">
      </div>
      <div class="col-sm-2">
            <input type="text" class="form-control" id="stn" placeholder="Station 3" name="stn3" value="'''+stn3+'''">
      </div>
      <div class="col-sm-2">
            <input type="text" class="form-control" id="stn" placeholder="Station 4,5,6,etc." name="stn4" value="'''+stn4+'''">
      </div>
 </div>               
<!---(station) ----------------------->	  
	    
	  
<!---TIME OPTION ----------------------->  
<div class="form-group">
      <label class="control-label col-sm-2" for="pwd">Date Range:</label>
      <div class="col-sm-4">          
            Start: <input class="form-control" placeholder="YYYY-MM-DD HH:MM" type="text" name="start" value="'''+start+'''">
      </div>
      <div class="col-sm-4">
            End: <input class="form-control" placeholder="YYYY-MM-DD HH:MM" type="text" name="end" value="'''+end+'''">
      </div>
</div>
<!---(time option) ----------------------->


<!--- Variable Type -----------------------> 
<div class="form-group">
    <label class="control-label col-md-2" for="variable">Variable:</label>
    <div class="col-md-4">      
        <select class="form-control" id="variable" name="variable">''')
# display is the variable name as it will display on the webpage
# value is the value used
display = ['Air Temperature', 'Relative Humidity', 'Wind Speed', 'Wind Direction', 'Wind Barbs', 'Pressure', 'PM 2.5 Concentration', 'Ozone Concentration']
value = ['air_temp', 'relative_humidity', 'wind_speed', 'wind_direction', 'wind_direction,wind_speed', 'pressure', 'PM_25_concentration', 'ozone_concentration']

for i in range(0,len(value)):
   if variable == value[i]:
      print('''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>''')
   else:
      print('''<option value="'''+value[i]+'''">'''+display[i]+'''</option>''')
print(''' </select>
    </div>

<!---Units ----------------------------->	 
<label class="control-label col-sm-1" for="pwd">Units:</label>
<div class="col-sm-3 btn-group" data-toggle="buttons">

''')
if units == 'metric':
    print('''
        <label class="btn btn-default active">
            <input type="radio" name="units" id="units" autocomplete="off" value='metric' checked> Metric
        </label>
        <label class="btn btn-default">
            <input type="radio" name="units" id="units" autocomplete="off" value='english'> English
        </label>
    ''')
elif units == 'english':
    print('''
        <label class="btn btn-default">
            <input type="radio" name="units" id="units" autocomplete="off" value='metric'> Metric
        </label>
        <label class="btn btn-default active">
            <input type="radio" name="units" id="units" autocomplete="off" value='english' checked> English
        </label>''')
print('''
      </div>
<!---(units) ---------------------------->

</div>
<!---(variable) ----------------------->



<!-- Submit Button ----------------------------------------------------------->
<div class="form-group">        
      <div class="col-sm-offset-5 col-sm-10">
            <button type="submit" class="btn btn-success">Make Plot</button>
      </div>
</div>
<!-- (Submit Button) -----------------------------------------------------------> 
</form>
</div>
<hr>''')


# =============================================================================
#  Image
# =============================================================================
URL =  'https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/temp/'
print('<img onclick="window.open(this.src)" src = "%s.png"/>' % (URL+NAME)) # Display saved figure
# =============================================================================

demoURL = a['URL']
import re
result = re.search('&token=(.*)&stid=', demoURL)
demoURL = demoURL.replace(result.group(1), 'demotoken')
print('''
<br>
      <div align='right'  style="width:90%;max-width:900px">
            <a style="color:black;" href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/ts_multistations.cgi" target="_blank">
                  <i class="fab fa-github fa-fw"></i>Page
            </a>
             | 
            <a style="color:black;" href="'''+demoURL+'''" target="_blank">
                  <i class="fa fa-download fa-fw"></i>Raw Data
            </a>
      </div>


<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank">
      <img class="style1" src="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px">
</a>

</div>
<script src="js/site/siteclose.js"></script>
</body>
</html>
''')
