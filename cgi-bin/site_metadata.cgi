#!/usr/local/bin/python

import numpy as np
import cgi, cgitb
cgitb.enable()
import gzip, os, sys, datetime, re, time, urllib2, collections, calendar, json
from operator import itemgetter
import tables as pytbls
import MySQLdb as mysqldb

## Set timezone first

os.environ['TZ'] = 'Etc/Greenwich'
time.tzset()

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()

regionlist = ['GSL','SYR','SLC']
try:
	myregion = form["region"].value
except:
	myregion = 'GSL'

if(myregion not in regionlist):
	myregion = 'GSL'

regionmap = {'GSL': '41.121070,-112.355132,10',
'SYR': '41.005733,-112.258307,10',
'SLC': '40.686562,-112.167544,10',
}

regionmapzoom = {'GSL': '9',
'SYR': '10',
'SLC': '10',
}

mobilestidlist = ['CW***','KSL5','TRX##','UUTK#','UNERD']
mobiledes = {
'CW***': 'Con-Way Freight Truck Observations (*** denotes IDs for different vehicles)',
'KSL5': 'KSL Chopper 5',
'TRX##': 'UTA TRAX Light Rail Car Observations (## denotes IDs for different cars)',
'UUTK#': 'University of Utah ATMOS Dept Mobile Observations (## denotes IDs for different vehicles)',
'UNERD': 'University of Utah NerdMobile Observations'
}
	
## Connect to database and get data!
	
dbconnection = None
try:
	stninfoids = []
	dbconnection = mysqldb.connect('meso2.chpc.utah.edu','metwww','wind','mesobest')
	dbcur = dbconnection.cursor()
	dbquerymeta = "SELECT S.ID,S.STID,S.LATITUDE,S.LONGITUDE,M.MNAME,S.NAME,S.ELEVATION from STNINFO S, MNET M where S.MNET_ID=M.ID AND (S.MNET_ID=1011 OR S.STID in (\'MTMET\',\'NAA\',\'GSLM\',\'LMS\',\'FWP\',\'QSY\',\'SNX\',\'BGRUT\',\'QSA\',\'QED\',\'QHW\',\'QBV\',\'QHV\',\'QBR\',\'QO2\',\'QH3\',\'O3S07\',\'O3S08\')) ORDER BY S.STID"
	dbcur.execute(dbquerymeta)
	metadata = dbcur.fetchall()
	dbconnection.close()
except mysqldb.Error, e:
	skip = 1

## Now organize lists!

# print "Content-Type: text/html\n"

stninfoidlist = []
latdict = {}
londict = {}
mnetdict = {}
stiddict = {}

allstninfoidlist = []
allstidlist = []
alllatlist = []
alllonlist = []
allmnetlist = []
allnamelist = []
allelevlist = []
obsdatalist = {}
stndattims = {}

obsdatalist = {}
stndattims = {}

for metarow in metadata:
	allstninfoidlist.append(metarow[0])
	allstidlist.append(metarow[1])
	alllatlist.append(("%.5f" % float(metarow[2])))
	alllonlist.append(("%.5f" % float(metarow[3])))
	allmnetlist.append(metarow[4])
	allnamelist.append(metarow[5])
	allelevlist.append(("%d" % (float(metarow[6])*0.3048)))

