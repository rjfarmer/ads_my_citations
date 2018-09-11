#!/usr/bin/env python3

import ads as ads
from feedgen.feed import FeedGenerator
from time import sleep

HOME_FOLDER="/home/rob/"

with open(HOME_FOLDER+".ads/orcid") as f:
	token=f.readline()

ORCID=token.strip()

RSS_FILE="/var/www/html/ads_mesa_feed.xml"
BASE_URL="https://ui.adsabs.harvard.edu/#abs/"
MAX_NUM=100

MESA_BIBS=["2011ApJS..192....3P","2013ApJS..208....4P","2015ApJS..220...15P","2018ApJS..234...34P"]


with open(HOME_FOLDER+".ads/dev_key") as f:
	token=f.readline()

ads.config.token=token.strip()

#Get MESA papers
papers=[list(ads.SearchQuery(bibcode=bibcode,fl=['citation']))[0] for bibcode in MESA_BIBS]


#get the bibcodes for citations to MESA papers
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
#Get each paper that cited a MESA paper
for bibcode in sub_cites:
	try:
		x=list(ads.SearchQuery(bibcode=bibcode,fl=['title','bibcode','pubdate']))
		#Some arixvs dont seem to return properly
		if len(x)>0:
			papers.append(x[0])
		sleep(0.01)
	except:
		pass

#Extract info
allp=[]
for p in papers:
	allp.append({'title':p.title[0],'bibcode':p.bibcode,'pub':p.pubdate})

#Most recent first
allp=sorted(allp,key=lambda k:k['pub'], reverse=False)

#Make RSS feed
fg = FeedGenerator()
fg.id(BASE_URL)
fg.link(href=BASE_URL,rel='self')
#fg.link(href=BASE_URL,rel='alternate')
fg.title('MESA ADS citation feed')
fg.author( {'name':'abc','email':'abc@fake.com'} )
fg.logo('')
fg.subtitle('RSS feed of MESA citations')
fg.language('en')

for i in allp:
	fe=fg.add_entry()
	fe.id(BASE_URL+i['bibcode'])
	fe.link(href=BASE_URL+i['bibcode'])
	fe.title(i['title'])

rssfeed  = fg.rss_str(pretty=True)
fg.rss_file(RSS_FILE)

