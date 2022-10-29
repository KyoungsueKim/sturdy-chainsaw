import base
import flag

# from ..core import base

current_id = 0
last_economy_date = 0


def article() -> dict:
    global last_economy_date, current_id

    try:
        result = {}
        soup = base.getDynamicSoup('https://kr.investing.com/news/stock-market-news')
        article_list = soup.find_all('article', {'class': 'js-article-item'})
        for i in range(len(article_list)):
            id = int(article_list[i]['data-id'])
            element = article_list[i].find('a', {'class': 'title'})
            text = element.text

            # 최신 글 이라면
            if ("퇴근길" in text or "브런치" in text) and (current_id < id):
                current_id = id
                type = "퇴근길" if "퇴근길" in text else "브런치"
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
                emoji = flag.flag(event.find('td', {'class': 'flagCur'}).text[2:4])
                result.append({'datetime': datetime, 'country': country, 'title': title, 'id': id, 'emoji': emoji})

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
