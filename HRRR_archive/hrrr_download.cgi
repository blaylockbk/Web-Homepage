#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 6, 2017
"""

import sys
import cgi, cgitb
import time
from datetime import date, timedelta
cgitb.enable()

form = cgi.FieldStorage()

yesterday = date.today() - timedelta(days=1)

try:
      model = form['model'].value
except:
      model = 'oper'
try:
      field = form['field'].value
except:
      field = 'sfc'
try:
      date = form['date'].value
except:
      date = yesterday.strftime('%Y-%m-%d %H:%M')

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>Multi-station Time Series</title>
</head>'''

print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 


      

<p align=center>Powered By:<br>
<a href="https://mesowest.org/" target="_blank"><img class="style1" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/MesoWest/MesoWest_1997-2017_largeyears.png" style="background-color:#990000; height:50px"></a>
<br>
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''
