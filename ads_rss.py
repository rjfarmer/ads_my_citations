#!/usr/bin/env python3

import ads as ads
from feedgen.feed import FeedGenerator
import urllib

HOME_FOLDER="/home/rob/"

with open(HOME_FOLDER+".ads/orcid") as f:
	token=f.readline()
ORCID=token

RSS_FILE="/var/www/html/ads_rss_feed.xml"
BASE_URL="http://adsabs.harvard.edu/abs/"
CUR_YEAR='2017'
MAX_NUM=100

with open(HOME_FOLDER+".ads/dev_key") as f:
	token=f.readline()

ads.config.token=token.strip()

#Get my papers
papers=ads.SearchQuery(orcid_user=ORCID,fl=['citation'])

#get the bibcodes for citations to my papers
all_cites=[]
for p in papers:
	if p.citation is not None:
		all_cites.extend(p.citation)

#Uniquify the list
all_cites=list(set(all_cites))

#Sort papers bibcodes
all_cites.sort()

#Reverse so most recet first
all_cites=all_cites[::-1]

#Limit the number
sub_cites=all_cites[:MAX_NUM]

papers=[]
#Get each paper that cited one of my papers
for bibcode in sub_cites:
	x=list(ads.SearchQuery(bibcode=bibcode,fl=['title','bibcode','pubdate']))
	#Some arixvs dont seem to return properly
	if len(x)>0:
		papers.append(x[0])

#Extract info
allp=[]
for p in papers:
	allp.append({'title':p.title,'bibcode':p.bibcode,'pub':p.pubdate})

#Most recent first
allp=sorted(allp,key=lambda k:k['pub'], reverse=True)

#Make RSS feed
fg = FeedGenerator()
fg.id(BASE_URL)
fg.link(href=BASE_URL,rel='self')
#fg.link(href=BASE_URL,rel='alternate')
fg.title('ADS citation feed')
fg.author( {'name':'abc','email':'abc@fake.com'} )
fg.logo('')
fg.subtitle('RSS feed of my ads citations')
fg.language('en')

for i in allp:
	fe=fg.add_entry()
	fe.id(BASE_URL+i['bibcode'])
	fe.link(href=BASE_URL+i['bibcode'])
	fe.title(i['title'][0])

rssfeed  = fg.rss_str(pretty=True)
fg.rss_file(RSS_FILE)

