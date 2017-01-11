#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

import sys
import cgi, cgitb
import matplotlib as mpl
import numpy as np


cgitb.enable()

form = cgi.FieldStorage()

print "Content-Type: text/html\n"
print "python version: ", sys.version
print "<br><br>"
print "matplotlib version:", mpl.__version__
print "<br><br>"
print "numpy version:", np.__version__
print "<br><br>"
