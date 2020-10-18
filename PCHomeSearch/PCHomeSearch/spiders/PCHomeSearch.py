import scrapy
import json
import urllib

from PCHomeSearch.items import PchomesearchItem

class PCHomeSearch(scrapy.Spider):
    name = "PCHomeSearch"

    def __init__(self, keyword='', p='', *args, **kwargs):
        super(PCHomeSearch, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.p = p

    def start_requests(self):

        #urls = []
        #for i in range(1,2):
        #   str_idx = ''+('%s' % i)
        #   urls.append('http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=iphone&page='+str_idx+'&sort=rnk/dc')
        
        urls = []
        for i in range(1,int(self.p)):
            str_idx = ''+('%s' % i)
            urls.append('https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+urllib.parse.quote(self.keyword)+'&page='+str_idx+'&sort=rnk/dc')

        #urls = [
        #    'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=iphone&page=1&sort=rnk/dc',
        #]
        for url in urls:
            print (url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_data = json.loads(response.body.decode('utf-8'))

        item = PchomesearchItem()
        for json_array in json_data["prods"]:
            item['title'] = json_array["name"]
            item['link'] = "http://24h.pchome.com.tw/prod/"+json_array["Id"]
            item['price'] = json_array["price"]
            yield item
            
        print('\n')
        self.log('HTML %s loaded' % response.url)