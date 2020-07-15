import scrapy
import shutil
import time
import os
from scrapy.crawler import CrawlerProcess

class CoverSpider(scrapy.Spider):
    name = "pyimagesearch-cover-spider"
    start_urls = ["https://magpi.raspberrypi.org/issues"]

    try:
        shutil.rmtree('./filestore')
        print("removing old filestore")
    except OSError:
        pass

    time.sleep(0.5)

    try:
        os.makedirs('./filestore')
        print("making new filestore")
    except OSError:
        pass

    def parse(self, response):
        links = response.xpath("//*[@class='c-link']//img/@src").getall()

        for image_url in links:

            yield response.follow(
                url=image_url,
                callback=self.scrape_image
            )

    def scrape_image(self,response):
        file_name = response.url.split("?")[0].split("/")[-1]
        with open("filestore/" + file_name,'wb') as f:
            f.write(response.body)

#  main driver #
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CoverSpider)
    process.start()
