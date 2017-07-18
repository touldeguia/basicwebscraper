#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 12:09:48 2017

@author: toul
"""

import requests, os, bs4
url = 'http://xkcd.com'  #URL
os.chdir('/Users/toul/Code')
os.makedirs('xkcd', exist_ok=True) # storing comics 
while not url.endswith('#'):
    #TODO: download the page
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    
    soup = bs4.BeautifulSoup(res.text, "lxml")
    
   
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        try:
            comicUrl =  'http:' + comicElem[0].get('src')   
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()
        except requests.exceptions.MissingSchema:    
       # skip if not a normal image file
            prev = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prev.get('href')
            continue
        
        imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(1000000):
            imageFile.write(chunk)
        imageFile.close()

        prevLink = soup.select('a[rel="prev"]')[0]
        url = 'http://xkcd.com' + prevLink.get('href')
    
    
print('Done.. ')

