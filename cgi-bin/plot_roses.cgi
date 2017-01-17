#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# June 26, 2015
# Brian Blaylock
# Updates: 
#		August 20, 2015: added ability to filter based on a threshold
#
#

# This program will grab ozone and wind data from the MesoWest API and 
# Plot a wind rose

import sys
import math as m
import matplotlib as mp
mp.use('Agg')
import matplotlib.pyplot as plt

import time
from datetime import datetime, timedelta
import numpy as np
import json
import urllib2

from numpy import arange
from numpy.random import random
import matplotlib.cm as cm
from windrose import WindroseAxes
import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
from BB_MesoWest.MesoWest_timeseries import get_mesowest_ts
from BB_wx_calcs.wind import wind_spddir_to_uv


import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.

#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

form = cgi.FieldStorage()	# CGI function takes in web arguments

stn  = form['stn'].value
rose_type = form['rose_type'].value
start = form['start'].value
end = form['end'].value
tz = form['tz'].value
HI = form['HI'].value
threshold = form['threshold'].value
plot_max = form['plot_max'].value

DATE_START = datetime.strptime(start, '%Y-%m-%d %H:%M')
DATE_END = datetime.strptime(end, '%Y-%m-%d %H:%M')

# Make MesoWest query
variable = 'wind_direction,wind_speed,ozone_concentration,PM_25_concentration'
a = get_mesowest_ts(stn, DATE_START, DATE_END, variables=variable, verbose=True)

## Sidebar Text
all_text = '' \
+ 'Station      : '+ stn \
+ '\nRose Type    : '+ rose_type \
+ '\nStart        : ' + start \
+ '\nEnd          : ' + end \
+ '\nTime Zone    : UTC-' + tz +' h' \
+ '\nHour Interval: ' + HI \
+ '\nThreshold    : ' + threshold \
+ '\nPlot Max     : ' + plot_max \
+ '\nTotal Obs    : *coming soon*'

"""
Filter the data
"""
# Filter by threshold (wind speed, ozone concentration, etc.)
if rose_type == 'wind' and int(threshold) != 0:
	locs = np.argwhere(a['wind_speed'] >= int(threshold))
	for k in a.keys():
		try:
			a[k]=a[k][locs]
		except:
			# probably isn't an interable array. Might be lat/lon, elevation, etc.
			pass


##-----------------------------------------------------------------------------
#A quick way to create new windrose axes...
def new_axes():
	fig = plt.figure(figsize=(6,8), dpi=80, facecolor='w', edgecolor='w')
	rect = [0.1, 0.1, 0.8, 0.8]
	ax = WindroseAxes(fig, rect, axisbg='w')
	fig.add_axes(ax)
	return ax

#...and adjust the legend box
def set_legend(ax):
	l = ax.legend()
	plt.setp(l.get_texts())
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':15})
##-----------------------------------------------------------------------------

"""
Finally, we are ready to create the Rose Plots :)
"""

if rose_type =="wind":
	ws = a['wind_speed']
	wd = a['wind_direction']

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.bar(wd, ws, nsector = 16, normed=True, \
				   opening=.95, edgecolor='w')

	plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.6),prop={'size':15})

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	
	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text,fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

elif rose_type =="wind_clock":

	# Make array of hours and convert it to a "degree" for
    # The polar plot (multiply the hour by 15)
	hour = [i.hour*15 for i in a['DATETIME']]

	ws = a['wind_speed']
	wd = hour

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.contourf(wd, ws, nsector = 24, \
    			    normed=True, \
			   edgecolor='none', \
			   )

	plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.6),prop={'size':15})

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	ax.set_xticklabels(['06:00','03:00','00:00','21:00', '18:00','15:00','12:00','09:00'], fontsize = 15)

	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text,fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

elif rose_type == "ozone":
	ws = a['ozone_concentration']
	wd = a['wind_direction']

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.bar(wd, ws, nsector = 16, \
				bins = [0,60,75,95,115], normed=True, \
				opening=.95, edgecolor='w', \
				colors = ('green','yellow','orange', 'red', 'purple'))

	plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.6),prop={'size':15})

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	
	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text,fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

elif rose_type =="ozone_clock":

	# Make array of hours and convert it to a "degree" for
    # The polar plot (multiply the hour by 15)
	hour = [i.hour*15 for i in a['DATETIME']]

	ws = a['ozone_concentration']
	wd = hour

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.contourf(wd, ws, nsector = 24, \
    			    normed=True, \
			   edgecolor='none', \
			   bins = [0,60,75,95,115], \
				colors = ('green','yellow','orange', 'red', 'purple')
			   )

	plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.6),prop={'size':15})

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	ax.set_xticklabels(['06:00','03:00','00:00','21:00', '18:00','15:00','12:00','09:00'], fontsize = 15)

	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text,fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.
