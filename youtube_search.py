import codecs
import urllib.request
import re
import urllib.parse
import unicodedata
from Variables import *


def url_encode_string(string: str):
    return urllib.parse.quote_plus(string)


def get_raw_page(query: str):
    if not query:
        query = input("give me the link: ")
    else:
        query = url_encode_string(query)
    link = YT_SEARCH.format(query)
    return urllib.request.urlopen(link).read().decode()


def remove_dupes_from_list(li: list):
    filtered_list = []
    for i in li:
        if i not in filtered_list:
            filtered_list.append(i)
    return filtered_list


def get_urls(page_content: str):
    video_urls = remove_dupes_from_list(re.findall(YT_URL_FORMAT, page_content))
    return video_urls[:7]


def purify_title_from_raw(raw_content: str):
    return re.search(YT_TITLE_TEXT_RANGE, raw_content).group(1)


def decode_list_items(li: list):
    final_list = []
    for item in li:
        if len(item) == 4 and ' ' not in item:
            item = codecs.unicode_escape_decode(f'\\u{item}')[0]
        final_list.append(item)
    return final_list


def sanitize_title(title: str):
    pattern = r'\\u(\S{4})'
    list_seperated = re.split(pattern, title)
    sanitized = ' '.join(decode_list_items(list_seperated))
    return sanitized


def get_titles(page_content: str, list_of_urls: list):
    titles = []
    for i in list_of_urls:
        content = re.search(YT_TITLE_RANGE.format(i, i), page_content).group(1)
        title = purify_title_from_raw(content)
        sanitized_title = sanitize_title(title)
        titles.append(sanitized_title)
    return titles


def format_data(urls: list, titles: list):
    i = 0
    final_data = {}
    while i < len(urls):
        data = {"url": YT_URL.format(urls[i]), "title": titles[i]}
        final_data[i + 1] = data
        i += 1
    return final_data


def get_first_five_yts(query: str):
    all_content = get_raw_page(query)
    urls = get_urls(all_content)
    titles = get_titles(all_content, urls)
    data = format_data(urls, titles)
    print(data)


get_first_five_yts('abc')
