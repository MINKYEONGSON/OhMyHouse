from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import datetime


def get_data():
    #: url

    params = urllib.parse.urlencode({'multi_itm_seq': 1, 'srchTp': 0, 'srchWord': '모집'}).encode('utf-8')
    req = urllib.request.Request(url='https://www.i-sh.co.kr/main/lay2/program/S1T294C296/www/brd/m_244/list.do')
    # req.set_proxy('127.0.0.1:8080', 'http')
    f = urllib.request.urlopen(req, data=params)
    html_doc = f.read().decode('UTF-8')

    #: parse
    article = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    #print(soup.prettify())
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    articleLink = '<a href="https://www.i-sh.co.kr/main/lay2/program/S1T294C296/www/brd/m_244/view.do?seq=%s">%s</a>'
    for tr in rows:
        date = str(tr.find_all('td')[3].get_text())
        date_tmp = date.replace('\t', '').replace('\r\n', '')
        tmp = date_tmp.split('-')
        date_str = datetime.date(year=int(tmp[0]), month=int(tmp[1]), day=int(tmp[2]))
        today = datetime.date.today()
        if today - date_str < datetime.timedelta(days=30):
            subject = str(tr.find('a').get_text())
            subject = subject.replace('\t', '').replace('\r\n', '')
            tmp = tr.find('a')['onclick']
            id = int(tmp.split('\'')[1])
            article.append({'type': 'SH분양', 'date': date_str, 'subject': subject, 'id': id, 'link': articleLink % (id, subject)})

    #print(article)
    return article
