#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# January 1, 2017                                 It's cold outside


"""
This script plots multiple stations on one plot
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#style_path = '/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2/BB_mplstyle/'
#plt.style.use([style_path+'publications.mplstyle',
#               style_path+'width_100.mplstyle',
#               style_path+'dpi_web.mplstyle'])

## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [16,9]
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['axes.labelsize'] = 17
mpl.rcParams['axes.titlesize'] =20
mpl.rcParams['grid.linewidth'] = .25

mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.loc'] = 'best'

mpl.rcParams['savefig.bbox'] = 'tight'
#mpl.rcParams['savefig.dpi'] = 1000     # For publication purposes

from matplotlib.dates import DateFormatter, HourLocator
from datetime import datetime, timedelta
from collections import OrderedDict

import numpy as np

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
from BB_MesoWest.MesoWest_timeseries import get_mesowest_ts
from BB_wx_calcs.wind import wind_spddir_to_uv

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

#print sys.modules.keys()
#print 'matplitlib version', mpl.__version__,'<br><br>'

form = cgi.FieldStorage()	# CGI function takes in web arguments

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
      units = 'metric'
      variable = 'air_temp'

#print stn1, stn2, stn3, stn4, start, end, units

DATE_START = datetime.strptime(start, '%Y-%m-%d %H:%M')
DATE_END = datetime.strptime(end, '%Y-%m-%d %H:%M')

save_date = DATE_START.strftime('%Y%m%d')+'-'+DATE_END.strftime('%Y%m%d')

stations = []
if stn1 != '':
    stations.append(stn1)
if stn2 != '':
    stations.append(stn2)
if stn3 != '':
    stations.append(stn3)
if stn4 != '':
    # allow a hack in the last field to allow more than one station input
    # if station names are separated by a comma.
    stns = stn4.split(',')
    for s in stns:
        stations.append(s)

# Preserve the requested order of the stations
data = OrderedDict()

# Get the data from MesoWest
for s in stations:
    a = get_mesowest_ts(s, DATE_START, DATE_END, variables=variable, verbose=False)
    if a != 'ERROR':
        data[s] = a
        
    #debug MesoWest API
    # print a['URL']
    
    # Replace 999 values in air temperature
    #if variable == 'air_temp':
    #    a['air_temp'][a['air_temp']==999] = np.nan
    
## Create the figure

fig, ax1 = plt.subplots(1, 1, figsize=[16,9])
count = 0
# order of the colors plotted (more than 4 available, if you now the stn4 input hack)
color = ['b', 'g', 'r', 'darkorange', 'k', 'palevioletred', 'paleturquoise', 'palegreen', 'orchid', 'steelblue', 'crimson', 'darkcyan', 'sandybrown', 'darkgrey']*2
for s in data.keys():
    try:
        if units == 'english' and variable == 'air_temp':
            ax1.plot(data[s]['DATETIME'], data[s][variable]*9/5.+32,
                     label=s.upper(),
                     linewidth=2.5,
                     color=color[count])
            plt.title('MesoWest Air Temperature')
            plt.ylabel('Temperature (F)')

        elif variable == 'air_temp':
            ax1.plot(data[s]['DATETIME'], data[s][variable],
                     label=s.upper(),
                     linewidth=2.5,
                     color=color[count])
            plt.title('MesoWest Air Temperature')
            plt.ylabel('Temperature (C)')

        elif variable == 'relative_humidity':
            ax1.plot(data[s]['DATETIME'], data[s][variable],
                     label=s.upper(),
                     linewidth=2.5,
                     color=color[count])
            ax1.set_ylim([0, 100])
            plt.title('MesoWest Relative Humidity')
            plt.ylabel('Relative Humidity (%)')

        elif variable == 'wind_direction':
            ax1.scatter(data[s]['DATETIME'], data[s][variable],
                        label=s.upper(),
                        color=color[count]
                       )
            plt.ylim([0,360])
            plt.yticks(range(0,361,45), ['N','NE','E','SE','S','SW','W','NW','N',])
            plt.title('MesoWest Wind Direction')
            plt.ylabel('Wind Direction')

        elif units == 'english' and variable == 'wind_speed':
            ax1.plot(data[s]['DATETIME'], data[s][variable]*2.2369,
                     label=s.upper(),
                     linewidth=2.5,
                     color=color[count])
            plt.title('MesoWest Wind Speed')
            plt.ylabel('Wind Speed (MPH)') 
        
        elif variable == 'wind_speed':
            ax1.plot(data[s]['DATETIME'], data[s][variable],
                     label=s.upper(),
                     linewidth=2.5,
                     color=color[count])
            plt.title('MesoWest Wind Speed')
            plt.ylabel('Wind Speed (ms$\mathregular{^{-1}}$)')

        elif variable == 'wind_direction,wind_speed':
            # Make a wind barb.
            y = np.ones_like(data[s]['DATETIME'])*(4-count)
            u, v = wind_spddir_to_uv(data[s]['wind_speed'], data[s]['wind_direction'])

            # plt.barbs can not take a datetime, so find the date indexes:
            idx = mpl.dates.date2num(data[s]['DATETIME'])

            ax1.barbs(idx, y, u, v,
                      label=s.upper(),
                      color=color[count],
                      length=9,
                      barb_increments=dict(half=2.5, full=5, flag=25))

            plt.title('MesoWest Wind Speed')
            plt.ylabel('Half=2.5, Full=5, Flag=25 (ms$\mathregular{^{-1}}$)')    
            plt.yticks([0,1,2,3], ['','','',''])
            plt.ylim([4-count-.5,4.75])
        else:
            ax1.plot(data[s]['DATETIME'], data[s][variable],
                     label=s.upper(),
                     linewidth=2.5,
                     color=color[count])
            plt.title('MesoWest '+variable)
            plt.ylabel(variable)
    except:
        #error plotting stations
        pass
    
    count+=1

plt.grid()

if variable == 'wind_direction,wind_speed':
    plt.legend(ncol=4,loc='upper center')
else:
    plt.legend()

plt.xlabel('Date/Time (UTC)')
plt.xlim([DATE_START,DATE_END])

if (DATE_END-DATE_START).days == 0:
    ax1.xaxis.set_major_locator(HourLocator(byhour=[0,3,6,9,12,15,18,21]))
    dateFmt = DateFormatter('%b %d\n%H:%M')
    ax1.xaxis.set_major_formatter(dateFmt)
elif (DATE_END-DATE_START).days < 3:
    ax1.xaxis.set_major_locator(HourLocator(byhour=[0,6,12,18]))
    dateFmt = DateFormatter('%b %d\n%H:%M')
    ax1.xaxis.set_major_formatter(dateFmt)
elif (DATE_END-DATE_START).days < 6:
    ax1.xaxis.set_major_locator(HourLocator(byhour=[0,12]))
    dateFmt = DateFormatter('%b %d\n%H:%M')
    ax1.xaxis.set_major_formatter(dateFmt)
else:
    dateFmt = DateFormatter('%b %d\n%Y')
    ax1.xaxis.set_major_formatter(dateFmt)

plt.savefig(sys.stdout)	# Plot standard output.
