import urllib.request
import re
from Variables import *


def get_raw_page(query: str):
    if not query:
        query = input("give me the link: ")
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
    return video_urls[:4]


def purify_title_from_raw(raw_content: str):
    return re.search(YT_TITLE_TEXT_RANGE, raw_content).group(1)


def get_titles(page_content: str, list_of_urls: list):
    titles = []
    for i in list_of_urls:
        content = re.search(YT_TITLE_RANGE.format(i, i), page_content).group(1)
        titles.append(purify_title_from_raw(content))
    return titles


def get_first_five_yts(query: str):
    all_content = get_raw_page(query)
    urls = get_urls(all_content)
    titles = get_titles(all_content, urls)
    print("result:\n{}\n{}".format(titles, urls))


get_first_five_yts('abc')
