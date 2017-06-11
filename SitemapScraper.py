import requests, json, webbrowser
from bs4 import BeautifulSoup
from lxml import etree

from colorama import init
init()


from classes.logger import logger

log = logger().log

class scraper:
    def __init__(self, siteURL):
        self.siteURL = siteURL

    def getSitemap(self):
        log('Grabbing Sitemap', 'info')
        sitemapURL = self.siteURL + '/sitemap_products_1.xml'
        sitemapXML = requests.get(sitemapURL)
        root = etree.fromstring(sitemapXML.content)
        root = list(root)
        del root[:1]

        productsLoaded = []
        productsFound = 0

        for item in root:
            try:
                productData = {
					"title" : item[3][1].text,
					"url" : item[0].text,
					"image" : item[3][0].text,
				}

                productsLoaded.append(productData)
                productsFound += 1

            except:
                pass


        log('Got {} Products From Sitemap'.format(str(productsFound)), 'success')

        return productsLoaded

    def matchKeywords(self, itemTitle, keywords):
		keywords = keywords.split(' ')
		if all(i.lower() in itemTitle.lower() for i in keywords):
			return True
		return False

    def keywordSearch(self, productsLoaded, keywords):
        log('Searching For {}...'.format(keywords), 'info')
        for item in productsLoaded:
            if self.matchKeywords(item['title'], keywords):
                log('Found {} At - {}'.format(item['title'], item['url']), 'success')
                return item

    def getVariants(self, itemData):
        log('Grabbing Variants', 'info')
        itemURL = itemData['url'] + '.json'

        resp = requests.get(itemURL)

        itemJSON = resp.json()

        for item in itemJSON['product']['variants']:
            log('{} - {}'.format(str(item['title']), str(item['id'])), 'info')

        log('Retrieved All Variants!', 'success')

        return itemJSON['product']['variants']

    def selectSize(self, variants):
        while True:
            selectedSize = raw_input('Select Size: ')

            for item in variants:
                if str(item['title']) == str(selectedSize):
                    return item

            log('{} Is Not A Valid Size', 'warning')
            print

    def openCheckout(self, variant):
        log('Opening Browser For Size - {}'.format(str(size['title'])), 'info')
        atcURL = self.siteURL + '/cart/{}:1'.format(str(size['id']))

        webbrowser.open(atcURL)
        log('Opened Browser!', 'success')

log('Sitemap Scraper - @Joshuab_33', 'info')
log('Log Class BY @eggins', 'info')

siteURL = raw_input('Site URL including HTTP:// ')
keywords = raw_input('Keywords (seperated by a spaxc): ')
s = scraper(siteURL)

productsLoaded = s.getSitemap()

itemInfo = s.keywordSearch(productsLoaded, keywords)

variants = s.getVariants(itemInfo)

size = s.selectSize(variants)

s.openCheckout(size)

raw_input('Press Enter To Exit!')
