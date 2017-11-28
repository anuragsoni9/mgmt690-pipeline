import numpy as np
import os
import argparse
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt; plt.rcdefaults()

# command line arguments
parser = argparse.ArgumentParser(description='Validate image for object detection.')
parser.add_argument('inThreatDir', type=str, help='Input directory for threat files.')
parser.add_argument('outDir', type=str, help='Output directory for plots.')
args = parser.parse_args()

# walk the input threat files in the input directory.
devIDs = []
threats = []
for dirpath, dirs, files in os.walk(args.inThreatDir):
    for dir in dirs:
        devIDs.append(dir)
        for dirpathinner, dirsinner, filesinner in os.walk(os.path.join(args.inThreatDir, dir)):
            threats.append(len(filesinner))
y_pos = np.arange(len(devIDs))

# Create the plot.
plt.bar(y_pos, threats, align='center', alpha=0.5)
plt.xticks(y_pos, devIDs)
plt.ylabel('Threats')
plt.title('Detected Threats by Device/User ID')
 
plt.savefig(os.path.join(args.outDir, 'threats.png'))
