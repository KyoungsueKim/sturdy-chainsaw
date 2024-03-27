from datetime import date, timedelta, datetime
import bs4
import flag
from typing import Optional
import base
from httpx import URL


class Config:
    current_id = 0


def _scrape_article(article_item: bs4.Tag) -> Optional[dict]:
    if not "data-id" in article_item.attrs:
        return None

    id = int(article_item["data-id"])
    element = article_item.find("a", {"class": "title"})
    text = element.text
    # 최신 글 이라면
    if (("주요" or "마감") in text) and (Config.current_id < id):
        Config.current_id = id
        type = "주요"
        url = "https://kr.investing.com" + element["href"]
        soup = base.getSoup(url)
        article_page = soup.find("div", {"class": "WYSIWYG articlePage"})
        img_url = article_page.find("img")["src"]
        contents = [
            title.text for title in article_page.find_all("p") if ("◇" or "■") in title.text
        ]
        return {"type": type, "img_url": img_url, "article": contents, "url": url}


def article() -> dict:
    url = "https://kr.investing.com/news/stock-market-news"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Sec-Fetch-Site": "none",
        "Accept-Encoding": "gzip",
        "Sec-Fetch-Mode": "navigate",
        "Host": "kr.investing.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Connection": "keep-alive",
    }
    soup = base.getSoup(url, headers=headers)
    article_list = soup.find_all("article", {"class": "js-article-item"})
    # use next to get the first non-None result
    article = next(
        (
            result
            for result in (
                _scrape_article(article_item) for article_item in article_list
            )
            if result is not None
        ),
        {},
    )
    return article


