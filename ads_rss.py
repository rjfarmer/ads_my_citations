#!/usr/bin/env python3

import ads as ads
from feedgen.feed import FeedGenerator
import urllib

HOME_FOLDER="/home/rob/"
ORCID="0000-0003-3441-7624"

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

all_cites.sort()

#Only recent ones
this_year=[i for i in all_cites if i.startswith(CUR_YEAR)]

#Limit the number
this_year=this_year[:MAX_NUM]

#Get the each paper that cited my paper
papers=[list(ads.SearchQuery(bibcode=bibcode,fl=['title','bibcode','pubdate']))[0] for bibcode in this_year]

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
fg.subtitle('RSS feed of ads citations')
fg.language('en')

for i in allp:
	fe=fg.add_entry()
	fe.id(BASE_URL+i['bibcode'])
	fe.link(href=BASE_URL+i['bibcode'])
	fe.title(i['title'][0])

rssfeed  = fg.rss_str(pretty=True)
fg.rss_file(RSS_FILE)

