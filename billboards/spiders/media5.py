#-*- coding: utf-8 -*-

import scrapy
import json
from lxml import html

def strip_html(s):
    return str(html.fromstring(s).text_content())

def try_cast_float(s):
    try:
        return float(string)
    except:
        return None


class Media5Spider(scrapy.Spider):
    name = 'media5'
    allowed_domains = ['media5.co.nz']
    start_urls = ['http://media5.co.nz/our-portfolio/']

    def parse(self, response):
        anchors = response.css("h2.fusion-post-title a") # cards / billboards
        yield from response.follow_all(anchors, callback=self.parse)

        if response.url.startswith("http://media5.co.nz/billboards/"):
            title = response.css("h1.entry-title::text").get().replace("–", "-")
            image = response.css(".fusion-flexslider a::attr(href)").get()
            description = response.css(".fusion-text p::text").get()
            if description:
                description = description.replace(u"\u00A0", " ").replace("–", "-").replace("’", "'").replace("×", "x").replace("“", '"').replace('”','"')
            categories = response.css(".project-terms a::text").getall()
            details = response.css(".fusion-text p::text").getall()

            result = dict(
                title=title,
                image=image,
                description=description,
                categories=categories,
                details=details,
                url=response.url
            )

            pattern = r'addresses: (.+),'
            json_data = response.css('script::text').re_first(pattern)
            if json_data:
                address = json.loads(json_data)[0]
                result["address"] = strip_html(address.get("address")).replace("Get directions", "").strip()
                result["latitude"] = try_cast_float(address.get("latitude"))
                result["longitude"] = try_cast_float(address.get("longitude"))

            yield result