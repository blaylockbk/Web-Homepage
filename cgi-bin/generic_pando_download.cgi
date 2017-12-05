#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
Decebmer 5, 2017
"""

import subprocess
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()


## Get Bucket name from the form, or set default
try:
    bucket = form['BUCKET'].value
except:
    # Demo, default buckete
    bucket = 'HRRR/oper/prs/20170101/'


## Create list of files in the bucket with rclone

# 1) The location of the rclone command
rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'

# 2) The rclone comand to list files in this bucket, splitting the 11th column to get file names
#    horelS3 is the bucket named I configured rclone to access the Horel Pando allocation.

ls = ' ls horelS3:%s' % bucket

# 3) Execute the rclone ls comand
rclone_out = subprocess.check_output(rclone + ls, shell=True)

# 4) Split the file names to a list
flist = rclone_out.split('\n')

# 5) Remove empty elements. There is always one at the end.
flist.remove('')

# 6) Order the files
flist.sort() 

## Pando Bucket URL
baseURL = 'https://pando-rgw01.chpc.utah.edu/'

## Print the HTML content
print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>Download from Pando</title>
</head>
<body style="padding-left:50px">

<h1> Download from Pando</h1>
<form>
<h4>Bucket URL: ''' + baseURL + '''<input type=text size=50 name=BUCKET value=%s></h4>''' % bucket
print '<hr>'

## Create an HTML link for each file
print '''
<table cellspacing=5>
<tr><th>File Object Name</th><th>Size</th><tr>
'''
for f in flist:
    # Build the URL for each file
    SIZE = float(f.split(' ')[-2])
    FILE = f.split(' ')[-1]
    URL = baseURL + bucket + FILE
    print '''<tr><td><a href="%s">%s</a></td><td align="right" style="padding-left:30px"><b>%.2f GB</b></td></tr>''' % (URL, FILE, SIZE/10**9)

print '''
</table>
</body>
</html>
'''
