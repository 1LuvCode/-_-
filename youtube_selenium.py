import requests, re
from selenium import webdriver
from bs4 import BeautifulSoup


def is_fine(res):
    if res.status_code == requests.codes.ok:
        return {'is_ok':True, 'text':'Fine', 'url':None}
    else:
        return {'is_ok':False, 'text':f'Error Code : {res.status_code}', 'url':None}


def create_soup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    res = requests.get(url, headers=headers)

    if is_fine(res)['is_ok']:
        soup = BeautifulSoup(res.text, 'lxml')
        return {'is_ok':True, 'my_soup':soup}
    else:
        return {'is_ok':False, 'text':is_fine(res)['text'], 'url':None}


def crapping_youtube():
    # p = re.compile('카드뉴스')
    # covid_idx = 0
    # covid_txt = None
    my_options = webdriver.ChromeOptions()
    my_options.headless = True
    my_options.add_argument('windows-size=1920x1080')
    my_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')

    driver = webdriver.Chrome(options=my_options)
    driver.maximize_window()

    # 페이지 이동
    url = 'https://www.youtube.com'
    driver.get(url)

    pass


if __name__ == '__main__':
    crapping_youtube()