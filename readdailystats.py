#!/usr/bin/env python3
#
# File: readdailystats.py
#
# Created: Thursday, November 20 2014 by rejuvyesh <mail@rejuvyesh.com>
#

# arbtt-stats --for-each=day --output-format=CSV -x 'tday:night' -x 'tday:morning' -x 'tday:lunchtime' -x 'tday:afternoon' -x 'tday:evening' -x 'tday:late-evening' > cleanstats.csv

from colour import Color
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

    # Save json for this day
    export.append({'fname': jsonname, 'totalTime': totalTime})
    toJson(sorted(export, key=lambda x: x['fname']), '/tmp/loglist.json')
    toJson(sorted(data, key=lambda x: x['label']), '/tmp/data/'+jsonname)


def dailyUsage(dailyfile, minutefile):
  """

  Arguments:
  - `dailyfile`:
  - `minutefile`:
  """
  tags = set({'misc'})
  dailydata = {}
  with open(dailyfile, 'r') as f:
    dailystats = csv.reader(f, delimiter=',')
    next(dailystats)   # Skip headers
    for row in dailystats:
      if row[0] in dailydata.keys():
        # {'tag' : {'time', 'percent'}}
        tags.update({row[1]})
        dailydata[row[0]].append({row[1]: {'Time': row[2], 'Percent': row[3]}})
      else:
        dailydata[row[0]] = [{row[1]: {'Time': row[2], 'Percent': row[3]}}]
  col = {}
  category20 = [
    "#1f77b4", "#aec7e8",
    "#ff7f0e", "#ffbb78",
    "#2ca02c", "#98df8a",
    "#d62728", "#ff9896",
    "#9467bd", "#c5b0d5",
    "#8c564b", "#c49c94",
    "#e377c2", "#f7b6d2",
    "#7f7f7f", "#c7c7c7",
    "#bcbd22", "#dbdb8d",
    "#17becf", "#9edae5"
  ]
  for i, t in enumerate(tags):
    col[t] = category20[i % len(category20)]

  # Load data for every minute
  minutedata = {}
  with open(minutefile, 'r') as f:
    next(f)
    cont = f.readlines()
    for row in cont:
      day, value = row.split(' ')
      time, tag, _, _ = value.split(',')
      hour, minute = [int(x) for x in time.split(':')]
      moment = hour*60 + minute
      if day in minutedata.keys():
        if tag in minutedata[day].keys():
          minutedata[day][tag].append(moment)
        else:
          minutedata[day][tag] = [moment]
      else:
        minutedata[day] = {tag: [moment]}


if __name__ == '__main__':
  if len(sys.argv) <= 2:
    printf("Error: need two csv files")
    exit(-1)
  else:
    dailyfile = sys.argv[1]
    minutefile = sys.argv[2]
    dailyUsage(dailyfile, minutefile)
