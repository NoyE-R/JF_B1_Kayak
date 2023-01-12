import os
import logging
import pandas as pd
import json
import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_user_agents

# generate the list of url needed for the spider
order = ['popularity', 'upsort_bh', 'class', 'distance_from_search', 'bayesian_review_score']

file = pd.read_csv('src/city_to_scrap.csv', header=None)
file.rename(columns={0:"ville"}, inplace=True)
ville = [ville for ville in file["ville"]]
list_url = []
for o in order:
    for v in ville:
        list_url.append("https://www.booking.com/searchresults.fr.html?ss=" + v + "&order=" + o)

class HotelSpider(scrapy.Spider):
    name = 'hotel'    
    start_urls = list_url

    def parse(self, response):
        name_hotel = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[*]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a[@data-testid="title-link"]/div[1]/text()').getall()      
        url_hotel = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[*]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a[@data-testid="title-link"]/@href').getall()
        
        yield {'url_tested': response.request.url,
               'name_hotel': name_hotel,
               'url_hotel': url_hotel
              }

# Name of the file where the results will be saved
filename = "list_hotel.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('kayak/src'):
        os.remove('kayak/src' + filename)
