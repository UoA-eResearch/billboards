import scrapy
import json

class LumoSpider(scrapy.Spider):
    name = 'lumo'
    allowed_domains = ['lumodigital.nz']
    start_urls = ['https://lumodigital.nz/our-sites/']

    def parse(self, response):
        anchors = response.css("a.sites-item")
        yield from response.follow_all(anchors, self.parse)

        if response.url.startswith("https://lumodigital.nz/site/"):
            title = response.css("h1.site-title::text").get()
            image = response.css("div.images img::attr(src)").get()
            address = response.css(".site-content-title::text").get()
            description = response.css(".site-content-content>::text").get()

            specs = response.css("table.key-specs-table tr")
            details = []
            for row in specs:
                details.append(": ".join(e.strip(":") for e in row.css("td::text").getall()))

            pattern = r'position:\s*{lat:\s*(-\d+.\d+),\s*lng:\s*(\d+.\d+)'
            latlong = response.css('script::text').re(pattern)

            yield dict(title=title, image=image, address=address, description=description, details=details, url=response.url, latitude=float(latlong[0]), longitude=float(latlong[1]))
