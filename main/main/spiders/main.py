import scrapy


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
            break

    def parse_data(self, response):
        page = response.url.split("/")[-2]
        filename = 'task3-%s.html' % page
        result = response.xpath('//script[contains(.,"title")]/text()').extract()
        yield {
            'title': result[0]
        }
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        #

        # for quote in response.css('div.quote'):
        #     yield {
        #         # 'Job':
        #         # 'Title':
        #         # 'Company':
        #         # 'Company':
        #         # 'logo’s':
        #         # 'image_url':
        #         # 'Location':
        #         # 'Skills required':
        #         # 'Perks offered':
        #         # 'About':
        #         # 'this':
        #         # 'job':
        #         # 'Description':
        #         # 'Job':
        #         # 'link':
        #
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }
