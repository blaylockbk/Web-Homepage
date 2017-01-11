#!/usr/local/bin/python

import numpy as np
import cgi, cgitb
cgitb.enable()
import gzip, os, sys, datetime, re, time, urllib2, collections, calendar, json
from operator import itemgetter
import tables as pytbls

# print "Content-Type: text/plain\n"

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()
	
try:
	mytzone = form["tz"].value
except:
	mytzone = 'local'
	
if(mytzone != 'utc'):
	mytzone = 'local'

try:
	mystat = form["stat"].value
except:
	mystat = 'obs'
	
if(mystat != '8hr'):
	mystat = 'obs'
	
## Cheap way of getting timezone offsets

utctzoff = int(time.mktime(time.gmtime())) - int(time.mktime(time.localtime()))
	
## Set timezone first

if(mytzone == 'utc'):
	os.environ['TZ'] = 'Etc/Greenwich'
	time.tzset()
	tzout = ' UTC'
	mwtzlink = 'GMT'
	utctzoff = 0
else:
	tzout = ' Local'
	mwtzlink = 'LOCAL'
	
## Figure out current time and get current year
	
currtime = datetime.datetime.utcnow()
pasttime = currtime-datetime.timedelta(days=1)
curyr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')

## Read and determine what time period we are looking at!

try:
	paston = int(form["past"].value)
except:
	paston = 0
	
if(paston != 1):
	paston = 0

try:
	if(paston == 1):
		yr = form["yr"].value
		mo = form["mo"].value
		dy = form["dy"].value
	else:
		if(mytzone == 'utc'):
			yr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')
			mo = datetime.datetime.strftime(datetime.datetime.utcnow(),'%m')
			dy = datetime.datetime.strftime(datetime.datetime.utcnow(),'%d')
		else:
			yr = datetime.datetime.strftime(datetime.datetime.now(),'%Y')
			mo = datetime.datetime.strftime(datetime.datetime.now(),'%m')
			dy = datetime.datetime.strftime(datetime.datetime.now(),'%d')
except:
	if(mytzone == 'utc'):
		yr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')
		mo = datetime.datetime.strftime(datetime.datetime.utcnow(),'%m')
		dy = datetime.datetime.strftime(datetime.datetime.utcnow(),'%d')
	else:
		yr = datetime.datetime.strftime(datetime.datetime.now(),'%Y')
		mo = datetime.datetime.strftime(datetime.datetime.now(),'%m')
		dy = datetime.datetime.strftime(datetime.datetime.now(),'%d')
		
## Define some default dictionaries for HDF5 files to query, variables, and display methods

filetypelist = ['cr1000','esampler','2b']
varoptionlist = ['OZNE','PM25','TMPC','RELH','VOLT']

varoptions = {'TMPC': 'Temperature',
'RELH': 'Relative Humidity',
'PM25': 'PM2.5 Concentration',
'VOLT': 'Battery Voltage',
'OZNE': 'Ozone Concentration'}

varunits = {'TMPC': 'deg C',
'RELH': '%',
'PM25': 'ug/m<sup>3</sup>',
'VOLT': 'volts',
'OZNE': 'ppbv'}

varapi = {'TMPC': 'air_temp',
'RELH': 'relative_humidity',
'PM25': 'PM_25_concentration',
'VOLT': 'volt',
'OZNE': 'ozone_concentration'}

vartemplist = ['TMPC','TICC','ITMP']
varrhlist = ['RELH','INRH']
varotherlist = ['FLOW']

opacoptionlist = ['On','Off']

tzoptions = {'local': 'Local','utc': 'UTC'}
tzoptionlist = ['local','utc']

statoptions = {'8hr': '8-Hr Average','obs': 'Actual Observations'}
statoptionlist = ['obs','8hr']

## Define defaults for the home page rendering if not chosen

try:
	varchoice1 = form["var1"].value
except:
	varchoice1 = 'OZNE'

if(varchoice1 not in varoptions):
	varchoice1 = 'OZNE'

opacchoice = 'On'

try:
	minback = int(form["min"].value)
except:
	minback = 1440

if(minback > 43200):
	minback = 43200

## Figure out timestamps for HDF5 querying, API querying, and displays

try:
	epochend = int(time.mktime(time.strptime(yr+mo+dy+'0000','%Y%m%d%H%M')))
except:
	epochend = ((int(time.mktime(time.localtime()))/86400)*86400)

if(mystat == '8hr'):
	epochstart = int(epochend-(60.*minback)-(8*3600))
