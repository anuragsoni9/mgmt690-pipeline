import os
import argparse
import json

# command line arguments
parser = argparse.ArgumentParser(description='Validate image for object detection.')
parser.add_argument('inObjectDir', type=str, help='Input directory for object files.')
parser.add_argument('inRuleDir', type=str, help='Input directory for the rule file.')
parser.add_argument('outDir', type=str, help='Output directory for threat files.')
args = parser.parse_args()

# parse the rules.
rules = json.load(open(os.path.join(args.inRuleDir, 'rule.json')))
threats = rules["threat_classes"]

# walk the input object files in the input directory.
for dirpath, dirs, files in os.walk(args.inObjectDir):
    for file in files:
        objects = json.load(open(os.path.join(args.inObjectDir, file)))
        for object in objects["objects"]:
            if object['class'] in threats:
                if not os.path.exists(os.path.join(args.outDir, args.inObjectDir.split('/')[-1])):
                    os.makedirs(os.path.join(args.outDir, args.inObjectDir.split('/')[-1]))
                os.symlink(file, os.path.join(args.outDir, args.inObjectDir.split('/')[-1], os.path.basename(file)))
                break
