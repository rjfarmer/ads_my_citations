# ads_my_citations
Make an RSS feed of papers that cites your papers

Will need:

````bash
pip3 install ads feedgen
````

apache installed and running

An ADS key from:

* https://ui.adsabs.harvard.edu/#user/settings/token

Stored in file

````bash
 ~/.ads/dev_key 
````

Create file 

````bash
~/.ads/orcid
````

with your ORCID number.

Edit ads\_rss.py and set your home folder.

Run with:

````bash
sudo python3 ads_rss.py
````

I would recommend you set up a cron job to re-run daily

Point firefox to:

````bash
feed:///localhost/ads_rss_feed.xml
````
OR chrome, first install a rss feed reader and add:

````bash
localhost/ads_rss_feed.xml
````

Profit!
