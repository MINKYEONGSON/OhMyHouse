from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import datetime


def logit(area):
    #: url
    params = urllib.parse.urlencode({'beginPd': '202001', 'suplyAreaCode': area}).encode('utf-8')
    req = urllib.request.Request(url='https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do')
    # req.set_proxy('127.0.0.1:8080', 'http')
    f = urllib.request.urlopen(req, data=params)
    html_doc = f.read().decode('UTF-8')
    #: parse
    article = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    #print(soup.prettify())
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    articleLink = '<a href="https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=%s&pblancNo=%s&gvPgmId=AIA01M01">%s</a>'
    for tr in rows:
        td_list = tr.find_all('td')
        type = td_list[2].get_text()
        if type != '분양전환 불가임대':
            tmp = td_list[6].get_text().split('-')
            date = datetime.date(year=int(tmp[0]), month=int(tmp[1]), day=int(tmp[2]))
            tmp = td_list[7].get_text().split('~')[0].split('-')
            start_date = datetime.date(year=int(tmp[0]), month=int(tmp[1]), day=int(tmp[2]))
            tmp = td_list[7].get_text().split('~')[1].split('-')
            end_date = datetime.date(year=int(tmp[0]), month=int(tmp[1]), day=int(tmp[2]))
            today = datetime.date.today()
            if today <= start_date:
                subject = str(td_list[3].get_text())
                id = int(tr['data-pbno'])
                article.append({'type': type, 'area': area, 'start_date': start_date, 'end_date': end_date, 'date':date, 'subject': subject, 'id': id, 'link': articleLink % (id, id, subject)})
    return article


def get_data():
    article = []
    article += logit('서울')
    article += logit('경기')
    article += logit('인천')
    #print(article)
    return article
