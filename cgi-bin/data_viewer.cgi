#!/usr/bin/python

import sys
import cgi, cgitb
import time
import datetime
cgitb.enable()

form = cgi.FieldStorage()

current = datetime.datetime.now()

try:
   id = form['id'].value
except:
   id = 'USDR1'

try:
   interval = form['interval'].value
except:
   interval = '30'

try:
   snr = form['snr'].value
except:
   snr = '05'

try:
   eyr = form['eyr'].value
   emo = form['emo'].value
   edy = form['edy'].value
   ehr = form['ehr'].value

   syr = form['syr'].value
   smo = form['smo'].value
   sdy = form['sdy'].value
   shr = form['shr'].value

except:
   eyr = ("%04d" % current.year)
   emo = ("%02d" % current.month)
   edy = ("%02d" % current.day)
   ehr = ("%02d" % current.hour)

   syr = ("%04d" % (current-datetime.timedelta(0.5)).year)
   smo = ("%02d" % (current-datetime.timedelta(0.5)).month)
   sdy = ("%02d" % (current-datetime.timedelta(0.5)).day)
   shr = ("%02d" % (current-datetime.timedelta(0.5)).hour)

# Get epoch time stamps for plotting ceilometer data.

beg_date = datetime.datetime(int(syr),int(smo),int(sdy),int(shr),00,00)
end_date = datetime.datetime(int(eyr),int(emo),int(edy),int(ehr),00,00)
beg_epoch = time.mktime(beg_date.timetuple())
end_epoch = time.mktime(end_date.timetuple())

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/~u0875930/PCAPS_Modeling/anoceanofsky.css"/>
<title>Data Viewer</title>
</head>'''

print '''
<body link="#FFFFFF">
<div id="page">
   <div class="topNaviagationLink"><a href="/~u0875930/pcaps_modeling.html">Home</a></div>
   <div class="topNaviagationLink" style="width:150px"><a href="/~u0875930/PCAPS_Modeling/iop5.html">IOP5 (1-9 Jan, 2011)</a></div>
   <div class="topNaviagationLink"><a href="/~u0875930/PCAPS_Modeling/Jan2015.html">1-9 Jan, 2015</a></div>
   <div class="topNaviagationLink"><a href="/~u0875930/cgi-bin/data_viewer.cgi">Data Viewer</a></div>
   <div class="topNaviagationLink"><a href="/~u0875930/PCAPS_Modeling/presentations.html">Presentations</a></div>
   <div class="topNaviagationLink"><a href="/~u0875930/PCAPS_Modeling/refs.html">References</a></div>
   <div class="topNaviagationLink" style="width:150px"><a href="/~u0875930/PCAPS_Modeling/add_links.html">Additional Links</a></div>
</div>
<div id="dataviewerPicture" style="height:200px">
   <div class="picture" style="height:180px">
   </div>
