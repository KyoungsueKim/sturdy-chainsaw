import base
from datetime import datetime
#from ..core import base

last_date = datetime(2021, 1, 1)

def article() -> dict:
    global last_date

    soup = base.getSoup('https://www.yna.co.kr/economy/international-economy')
    try:
        result_set = [result for result in soup.find_all('div', {'class': 'item-box01'}) if len(result.find_all('span', {'class': 'txt-time'})) > 0]
        article_date = datetime.strptime(datetime.now().strftime('%Y') + '-' + result_set[0].find('span', {'class': 'txt-time'}).text, '%Y-%m-%d %H:%M')

        if article_date > last_date:
            last_date = article_date

            title = result_set[0].find('strong', {'class': 'tit-news'}).text
            url = 'https:' + result_set[0].find('a')['href']
            img_url = 'https:' + result_set[0].find('img')['src']
            return {'title': title, 'url': url, 'img_url': img_url}

    except:
        return None