# Brian Blaylock
# January 5, 2018                            Oh boy, do I need a nap right now.

"""
Get the current size of our Pando archive.
"""

import numpy
import subprocess
from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt

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
columns = ['DATE', 'GOES16','HRRR','horel-archive','other']
new_line = '%s,%.2f,%.2f,%.2f,%.2f\n' % (DATE.strftime('%Y-%m-%d'), sizes['GOES16'], sizes['HRRR'], sizes['horel-archive'], sizes['Brian'])

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
y = np.row_stack([data['Brian'], data['horelarchive'], data['GOES16'], data['HRRR']])

plt.stackplot(DATES,y)
plt.axhline(y=allocation)
plt.show()