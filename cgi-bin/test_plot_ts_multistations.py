#!/usr/bin/env python

# Brian Blaylock
# September 1, 2017                                 It's cold outside


"""
This script plots multiplut stations on one plot
"""

import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
#style_path = '/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2/BB_mplstyle/'
#plt.style.use([style_path+'publications.mplstyle',
#               style_path+'width_100.mplstyle',
#               style_path+'dpi_web.mplstyle'])

## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [16,9]
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['axes.labelsize'] = 15
mpl.rcParams['axes.titlesize'] =20
mpl.rcParams['grid.linewidth'] = .25

mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['legend.loc'] = 'best'


#mpl.rcParams['savefig.bbox'] = 'tight'
#mpl.rcParams['savefig.dpi'] = 1000

from matplotlib.dates import DateFormatter, HourLocator
from datetime import datetime, timedelta
from collections import OrderedDict

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
from BB_MesoWest.MesoWest_timeseries import get_mesowest_ts

#import cgi
#import cgitb
#cgitb.enable()	# Spits out error to browser in coherent format.


#print "Content-Type: text/html\n"
#print "Content-Type: image/png\n"

#print 'hi'
#print sys.modules.keys()
#print 'matplitlib version', mpl.__version__,'<br><br>'

#form = cgi.FieldStorage()	# CGI function takes in web arguments

current = datetime.now()
onedayago = datetime.now()-timedelta(days=1)

stn1 = 'KLGU'
stn2 = ''
stn3 = 'KYWF1'
stn4 = ''
start = '2017-01-01 00:00'
end = '2017-01-09 21:01'
units = 'F'
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
    stations.append(stn4)    

data = OrderedDict()

# Get the data from MesoWest
for s in stations:
    data[s] = get_mesowest_ts(s, DATE_START, DATE_END, variables=variable)

"""
Plot
"""
#fig, ax1 = plt.subplots(1, 1)
fig = plt.figure(figsize=[16,9])
count = 0
color = ['b','g','r','darkorange']
for s in data.keys():
    try:
        if units == 'F' and variable=='air_temp':
            plt.plot(data[s]['DATETIME'], data[s][variable]*9/5.+32,
                    label=s.upper(),
                    linewidth=2.5,
                    color=color[count])
        elif variable=='wind_direction':
            plt.scatter(data[s]['DATETIME'], data[s][variable],
                    label=s.upper(),
                    color=color[count]
                    )
            plt.ylim([0,360])
            plt.yticks(range(0,361,45))
        else:
            plt.plot(data[s]['DATETIME'], data[s][variable],
                    label=s.upper(),
                    linewidth=2.5,
                    color=color[count])
    except:
        #error plotting stations
        pass
    
    count+=1

plt.grid()

plt.legend()

plt.xlabel('Date/Time (UTC)')

if units == 'F' and variable=='air_temp':
    plt.title('MesoWest Air Temperature')
    plt.ylabel('Temperature (F)')
elif variable=='air_temp':
    plt.title('MesoWest Air Temperature')
    plt.ylabel('Temperature (C)')
elif variable=='relative_humidity':
    plt.title('MesoWest Relative Humidity')
    plt.ylabel('Relative Humidity (%)')
elif variable=='wind_speed':
    plt.title('MesoWest Wind Speed')
    plt.ylabel('Wind Speed (ms$\mathregular{^{-1}}$)')
elif variable=='wind_direction':
    plt.title('MesoWest Wind Direction')
    plt.ylabel('Wind Direction (degrees)')

plt.xlim([DATE_START,DATE_END])

#ax1.xaxis.set_major_locator(HourLocator(byhour=[0,12]))
dateFmt = DateFormatter('%b %d\n%H:%M')

#ax1.xaxis.set_major_formatter(dateFmt)


ax = plt.gcf().axes[0]
ax.xaxis.set_major_formatter(dateFmt)

plt.show()
#plt.savefig(sys.stdout, bbox_inches='tight')	# Plot standard output.

