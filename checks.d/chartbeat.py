import json
from urllib2 import Request, urlopen, URLError
from checks import AgentCheck

class Chartbeat(AgentCheck):
    APIURL = 'https://api.chartbeat.com/live/quickstats/v4/'

    def __init__(self, name, init_config, agentConfig, instances=None):

        AgentCheck.__init__(self, name, init_config, agentConfig, instances=instances)

    def check(self, instance):

        if instance.get("site", None) is None:
            raise Exception("add a site")
        site = instance.get('site')

        if instance.get("path", None) is None:
            raise Exception("add a patch")
        path = instance.get('path')

        apikey = self.init_config.get('apikey')
        host = self.init_config.get('host')

        if path == 'total':
            url = self.APIURL+'?apikey='+apikey+'&host='+host
        else:
            url = self.APIURL+'?apikey='+apikey+'&host='+host+'&path='+path

        request = Request(url)

        # Load the data
        try:
            response = urlopen(request)
            res = json.loads(response.read())
        except URLError, e:
            print 'ERROR: ', e
        '''
        engaged_visit [h]: Number of concurrents that are engaging with the site
        engaged_time [h]: Number of concurrents that have engaged times that fall within the following
        time buckets (in seconds): 0-15,15-30,30-45,45-60,60-120,180-240,240-300,300-600,600-900,900+
        links: Concurrents from Link Traffic sources
        people: Concurrents
        read: Concurrents on the page that are reading
        writing_visit [h]: Number of concurrents that are writing
        direct: Concurrents from Direct Traffic Sources
        visits: Concurrents; matches "people"
        recirc: Total concurrents that have moved on to a second page from an article page
        subscr: The number of people arriving from a web based subscription server (e.g. Google Reader).
        platform: Concurrents by platform type (app, desktop, mobile, tablet)
        platform_engaged: Concurrents that have currently engaging by platform type
        article: If an article page, will return the number of concurrents on that page, else 0
        toprefs: Top referrers for that page
        search: Concurrents from Search Traffic Sources
        crowd: Null
        domload [h]: Number of concurrents broken down by how long their DOM took to load that fall within the following time buckets (in seconds): 1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-10,10+ seconds
        visit [h]: Histogram breakdown of total concurrents
        write: Concurrents on the page that are writing
        num_ref: Number of unique referrers
        idle: Number of concurrents that are idle on the page (2+ hours of inactivity)
        internal: Concurrents from Internal Traffic Sources
        social: Concurrents from Social Traffic Sources
        new: Concurrents that are classified as "new" (i.e. first visit in the last 30 days)
        scroll [h]: Number of concurrents that made it down a certain way of the page--histogram buckets are broken down into 10% intervals of the page.
        '''

        # format the data
        data = {
             #"engaged_visit": res['data']['stats']['engaged_visit']['hist'][0],
             "engaged_time": res['data']['stats']['engaged_time']['avg'],
             "links": res['data']['stats']['links'],
             "people": res['data']['stats']['people'],
             "read": res['data']['stats']['read'],
             #"writing_visit": res['data']['stats']['writing_visit']['hist'][0],
             "direct": res['data']['stats']['direct'],
             "visits": res['data']['stats']['visits'],
             "recirc": res['data']['stats']['recirc'],
             "subscr": res['data']['stats']['subscr'],
             "article": res['data']['stats']['article'],
             #"pages": res['data']['stats']['pages'],
             "search": res['data']['stats']['search'],
             "crowd": res['data']['stats']['crowd'],
             #"domload": res['data']['stats']['domload']['hist'][0],
             #"visit": res['data']['stats']['visit']['hist'][0],
             "idle": res['data']['stats']['idle'],
             "internal": res['data']['stats']['internal'],
             "social": res['data']['stats']['social'],
             "new": res['data']['stats']['new'],
             #"scroll": res['data']['stats']['scroll']['hist'][0]
           }

        people_sum = 0
        time_sum = 0
        for time, people in enumerate(res['data']['stats']['domload']['hist']):
            time_sum += people*(time+1.0)
            people_sum += people

        data['domload'] = time_sum/people_sum

        # send the data
        try:
            for field, value in data.iteritems():
                # self.log.debug(data)
                tags = ['site:%s' % site]
                self.gauge('chartbeat.'+field, value, tags=tags)
        except ValueError:
            self.log.error("Failed to save data")
            return
