import requests
from lxml import html

def get_trains(url):
    ra = requests.get(url=url)
    ra_html = html.fromstring(ra.content)
    title = ra_html.xpath('//div[@class="sch-title__title h2"]/text()')
    date = ra_html.xpath('//div[@class="sch-title__date h3"]/text()')
    types = ra_html.xpath(
        '//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__train-type"]/span[@class="sch-table__route-type"]/text()')
    departures = ra_html.xpath(
        '//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__time train-from-time"]/text()')
    lenght = len(departures) if len(departures) < 3 else 3
    result = f'{title[0]} {date[0]}\n'
    for i in range(lenght):
        result += f'{departures[i]} {types[i][:3]}\n'
    return result
