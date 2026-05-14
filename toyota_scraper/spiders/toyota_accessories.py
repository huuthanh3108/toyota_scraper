import scrapy
from datetime import datetime
from crawlab import save_item

class ToyotaAccessorySpider(scrapy.Spider):
    name = "toyota_accessories"
    allowed_domains = ["danang.toyota.com.vn"]
    start_urls = [
        "https://danang.toyota.com.vn/phu-tung-phu-kien-chinh-hang?p=1"
    ]

    def parse(self, response):
        products = response.css("div.phukien-home")

        for product in products:
            result = {
                "name": product.css(".description h4::text").get(default="").strip(),
                "price": product.css(".price-phukien span::text").get(default="").strip(),
                "image": product.css(".img img::attr(data-src)").get(),
                "url": response.urljoin(
                    product.css(".img img::attr(data-src)").get()
                ),
                "crawl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_item(result)

        # pagination
        next_page = response.css("ul.pagination li:last-child[class~='action'] a::attr(href)").get(default=None)
        print("NEXT:", next_page)
        if next_page:
            yield response.follow(next_page.strip(), callback=self.parse)
