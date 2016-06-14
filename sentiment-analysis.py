import json
import requests
import sys

# retrieve command line arguments
if len(sys.argv) != 2:
  print ("Usage: python sentiment-analysis.py [filename]")
  exit(1)

filename = sys.argv[1]


# configuration variables
minimum_confidence = 25.0 # from 0 to 100 - higher is more confident. Set to 0 to use all data.
url = "http://sentiment.vivekn.com/api/batch/"
verbose_mode = False  # shows the details of the confidence levels


# open the file and read in the JSON
try:
  with open(filename) as data_file:
    json_data = json.load(data_file)
except json.JSONDecodeError as e:
  print ("Error: Malformed JSON")
  exit(1)


# extract the parent comments
parent_comments = {}

for user in json_data:
  parent_comments[user["user"]] = list()
  for comment in user["data"]:
    parent_comments[user["user"]].append(comment["comment"])

# go through for each user and send the post request to the API
for user in list(parent_comments.keys()):
  # set up variables
  sentiments = list()
  results = {}
  results['Positive'], results['Neutral'], results['Negative'] = 0, 0, 0

  # make the request
  payload = {'txt': json.JSONEncoder(parent_comments[user]) }
  r = requests.post(url, data=json.dumps(parent_comments[user]))
  json_response = r.json()

  # for each comment, add it if it exceeds the minimum confidence
  for comment in json_response:
    sentiment = comment["result"]
    confidence = float(comment["confidence"])

    if confidence >= minimum_confidence:
      sentiments.append([sentiment, confidence])
      results[sentiment] = results[sentiment] + 1

  # for now it just prints, we need to save the data eventually
  print ( user )
  if verbose_mode:
    print ( sentiments ) # outputs more details about confidence levels
  print ( results )
  print ( "-----------" )




