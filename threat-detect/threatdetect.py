import os
import argparse
import json

# command line arguments
parser = argparse.ArgumentParser(description='Validate image for object detection.')
parser.add_argument('inObjectFile', type=str, help='Input object file.')
parser.add_argument('inRuleDir', type=str, help='Input directory for the rule file.')
parser.add_argument('outDir', type=str, help='Output directory for threat files.')
args = parser.parse_args()

# parse the rules.
rules = json.load(open(os.path.join(args.inRuleDir, 'rule.json')))
threats = rules["threat_classes"]

# walk the input object files in the input directory.
objects = json.load(open(args.inObjectFile))
for object in objects["objects"]:
    if object['class'] in threats:
        if not os.path.exists(os.path.join(args.outDir, args.inObjectFile.split('/')[-2])):
            os.makedirs(os.path.join(args.outDir, args.inObjectFile.split('/')[-2]))
        os.symlink(args.inObjectFile, os.path.join(args.outDir, args.inObjectFile.split('/')[-2], os.path.basename(args.inObjectFile)))
        break
