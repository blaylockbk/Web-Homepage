#!/usr/local/bin/python

import numpy as np
import cgi, cgitb
cgitb.enable()
import gzip, os, sys, datetime, re, time, urllib2, collections, calendar, json
from operator import itemgetter
import tables as pytbls

## Set timezone first

os.environ['TZ'] = 'Etc/Greenwich'
time.tzset()

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()

try:
	stidin1 = form["stid"].value
except:
	stidin1 = 'TRX01'
	
## Figure out current time and get current year
	
currtime = datetime.datetime.utcnow()
pasttime = currtime-datetime.timedelta(days=1)
curyr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')

try:
	yr = form["yr"].value
	mo = form["mo"].value
	dy = form["dy"].value
	hr = form["hr"].value
	mm = form["mm"].value
except:
	yr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')
	mo = datetime.datetime.strftime(datetime.datetime.utcnow(),'%m')
	dy = datetime.datetime.strftime(datetime.datetime.utcnow(),'%d')
	hr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%H')
	mm = datetime.datetime.strftime(datetime.datetime.utcnow(),'%M')			

## Define a listing of mobile station IDs (remember these are HDF5 files that have different names for each ID)

mobilestidlist = ['TRX01','UUTK1','UUTK2','KSL5','UNERD','UUTK3']
mobilestnname = {
	'TRX01': 'UTA TRAX',
	'UUTK1': 'UofU ATMOS Mobile',
	'UUTK2': 'UofU ATMOS Mobile',
	'UUTK3': 'UofU ATMOS Mobile',
	'UNERD': 'UofU NerdMobile',
	'KSL5': 'KSL Chopper 5'
}

## Define defaults for the home page rendering if not chosen

try:
	minback = int(form["min"].value)
except:
	minback = 60

if(minback > 2880):
	minback = 2880

## Figure out timestamps for HDF5 querying, API querying, and displays

try:
	epochend = int(time.mktime(time.strptime(yr+mo+dy+hr+mm,'%Y%m%d%H%M')))
except:
	epochend = int(time.mktime(time.localtime()))

epochstart = int(epochend-(60.*minback))

## Begin HTML content
	
print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>Ozone Study Time Series Archive</title>
<script src="/gslso3s/js/site/siteopen.js"></script>
</head>
<body>
<script src="/gslso3s/js/site/sitemenu.js"></script>
<br>
<b><font COLOR="#0000DD" SIZE=+3>Great Salt Lake Summer Ozone Study - Download Mobile Data</font></b>
<br><br>
<div style="width:900px">
This page provides access to mobile observations collected as part of the Great Salt Lake Summer 2015 Ozone Study.<br><br>
Data can be downloaded by using the options below to select a desired station and time period and then clicking "Download Data".<br><br>
Data is returned in a comma-delimited text form to the browser, with a few header lines denoting time period requested and column descriptions.  At this time, <u><b>requests and data only in UTC</u></b> are supported, so all data requests and returned data are in UTC.
<br><br>
All variables recorded by a station are returned, and null or missing values are denoted with a "-9999" value.
<br><br>

<form method="GET" action="download_mobile_data.cgi">
	<b>Time Options:</b><span style="padding-left:10px">
	Year:
	<select name="yr">'''
for i in range(2015,int(curyr)+1):
	if yr == ("%04d" % i):
		print '''		<option selected="selected">'''+"%04d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%04d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
	Month:
	<select name="mo">'''
for i in range(1,13):
	if mo == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>	
	<span style="padding-left:5px">
	Day:
	<select name="dy">'''	
for i in range(1,32):
	if dy == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
	Hour:
	<select name="hr">'''	
for i in range(0,24):
	if hr == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
	Minute:
	<select name="mm">'''	
for i in range(0,60):
	if mm == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
	Period:
	<select name="min">'''

minint = [30,60,120,180,360,720,1440,2160,2880]
timeint = ['30 min','1 h','2 h','3 h','6 h','12 h','1 day','1.5 days','2 days']

for i in range(0,len(minint)):
	if str(minback) == str(minint[i]):
		print '''		<option selected="selected" value="'''+str(minint[i])+'''">'''+timeint[i]+'''</option>'''
	else:
		print '''		<option value="'''+str(minint[i])+'''">'''+timeint[i]+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
	<br><br>
	<b>Station Options:</b><span style="padding-left:10px">
	Station ID:'''
	
print'''<select name="stid">'''
for stid in sorted(mobilestidlist):
	if stidin1 == stid:
		print '''		<option selected="selected" value="'''+stid+'''">'''+("%s (%s)" % (mobilestnname[stid],stid))+'''</option>'''
	else:
		print '''		<option value="'''+stid+'''">'''+("%s (%s)" % (mobilestnname[stid],stid))+'''</option>'''
print '''	</select>'''	
# print'''	<input size=10 type="text" value="'''+stidin1+'''" name="stn1"/>'''
print'''<br><br>
<input type="submit" value="Download Data">
</form></div>
<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>
'''

sys.exit()