else:
	epochstart = int(epochend-(60.*minback))

currtimestring = time.strftime('%Y-%m-%d',time.localtime(epochend))
pasttimestring = time.strftime('%Y-%m-%d'+tzout,time.localtime(epochstart))
timeday8hr = time.strftime('%Y%m%d',time.localtime(epochend))

apitimeend = time.strftime('%Y%m%d%H%M',time.gmtime(epochend+86400))
apitimestart = time.strftime('%Y%m%d%H%M',time.gmtime(epochstart+86400))
epochstartstat = int(epochend-(60.*minback))+86400

## Define MesoWest V2 API Parsing Function and Defaults

apitoken = 'a94df50babad4344bd7e183c5688c5e6'
apivarlist = varapi[varchoice1]
vardatalistv2 = [str(varapi[varchoice1])+'_set_1']

stidlist = []
plotstn = {}
insitustnname = {}
insitustnlat = {}
insitustnlon = {}
insitustnlon = {}
insitumax = {}
insitumaxepoch = {}
insitumin = {}
insituminepoch = {}
insituavg = {}
insitustd = {}

tablemaxcolor = {}
tablemincolor = {}
tableavgcolor = {}
tablemaxtextcolor = {}
tablemintextcolor = {}
tableavgtextcolor = {}

stnsabv75stdlastday = {}
daysabv75std = {}
stnsabv65stdlastday = {}
daysabv65std = {}

def ParseDataV2Stats(jsondata):
	for station in jsondata['STATION']:
		insitustnname[station['STID']] = station['NAME']
		insitustnlat[station['STID']] = station['LATITUDE']
		insitustnlon[station['STID']] = station['LONGITUDE']
		plotstn[station['STID']] = 0		
		tablemaxcolor[station['STID']] = '#000000'
		tablemaxtextcolor[station['STID']] = '#FFFFFF'
		tablemincolor[station['STID']] = '#000000'
		tablemintextcolor[station['STID']] = '#FFFFFF'
		tableavgcolor[station['STID']] = '#000000'
		tableavgtextcolor[station['STID']] = '#FFFFFF'
		try:
			if(int(form[station['STID']].value) == 1):
				plotstn[station['STID']] = 1
		except:
			skip = 1
		if(station['STID'] == 'QH3' or station['STID'] == 'QHW'):
			vardatalistv2 = [str(varapi[varchoice1])+'_set_2']
		else:
			vardatalistv2 = [str(varapi[varchoice1])+'_set_1']
		try:
			if(int(station['MNET_ID']) < 2000):
				for key in station['OBSERVATIONS']:
					if key in vardatalistv2:
						temptimelist = ''
						templist = ''
						temptimelist_filter1 = ''
						templist_filter1 = ''
						temptimelist_filter2 = ''
						templist_filter2 = ''
						temptimelist = station['OBSERVATIONS']['date_time']					
						templist = station['OBSERVATIONS'][key]
						templist_filter1 = [v for v in templist if v is not None]
						temptimelist_filter1 = [v for v,w in zip(temptimelist,templist) if w is not None]
						templist_filter2 = [v for v in templist_filter1 if v != '']
						temptimelist_filter2 = [v for v,w in zip(temptimelist_filter1,templist_filter1) if w != '']
						temptimelist_filter2 = [int(calendar.timegm(time.strptime(v,'%Y-%m-%dT%H:%M:%SZ'))) for v in temptimelist_filter2]
						if(mystat == '8hr'):
							new8hrtimelist = []
							new8hrdatalist = []
							for k in range(0,len(temptimelist_filter2)):
								if(temptimelist_filter2[k] >= epochstartstat):
									temp8hrtime = [v for v,w in zip(temptimelist_filter2,templist_filter2) if (temptimelist_filter2[k]-v) >= 0 and (temptimelist_filter2[k]-v) < (8*3600)]
									temp8hrdata = [w for v,w in zip(temptimelist_filter2,templist_filter2) if (temptimelist_filter2[k]-v) >= 0 and (temptimelist_filter2[k]-v) < (8*3600)]
									temp8hrtimecheck = temp8hrtime[-1] - temp8hrtime[0]
									if(temp8hrtimecheck > (5*3600)):
										new8hrtimelist.append(temptimelist_filter2[k])
										new8hrdatalist.append(np.mean(temp8hrdata))
										day8hr = time.strftime('%Y%m%d',time.localtime(temptimelist_filter2[k]))
										if(temptimelist_filter2[k] < (epochend+86400)):
											if(np.mean(temp8hrdata) > 75):
												if(day8hr == timeday8hr):
													stnsabv75stdlastday[station['STID']] = 1
												daysabv75std[day8hr] = 1
											if(np.mean(temp8hrdata) > 65):
												if(day8hr == timeday8hr):
													stnsabv65stdlastday[station['STID']] = 1
												daysabv65std[day8hr] = 1												
							temptimelist_filter2 = new8hrtimelist
							templist_filter2 = new8hrdatalist
						temptimelist_filter2 = [time.strftime('%Y-%m-%d %H:%M',time.localtime(v)) for v in temptimelist_filter2]
						# if(station['STID'] == 'MTMET'):
							# print temptimelist_filter2
							# print templist_filter2
						insitumax[station['STID']] = np.max(templist_filter2)
						insitumaxepoch[station['STID']] = temptimelist_filter2[np.argmax(templist_filter2)]
						insitumin[station['STID']] = np.min(templist_filter2)
						insituminepoch[station['STID']] = temptimelist_filter2[np.argmin(templist_filter2)]
						insituavg[station['STID']] = np.mean(templist_filter2)
						insitustd[station['STID']] = np.max(templist_filter2) - np.min(templist_filter2)
						# insitustd[station['STID']] = np.std(templist_filter2)
						for j in range(0,len(colorlist)):
							if(insitumax[station['STID']] >= colorminlist[j]):
								tablemaxcolor[station['STID']] = colorlist[j]
								tablemaxtextcolor[station['STID']] = colortextlist[j]
							if(insitumin[station['STID']] >= colorminlist[j]):
								tablemincolor[station['STID']] = colorlist[j]
								tablemintextcolor[station['STID']] = colortextlist[j]
							if(insituavg[station['STID']] >= colorminlist[j]):
								tableavgcolor[station['STID']] = colorlist[j]
								tableavgtextcolor[station['STID']] = colortextlist[j]
						stidlist.append(station['STID'])
		except:
			skip = 1

