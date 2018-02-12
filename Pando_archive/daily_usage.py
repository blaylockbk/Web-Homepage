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
from datetime import date, datetime, timedelta
import numpy as np

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [8, 5]
mpl.rcParams['figure.titlesize'] = 15
mpl.rcParams['figure.titleweight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['lines.linewidth'] = 1.8
mpl.rcParams['grid.linewidth'] = .1
mpl.rcParams['figure.subplot.wspace'] = 0.05
mpl.rcParams['figure.subplot.hspace'] = 0.01
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['legend.framealpha'] = .75
mpl.rcParams['legend.loc'] = 'best'
mpl.rcParams['savefig.bbox'] = 'tight'

mpl.rcParams['savefig.dpi'] = 100

# Allocation (in GB)
allocation = 60 * 1e3

# Today's Date
DATE = date.today()

## --- Get size of each bucket (in GB) ---
sizes = {}
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


## --- Create a plot ---
data = np.genfromtxt('Pando_Space.csv',
                      delimiter=',',
                      skip_header=6,
                      names=True,
                      dtype=None)

DATES = map(lambda x: datetime.strptime(x,'%Y-%m-%d'), data['DATE'])
y = np.row_stack([data['GOES16'], data['hrrr'], data['hrrrX'], data['hrrrAK']])

plt.stackplot(DATES,y, labels=names, colors=['#da4f4a', '#016ecd', '#5cb85c', '#faa632'],
              linewidths=0)
plt.ylim([0,allocation])
plt.legend()
plt.ylabel('Size in GB')
plt.title('Pando Usage and Allocation', loc='left')
plt.title('Updated: %s' % datetime.now().strftime('%d %b %Y %H:%M'), loc='right')
plt.grid()

formatter = DateFormatter('%b-%d\n%Y')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.savefig('remaining_space_plot.png')

## --- How much space was used yesterday? ---
total_today   = data['GOES16'][-1] + data['hrrr'][-1] + data['hrrrX'][-1] + data['hrrrAK'][-1]
total_yesterday = data['GOES16'][-2] + data['hrrr'][-2] + data['hrrrX'][-2] + data['hrrrAK'][-2]

one_day_useage = total_today-total_yesterday
days_till_full = int(allocation/one_day_useage)

date_full = DATE+timedelta(days=days_till_full)

## --- Create HTML Page ---
html = '''
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
  <script src='./js/pando_status.js'></script>
    <center><font size=12> %.1f TB out of 60 TB</font>
    <div class="progress" style="max-width:700px;height:35px">
            <div class="progress-bar progress-bar-danger" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
            <div class="progress-bar progress-bar-primary" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
            <div class="progress-bar progress-bar-success" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
            <div class="progress-bar progress-bar-warning" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
          </div>

    <table class="table table-bordered" style='text-align:center;max-width:700px'>
      <tr>
        <th style='text-align:center'>Space Used Yesterday</th>
        <th style='text-align:center'>Estimated Days Until Full</th>
        <th style='text-align:center'>Estimated Full Date</th>
      </tr>
      <tr>
        <td>%.2f GB</td>
        <td>%s</td>
        <td>%s</td>
      </tr>
  </table>
  </center>
    <p style="text-align:center;"><img style='width:100%%;max-width:850px'src="./Pando_archive/remaining_space_plot.png">
</div>
<script src="./js/site/siteclose.js"></script>
</body>
</html>''' % (total_today/1000,
              data['GOES16'][-1]/allocation*100,
              data['hrrr'][-1]/allocation*100,
              data['hrrrX'][-1]/allocation*100,
              data['hrrrAK'][-1]/allocation*100,
              one_day_useage,
              days_till_full,
              date_full.strftime('%d %B %Y'))

with open('index.html', 'w') as f:
    f.write(html)
