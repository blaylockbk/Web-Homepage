#!/usr/bin/python

# September 05, 2015
# Brian Blaylock
# 
#

# This program will grab WX data from the MesoWest API and 
# Plot a time series

import sys                           # <-- This is necessary for cgi
import matplotlib as mp
mp.use('Agg')
import matplotlib.pyplot as plt

import datetime
import numpy as np
import json
import urllib2


import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.

#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"


import numpy as np
import datetime
import json
import urllib2

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator, MonthLocator, DayLocator, HourLocator
import matplotlib as mpl
import os  



token = '2562b729557f45f5958516081f06c9eb' #Request your own token at http://mesowest.org/api/signup/

variables = 'wind_direction,wind_speed,wind_gust,air_temp,dew_point_temperature,relative_humidity,ozone_concentration'

def wind_spddir_to_uv(wspd,wdir):
    """
    calculated the u and v wind components from wind speed and direction
    Input:
        wspd: wind speed
        wdir: wind direction
    Output:
        u: u wind component
        v: v wind component
    """    
    
    rad = 4.0*np.arctan(1)/180.
    u = -wspd*np.sin(rad*wdir)
    v = -wspd*np.cos(rad*wdir)

    return u,v
    
def get_mesowest_ts(stationID,start_time,end_time):
    """
    Makes a time series query from the MesoWest API
    
    Input:
        stationID  : string of the station ID
        start_time : datetime object of the start time in UTC
        end_time   : datetime object of the end time in UTC
        
    Output:
        a dictionary of the data
    """

    # convert the start and end time to the string format requried by the API
    start = start_time.strftime("%Y%m%d%H%M")
    end = end_time.strftime("%Y%m%d%H%M")
    
    # The API request URL
    URL = 'http://api.mesowest.net/v2/stations/timeseries?stid='+stationID+'&start='+start+'&end='+end+'&vars='+variables+'&obtimezone=utc&token='+token
    
    ##Open URL and read the content
    f = urllib2.urlopen(URL)
    data = f.read()
    
    ##Convert that json string into some python readable format
    data = json.loads(data)
    
    # Need to do some special stuff with the dates
    ##Get date and times
    dates = data["STATION"][0]["OBSERVATIONS"]["date_time"]
    ##Convert to datetime and put into a numpy array
    DATES = np.array([]) #initialize the array to store converted datetimes    
    ##Loop through each date. Convert into datetime format and put into DATES array
    ## NOTE: only works for MDT which is 6 hours behind UTC
    for j in dates:
    	try:
    		converted_time = datetime.datetime.strptime(j,'%Y-%m-%dT%H:%M:%SZ')
    		DATES = np.append(DATES,converted_time)
    		#print 'Times are in UTC'
    	except:
    		converted_time = datetime.datetime.strptime(j,'%Y-%m-%dT%H:%M:%S-0600')
    		DATES = np.append(DATES,converted_time)
    		#print 'Times are in Local Time'    
    
    stn_name = str(data['STATION'][0]['NAME'])
    stn_id   = str(data['STATION'][0]['STID'])
    
    try:
        temp     = np.array(data['STATION'][0]["OBSERVATIONS"]["air_temp_set_1"],dtype=float) 
    except:
        temp = np.ones(len(DATES))*np.nan
    try:
        rh       = np.array(data['STATION'][0]["OBSERVATIONS"]["relative_humidity_set_1"],dtype=float)
    except:
        rh = np.ones(len(DATES))*np.nan
    try:
        wd       = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_direction_set_1"],dtype=float)
    except:
        wd = np.ones(len(DATES))*np.nan
    try:
        ws	   = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_speed_set_1"],dtype=float)
    except:
        ws = np.ones(len(DATES))*np.nan
    try:
        wg	   = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_gust_set_1"],dtype=float)
    except:
        wg = np.ones(len(DATES))*np.nan
    try:
        if (station == 'FWP') or (station =='LMS') or (station =='GSLM'):
            o3    = np.array(data['STATION'][0]["OBSERVATIONS"]["ozone_concentration_set_2"],dtype=float)
        else:
            o3    = np.array(data['STATION'][0]["OBSERVATIONS"]["ozone_concentration_set_1"],dtype=float)
    except:
        o3 = np.ones(len(DATES))*np.nan
    
       
    
    
    data_dict = {
                'station name':stn_name,
                'station id':stn_id,
                'datetimes':DATES,                
                'temperature':temp,
                'relative humidity':rh,
                'wind direction':wd,
                'wind speed':ws,
                'wind gust':wg,
                'ozone':o3
                }
                
    return data_dict

    
station = 'WBB'
start_time = datetime.datetime(2016,2,18,15)
end_time = datetime.datetime(2016,2,18,21)

a = get_mesowest_ts(station,start_time,end_time)


# Make a quick temperature plot
temp = a['temperature']
RH = a['relative humidity']
dates = a['datetimes']
o3 = a['ozone']
wd = a['wind direction']
ws = a['wind speed']
wg = a['wind gust'] 

# Convert wind to U and V components
u,v = wind_spddir_to_uv(ws,wd)

#convert dates from UTC to mountain time (-6 hours)
#dates = dates - datetime.timedelta(hours=6)



tick_font = 12
label_font = 15
lw = 4

width=12
height=6


mpl.rcParams['xtick.labelsize'] = tick_font
mpl.rcParams['ytick.labelsize'] = tick_font

fig = plt.figure(figsize=(width,height))
ax = fig.add_subplot(111)
plt.title(station+' '+a['station name'],fontsize=label_font)
ax.plot(dates, temp, 'r', label = 'Temperature', lw=lw)  



plt.savefig(sys.stdout, dpi=100, bbox_inches='tight')	# Plot standard output.