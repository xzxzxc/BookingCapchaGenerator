from selenium import webdriver
from scrapy import Spider, Item
from scrapy.pipelines.images import ImagesPipeline

items_count = 1
audios_count = 5

class TestSpider(Spider):
    name = "booking"
    startUrl = 'https://booking.uz.gov.ua/en/?from=2200001&to=2218000&date=2019-08-12&time=00%3A00&url=train-list'
    startUrls = [self.startUrl]

    def __init__(self):
        Spider.__init__(self)
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)

        for i in range(0, items_count):
            img_url = response.css('div.input > img').get().attrib['src']
            yield {'image_urls': [img_url]}

            for j in range(0, audios_count):
                audio_url = response.css('audio > source.wav').get().attrib['src']
                yield {'file_urls': [audio_url]}

            #yield response.follow(next_page, self.parse)

    