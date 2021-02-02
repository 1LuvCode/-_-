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


# def crapping_covid_19():
#     p = re.compile('카드뉴스')
#     covid_idx = 0
#     covid_txt = None
#
#     my_options = webdriver.ChromeOptions()
#     my_options.headless = True
#     my_options.add_argument('windows-size=1920x1080')
#     my_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')
#
#     browser = webdriver.Chrome(options=my_options)
#     browser.maximize_window()
#
#     # 페이지 이동
#     covid_url = 'http://ncov.mohw.go.kr/tcmBoardList.do?pageIndex=1&brdId=3&brdGubun=&board_id=&search_item=1&search_content='
#     browser.get(covid_url)
#
#     # 최근 정례브리핑 클릭 및 url 정보 가져오기
#     briefing_tag = browser.find_elements_by_class_name('bl_link')
#     # browser.find_element_by_link_text('정례브리핑').click()
#
#     for index, tag in enumerate(briefing_tag):
#         m = p.search(tag.text)
#
#         if m:
#             # print(tag.text)
#             # print(f'index = {index}')
#             covid_idx = index
#             covid_txt = tag.text
#             break
#
#     try:
#         briefing_tag[covid_idx].click()
#         # print(browser.current_url)
#         covid_url = browser.current_url
#         browser.quit()
#         soup = create_soup(url=covid_url)
#
#         if soup['is_ok'] == False:
#             # print('creating soup failed ... ')
#             return {'is_ok':False, 'text':'creating soup failed ... ' + soup['text'], 'url':None}
#         else:
#             covid_brief_img = soup['my_soup'].find('img', attrs={'alt':''})
#             img_url = 'http://ncov.mohw.go.kr' + covid_brief_img['src']
#             return {'is_ok':True, 'text':covid_txt, 'url':img_url}
#
#             # img_res = requests.get(img_url)
#             #
#             # if is_fine(img_res):
#             #     with open('covid_19_briefing.jpg', 'wb') as f:
#             #         f.write(img_res.content)
#             #     return (True, '이미지 불러오기 성공')
#             # else:
#             #     print('이미지 불러오기 실패')
#             #     return (False, '이미지 불러오기 실패')
#
#     except IndexError as e:
#         # print(f'{e} ... 데이터 받아오기 실패')
#         browser.quit()
#         return {'is_ok':False, 'text':f'{e} ... 조건을 만족하는 데이터 받아오기 실패', 'url':None}
#

def updated_covid_19():
    url = 'http://ncov.mohw.go.kr'
    soup = create_soup(url=url)

    if not soup['is_ok']:
        print('creating soup failed ... ')
        return {'is_ok': False, 'text': 'creating soup failed ... ' + soup['text'], 'url': None}
    else:
        refer_material = soup['my_soup'].find('span', attrs={'class':'livedate'}).getText()
        title = '환자 현황 ' + refer_material
        # print(title)
        occurance = soup['my_soup'].find('div', attrs={'class':'liveNum_today_new'}).find_all('span', attrs={'class':'data'})
        donate_occur = occurance[0].getText()
        overseas_occur = occurance[1].getText()
        # print(donate_occur, overseas_occur)
        # total_infected_patients = soup['my_soup'].find('div', attrs={'class':'liveNum'}).find('span', attrs={'class':'num'})
        # print(total_infected_patients.getText())
        # before_total = soup['my_soup'].find('div', attrs={'class':'liveNum'}).find('span', attrs={'class':'before'})
        # print(before_total.getText())
        # quarantine_release = soup['my_soup'].find('div', attrs={'class':'liveNum'}).find('span', attrs={'class':'num'})
        board_list = soup['my_soup'].find('div', attrs={'class':'liveNum'}).find_all('li')
        total_infected_patients = board_list[0].find('span', attrs={'class':'num'}).getText()
        before_total = board_list[0].find('span', attrs={'class':'before'}).getText()
        quarantine_release = board_list[1].find('span', attrs={'class':'num'}).getText()
        before_quarantine_release = board_list[1].find('span', attrs={'class':'before'}).getText()
        on_cure = board_list[2].find('span', attrs={'class':'num'}).getText()
        before_on_cure = board_list[2].find('span', attrs={'class':'before'}).getText()
        death = board_list[3].find('span', attrs={'class':'num'}).getText()
        before_death = board_list[3].find('span', attrs={'class':'before'}).getText()

        # print(f'{total_infected_patients}\n{before_total}\n{quarantine_release}\n{before_quarantine_release}\n{on_cure}\n{before_on_cure}\n{death}\n{before_death}')
        return {
            'is_ok':True,
            'title':title,
            'donate_occur':donate_occur,
            'overseas_occur':overseas_occur,
            'total_infected_patients':total_infected_patients,
            'before_total':before_total,
            'quarantine_release':quarantine_release,
            'before_quarantine_release':before_quarantine_release,
            'on_cure':on_cure,
            'before_on_cure':before_on_cure,
            'death':death,
            'before_death':before_death
        }
#
if __name__ == '__main__':
    my_dict = updated_covid_19()
    print(my_dict['donate_occur'])