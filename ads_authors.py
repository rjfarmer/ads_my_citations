#!/usr/bin/env python3

import ads as ads
import os
from feedgen.feed import FeedGenerator
import urllib
from time import sleep

HOME_FOLDER="/home/rob/"

with open(HOME_FOLDER+".ads/orcid") as f:
	token=f.readline()

ORCID=token

RSS_FILE="/var/www/html/ads_authors.xml"
BASE_URL="https://ui.adsabs.harvard.edu/#abs/"
MAX_NUM=100

with open(os.path.join(HOME_FOLDER,".ads/dev_key")) as f:
	token=f.readline()

ads.config.token=token.strip()

authors=["de mink, selma","Timmes,f","kolb, ulrich", "fields, carl","petermann, ilka",
		"woosley, stan", "heger, alex","bildsten, lars", "townsend, richard","schwab, josiah","paxton, bill"
		"marchant, pablo","dessart, luca","Gotberg, Ylva","Renzo, Mathieu","Mandel, Ilya","Phinney, Sterl",
		"Podsiadlowski, Philipp","Justham, Stephen","Fryer, chris", "patton, kelly"]

#Get papers
allp=[]
for i in authors:
	papers=ads.SearchQuery(author=i,
						fl=['title','pubdate','bibcode'],
						rows=50,
						sort='pubdate')
	for p in papers:
		allp.append({'title':p.title[0],'bibcode':p.bibcode,'pub':p.pubdate})
		sleep(0.01)


#Dedup
allp=[dict(y) for y in set(tuple(x.items()) for x in allp)]

#Most recent first
allp=sorted(allp,key=lambda k:k['pub'], reverse=False)

#truncate
allp=allp[len(allp)-MAX_NUM:]


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