## Define color lists for map plotting legends

colorlist = ['#FF0000','#FFFF00','#0000FF','#00FFFF','#00FF00']
colortextlist = ['#FFFFFF','#000000','#FFFFFF','#000000','#000000']
colormaxlist = [1,2,3,4,10]
colorminlist = [0,1,2,3,4]

if(varchoice1 == 'PM25'):
	colorlist = ['#00FFFF','#00CCFF','#0099FF','#00FF00','#009900','#006600','#FFFF00','#FFE600','#FFCD00','#FF7E00','#FF5000','#FF0000','#990000','#CC0033','#FF00FF']
	colortextlist = ['#000000','#000000','#FFFFFF','#000000','#FFFFFF','#FFFFFF','#000000','#000000','#000000','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF']
	colormaxlist = [2,4,6,8,10,12,20,28,35.5,45.5,55.5,85.5,115.5,150.5,  300]
	colorminlist = [0,2,4,6, 8,10,12,20,  28,35.5,45.5,55.5, 85.5,115.5,150.5]

if(varchoice1 == 'VOLT'):
	colorlist = ['#003300','#006600','#009900','#00CC00','#00FF00','#999900','#CCCC00','#FFFF00','#FF6600','#FF0000']
	colortextlist = ['#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000','#000000','#000000','#000000','#000000','#FFFFFF']
	colormaxlist = [5,8,9,10,11,12,13,14,15,100]
	colorminlist = [0,5,8, 9,10,11,12,13,14, 15]

if(varchoice1 == 'OZNE'):
	colorlist = ['#00FFFF','#00CCFF','#0099FF','#00FF00','#009900','#006600','#FFFF00','#FFE600','#FFCD00','#FF7E00','#FF5000','#FF0000','#990000','#CC0033','#FF00FF']
	colortextlist = ['#000000','#000000','#FFFFFF','#000000','#FFFFFF','#FFFFFF','#000000','#000000','#000000','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF']
	colormaxlist = [10,20,30,40,50,60,65,70,75,85,95,105,110,115,500]
	colorminlist = [ 0,10,20,30,40,50,60,65,70,75,85, 95,105,110,115]

if(varchoice1 in vartemplist):
	colorlist = ['#330033','#990099','#3300CC','#00FFFF','#00CCFF','#0066CC','#0000FF','#003333','#006600','#FFFF00','#FF6600','#FF0000','#FF0066','#FF00FF','#FF99FF','#FFFFFF']
	colortextlist = ['#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000']
	colormaxlist = [-20,-15,-10, -5, 0,5,10,15,20,25,30,35,40,45,50,100]
	colorminlist = [-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50]

