import requests
from lxml import html

base_url = "https://baraholka.onliner.by"
global_mess = None

def search_baraholka(query):
    r = requests.get(url=f"https://baraholka.onliner.by/search.php?q={query}&by=up&cat=1&topicTitle=1")
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
