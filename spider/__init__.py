from spider.cbgspider import Spider
from spider.parse import Parse

class Engine:
    def __init__(self, url):
        self.spider = Spider(url)
        self.parse = Parse(self.spider.json_data)

    @property
    def get_parse_result(self):
        return self.parse.start_parse()

    @property
    def get_html(self):
        return self.spider.html

    @property
    def get_base_data(self):
        return self.spider.base_data



if __name__ == '__main__':
    # engine = Engine(r'https://xyq.cbg.163.com/equip?s=132&eid=201809032000113-132-DUW7DXJNIWED&view_loc=equip_list')
    # engine = Engine(r'https://xyq.cbg.163.com/equip?s=132&eid=201808302200113-132-YX9SVYZXJIRY&view_loc=equip_list')
    # engine = Engine(r'https://xyq.cbg.163.com/equip?s=482&eid=201809132100113-482-7SCLOBWBBM3W&view_loc=equip_list')
    engine = Engine(r'https://xyq.cbg.163.com/equip?s=482&eid=201808062200113-482-Y6CGKXZDUSER&view_loc=equip_list')
    print(engine.get_parse_result)
    print(engine.get_base_data)