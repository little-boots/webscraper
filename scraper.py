from bs4 import BeautifulSoup as bs
import requests
import selenium
from splinter import Browser
import pandas as pd
import json


#############################
# Initialize selenium
#############################

executable_path = {'executable_path': '/usr/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)

#############################
# Scrape NASA.gov
#############################

def nasa():
    try:
        NASAurl = 'https://mars.nasa.gov/news'
        browser.visit(NASAurl)

        html = browser.html
        soup = bs(html, 'html.parser')

        newsTitle = soup.find('div', class_='image_and_description_container')\
                        .find('div', class_='list_text')\
                        .find('div', class_='content_title')\
                        .find('a')\
                        .text

        newsP = soup.find('div', class_='image_and_description_container')\
                    .find('div', class_='list_text')\
                    .find('div', class_='article_teaser_body')\
                    .text

        return newsTitle, newsP
    except:
        return None, None

#############################
# Scrape JPL.NASA.gov
#############################

def jpl():
    try:
        JPLurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

        browser.visit(JPLurl)
        browser.click_link_by_partial_text('FULL IMAGE')

        html = browser.html
        soup = bs(html, 'html.parser')

        imageLink = soup.find('img', class_='fancybox-image')['src']
        featuredImageURL = 'https://www.jpl.nasa.gov' + imageLink
        return featuredImageURL
    except:
        return None

#############################
# Scrape Twitter
#############################

def twitter():
    try:
        Twitterurl = 'https://twitter.com/marswxreport?lang=en'

        browser.visit(Twitterurl)
        html = browser.html
        soup = bs(html, 'html.parser')

        weatherTweet = soup.find('p', class_='tweet-text').text
        return weatherTweet
    except:
        return None

#############################
# Scrape Space-Facts
#############################

def spacefacts():
    try:
        MarsFactsurl = 'https://space-facts.com/mars'
        tables = pd.read_html(MarsFactsurl)

        #earthcompare = tables[0]
        marsfacts    = tables[1]

        marsfactshtml = marsfacts.to_html()
        return marsfactshtml
    except:
        return None

#############################
# Scrape USGS
#############################

def usgs():
    try:
        USGSurl =\
            'https://astrogeology.usgs.gov/search/' + \
            'results?q=hemisphere+enhanced&c1=target&v1=Mars'

        browser.visit(USGSurl)
        html = browser.html
        soup = bs(html, 'html.parser')

        links = soup.find('div', class_='results').find_all('a')
        image_dict = {}

        lwt = [link for link in links if link.text]

        for link in lwt:
            text = link.text
            url  = 'https://astrogeology.usgs.gov' + link['href']

            browser.visit(url)
            html = browser.html
            soup = bs(html, 'html.parser')

            dl_links = soup.find('div', class_='downloads').find_all('a')

            for dl_link in dl_links:
                if dl_link.text == 'Original':
                    img_link = dl_link['href']
                    image_dict[text] = img_link

        return image_dict
    except:
        return None

def Scrape():
    newsTitle, newsP = nasa()
    featuredImageURL = jpl()
    weatherTweet = twitter()
    marsfactshtml = spacefacts()
    image_dict = usgs()

    scrape_dict = {
        'newsTitle': newsTitle,
        'newsP': newsP,
        'featuredImageURL': featuredImageURL,
        'weatherTweet': weatherTweet,
        'marsfactshtml': marsfactshtml,
        'image_dict': image_dict
    }

    return scrape_dict

print(Scrape())
