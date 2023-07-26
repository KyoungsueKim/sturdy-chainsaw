import asyncio
import sys

import html
import httpx
import flag
from bs4 import BeautifulSoup
import brotli

import base

async def main():
    # url = "https://kr.investing.com/economic-calendar/Service/getCalendarFilteredData"
    # headers = {
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "Pragma": "no-cache",
    #     "Accept": "*/*",
    #     "Sec-Fetch-Site": "same-origin",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Cache-Control": "no-cache",
    #     "Sec-Fetch-Mode": "cors",
    #     "Accept-Encoding": "br",
    #     "Origin": "https://kr.investing.com",
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
    #     "Referer": "https://kr.investing.com/economic-calendar/",
    #     "Connection": "keep-alive",
    #     "Host": "kr.investing.com",
    #     "Sec-Fetch-Dest": "empty",
    #     "X-Requested-With": "XMLHttpRequest",
    # }
    # data = {
    #     "importance": ["3"],
    #     "timeZone": '88',
    #     "timeFrame": "thisWeek",
    #     "timeFilter": "timeRemain",
    #     "timezoneId": "88",
    #     "dateFrom": "2023-07-23",
    #     "dateTo": "2023-07-29",
    #     "timezoneCurrentTime": "15:55",
    #     "timezoneFormat": "(GMT +9:00)",
    #     "offsetSec": 32400,
    #     "isFiltered": True,
    #     "filterButtonState": "On",
    # }
    #
    # with httpx.Client(http2=True) as client:
    #     response = client.post(url, headers=headers, data=data)
    #     try:
    #         response_text = html.unescape(bytes(response.text.replace('\/', '/'), "utf-8").decode("unicode_escape"))
    #         soup = BeautifulSoup(response_text, "html.parser")
    #         event_set = soup.find_all('tr', {'class': 'js-event-item'})
    #
    #         result = []
    #         events = [event for event in event_set if len(event.find_all('td', {'data-img_key': 'bull3'})) > 0]
    #         for event in events:
    #             datetime = event['data-event-datetime']
    #             country = event.find('span')['title']
    #             title = " ".join(event.find('a').text.split())
    #             id = event['event_attr_id']
    #             emoji = flag.flag(event.find('td', {'class': 'flagCur'}).text[2:4])
    #             result.append({'datetime': datetime, 'country': country, 'title': title, 'id': id, 'emoji': emoji})
    #         print(result)
    #     except Exception as e:
    #         print(f"HTML 파싱 에러. {e}", file=sys.stderr)

    current_id = 0
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Sec-Fetch-Site": "none",
        "Accept-Encoding": "br",
        "Sec-Fetch-Mode": "navigate",
        "Host": "kr.investing.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Connection": "keep-alive",
    }
    with httpx.Client(http2=True) as client:
        response = client.get("https://kr.investing.com/news/stock-market-news", headers=headers)
        try:
            soup = BeautifulSoup(response.text, "html.parser")

            article_list = soup.find_all('article', {'class': 'js-article-item'})
            result = {}
            for i in range(len(article_list)):
                if not 'data-id' in article_list[i].attrs:
                    continue

                id = int(article_list[i]['data-id'])
                element = article_list[i].find('a', {'class': 'title'})
                text = element.text

                # 최신 글 이라면
                if ("주요뉴스" in text) and (current_id < id):
                    current_id = id
                    type = "주요뉴스"
                    url = 'https://kr.investing.com' + element['href']
                    soup = base.getDynamicSoup(url)

                    articlePage = soup.find('div', {'class': 'WYSIWYG articlePage'})
                    img_url = articlePage.find('img')['src']
                    contents = [title.text for title in articlePage.find_all('p') if '▲' in title.text]

                    result['type'] = type
                    result['img_url'] = img_url
                    result['article'] = contents
                    result['url'] = url
        except Exception as e:
            print(f"HTML 파싱 에러. {e}", file=sys.stderr)


if __name__ == '__main__':
    asyncio.run(main())