import colorama
import os
import sys
import requests
import shutil
from collections import deque
from bs4 import BeautifulSoup

from colorama import Fore, Back, Style

colorama.init()

user_agent = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/84.0.4147.135 YaBrowser/20.8.3.132 (beta) '
                            'Yowser/2.5 Safari/537.36'}

browse_history = deque()
accepted_tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
# storage = sys.argv[1]
storage = 'storage'
try:
    os.mkdir(storage)
except FileExistsError:
    shutil.rmtree(storage)
    os.mkdir(storage)


def get_path(file):
    return os.path.join(storage, file)


def get_file_name(url):
    file_name = url.rsplit('.', maxsplit=1)[0].rsplit('/', maxsplit=1)[-1]
    return file_name


def get_page(page):
    url = page if page.startswith('https://') else 'https://' + page
    try:
        response = requests.get(url, headers=user_agent)
        if response.status_code == 200:
            return response.content
    except ConnectionError:
        # print('connection error-----<')
        return False


def use_cache(page: str):  # change page to file
    # file = page.rsplit('.', maxsplit=1)[0].rsplit('/', maxsplit=1)[-1]
    # storage_path = os.path.join(storage, file)
    storage_path = get_path(get_file_name(page))
    if os.path.isfile(storage_path):
        with open(storage_path, 'r') as fh:
            print(fh.read())
        return True
    else:
        return False


# def switch_tab(tab):
#     pass


def add_cache(file_name, page_content):
    path = get_path(file_name)
    with open(path, 'w') as fh:
        fh.write(page_content)


def open_url_add_history_cache(url):
    content = get_page(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all(accepted_tags)

        cached_content = []
        for t in tags:
            if t.decode().startswith('<a'):
                text_block = t.get_text(separator='\n').strip()
                colored = (Fore.BLUE + text_block + Style.RESET_ALL)
                print(colored)
                cached_content.append(colored)
            else:
                text_block = t.get_text(separator='\n').strip()
                print(text_block)
                cached_content.append(text_block)

        file_name = get_file_name(url)

        # create cache file with printable content
        add_cache(file_name, '\n'.join(cached_content))

        # add record to browsing history
        browse_history.append(file_name)


def back_button():
    try:
        browse_history.pop()
        prev_site = browse_history[-1]
        use_cache(prev_site)

    except IndexError:
        pass


def perform_action(command):
    if command == 'exit':
        return False

    elif command == 'back':
        back_button()
        return True

    elif '.' not in command:

        cache_is_used = use_cache(command)
        # print('try to use cache ---<')
        # print(f"cache is used: {cache_is_used}")

        if not cache_is_used:
            print('Error: Incorrect URL')
            return True

        else:
            return True

    if '.' in command:
        open_url_add_history_cache(command)
        return True


while True:
    user_command = input()

    if not perform_action(user_command):
        break
