import ssl

import base
from datetime import datetime

class Config:
    last_economy_date = datetime(2021, 1, 1)
    last_break_date = datetime(2021, 1, 1)


def economy() -> dict:
    # SSL 컨텍스트 생성
    ssl_context = ssl.create_default_context()
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1  # TLSv1 허용

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Encoding": "gzip",
        "Sec-Fetch-Mode": "navigate",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Connection": "keep-alive",
        "Origin": "https://www.yna.co.kr",
    }

    soup = base.getSoup('https://www.yna.co.kr/economy/all', headers=headers, verify=ssl_context, http2=True)
    result_set = [result for result in soup.find_all('div', {'class': 'item-box01'}) if len(result.find_all('span', {'class': 'txt-time'})) > 0]
    article_date = datetime.strptime(datetime.now().strftime('%Y') + '-' + result_set[0].find('span', {'class': 'txt-time'}).text, '%Y-%m-%d %H:%M')

    if article_date > Config.last_economy_date:
        Config.last_economy_date = article_date

        title = result_set[0].find('strong', {'class': 'tit-news'}).text
        url = 'https:' + result_set[0].find('a')['href']
        img_url = 'https:' + result_set[0].find('img')['src']
        return {'title': title, 'url': url, 'img_url': img_url}


def break_news() -> dict:
    soup = base.getSoup('https://www.yna.co.kr/theme/breaknews-history')
    article = soup.find('ul', {'class': 'list'}).find_all('li')[0]
    uptime = datetime.strptime(article.find('span', {'class': 'txt-time'}).text, '%Y-%m-%d %H:%M')

    if uptime > Config.last_break_date:
        Config.last_break_date = uptime

        title = article.find('strong', {'class': 'tit-news'}).text
        url = 'https:' + article.find('a')['href']
        img_url = 'https:' + article.find('img')['src']

        return {'title': title, 'url': url, 'img_url': img_url}
