import logging
import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from googletrans import Translator

spiegel_base_url = 'https://www.spiegel.de'
translator = Translator()

def is_good_response(resp):
    """
    Returns True if the resp seems to be HTML by checking
    Content-Type in the header, otherwise, False.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type
            and content_type.find('html') > -1)

def simple_get(url):
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return
    except RequestException as e:
        logging.error(e)
    return

def save_html(html_str, filename):
    with open(filename, 'wb') as f:
        f.write(html_str)

def parse_spiegel_politik_html(html_str=None):
    if not html_str:
        html_str = open('spiegel_politik.html').read()

    html = BeautifulSoup(html_str, 'html.parser')
    news = html.select('div.main-content > div.teaser > div.clearfix')
    for item in news:
        title = item.select_one('h2.article-title').select_one('a')
        title_en = translator.translate(title.text).text
        print(f"title: {title_en}")
        link = f"{spiegel_base_url}{title['href']}"
        print(f"link: {link}")
        intro = item.select_one('p.article-intro').text
        intro_en = translator.translate(intro).text
        print(f"intro: {intro_en}")

    print(f'total {len(news)} news in spiegel politics.')


def parse_parse_welt_politik_html(html_str=None):
    if not html_str:
        html_str = open('welt_politik.html').read()

    html = BeautifulSoup(html_str, 'html.parser')


if __name__ == '__main__':
    #html_str = simple_get('https://www.spiegel.de/politik/')
    #save_html(html_str, 'spiegel_politik.html')
    parse_spiegel_politik_html()
