#!/usr/bin/python

# September 05, 2015
# Brian Blaylock
# 
#

# This program will grab WX data from the MesoWest API and 
# Plot a time series

import sys
sys.path.append("/uufs/chpc.utah.edu/common/home/u0553130/pyBKB")
import math as m
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
import numpy as np
import json
import urllib2
from matplotlib.dates import DateFormatter, YearLocator, MonthLocator, DayLocator, HourLocator

from numpy import arange
from numpy.random import random
import matplotlib.cm as cm
from windrose import WindroseAxes
from BB_MesoWest import mesowest_stations_radius as MW


import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


label_font  = 10    
tick_font   = 8 
legend_font = 10

width=7.48  # refer to above table
height=width/4   # adjust as needed, but bbox="tight" should take care of most of this


## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['xtick.labelsize'] = tick_font
mpl.rcParams['ytick.labelsize'] = tick_font
mpl.rcParams['axes.labelsize'] = label_font
mpl.rcParams['legend.fontsize'] = legend_font

mpl.rcParams['figure.figsize'] = [width,height] 

mpl.rcParams['grid.linewidth'] = .25

#mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 1000


#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

form = cgi.FieldStorage()	# CGI function takes in web arguments

id  = form['id'].value

time_option = form['time_option'].value

units = form['units'].value

plot_type = form['plot_type'].value


syr = form['syr'].value
smo = form['smo'].value
sdy = form['sdy'].value
shr = form['shr'].value

eyr = form['eyr'].value
emo = form['emo'].value
edy = form['edy'].value
ehr = form['ehr'].value


beg_date = datetime(int(syr),int(smo),int(sdy),int(shr),00,00)
end_date = datetime(int(eyr),int(emo),int(edy),int(ehr),00,00)

#Since the API thinks in terms of UTC time, this adjust the local times to
# the times we want to retrieve.
if time_option == 'local':
    beg_date = beg_date+timedelta(hours=6)
    end_date = end_date+timedelta(hours=6)

#if time_option=="local":
#    beg_date = beg_date + timedelta(hours=6)


################
## API QUERY ###
################
# Import data from MesoWest API
## API Query
#---------------------------------------------------------------------------
token = '2562b729557f45f5958516081f06c9eb' #This token belongs to Brian Blaylock

station = id


## dateformat YYYYMMDDHHMM
start_time = datetime.strftime(beg_date, "%Y%m%d%H%M")
end_time = datetime.strftime(end_date, "%Y%m%d%H%M")

variables = 'wind_direction,wind_speed,wind_gust,air_temp,dew_point_temperature,relative_humidity'

URL = 'http://api.mesowest.net/v2/stations/timeseries?stid='+station+'&start='+start_time+'&end='+end_time+'&vars='+variables+'&obtimezone='+time_option+'&token='+token

##Open URL and read the content
f = urllib2.urlopen(URL)
data = f.read()

##Convert that json string into some python readable format
data = json.loads(data)

##Get station name and id
stn_name = data['STATION'][0]['NAME']
stn_id = data['STATION'][0]['STID']

var1     = np.array(data['STATION'][0]["OBSERVATIONS"]["air_temp_set_1"])
var2     = data['STATION'][0]["OBSERVATIONS"]["relative_humidity_set_1"]
wd		 = data['STATION'][0]["OBSERVATIONS"]["wind_direction_set_1"]
ws		 = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_speed_set_1"])
wg		 = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_gust_set_1"])
if units =="english":
	ws   = 2.23693629205*ws
	wg   = 2.23693629205*wg
	var1     = var1*9/5+32
    
##Get date and times
dates = data["STATION"][0]["OBSERVATIONS"]["date_time"]
##Convert to datetime and put into a numpy array
DATES = np.array([]) #initialize the array to store converted datetimes

##Loop through each date. Convert into datetime format and put into DATES array
for j in dates:
	try:
		converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%SZ')
		DATES = np.append(DATES,converted_time)
		#print 'Times are in UTC'
	except:
         try:
             converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%S-0600')
             DATES = np.append(DATES,converted_time)         
         except:
             converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%S-0700')
             DATES = np.append(DATES,converted_time)

# Create DateString for plot title
s_datestring = datetime.strftime(DATES[0],"%b %d, %Y %H:%M")
e_datestring = datetime.strftime(DATES[-1],"%b %d, %Y %H:%M")
##-----------------------------------------------------


plt.figure(figsize=(width,height))	

if plot_type=="temp_RH":

    fig = plt.figure(figsize=(16,4))
    ax = fig.add_subplot(111)
    plt.title(stn_name+" Temperature and Relative Humidity\n"+s_datestring +"-"+ e_datestring+" "+time_option)
    ax.plot(DATES, var1, 'r', label = 'Temperature', linewidth="4")
    ax2 = ax.twinx()
    ax2.plot(DATES, var2, 'g', label = 'Relative Humidity', linewidth="4")
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid()
    ax.set_xlabel("")
    ax.set_ylabel(r"Temperature ($^\circ$C)")
    if units == "english":
        ax.set_ylabel(r"Temperature ($^\circ$F)")
    ax2.set_ylabel("Relative Humidity (%)")

    if (DATES[-1]-DATES[0]).days <10:
        ##Format Ticks##
        ##----------------------------------
        # Find months
        months = MonthLocator()
        # Find days
        days = DayLocator()
        # Find each 0 and 12 hours
        hours = HourLocator(byhour=[0,6,12,18])
        # Find all hours
        hours_each = HourLocator()
        # Tick label format style
        dateFmt = DateFormatter('%b %d\n%H:%M')
        # Set the x-axis major tick marks
        ax.xaxis.set_major_locator(hours)
        # Set the x-axis labels
        ax.xaxis.set_major_formatter(dateFmt)
        # For additional, unlabeled ticks, set x-axis minor axis
        ax.xaxis.set_minor_locator(hours_each)
    

    ##output image
    ##--------------------------------------
    plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

if plot_type == "wind":
        
    fig = plt.figure(figsize=(16,4))
    ax = fig.add_subplot(111)
    plt.title(stn_name+" Winds\n"+s_datestring +"-"+ e_datestring+" "+time_option)
    ax.plot(DATES, ws, label = 'Wind Speed', linewidth="2")
    ax.plot(DATES, wg, '--', label = 'Wind Gust', linewidth="2")
    ax2 = ax.twinx()
    ax2.plot(DATES, wd, 'og', label = 'Wind Direction')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid()
    ax.set_xlabel("")
    ax2.set_ylim([0,360])
    ax2.set_yticks([0,45,90,135,180,225,270,315,360])
    ax2.set_yticklabels(['N','NE','E','SE','S','SW','W','NW','N'])
    ax.set_ylabel("Wind Speed (m/s)")
    if units == "english":
        ax.set_ylabel("Wind Speed (mph)")
    ax2.set_ylabel("Wind Direction")

    if (DATES[-1]-DATES[0]).days <10:
        ##Format Ticks##
        ##----------------------------------
        # Find months
        months = MonthLocator()
        # Find days
        days = DayLocator()
        # Find each 0 and 12 hours
        hours = HourLocator(byhour=[0,6,12,18])
        # Find all hours
        hours_each = HourLocator()
        # Tick label format style
        dateFmt = DateFormatter('%b %d\n%H:%M')
        # Set the x-axis major tick marks
        ax.xaxis.set_major_locator(hours)
        # Set the x-axis labels
        ax.xaxis.set_major_formatter(dateFmt)
        # For additional, unlabeled ticks, set x-axis minor axis
        ax.xaxis.set_minor_locator(hours_each)

    ##output image
    ##--------------------------------------
    plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.