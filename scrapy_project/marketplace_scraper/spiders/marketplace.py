import scrapy
from datetime import date


class MarketplaceSpider(scrapy.Spider):
    name = "marketplace"
    allowed_domains = ["localhost"]

    start_urls = [
        "http://localhost:8000/marketplace.html"
    ]

    def parse(self, response):

        for index, listing in enumerate(
            response.css("div.listing"),
            start=1
        ):

            title = listing.css("h2.title::text").get()
            price = listing.css("span.price::text").get()
            condition = listing.css("span.condition::text").get()
            seller = listing.css("span.seller::text").get()

            yield {
                "listing_id": f"LST-{index:04d}",
                "listing_title": title.strip() if title else None,
                "listed_price": self.clean_price(price),
                "condition": condition.strip() if condition else None,
                "seller": seller.strip() if seller else None,
                "listing_date": str(date.today()),
                "marketplace": "EchoChain Mock Marketplace"
            }

    def clean_price(self, price):

        if not price:
            return None

        return int(
            price.replace("₹", "")
                 .replace(",", "")
                 .strip()
        )