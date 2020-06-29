import scrapy
from w3lib.html import remove_tags

def try_cast_float(s):
    try:
        return float(s)
    except:
        return s

class GomediaSpider(scrapy.Spider):
    name = 'gomedia'
    allowed_domains = ['gomedia.co.nz']
    start_urls = ['http://www.gomedia.co.nz/?s=']

    def parse_details(self, response):
        if response.url.startswith("https://www.gomedia.co.nz/billboard/"):
            title = response.css("h1.title::text").get()
            image = response.css("div.imgholder img::attr(src)").get()
            description = response.css("div.billdesc p::text").get()
            stats = response.css("div.stats p")
            details = []
            for stat in stats:
                details.append(": ".join(stat.css("::text").getall()))

            latlong = response.meta["latlong"]

            yield dict(title=title, description=description, image=image, details=details, url=response.url, latitude=try_cast_float(latlong[0]), longitude=try_cast_float(latlong[1]))

    def parse(self, response):
        cards = response.css("div.hoverstate")
        for card in cards:
            latlong = card.attrib["data-coords"].split(";")
            yield response.follow(card.attrib["rel"], callback=self.parse_details, meta={'latlong': latlong})
