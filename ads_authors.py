#!/usr/bin/env python3

import ads as ads
from feedgen.feed import FeedGenerator
import urllib

HOME_FOLDER="/home/rob/"

with open(HOME_FOLDER+".ads/orcid") as f:
	token=f.readline()

ORCID=token

RSS_FILE="/var/www/html/ads_authors.xml"
BASE_URL="http://adsabs.harvard.edu/abs/"
MAX_NUM=100

with open(HOME_FOLDER+".ads/dev_key") as f:
	token=f.readline()

ads.config.token=token.strip()

authors=["de mink, s","Timmes,f","kolb, u", "fields, c","petermann, i",
		"woosley, s", "heger, a","bildsten, l", "townsend, r","schwab, j",
		"marchant, p","dessart, l","Gotberg, Ylva","Renzo, Mathieu"]

#Get papers
allp=[]
for i in authors:
	papers=ads.SearchQuery(author=i,
						fl=['title','pubdate','bibcode'],
						rows=50,
						sort='pubdate')
	for p in papers:
		allp.append({'title':p.title[0],'bibcode':p.bibcode,'pub':p.pubdate})


#Dedup
allp=[dict(y) for y in set(tuple(x.items()) for x in allp)]

#Most recent first
allp=sorted(allp,key=lambda k:k['pub'], reverse=True)

#truncate
allp=allp[:MAX_NUM]


#Make RSS feed
fg = FeedGenerator()
fg.id(BASE_URL)
fg.link(href=BASE_URL,rel='self')
#fg.link(href=BASE_URL,rel='alternate')
fg.title('ADS citation feed')
fg.author( {'name':'abc','email':'abc@fake.com'} )
fg.logo('')
fg.subtitle('RSS feed of my ads authors')
fg.language('en')

for i in allp:
	fe=fg.add_entry()
	fe.id(BASE_URL+i['bibcode'])
	fe.link(href=BASE_URL+i['bibcode'])
	fe.title(i['title'])

rssfeed  = fg.rss_str(pretty=True)
fg.rss_file(RSS_FILE)
