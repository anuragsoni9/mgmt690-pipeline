import os
import argparse

# command line arguments
parser = argparse.ArgumentParser(description='Validate image for object detection.')
parser.add_argument('inFile', type=str, help='Input file.')
parser.add_argument('outDirValid', type=str, help='Output directory for valid images.')
parser.add_argument('outDirInvalid', type=str, help='Output directory for invalid images.')
args = parser.parse_args()

valid = True

# extract the base file name
filename = os.path.basename(args.inFile)

# validate the metadata
metadata = os.path.splitext(filename)[0].split("_")

if len(metadata) != 2:
    valid = False
else:
    if len(metadata[0]) == 0:
        valid = False
    elif len(metadata[1]) < 10 or not metadata[1].isdigit():
        valid = False

# move the image to the appropriate directory
if valid:
    os.symlink(args.inFile, os.path.join(args.outDirValid, filename))
else:
    os.symlink(args.inFile, os.path.join(args.outDirInvalid, filename))

