import base
from datetime import datetime


def post(username: str, checkpoint: list) -> dict:
    url = f'https://m.blog.naver.com/{username}?categoryNo=0&listStyle=post'
    try:
        soup = base.getDynamicSoup(url)
        url = soup.find_all('div', {'class': 'item__u7k_a'})[0].find('a')['href']
        if checkpoint[0] != url:
            soup = base.getSoup(url)

            title = soup.find('h3', {'class': 'tit_h3'}).text
            post = soup.find('div', {'class': 'post_ct'}).find_all('p')
            text = '\n'.join([item.text for item in post])

            return {'title': title, 'text': text, 'url': url}

        else:
            return None

    except Exception as e:
        return None