import logging
import pandas as pd
import json
import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_user_agents

# generate the list of url needed for the spider
file = pd.read_csv("list_hotel_clean.csv")
list_url = [url.strip() for url in file["url_short"]]

class CarHotelSpider(scrapy.Spider):
    name = 'car_hotel'    
    start_urls = list_url

    def parse(self, response):
        description_hotel = response.xpath('//*[@id="property_description_content"]/p/text()').getall()
        score_hotel = response.xpath('//*[@data-testid="review-score-component"]/div[1]/text()').get()
        coordinates_hotel = response.xpath('//*[@id="hotel_sidebar_static_map"]').attrib["data-atlas-latlng"]
        address_hotel = response.xpath('//*[@id="showMap2"]/span[1]/text()').get()
        animals = response.xpath('//*[@id="hotelPoliciesInc"]/[-1]/text()').get()
        
        yield {'url_hotel': response.request.url,
                'description_hotel': description_hotel,
                'score_hotel': score_hotel,
                'coordinates_hotel': coordinates_hotel,
                'adresse_hotel': address_hotel,
                'animals_hotel': animals
                }