</div>'''

print'''        
<div class="contentBox">
<div class="innerBox">
   <br>
   <div class="contentText">
      <form method="GET" action="data_viewer.cgi">
      <font size="4">Some tips for plotting:</font>
      <br>
      <br>
      <ul>
      <li class="b1">Use this webpage to plot sodar data using the new API offered by the Mesowest Above Surface Network (ASN).</li> 
      <li class="b1">Sodar data is plotted at an interval of your choosing (15 min, 30 min, or 1 hr) from the requested begin time to end time.</li>
      <li class="b1">The plot defaults to the most recent 12 hours worth of observations with 30 minute resolution and a signal to noise ratio (SNR) 
      threshold of 5. The SNR threshold is a way to filter out potentially bad data. All observations with an SNR greater than the 
      selected threshold will be plotted. (A threshold of 00 will allow all observations to be plotted.)</li>
      <li class="b1">Try to keep the density of your requested observations in mind. (The plot's size is currently fixed.)</li>
      <li class="b1">Data is available from January 1st, 2015 onward.</li> 
      <li class="b1">Send any questions/concerns to chris.foster@utah.edu.</li>
      <br>

      <table>
      <tr>
         <td>Station ID:</td>
      <td>
         <select name="id">'''

stn_ids = ['USDR1','USDR2']

for i in range(0,len(stn_ids)):
   if str(id) == str(stn_ids[i]):
      print'''<option selected="selected">'''+stn_ids[i]+'''</option>'''
   else:
      print'''<option>'''+stn_ids[i]+'''</option>'''
print''' </select>
      </td>
      </tr>

      <tr>
      <td>Observation Interval:</td>
      <td>
         <select name="interval">'''

disp_int = ['15 mins','30 mins','1 hour']
true_int = ['15','30','60']

for i in range(0,len(true_int)):
   if str(interval) == str(true_int[i]):
      print'''<option selected="selected" value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
   else:
      print'''<option value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
print''' </select>
      </td>
      </tr>

      <tr>
         <td>SNR Threshold:</td>
      <td>
         <select name="snr">'''
for i in range(11):
   if snr == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>
      </td>
      </tr>

      </table>
   </div>

      <br>
      <table style="width:75%">
      <tr>
         <td></td>
         <td>Month</td>
         <td>Day</td>
         <td>Year</td>
         <td>Hour</td>
      </tr>

      <tr>
         <td>
         Begin Time:
         </td>

         <td>
         <select name="smo">'''
for i in range(1,13):
   if smo == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name="sdy">'''
for i in range(1,32):
   if sdy == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name ="syr">
            <option>2015</option>
         </select>
         </td>

         <td>
         <select name="shr">'''
for i in range(0,24):
   if shr == str("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>
      </tr>

      <tr>
         <td>
         End Time:
         </td>

         <td>
         <select name="emo">'''
for i in range(1,13):
   if emo == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name="edy">'''
for i in range(1,32):
   if edy == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name ="eyr">
            <option>2015</option>
         </select>
         </td>

         <td>
         <select name="ehr">'''
for i in range(0,24):
   if ehr == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

      </tr>
      </table>

   <br>
   <div class="imageText">
      <input type="submit" value="Change Data Options">
   </div>
   </form>
   </div>

<br>
<div class="imageText">
   <a href="plot_asn_sodar.cgi?id='''+id+'''&interval='''+str(interval)+'''&snr='''+str(snr)+'''&smo='''+str(smo)+'''&sdy='''+str(sdy)+'''&syr='''+str(syr)+'''
   &shr='''+str(shr)+'''&emo='''+str(emo)+'''&edy='''+str(edy)+'''&eyr='''+str(eyr)+'''&ehr='''+str(ehr)+'''">
      <img src="plot_asn_sodar.cgi?id='''+id+'''&interval='''+str(interval)+'''&snr='''+str(snr)+'''&smo='''+str(smo)+'''&sdy='''+str(sdy)+'''&syr='''+str(syr)+'''
      &shr='''+str(shr)+'''&emo='''+str(emo)+'''&edy='''+str(edy)+'''&eyr='''+str(eyr)+'''&ehr='''+str(ehr)+'''" width="100%">
   </a>
   <br><br>
</div>
<div style="padding-left: 35px;">
   Ceilometer backscatter from '''+str(beg_date)+''' to '''+str(end_date)+''' at UUCLB (surface to 750 m)
   <br>
   <img src="https://asn.synoptic.io/api/v1/series?senabbr=UUCLB&variables=BS&token=123123&Begin='''+str(beg_epoch)+'''&End='''+str(end_epoch)+'''
   &OutputFormat=tile&ColorBarID=2&MinContourVal=-7&MaxContourVal=-4&ImageDimensions=780,325&ImageCeil=750" width="89%">
</div>
<br><br>'''
#<div class="imageText">
#   <img src="/~u0875930/PCAPS_Modeling/station_locations.png" width="60%">
#   <br>
#   Locations of stations with data plotted on this page (Google Earth image)
#</div>
'''
   <br>
   <br>
   
</div>
</div>
<div id="footer"></div>
</body>
</html>
'''
