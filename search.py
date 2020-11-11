# -*- coding: utf-8 -*-
import requests
from lxml import html

global_mess = None
is_searching = True


def search(query):
    result = []
    r = requests.get(url=f'https://baraholka.onliner.by/search.php?q={query}&by=up&cat=1&topicTitle=1')
    r_html = html.fromstring(r.content)
    links = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//span[@class="img-va"]//a/@href')
    titles = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//h2[@class="wraptxt"]//a/text()')
    prices = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//div[@class="price-primary"]/text()')

    for i in range(len(links) if len(links) < 3 else 3):
        result.append([f'https://baraholka.onliner.by{links[i]}', titles[i], prices[i]])

    r = requests.get(url=f'https://www.kufar.by/listings?ot=1&rgn=7&query={query}')
    r_html = html.fromstring(r.content.decode('utf-8', 'ignore'))
    links = r_html.xpath('//article/div/a/@href')
    titles = r_html.xpath('//article/div/a/div/img/@alt')
    prices = r_html.xpath('//article/div/a/div/div/div/div/span/text()')

    for i in range(len(links) if len(links) < 3 else 3):
        result.append([links[i], titles[i], prices[i]])

    print(result)

    return result
