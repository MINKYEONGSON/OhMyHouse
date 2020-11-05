from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import datetime


def get_data():
    #: url
    params = urllib.parse.urlencode({'tgtTypeCd': 'SUB_CONT', 'searchKey': '모집중'}).encode('utf-8')
    req = urllib.request.Request(url='https://www.mss.go.kr/site/seoul/ex/bbs/List.do?cbIdx=146')
    # req.set_proxy('127.0.0.1:8080', 'http')
    f = urllib.request.urlopen(req, data=params)
    html_doc = f.read().decode('UTF-8')

    #: parse
    article = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    articleLink = '<a href="https://www.mss.go.kr/site/seoul/ex/bbs/View.do?cbIdx=146&bcIdx=%s">%s</a>'
    for tr in rows:
        tmp = tr.find_all('td')[5].get_text().split('.')
        date = datetime.date(year=int(tmp[0]), month=int(tmp[1]), day=int(tmp[2]))
        today = datetime.date.today()
        if today - date < datetime.timedelta(days=30):
            subject = tr.find('strong').get_text()
            id = tr.find('a')['onclick'].split('\'')[3]
            if subject.find('모집완료') == -1 and subject.find('발표') == -1 :
                article.append({'type': '중소특공', 'area': '서울', 'date': date, 'subject': subject, 'id': id, 'link': articleLink % (id, subject)})

    #print(article)
    return article
