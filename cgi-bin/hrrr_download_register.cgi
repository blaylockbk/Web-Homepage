#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
March 6, 2017

Webpage to Download HRRR file from Pando archive. Also display .idx file and sample image.
"""

import sys
import os
import subprocess
import cgi, cgitb
import time
from datetime import date, datetime, timedelta
cgitb.enable()

form = cgi.FieldStorage()

yesterday = date.today()
max_date = date.today().strftime('%Y-%m-%d')

try:
    model = cgi.escape(form['model'].value)
except:
    model = 'hrrr'
try:
    field = cgi.escape(form['field'].value)
except:
    field = 'sfc'
try:
    Date = cgi.escape(form['date'].value)
except:
    Date = yesterday.strftime('%Y-%m-%d')
try:
    link2 = cgi.escape(form['link2'].value)
except:
    link2 = 'grib2'

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRR Register</title>


</head>'''

print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print '''
<div id="content" class="container">
    <h1 align="center">
    <i class="fa fa-user-plus" aria-hidden="true"></i> HRRR Archive Registration
    </h1>

<script src='./js/pando_status.js'></script>
<script src='./js/HRRR_status.js'></script>

<div class="container" style="max-width:650px">  
  <h4><b>Please tell us a little about yourself and read the 
      <a href="./hrrr_practices.html">
      Best Practices</a></b></h4>

  <form class="form-horizontal" action="./send_form_to_csv.py" method="post">
    
    <div class="form-group">
        <div class="input-group">                               
        <span class="input-group-addon"><i class="fa fa-user fa-fw"></i></span>
        <input required name="name" type="text" class="form-control" placeholder="First and last name">
        </div>
    </div>
    
    <div class="form-group">
        <div class="input-group">                               
        <span class="input-group-addon"><i class="fa fa-envelope fa-fw"></i></span>
        <input required name="email" type="email" class="form-control" placeholder="Email">
        </div>
    </div>

    <div class="form-group">
        <div class="input-group">                               
        <span class="input-group-addon"><i class="fa fa-globe fa-fw"></i></span>
        <input required name="location" type="text" class="form-control" placeholder="Where are you from? State, University, Company, etc.">
        </div>
    </div>

    <div class="form-group">
        <div class="input-group">
        <span class="input-group-addon"><i class="fa fa-comment fa-fw"></i></span>           
            <textarea required class="form-control" rows=4  type="text" name="description"  placeholder="How do you plan using HRRR data? Are you working on a graduate degree? Are you verifying surface temperatures? etc."></textarea>
        </div>
    </div>

    <div class="form-group">        
      <div class="">
        <div class="checkbox">
          <label><input name="contact" type="checkbox" checked> Can we contact you? (updates, outages, surveys, etc.)</label>
        </div>
      </div>
    </div>

    <div class="form-group">        
      <div class="">
        <button type="submit" class="btn btn-success">Submit</button> <small>By clicking "Submit" you agree to the <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_practices.html" target="_blank">Best Practices</a></small>
      </div>
    </div>
    <input type="hidden" name="_next" value="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi" />
    <input type="hidden" name="_subject" value="New HRRR Download Request" />
  </form>
</div>
<div align="right" style="padding-right:10px">
  <small><small><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi">I already registered</a></small></small>
</div>
<br>

<script src='./js/climate_acknowledgement.js'></script>
</div>
<script src="./js/site/siteclose.js"></script>
</body>
</html>
'''