if(varchoice1 in varrhlist):
	colorlist = ['#660000','#990000','#993300','#996600','#663300','#333300','#003300','#006600','#00CC00','#00FF00']
	colortextlist = ['#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000']
	colormaxlist = [10,20,30,40,50,60,70,80,90,100]
	colorminlist = [0,10,20,30,40,50,60,70,80,90]

## Now request in-situ data from MesoWest API and store in lists as well

stnstidlist = []
stntimelist = []
stnlatlist = []
stnlonlist = []
stndatalist = []
stncolorlist = []

mwtimestring = time.strftime('&day1=%d&month1=%m&year1=%Y&hour1=%H',time.localtime(epochend+3600))
mobiletimestring = time.strftime('yr=%Y&mo=%m&dy=%d',time.localtime(epochend))

# try:
initialurl = 'http://api.mesowest.net/v2/stations/timeseries?bbox=-114,40,-111,43&network=9,153,1011&start='+apitimestart+'&end='+apitimeend+'&vars='+apivarlist+'&obtimezone=UTC&token='+apitoken
urlrequest = urllib2.Request(initialurl)
urlopener = urllib2.build_opener()
urldata = urlopener.open(urlrequest,timeout=90)
readdata = urldata.read()
data = json.loads(readdata)
ParseDataV2Stats(data)
# except:
	# skip = 1

## Begin HTML content

# sys.exit()

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>Ozone Study Statistics Interface</title>
<script src="/gslso3s/js/site/siteopen.js"></script>
</head>
<body>
<script src="/gslso3s/js/site/sitemenu.js"></script>
<br>
<b><font COLOR="#0000DD" SIZE=+3>Great Salt Lake Summer Ozone Study - Statistical Data Interface</font></b>
<br><br>
<div style="width:900px">
This page provides basic statistics for in-situ data collected from the Great Salt Lake Summer 2015 Ozone Study.<br>To choose different time or plotting options, use the options given below and in the table below and click "Change Time and Plot Options".
<br><br>
By default, the below plot will contain all available in-situ stations if no stations are selected using the check box options in the table.<br>Selecting specific stations to plot can be done using the check boxes in the sortable table and clicking "Change Time and Plot Options".
<br><br>
<form method="GET" action="statistic_summary.cgi">
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
	Timezone:
	<select name="tz">'''

for option in tzoptionlist:
	if mytzone == option:
		print '''		<option selected="selected" value="'''+option+'''">'''+tzoptions[option]+'''</option>'''
	else:
		print '''		<option value="'''+option+'''">'''+tzoptions[option]+'''</option>'''
print'''	</select>	
	<span style="padding-left:5px">
	Period:
	<select name="min">'''

minint = [1440,2880,4320,7200,10080,20160,43200]
timeint = ['1 day','2 days','3 days','5 days','7 days','14 days','30 days']

for i in range(0,len(minint)):
	if str(minback) == str(minint[i]):
		print '''		<option selected="selected" value="'''+str(minint[i])+'''">'''+timeint[i]+'''</option>'''
	else:
		print '''		<option value="'''+str(minint[i])+'''">'''+timeint[i]+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
	Data:
	<select name="stat">'''

for option in statoptionlist:
	if mystat == option:
		print '''		<option selected="selected" value="'''+option+'''">'''+statoptions[option]+'''</option>'''
	else:
		print '''		<option value="'''+option+'''">'''+statoptions[option]+'''</option>'''
print'''	</select>
	<span style="padding-left:5px">
<input type="hidden" name="past" value="1">
<br><br>
<input type="submit" value="Change Time and Plot Options">
</div><br>'''

plotstidlist = ''
for stid in sorted(stidlist):
	if(stid in plotstn and plotstn[stid] == 1):
		plotstidlist = plotstidlist+stid+','

if(len(plotstidlist) > 3):
	plotstidlist = plotstidlist[0:-1]
	print '''<img src="plot_all_series.cgi?'''+mobiletimestring+'''&tz='''+mytzone+'''&stat='''+mystat+'''&min='''+str(minback)+'''&stids='''+str(plotstidlist)+'''"><br><br>'''
else:
	print '''<img src="plot_all_series.cgi?'''+mobiletimestring+'''&tz='''+mytzone+'''&stat='''+mystat+'''&min='''+str(minback)+'''"><br><br>'''

