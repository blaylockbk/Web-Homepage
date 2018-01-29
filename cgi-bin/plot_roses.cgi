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
units = form['units'].value
threshold = form['threshold'].value
plot_max = form['plot_max'].value

DATE_START = datetime.strptime(start, '%Y-%m-%d %H:%M')
DATE_END = datetime.strptime(end, '%Y-%m-%d %H:%M')

# Make MesoWest query
if 'wind' in rose_type:
    variable = 'wind_direction,wind_speed'
elif 'ozone' in rose_type:
    variable = 'wind_direction,ozone_concentration'
elif 'pm' in rose_type:
    variable = 'wind_direction,PM_25_concentration'
a = get_mesowest_ts(stn, DATE_START, DATE_END, variables=variable, verbose=True)

# Adjust Datetime to requested Time Zone if not UTC
if tz != '0':
	minus_this = int(tz) #strip off the negative
	a['DATETIME'] = np.array([i-timedelta(hours=minus_this) for i in a['DATETIME']])

if rose_type=='wind' or rose_type=='wind_clock':
	if units == 'metric':
		unit = 'm/s'
	elif units == 'english':
		unit = 'MPH'
elif rose_type=='ozone' or rose_type=='ozone_clock':
	unit = 'ppb'
elif rose_type=='pm_25' or rose_type=='pm_clock':
	unit = 'ug/m3'

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
+ '\nUnits        : ' + unit \
+ '\nTotal Obs    : '

"""
Filter the data
"""
# Filter by hour interval (HI)
# get hours from each datetime
all_hours = np.array([i.hour for i in a['DATETIME']])

if HI != 'All Day':
	start_hour = int(HI[0:2])
	end_hour = int(HI[-2:])
	# Now get indexes between start and end hour
	HI_index = np.logical_and(all_hours<=end_hour,all_hours>=start_hour)
	if start_hour > end_hour:
		HI_index = np.logical_or(all_hours<=end_hour,all_hours>=start_hour)
	# reasign the variables in a dictionary based on this indexes
	for k in a.keys():
		if np.size(a[k]) == np.size(HI_index):
			a[k] = a[k][HI_index]

# Filter by threshold (wind speed, ozone concentration, etc.)
# Get indexes where ozone
threshold_float = float(threshold)
if threshold_float != 0:
	if rose_type=='wind' or rose_type=='wind_clock':
		threshold_index = a['wind_speed'] >= threshold_float
		a['wind_speed'] = a['wind_speed'][threshold_index]
		a['wind_direction'] = a['wind_direction'][threshold_index]
		a['DATETIME'] = a['DATETIME'][threshold_index]
	elif rose_type=='ozone' or rose_type=='ozone_clock':
		threshold_index = a['ozone_concentration'] >= threshold_float
		a['ozone_concentration'] = a['ozone_concentration'][threshold_index]
		a['wind_direction'] = a['wind_direction'][threshold_index]
		a['DATETIME'] = a['DATETIME'][threshold_index]
	elif rose_type=='pm_25' or rose_type=='pm_clock':
		threshold_index = a['PM_25_concentration'] >= threshold_float
		a['PM_25_concentration'] = a['PM_25_concentration'][threshold_index]
		a['wind_direction'] = a['wind_direction'][threshold_index]
		a['DATETIME'] = a['DATETIME'][threshold_index]
	
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
	leg = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':15})
	leg.draw_frame(False)
##-----------------------------------------------------------------------------

"""
Finally, we are ready to create the Rose Plots :)
"""

if rose_type =="wind":
	ws = a['wind_speed']
	wd = a['wind_direction']

	if units == 'english':
		# Convert m/s to mph
		ws = ws*2.2369
		bins = [0,4,8,12,16,20]
	else:
		bins = [0,2,4,6,8,10]

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.bar(wd, ws, nsector = 16, normed=True, \
				   bins = bins,
				   opening=.95, edgecolor='w')

	leg = plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.5),prop={'size':15})
	leg.draw_frame(False)

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	
	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text+str(len(ws)),fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
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

	leg = plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.5),prop={'size':15})
	leg.draw_frame(False)

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

	plt.figtext(1,.8,all_text+str(len(ws)),fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
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

	leg = plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.5),prop={'size':15})
	leg.draw_frame(False)

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	
	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text+str(len(ws)),fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
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

	leg = plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.5),prop={'size':15})
	leg.draw_frame(False)

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

	plt.figtext(1,.8,all_text+str(len(ws)),fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

elif rose_type == "pm_25":
	ws = a['PM_25_concentration']
	wd = a['wind_direction']

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.bar(wd, ws, nsector = 16, \
				bins=[0,12.1,35.,55.4,150.4], normed=True, \
				opening=.95, edgecolor='w', \
				colors = ('green','yellow','orange', 'red', 'purple'))

	leg = plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.5),prop={'size':15})
	leg.draw_frame(False)

	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	
	if plot_max=='auto':
		table = ax._info['table']
		wd_freq = np.sum(table, axis=0)
		ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5
	else:
		ax.set_rmax(plot_max)

	plt.figtext(1,.8,all_text+str(len(ws)),fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

elif rose_type =="pm_clock":

	# Make array of hours and convert it to a "degree" for
    # The polar plot (multiply the hour by 15)
	hour = [i.hour*15 for i in a['DATETIME']]

	ws = a['PM_25_concentration']
	wd = hour

	fig, (ax1) = plt.subplots(1,1)
	ax = new_axes()
	ax.contourf(wd, ws, nsector = 24, \
    			    normed=True, \
			   edgecolor='none', \
			   bins=[0,12.1,35.,55.4,150.4], \
				colors = ('green','yellow','orange', 'red', 'purple')
			   )

	leg = plt.legend(loc='bottom left', bbox_to_anchor=(1.6, 0.5),prop={'size':15})
	leg.draw_frame(False)

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

	plt.figtext(1,.8,all_text+str(len(ws)),fontname='monospace',va='top',backgroundcolor='white',fontsize=12)
	
	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.
