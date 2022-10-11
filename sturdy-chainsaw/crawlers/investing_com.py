import base

# from ..core import base

current_id = 0
last_date = 0


def article() -> str:
    global last_date, current_id

    soup = base.getSoup('https://kr.investing.com/news/stock-market-news')
    article_list = soup.find_all('article', {'class': 'js-article-item'})
    result = None
    for i in range(len(article_list)):
        try:
            id = int(article_list[i]['data-id'])
            text = article_list[i].find('a', {'class': 'title'}).text

            # 최신 글 이라면
            if ("퇴근길" in text or "브런치" in text) and (current_id < id):
                current_id = id
                result = text

        except Exception as e:
            pass

    return result


def calendar() -> list:
    try:
        url = 'https://kr.investing.com/economic-calendar/'
        commands = ['calendarFilters.timeFrameFilter(\'thisWeek\')']

        soup = base.getDynamicSoup(url=url, commands=commands)
        event_set = soup.find_all('tr', {'class': 'js-event-item'})

        result = []
        events = [event for event in event_set if len(event.find_all('td', {'data-img_key': 'bull3'})) > 0]
        for event in events:
            try:
                datetime = event['data-event-datetime']
                country = event.find('span')['title']
                title = " ".join(event.find('a').text.split())
                id = event['event_attr_id']
                result.append({'datetime': datetime, 'country': country, 'title': title, 'id': id})

            except:
                pass

        return result

    except:
        return {}


def calendar_find(id: str) -> dict:
    try:
        url = 'https://kr.investing.com/economic-calendar/'
        commands = ['calendarFilters.timeFrameFilter(\'thisWeek\')']

        soup = base.getDynamicSoup(url=url, commands=commands)
        find_result = soup.find_all('tr', {'event_attr_id': id})[0]

        country = find_result.find('span')['title']
        title = " ".join(find_result.find('a').text.split())
        actual = find_result.find('td', {'class': 'act'}).text
        forecast = find_result.find('td', {'class': 'fore'}).text
        previous = find_result.find('td', {'class': 'prev'}).text

        return {'country': country, 'title': title, 'actual': actual, 'forecast': forecast, 'previous': previous}

    except:
        return {}
