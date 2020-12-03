import requests
from lxml import html
from pandas import DataFrame


# r = requests.get(f'http://www.wikicfp.com/cfp/allcfp?&page=1')
# r_html = html.fromstring(r.content)
# print(r_html.xpath("//form[@name='myform']//tr[3]//a/@href"))


def get_links():
    links = []
    for i in range(1, 10):
        r = requests.get(f'http://www.wikicfp.com/cfp/allcfp?&page={i}')
        r_html = html.fromstring(r.content)
        link = r_html.xpath("//form[@name='myform']//tr[3]//a/@href")
        links.extend(link)
    return links


def get_fields_from_links(links):
    all_conferences = []
    for link in links:
        r = requests.get(f'http://www.wikicfp.com{link}')
        r_html = html.fromstring(r.content)
        link = r_html.xpath("(//tr[3]//a)[1]/@href")[0].strip()
        description = r_html.xpath("//span[@property='v:description']/text()")[0].strip()
        when = r_html.xpath("(//table[@class='gglu'])[1]//tr[1]//td/text()")[0].strip()
        if when != "N/A":
            whenfrom = when.split(' - ')[0]
            whento = when.split(' - ')[0]
        else:
            whenfrom = "N/A"
            whento = "N/A"
        where = r_html.xpath("(//table[@class='gglu'])[1]//tr[2]//td/text()")[0].strip()
        deadline = r_html.xpath("(//table[@class='gglu'])[1]//tr[3]//span[@property='v:startDate']/text()")
        deadline = deadline[0].strip() if deadline else "N/A"
        notification = r_html.xpath("(//table[@class='gglu'])[1]//tr[4]//span[@property='v:startDate']/text()")
        notification = notification[0].strip() if notification else "N/A"
        categories = r_html.xpath("(//table[@class='gglu'])[2]//h5/a[not(@class='blackbold')]/text()")
        categories = '; '.join(str(e) for e in categories) if categories else "N/A"
        conference = [link, description, whenfrom, whento, where, deadline, notification, categories]
        all_conferences.append(conference)
    return all_conferences


def save_to_spreadsheet(all_conferences):
    links = []
    descriptions = []
    whens_from = []
    whens_to = []
    wheres = []
    deadlines = []
    notifications = []
    categories = []
    for row in all_conferences:
        print(row)
    for row in all_conferences:
        links.append(row[0])
        descriptions.append(row[1])
        whens_from.append(row[2])
        whens_to.append(row[3])
        wheres.append(row[4])
        deadlines.append(row[5])
        notifications.append(row[6])
        categories.append(row[7])
    df = DataFrame({'Link': links, 'Description': descriptions, 'Starts': whens_from, 'Ends': whens_to, 'Where': wheres, 'Deadline': deadlines,
                    'Notification': notifications, 'Categories': categories})
    df.to_excel('test.xlsx', sheet_name='sheet1', index=False)


links = get_links()
all_conferences = get_fields_from_links(links=links)
print(f'============= {all_conferences}')
save_to_spreadsheet(all_conferences)
