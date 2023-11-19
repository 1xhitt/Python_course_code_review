import scrapy


class GnuscrapperSpider(scrapy.Spider):
    name = "gnuscrapper"
    allowed_domains = ["www.dns-shop.ru"]
    start_urls = ["https://www.d    ns-shop.ru/catalog/17a89aab16404e77/videokarty/"]

    def parse(self, response):
        cards = response.css('catalog-product')
        for card in cards:
            yield {
                'name':'',
                'price':'',
                'color':'',
                'color':'',
                'color':'',
                'color':'',
                'color':'',

            } 
        next_page = response.css('li.next a').attrib['href']
        
        if next_page is not None:
            if 'catalogue' in  next_page:
                next_page_url="https://books.toscrape.com/"+next_page
            else:
                next_page_url="https://books.toscrape.com/catalogue/"+next_page

        pass
