from lxml import html

import requests

ra = requests.get("https://pass.rw.by/ru/route/?from=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&from_exp=2100450&from_esr=140102&to=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&to_exp=&to_esr=&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=2020-10-26")
ra_html = html.fromstring(ra.content)
types = ra_html.xpath('//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__train-type"]/span[@class="sch-table__route-type"]/text()')
departures = ra_html.xpath('//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__time train-from-time"]/text()')
for i in range(len(departures)):
    print(f'{departures[i]} {types[i][:3]}')
