import scrapy
import re


class QuotesSpider(scrapy.Spider):
    name = 'task3'
    start_urls = [
        # 'https://stackoverflow.com/jobs?q=blockchain',
    ]

    def __init__(self, skill='blockchain', location='Boston USA', *args, **kwargs):
        self.start_urls.append(f'https://stackoverflow.com/jobs?q={skill}&l={location}&d=20&u=Km')
        super().__init__(*args, **kwargs)

    def parse(self, response):
        for res in response.xpath('//a[@class = "s-link stretched-link"]'):
            next_i = res.xpath('@href').extract()
            print(next_i)
            yield scrapy.Request(response.urljoin(str(next_i[0])), callback=self.parse_data)

    def parse_data(self, response):
        result = response.xpath('//script[contains(.,"title")]/text()').extract()
        title = re.compile('"title":"(.*?)"')
        comp_name = re.compile('"name":"(.*?)"')
        # logo = re.compile('"logo":"(.*?)"')
        skills = re.compile('"skills":\[(.*?)]')

        yield {
            'Job title': title.search(result[0]).group(1),

            'Company': comp_name.search(result[0]).group(1),

            'Company\'s logo Image Url': response.xpath(
                '''normalize-space(//header[@class="job-details--header grid mb24 gs12 gsx sm:fd-column sm:ta-center"]
                //img/@src)'''
                ).extract(),
            #logo.search(result[0]).group(1),

            'Location': response.xpath(
                '''normalize-space(//header[@class="job-details--header grid mb24 gs12 gsx sm:fd-column sm:ta-center"]
                //span[@class="fc-black-500"]/text())'''
                ).get(),

            'Skills Required': skills.search(result[0]).group(1),
            'Perks offered': response.xpath(
                '//section[contains(., "Benefits")]/ul//span/text()'
                ).extract(),

            'About This Job': response.xpath(
                '//section[contains(., "About this job")]//span/text()'
                ).extract(),

            'Description': ''.join(response.xpath(
                '//section[contains(., "Job description")]/div/ul//text()'
                ).getall()),

            'Job Link': response.url,
        }

