import requests, re
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


def crapping_op_gg(name:str):
    my_url = 'https://www.op.gg/summoner/userName=' + name.lower()
    # my_url = 'https://www.op.gg/summoner/userName=' + 'hide on bush'
    soup = create_soup(url=my_url)

    if soup['is_ok']:
        champ_list = []
        user_info = {
            'user-name':None,
            'profile-icon':None,
            'level':None,
            'solo-rank':None
             }
        champ_info = {
            'face':None,
            'name':None,
            'CSpMin':None,
            'grade':None,
            'kill':None,
            'death':None,
            'assist':None,
            'game_count':None,
            'winning_ratio':None
        }

        try:
            user_info['user-name'] = soup['my_soup'].find('div', attrs={'class':'Information'}).find('span', attrs={'class':'Name'}).text
            user_info['profile-icon'] = soup['my_soup'].find('img', attrs={'class':'ProfileImage'})['src']
            user_info['solo-rank'] = soup['my_soup'].find('div', attrs={'class':re.compile('^Medal')}).find('img')['src']
            user_info['level'] = soup['my_soup'].find('span', attrs={'class':'Level tip'}).text
            champs = soup['my_soup'].find_all('div', attrs={'class':'ChampionBox Ranked'})

            for champ in champs:
                # 항상 임시 변수 할당한 다음 append할 것을 잊지 않기!
                temp_champ_info = dict(champ_info)
                temp_champ_info['face'] = champ.find('div', attrs={'class':'Face'}).find('img', attrs={'class':'ChampionImage'})['src']
                temp_champ_info['name'] = champ.find('div', attrs={'class':'ChampionName'})['title'].split()
                temp_champ_info['CSpMin'] = champ.find('div', attrs={'class':'ChampionMinionKill tip'}).text.split()
                temp_champ_info['grade'] = champ.find('span', attrs={'class':'KDA'}).get_text()
                temp_champ_info['kill'] = champ.find('span', attrs={'class':'Kill'}).get_text()
                temp_champ_info['death'] = champ.find('span', attrs={'class':'Death'}).get_text()
                temp_champ_info['assist'] = champ.find('span', attrs={'class':'Assist'}).get_text()
                temp_champ_info['game_count'] = champ.find('div', attrs={'class':'Title'}).get_text()
                temp_champ_info['winning_ratio'] = champ.find('div', attrs={'class':re.compile('^WinRatio')}).text.split()
                champ_list.append(temp_champ_info)
                # print(f'{champ}\n\n\n')
                # print(temp_champ_info['grade'])

            # for idx, temp in enumerate(champ_list):
            #     print(f'{idx+1} : {temp}')
            # print(user_info)
        except AttributeError as e:
            print(e)
            return False
    else:
        print('실패')

    return {'user-info':user_info, 'champ-list':champ_list}


#
# if __name__ == '__main__':
#     crapping_op_gg('crazybirdking')
