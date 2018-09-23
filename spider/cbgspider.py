import json
import re
import requests
from lxml import etree

class Spider:
    def __init__(self, url):
        self.url = url
        self.base_data = None
        self.json_data = None
        self.xml = None

        self.session = requests.session()
        self.html = self.get_html()
        self.get_base()
        self.get_json()

    def get_html(self):
        result = self.session.get(self.url)
        result = self.session.get(self.url)
        result.encoding = 'gbk'
        return result.text

    def _get_html_by_xml(self):
        if self.xml is None:
            self.xml = etree.HTML(self.html)
        return self.xml

    def get_json(self):
        html = self._get_html_by_xml()
        data = html.xpath(".//textarea[@id='equip_desc_value']/text()")[0]
        data = data.replace('([',
                    '{').replace('])', '}').replace('({',
                    '[').replace('})', ']').replace(',}',
                    '}').replace(',]',']')

        def fun(s):
            old = s.groups()[0]
            return '"' + old + '' + '":'

        result = re.sub(r'(\d+):', fun, data[1:-1])

        self.json_data = json.loads(result)

    def get_base(self):
        base_data = re.findall('<script>.*?var\s*?equip\s*?=\s*?({.*?});',
                               self.html, re.DOTALL)[0].replace('\n\t',
                                                                '').replace('\n', '').replace(
            'safe_json_decode(\'null\')', '0')

        self.base_data = json.loads(base_data)