import os
import argparse
import json
import sendgrid
from sendgrid.helpers.mail import *

# command line arguments
parser = argparse.ArgumentParser(description='Validate image for object detection.')
parser.add_argument('inObjectFile', type=str, help='Input object file.')
parser.add_argument('inRuleDir', type=str, help='Input directory for the rule file.')
parser.add_argument('outDir', type=str, help='Output directory for threat files.')
parser.add_argument('sgKey', type=str, help='Sendgrid API key.')
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
        sg = sendgrid.SendGridAPIClient(apikey=args.sgKey)
        from_email = Email(rules["from_email"])
        to_email = Email(rules["to_email"])
        subject = "Alert! Possible Threat Detected by BAIM Security"
        content = Content("text/plain", "Check your security system. A possible threat has been detected!")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        break
