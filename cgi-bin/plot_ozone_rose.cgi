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

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.

print "Content-Type: text/html\n"
#print "Content-Type: image/png\n"

form = cgi.FieldStorage()	# CGI function takes in web arguments

id  = form['id'].value

rose_type = form['rose_type'].value

time_option = form['time_option'].value

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

variables = 'wind_direction,wind_speed'

URL = 'http://api.mesowest.net/v2/stations/timeseries?stid='+station+'&start='+start_time+'&end='+end_time+'&vars='+variables+'&obtimezone='+time_option+'&token='+token

##Open URL and read the content
f = urllib2.urlopen(URL)
data = f.read()

##Convert that json string into some python readable format
data = json.loads(data)

##Get station name and id
stn_name = data['STATION'][0]['NAME']
stn_id = data['STATION'][0]['STID']

wind_dir_raw = data['STATION'][0]["OBSERVATIONS"]["wind_direction_set_1"]
wind_spd_raw = data['STATION'][0]["OBSERVATIONS"]["wind_speed_set_1"]
	
##Convert raw data to a numpy array
wind_dir = np.array(wind_dir_raw,dtype=float)
wind_spd = np.array(wind_spd_raw,dtype=float)

##Get date and times
dates = data["STATION"][0]["OBSERVATIONS"]["date_time"]
##Convert to datetime and put into a numpy array
DATES = np.array([]) #initialize the array to store converted datetimes

##Loop through each date. Convert into datetime format and put into DATES array
## NOTE: only works for MDT which is 6 hours behind UTC
for j in dates:
	try:
		converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%SZ')
		DATES = np.append(DATES,converted_time)
		#print 'Times are in UTC'
	except:
		converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%S-0600')
		DATES = np.append(DATES,converted_time)
		#print 'Times are in Local Time'

# Create DateString for plot title
s_datestring = datetime.strftime(DATES[0],"%b %d, %Y %H:%M")
e_datestring = datetime.strftime(DATES[-1],"%b %d, %Y %H:%M")


##-----------------------------------------------------



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


	
if rose_type =="wspd":
	ws = wind_spd
	wd = wind_dir

	plt.figure(1)	
	ax = new_axes()
	ax.bar(wd, ws, nsector = 16, normed=True, \
				   opening=.95, edgecolor='w')

	plt.title("Wind Rose - "+stn_name+"\n"+s_datestring+" - "+e_datestring+" "+time_option, fontsize=15)
	#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':10})


	plt.grid(True)
	plt.yticks(np.arange(0,105,5))
	ax.set_yticklabels(['','','10%','', '20%','','30%','','40%','','50%'], fontsize = 15)
	
	table = ax._info['table']
	wd_freq = np.sum(table, axis=0)
	ax.set_rmax(np.floor(max(wd_freq)/5)*5+5) #set rmax to upper number divisible by 5


	#fig = plt.gcf()
	#fig.set_size_inches(5, 13)


	plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

if rose_type =="spd_clock":
    #for an ozone clock, it shows the ozone concentration
    #at each time of the day. Instead of a wind direction
    #as the "rose" direction, I convert the time of day into 
    #a polar coordinate.
    
    # Make array of hours and convert it to a "degree" for
    # The polar plot (multiply the hour by 15)
    hour = []
    for i in DATES:
        hour.append(i.hour*15)

    ws = wind_spd
    wd = hour

    plt.figure(1)	
    ax = new_axes()
    ax.contourf(wd, ws, nsector = 24, \
    			    normed=True, \
			   edgecolor='none', \
			   )

    plt.title("Wind Clock - "+stn_name+"\n"+s_datestring+" - "+e_datestring+" "+time_option, fontsize=15)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':10})
    plt.grid(True)
    plt.yticks(np.arange(0,105,5))
    ax.set_yticklabels(['','5%','10%','15%', '20%','25%','30%','','40%'], fontsize = 15)
    ax.set_xticklabels(['06:00','03:00','00:00','21:00', '18:00','15:00','12:00','09:00'], fontsize = 15)
    ax.set_rmax(4.8)
    #plt.legend()

    #fig = plt.gcf()
    #fig.set_size_inches(5, 13)


    plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.