def calendar() -> list:
    url = "https://kr.investing.com/economic-calendar/Service/getCalendarFilteredData"
    headers = {
        'Host': 'kr.investing.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': r'"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'accept': r'*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': r'?0',
        'user-agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': r'"macOS"',
        'origin': 'https://kr.investing.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://kr.investing.com/economic-calendar/',
        'accept-encoding': r'gzip, deflate',
        'accept-language': r'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = r'country%5B%5D=74&country%5B%5D=51&country%5B%5D=172&country%5B%5D=20&country%5B%5D=110&country%5B%5D=21&country%5B%5D=60&country%5B%5D=43&country%5B%5D=46&country%5B%5D=24&country%5B%5D=17&country%5B%5D=97&country%5B%5D=56&country%5B%5D=68&country%5B%5D=100&country%5B%5D=103&country%5B%5D=80&country%5B%5D=96&country%5B%5D=111&country%5B%5D=42&country%5B%5D=7&country%5B%5D=105&country%5B%5D=188&country%5B%5D=82&country%5B%5D=247&country%5B%5D=109&country%5B%5D=139&country%5B%5D=5&country%5B%5D=145&country%5B%5D=47&country%5B%5D=8&country%5B%5D=138&country%5B%5D=178&country%5B%5D=34&country%5B%5D=174&country%5B%5D=163&country%5B%5D=70&country%5B%5D=32&country%5B%5D=52&country%5B%5D=238&country%5B%5D=162&country%5B%5D=9&country%5B%5D=12&country%5B%5D=26&country%5B%5D=90&country%5B%5D=112&country%5B%5D=36&country%5B%5D=143&country%5B%5D=29&country%5B%5D=106&country%5B%5D=33&country%5B%5D=114&country%5B%5D=95&country%5B%5D=86&country%5B%5D=89&country%5B%5D=121&country%5B%5D=4&country%5B%5D=87&country%5B%5D=54&country%5B%5D=92&country%5B%5D=123&country%5B%5D=180&country%5B%5D=168&country%5B%5D=61&country%5B%5D=72&country%5B%5D=66&country%5B%5D=23&country%5B%5D=59&country%5B%5D=10&country%5B%5D=14&country%5B%5D=48&country%5B%5D=35&country%5B%5D=119&country%5B%5D=84&country%5B%5D=37&country%5B%5D=75&country%5B%5D=55&country%5B%5D=27&country%5B%5D=102&country%5B%5D=170&country%5B%5D=6&country%5B%5D=57&country%5B%5D=232&country%5B%5D=15&country%5B%5D=78&country%5B%5D=122&country%5B%5D=94&country%5B%5D=113&country%5B%5D=204&country%5B%5D=107&country%5B%5D=85&country%5B%5D=41&country%5B%5D=202&country%5B%5D=63&country%5B%5D=148&country%5B%5D=44&country%5B%5D=193&country%5B%5D=125&country%5B%5D=38&country%5B%5D=53&country%5B%5D=22&country%5B%5D=71&country%5B%5D=45&country%5B%5D=11&country%5B%5D=93&country%5B%5D=25&country%5B%5D=39&category%5B%5D=_employment&category%5B%5D=_economicActivity&category%5B%5D=_inflation&category%5B%5D=_credit&category%5B%5D=_centralBanks&category%5B%5D=_confidenceIndex&category%5B%5D=_balance&category%5B%5D=_Bonds&importance%5B%5D=3&timeZone=88&timeFilter=timeRemain&currentTab=thisWeek&submitFilters=1&limit_from=0'

    soup = base.postSoup(url, headers=headers, data=data, http2=True)
    event_set = soup.find_all("tr", {"class": "js-event-item"})

    result = []
    events = [
        event
        for event in event_set
        if len(event.find_all("td", {"data-img_key": "bull3"})) > 0
    ]
    for event in events:
        event_datetime = event["data-event-datetime"]
        country = event.find("span")["title"]
        title = " ".join(event.find("a").text.split())
        id = event["event_attr_id"]
        emoji = flag.flag(event.find("td", {"class": "flagCur"}).text[2:4])
        result.append(
            {
                "datetime": event_datetime,
                "country": country,
                "title": title,
                "id": id,
                "emoji": emoji,
            }
        )

    return result


def calendar_find(id: str) -> dict:
    url = "https://kr.investing.com/economic-calendar/Service/getCalendarFilteredData"
    headers = {
        'Host': 'kr.investing.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': r'"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'accept': r'*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': r'?0',
        'user-agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': r'"macOS"',
        'origin': 'https://kr.investing.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://kr.investing.com/economic-calendar/',
        'accept-encoding': r'gzip, deflate',
        'accept-language': r'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = r'country%5B%5D=74&country%5B%5D=51&country%5B%5D=172&country%5B%5D=20&country%5B%5D=110&country%5B%5D=21&country%5B%5D=60&country%5B%5D=43&country%5B%5D=46&country%5B%5D=24&country%5B%5D=17&country%5B%5D=97&country%5B%5D=56&country%5B%5D=68&country%5B%5D=100&country%5B%5D=103&country%5B%5D=80&country%5B%5D=96&country%5B%5D=111&country%5B%5D=42&country%5B%5D=7&country%5B%5D=105&country%5B%5D=188&country%5B%5D=82&country%5B%5D=247&country%5B%5D=109&country%5B%5D=139&country%5B%5D=5&country%5B%5D=145&country%5B%5D=47&country%5B%5D=8&country%5B%5D=138&country%5B%5D=178&country%5B%5D=34&country%5B%5D=174&country%5B%5D=163&country%5B%5D=70&country%5B%5D=32&country%5B%5D=52&country%5B%5D=238&country%5B%5D=162&country%5B%5D=9&country%5B%5D=12&country%5B%5D=26&country%5B%5D=90&country%5B%5D=112&country%5B%5D=36&country%5B%5D=143&country%5B%5D=29&country%5B%5D=106&country%5B%5D=33&country%5B%5D=114&country%5B%5D=95&country%5B%5D=86&country%5B%5D=89&country%5B%5D=121&country%5B%5D=4&country%5B%5D=87&country%5B%5D=54&country%5B%5D=92&country%5B%5D=123&country%5B%5D=180&country%5B%5D=168&country%5B%5D=61&country%5B%5D=72&country%5B%5D=66&country%5B%5D=23&country%5B%5D=59&country%5B%5D=10&country%5B%5D=14&country%5B%5D=48&country%5B%5D=35&country%5B%5D=119&country%5B%5D=84&country%5B%5D=37&country%5B%5D=75&country%5B%5D=55&country%5B%5D=27&country%5B%5D=102&country%5B%5D=170&country%5B%5D=6&country%5B%5D=57&country%5B%5D=232&country%5B%5D=15&country%5B%5D=78&country%5B%5D=122&country%5B%5D=94&country%5B%5D=113&country%5B%5D=204&country%5B%5D=107&country%5B%5D=85&country%5B%5D=41&country%5B%5D=202&country%5B%5D=63&country%5B%5D=148&country%5B%5D=44&country%5B%5D=193&country%5B%5D=125&country%5B%5D=38&country%5B%5D=53&country%5B%5D=22&country%5B%5D=71&country%5B%5D=45&country%5B%5D=11&country%5B%5D=93&country%5B%5D=25&country%5B%5D=39&category%5B%5D=_employment&category%5B%5D=_economicActivity&category%5B%5D=_inflation&category%5B%5D=_credit&category%5B%5D=_centralBanks&category%5B%5D=_confidenceIndex&category%5B%5D=_balance&category%5B%5D=_Bonds&importance%5B%5D=3&timeZone=88&timeFilter=timeRemain&currentTab=thisWeek&submitFilters=1&limit_from=0'

    soup = base.postSoup(url, headers=headers, data=data, http2=True)
    find_result = soup.find_all("tr", {"event_attr_id": id})[0]

    country = find_result.find("span")["title"]
    title = " ".join(find_result.find("a").text.split())
    actual = find_result.find("td", {"class": "act"}).text
    forecast = find_result.find("td", {"class": "fore"}).text
    previous = find_result.find("td", {"class": "prev"}).text

    return {
        "country": country,
        "title": title,
        "actual": actual,
        "forecast": forecast,
        "previous": previous,
    }
