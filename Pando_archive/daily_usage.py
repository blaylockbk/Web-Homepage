# Brian Blaylock
# January 5, 2018                            Oh boy, do I need a nap right now.

"""
Get the current size of our Pando archive.
"""

import matplotlib as mpl
mpl.use('Agg') #required for the CRON job. Says "do not open plot in a window"??
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy
import subprocess
from datetime import date, datetime
import numpy as np


# Allocation (in GB)
allocation = 60 * 1e3

# Todays Date
DATE = date.today()

# Get a list of buckets
buckets = subprocess.check_output('rclone lsd horelS3: | cut -c 44-', shell=True)
buckets = buckets.split('\n')
buckets.remove('')

sizes = {}
# Get size of each bucket (in GB)
buckets = ['GOES16', 'hrrr', 'hrrrX', 'hrrrak']
names = ['GOES16', 'hrrr', 'hrrrX', 'hrrrAK']
for b in buckets:
    outSize = subprocess.check_output('rclone size horelS3:%s/' % b, shell=True)
    print outSize
    sSIZE = outSize.index('(')+1
    eSIZE = outSize.index(' bytes)')
    Bytes = outSize[sSIZE:eSIZE]
    GB = int(Bytes) * 1e-9
    print b, GB
    sizes[b]=GB

# Create a new line for the Pando_Space.csv file
new_line = '%s,%.2f,%.2f,%.2f,%.2f\n' % (DATE.strftime('%Y-%m-%d'),
                                                   sizes['GOES16'],
                                                   sizes['hrrr'],
                                                   sizes['hrrrX'],
                                                   sizes['hrrrak'])

# Append to file
with open("Pando_Space.csv", "a") as myfile:
    myfile.write(new_line)


# Create a plot
data = np.genfromtxt('Pando_Space.csv',
                        delimiter=',',
                        skip_header=6,
                        names=True,
                        dtype=None)

DATES = [datetime.strptime(d, '%Y-%m-%d') for d in data['DATE']]
y = np.row_stack([data['GOES16'], data['hrrr'], data['hrrrX'], data['hrrrAK']])

plt.stackplot(DATES,y)
plt.ylim([0,allocation])
plt.ylabel('Size in GB')
plt.title('Pando Usage and Allocation')
plt.grid()


formatter = DateFormatter('%b-%d\n%Y')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.savefig('remaining_space_plot.png')

total = data['GOES16'][-1] + data['hrrr'][-1] + data['hrrrX'][-1] + data['hrrrAK'][-1]

# Create HTML Page
with open('index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>

<head>
<title>Pando Allocation</title>
<link rel="stylesheet" href="../css/brian_style.css" />
<script src="../js/site/siteopen.js"></script>
</head>


<body>

<a name="TOP"></a>
<script src="./js/site/sitemenu.js"></script>	

<h1 align="center"><i class="fa fa-database"></i> Horel Group Pando Allocation</h1>

<div class='container'>
    <center><font size=12>60 TB</font></center>
    <div class="progress" style="width:100%;height:30px">
            <div class="progress-bar progress-bar-default" role="progressbar" style="width:'''+str(int(data['GOES16'][-1]/allocation*100))+'''%">
              <font size=4>GOES16</font>
            </div>
            <div class="progress-bar progress-bar-success" role="progressbar" style="width:'''+str(int(data['hrrr'][-1]/allocation*100))+'''%">
              <font size=4>HRRRoper</font>
            </div>
            <div class="progress-bar progress-bar-warning" role="progressbar" style="width:'''+str(int(data['hrrrX'][-1]/allocation*100))+'''%">
              <font size=4>HRRRexp</font>
            </div>
            <div class="progress-bar progress-bar-info" role="progressbar" style="width:'''+str(int(data['hrrrAK'][-1]/allocation*100))+'''%">
              <font size=4>HRRRalaska</font>
            </div>
          </div>

    <center><h2>'''+str(round(total/1000,2))+''' TB out of 60 TB</h2></center>
    
    <p style="text-align:center;"><img align='middle' src="./Pando_archive/remaining_space_plot.png">
</div>

<script src="./js/site/siteclose.js"></script>
</body>
</html>''')
