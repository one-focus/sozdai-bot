import requests
from lxml import html

base_url = "https://baraholka.onliner.by"
global_mess = None
search_results = None


def search_baraholka(query):
    r = requests.get(url=f'https://baraholka.onliner.by/search.php?q={query}&by=up&cat=1&topicTitle=1')
    r_html = html.fromstring(r.content)
    icon = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//span[@class="img-va"]//img')
    link = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//span[@class="img-va"]//a')
    title = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//h2[@class="wraptxt"]//a/text()')
    desc = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//h2[@class="wraptxt"]/../p[2]/text()')
    price = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//div[@class="price-primary"]/text()')
    result = []
    for i in range(len(icon) if len(icon) < 5 else 5):
        result.append([icon[i].get("src").split("/icon/")[1], title[i], desc[i], price[i]])
    return result


def search_kufar(query):
    r = requests.get(url=f'https://www.kufar.by/listings?ot=1&query={query}')
    r_html = html.fromstring(r.content)
    links = r_html.xpath('//article/div/a/@href')
    titles = r_html.xpath('//article/div/a/div/img')
    # desc = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//h2[@class="wraptxt"]/../p[2]/text()')
    # price = r_html.xpath('//table[@class="ba-tbl-list__table"]/tr[not(@class)]//div[@class="price-primary"]/text()')
    # result = []
    # for i in range(len(link) if len(link) < 5 else 5):
    #     result.append([link[i].get("href"), title[i], desc[i], price[i]])
    # return result

    print(links)

    [print('title: {}'.format(title.get("alt"))) for title in titles]


search_kufar("холодильник")