## Finally, the tabular section below the map
if(mystat == '8hr'):
	print'''<table id="table1" width="800">
<tr>
<td class="table1"><b><font SIZE=+1>Number of days over period selected exceeding 75 ppbv:</font></b></td>
<td class="table1" width="75"><b><font SIZE=+1 color="#0000CC">'''+str(len(daysabv75std))+'''</font></b></td>
</tr>
<tr>
<td class="table1"><b><font SIZE=+1>Number of stations on '''+currtimestring+''' exceeding 75 ppbv:</font></b></td>
<td class="table1" width="75"><b><font SIZE=+1 color="#0000CC">'''+str(len(stnsabv75stdlastday))+'''</font></b></td>
</tr>
<tr>
<td class="table1"><b><font SIZE=+1>Number of days over period selected exceeding 65 ppbv:</font></b></td>
<td class="table1" width="75"><b><font SIZE=+1 color="#0000CC">'''+str(len(daysabv65std))+'''</font></b></td>
</tr>
<tr>
<td class="table1"><b><font SIZE=+1>Number of stations on '''+currtimestring+''' exceeding 65 ppbv:</font></b></td>
<td class="table1" width="75"><b><font SIZE=+1 color="#0000CC">'''+str(len(stnsabv65stdlastday))+'''</font></b></td>
</tr>
</table>
<br>'''
	print'''<b><font SIZE=+1 color="#0000CC">In-Situ 8-Hr Average Ozone Statistics (all values in ppbv)</font></b><br>'''
else:
	print'''<b><font SIZE=+1 color="#0000CC">In-Situ Ozone Observation Statistics (all values in ppbv)</font></b><br>'''	
print'''<table id="table1" class="sortable" width="1000">'''
print'''<tr><td class="table1"><b>Graph</b></td>
<th class="table1"><b>Station ID</b></th>
<th class="table1"><b>Average</b></th>
<th class="table1"><b>Range</b></th>
<th class="table1"><b>Maximum</b></th>
<th class="table1"><b>Max'''+tzout+''' Time</b></th>
<th class="table1"><b>Minimum</b></th>
<th class="table1"><b>Min'''+tzout+''' Time</b></th></tr>'''

# for stid in sorted(insitumax,key=insitumax.get,reverse=True):
i = 1
for stid in sorted(stidlist):
	# try:
	print'''<tr>'''
	if(stid in plotstn and plotstn[stid] == 1):
		print '''<td class="table1" align="center" sorttable_customkey="'''+str(i)+'''"><input type="checkbox" name="'''+stid+'''" value="1" checked></input>'''
	else:
		print '''<td class="table1" align="center" sorttable_customkey="'''+str(i)+'''"><input type="checkbox" name="'''+stid+'''" value="1"></input>'''
	print'''<td class="table1" align="center"><b>'''+("%s (%s)" % (insitustnname[stid],stid))+'''</b></td>
	<td class="table1" align="center" sorttable_customkey="'''+("%d" % (float(insituavg[stid])*100))+'''" bgcolor="'''+tableavgcolor[stid]+'''"><font color="'''+tableavgtextcolor[stid]+'''">'''+("%.2f" % insituavg[stid])+'''</td>
	<td class="table1" align="center" sorttable_customkey="'''+("%d" % (float(insitustd[stid])*100))+'''">'''+("%.2f" % insitustd[stid])+'''</td>
	<td class="table1" align="center" sorttable_customkey="'''+("%d" % (float(insitumax[stid])*100))+'''" bgcolor="'''+tablemaxcolor[stid]+'''"><font color="'''+tablemaxtextcolor[stid]+'''">'''+("%.2f" % insitumax[stid])+'''</td>
	<td class="table1" align="center" bgcolor="'''+tablemaxcolor[stid]+'''"><font color="'''+tablemaxtextcolor[stid]+'''">'''+insitumaxepoch[stid]+'''</td>
	<td class="table1" align="center" sorttable_customkey="'''+("%d" % (float(insitumin[stid])*100))+'''" bgcolor="'''+tablemincolor[stid]+'''"><font color="'''+tablemintextcolor[stid]+'''">'''+("%.2f" % insitumin[stid])+'''</td>
	<td class="table1" align="center" bgcolor="'''+tablemincolor[stid]+'''"><font color="'''+tablemintextcolor[stid]+'''">'''+insituminepoch[stid]+'''</td>'''
	print'''</tr>'''
	i = i + 1
	# except:
		# skip = 1
print'''</table>'''

print'''</form></div>
<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>
'''

sys.exit()