print "Content-Type: text/html\n"			
print'''<!DOCTYPE html>
<html>
<head>
<title>Ozone Study Site Metadata</title>
<script src="/gslso3s/js/site/siteopen.js"></script>
</head>
<body>
<script src="/gslso3s/js/site/sitemenu.js"></script>
<br>
<b><font COLOR="#0000DD" SIZE=+3>Great Salt Lake Summer Ozone Study - Site Locations</font></b>
<br><br>
<div style="width:900px">
This page provides metadata information for the sites that provide ozone observations as part of the Great Salt Lake Summer 2015 Ozone Study.  Utilize the map and sortable table below to view different sites.  Only in-situ sites are plotted on the map, mobile sites are shown in the sortable table below with some additional description.
<br><br>
<div id="map" style="width: 900px; height: 600px"></div>
<script>
var allstids = '''+str(allstidlist)+'''
var alllats = '''+str(alllatlist)+'''
var allmnets = '''+str(allmnetlist)+'''
var allnames = '''+str(allnamelist)+'''
var allelevs = '''+str(allelevlist)+'''
var alllons = '''+str(alllonlist)
print '''var cloudmadeUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
subDomains = ['otile1','otile2','otile3','otile4'],
cloudmadeAttribution = 'Map data &copy; 2013 OpenStreetMap contributors, Imagery &copy; 2013 CloudMade',
cloudmadeAttribution = 'Map data &copy; 2013 OpenStreetMap contributors, Imagery &copy; 2013 MapQuest',
cloudmade = new L.TileLayer(cloudmadeUrl, {
	maxZoom: 18, 
	attribution: cloudmadeAttribution, 
	subdomains: subDomains, 
	unloadInvisibleTiles: true,
	updateWhenIdle:false
});
map = new L.Map('map', {
	center: new L.LatLng('''+regionmap[myregion]+'''), 
	zoom: '''+regionmapzoom[myregion]+''', 
	layers: [cloudmade]
});
var datamarkerlist = [];
for (var j=0;j<allstids.length;j++) {
	iconHTML = '<a href="http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn='+allstids[j]+'" target="_blank"><b>'+allstids[j]+'</a><br>'+allnames[j]+'</b><br>Latitude: '+alllats[j]+'<br>Longitude: '+alllons[j]+'<br>Elevation: '+allelevs[j]+' m<br>Network: '+allmnets[j]		
	var tempmarker = new L.SquareMarker([alllats[j],alllons[j]], {
		radius: 4,
		color: 'black',
		weight: 1,
		opacity: 1,
		fillColor: 'yellow',
		fillOpacity: 1
	}).bindPopup(iconHTML);
	datamarkerlist.push(tempmarker);
}
obslayer = L.layerGroup(datamarkerlist).addTo(map);
</script></div><br>'''

## Finally, the tabular section below the map

print'''<table id="table1" class="sortable" width="1000">
<tr><th class="table1" width="100"><font SIZE=+1><b>Type</b></font></th>
<th class="table1" width="100"><font SIZE=+1><b>ID</b></font></th>
<th class="table1"><font SIZE=+1><b>Name</b></font></th>
<th class="table1"><font SIZE=+1><b>Latitude</b></font></th>
<th class="table1"><font SIZE=+1><b>Longitude</b></font></th>
<th class="table1"><font SIZE=+1><b>Elevation (m)</b></font></th>
<th class="table1"><font SIZE=+1><b>Network</b></font></th>
</tr>'''
for i in range(0,len(allstidlist)):
	try:
		print'''<tr><td class="table1"><font SIZE=+1><b>In-Situ</b></font></td><td class="table1"><font SIZE=+1><b><a href="http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn='''+allstidlist[i]+'''" target="_blank"><b>'''+allstidlist[i]+'''</a></b></font></td>
		<td class="table1"><font SIZE=+1><b>'''+allnamelist[i]+'''</b></font></td>
		<td class="table1"><font SIZE=+1><b>'''+alllatlist[i]+'''</b></font></td>
		<td class="table1"><font SIZE=+1><b>'''+alllonlist[i]+'''</b></font></td>
		<td class="table1"><font SIZE=+1><b>'''+allelevlist[i]+'''</b></font></td>
		<td class="table1"><font SIZE=+1><b>'''+allmnetlist[i]+'''</b></font></td>
		</tr>'''
	except:
		skip = 1
print'''</table><br>'''

print'''<table id="table1" class="sortable" width="1000">
<tr><th class="table1" width="100"><font SIZE=+1><b>Type</b></font></th>
<th class="table1" width="100"><font SIZE=+1><b>ID</b></font></th>
<th class="table1"><font SIZE=+1><b>Description</b></font></th>
</tr>'''
for stid in sorted(mobilestidlist):
	try:
		print'''<tr><td class="table1"><font SIZE=+1><b>Mobile</b></font></td><td class="table1"><font SIZE=+1><b>'''+stid+'''</b></font></td><td class="table1"><font SIZE=+1><b>'''+mobiledes[stid]+'''</b></font></td></tr>'''			
	except:
		skip = 1
print'''</table><br>'''

print'''
<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>'''

sys.exit()
