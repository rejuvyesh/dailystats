#!/usr/bin/env python3
#
# File: readdailystats.py
#
# Created: Thursday, November 20 2014 by rejuvyesh <mail@rejuvyesh.com>
#

# arbtt-stats --for-each=day --output-format=CSV -x 'tday:night' -x 'tday:morning' -x 'tday:lunchtime' -x 'tday:afternoon' -x 'tday:evening' -x 'tday:late-evening' > cleanstats.csv

import csv
import math
import json
import sys


def toJson(dic, jsonpath):
  '''
  Save to json
  '''
  with open(jsonpath, 'w') as f:
    json.dump(dic, f, sort_keys=True, indent=4)


def toChartJS(dic, color, name):
  '''
  Convert to Chart.JS format
  Arguments:
  - `dic`: Dictionary
  - `color`: Color of each label
  - `jsonpath`: Path of json file
  '''
  export = []

  for day in dic:
    jsonname = name + '-' + day + '.json'
    
    d = dic[day]
    # print(d)
    data = []
    tot = 0
    for index, item in enumerate(d):
      if 'totaltime' in item.keys():
        totalTime = d[index]['totaltime']['Time']
      else:
        tot += float(list(item.values())[0]['Percent'])
        per = float(list(item.values())[0]['Percent'])
        lab = list(item.keys())[0]
        data.append({"label": lab + ' (' + '{:.2f}'.format(per) + '%)', "value": per, "color": color[lab]})
    if tot <= 100:
      data.append({"label": 'misc'+' (' + '{:.2f}'.format(100-tot) + '%)', "value": 100-tot, "color": color['misc']})
    else:
      # normalize (bummer)
      newtot = 0
      for i, thing in enumerate(data):
        data[i]['value'] = (data[i]['value']/tot)*100
        newtot += data[i]['value']
      # data.append({"label": 'misc'+' (' + '{:.2f}'.format(100-newtot) + '%)', "value": 100-newtot})
    # Save json for this day
    export.append({'fname': jsonname, 'totalTime': totalTime})
    toJson(sorted(export, key=lambda x: x['fname']), '/tmp/loglist.json')
    toJson(sorted(data, key=lambda x: x['label']), '/tmp/data/'+jsonname)


if __name__ == '__main__':
  if len(sys.argv) <= 1:
    printf("Error: no csv file")
    exit(-1)
  else:
    csvfile = sys.argv[1]

  tags = set({'misc'})
  date = {}
  with open(csvfile, 'r') as f:
      dailystats = csv.reader(f, delimiter=',')
      next(dailystats)   # Skip headers
      for row in dailystats:
        if row[0] in date.keys():
          # {'tag' : {'time', 'percent'}}
          tags.update({row[1]})
          date[row[0]].append({row[1]: {'Time': row[2], 'Percent': row[3]}})
        else:
          date[row[0]] = [{row[1]: {'Time': row[2], 'Percent': row[3]}}]
  col = {}
  for i, t in enumerate(tags):
    col[t] = 'hsl(' + str(math.floor(((i+0.5)/len(tags)) * 360)) + ', 55%, 45%)'

  toChartJS(date, col, 'daily')
