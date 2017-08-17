#!/usr/bin/env python
import json
from urllib2 import Request, urlopen, URLError

APIURL = 'https://api.chartbeat.com/live/quickstats/v4/?apikey=4b6a95b8a5c3616f3ffd43a4911ffa76&host=srf.ch'
request = Request(APIURL)

try:
    response = urlopen(request)
    res = json.loads(response.read())
    data = { "engaged_visit": res['data']['stats']['engaged_visit']['hist'][0], 
         "engaged_time": res['data']['stats']['engaged_time']['hist'][0],
         "links": res['data']['stats']['links'],
         "people": res['data']['stats']['people'],
         "read": res['data']['stats']['read'],
         "writing_visit": res['data']['stats']['writing_visit']['hist'][0],
         "direct": res['data']['stats']['direct'],
         "visits": res['data']['stats']['visits'],
         "recirc": res['data']['stats']['recirc'],
         "subscr": res['data']['stats']['subscr'],
         "article": res['data']['stats']['article'],
         "pages": res['data']['stats']['pages'],
         "search": res['data']['stats']['search'],
         "crowd": res['data']['stats']['crowd'],
         "domload": res['data']['stats']['domload']['hist'][0],
         "visit": res['data']['stats']['visit']['hist'][0],
         "idle": res['data']['stats']['idle'],
         "internal": res['data']['stats']['internal'],
         "social": res['data']['stats']['social'],
         "new": res['data']['stats']['new'],
         "scroll": res['data']['stats']['scroll']['hist'][0]
       }
    print data
    #print kittens[559:1000]
except URLError, e:
    print 'No kittez. Got an error code:', e


