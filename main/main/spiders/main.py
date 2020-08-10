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
        page = response.url.split("/")[-2]
        filename = 'task3-%s.html' % page
        result = response.xpath('//script[contains(.,"title")]/text()').extract()
        title = re.compile('"title":"(.*?)"')
        locality = re.compile('"addressLocality":"(.*?)"')
        region = re.compile('"addressRegion":"(.*?)"')
        country = re.compile('"addressCountry":"(.*?)"')
        comp_name = re.compile('"name":"(.*?)"')
        logo = re.compile('"logo":"(.*?)"')
        skills = re.compile('"skills":\[(.*?)]')
        benefits = re.compile('"jobBenefits":\[(.*?)]')
        about = re.compile('"description":"<h2>(.*?)<h2>')

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
              #str(locality.search(result[0]).group(1))
               #             + ", " + str(region.search(result[0]).group(1))
                #            + ", " + str(country.search(result[0]).group(1)),
            'Skills Required': skills.search(result[0]).group(1),
            'Perks offered': response.xpath(
                '//section[contains(., "Benefits")]/ul//span/text()'
                ).extract(),
                #benefits.search(result[0]).group(1),

            'About This Job': response.xpath(
                '//section[contains(., "About this job")]//span/text()'
                ).extract(),
                #about.search(result[0]).group(1),

            'Description': ''.join(response.xpath(
                '//section[contains(., "Job description")]/div/ul//text()'
                ).getall()),

            'Job Link': response.url,
        }

