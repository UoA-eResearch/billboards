import scrapy
import json


class PhantomSpider(scrapy.Spider):
    name = 'phantom'
    start_urls = ['https://maps.0800phantom.co.nz/public/sites-map']

    def parse(self, response):
        data = response.css("#map::attr(data-locations)").get()
        data = json.loads(data)
        for l in data:
            yield dict(title=f"{l['code']} - {l['loadedPrice']}", latitude=l["lat"], longitude=l["lng"], description=l["fullAddress"], url="https://maps.0800phantom.co.nz/public/sites-map", image="https://maps.0800phantom.co.nz" + l['preview'])
