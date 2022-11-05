import base
import re
from bs4 import NavigableString, Tag

url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'


def post(username: str, checkpoint: list) -> dict:
    url = f'https://t.me/s/{username}'
    soup = base.getSoup(url)
    message = soup.find_all('div', {'class': 'tgme_widget_message_wrap'})[-1]
    post_num = int(message.find('div')['data-post'].split('/')[-1])

    if post_num > checkpoint[0]:
        checkpoint[0] = post_num

        image_url = message.find('a', {'class': 'tgme_widget_message_photo_wrap'})
        if image_url is not None:
            image_url = re.compile(url_regex).search(image_url['style'])[0]

        text_element = message.find('div', {'class': 'tgme_widget_message_text'})
        text = ''
        if text_element is not None:
            for element in text_element.contents:
                text += (element.text if hasattr(element, 'text') else element) + "\n"
            # text = [item for item in text.contents if isinstance(item, NavigableString)]
            # text = '\n'.join(text)

        link_priv_image = message.find('a', {'class': 'tgme_widget_message_link_preview'})
        if link_priv_image is not None and link_priv_image.find('i') is not None:
            link_priv_image = link_priv_image.find('i')
            link_priv_image = re.compile(url_regex).search(link_priv_image['style'])[0]
        else:
            link_priv_image = None

        link_priv_title = message.find('a', {'class': 'tgme_widget_message_link_preview'})
        if link_priv_title is not None:
            link_priv_title = link_priv_title.find('div', {'class': 'link_preview_title'}).text

        link_priv_dscrip = message.find('a', {'class': 'tgme_widget_message_link_preview'})
        if link_priv_dscrip is not None:
            link_priv_dscrip = link_priv_dscrip.find('div', {'class': 'link_preview_description'}).text

        url = url + f'/{post_num}'

        return {'image_url': image_url, 'text': text, 'link_priv_image': link_priv_image, 'link_priv_title': link_priv_title, 'link_priv_dscrip': link_priv_dscrip, 'url': url}