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
    result = f'{title[0]} {date[0]}\n'
    if len(departures):
        for i in range(len(departures)):
            result += f'{"🔴" if types[i][0].lower() == "г" else "🔷"} {departures[i]}\n'
    else:
        result += f'Нет поездов'
    return result
