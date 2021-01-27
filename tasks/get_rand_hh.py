import requests, json, os
from bs4 import BeautifulSoup

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(THIS_FOLDER, 'votd.txt')


def get_vac(query=None, *args, **kwargs):
    if query is None:
        search = ''
    else:
        search = '&text=' + query.replace(' ', '+')

    headers = {'User-Agent': 'api-test-agent'}

    response = requests.get(
        f'https://api.hh.ru/vacancies?search_period=7&area=1{search}&order_by=publication_time',
        params=headers
        )
    vac_id = response.json()['items'][0]['id']

    response = requests.get(
        f'https://api.hh.ru/vacancies/{vac_id}',
        params=headers
        )
    vac_data = response.json()

    vac = {}
    vac['id'] = vac_id
    vac['link'] = f'https://hh.ru/vacancy/{vac_id}'
    vac['name'] = vac_data['name']

    vac['employer_name'] = vac_data['employer']['name']
    vac['employer_url'] = vac_data['employer']['alternate_url']

    sal = vac_data.get('salary')
    if sal is None:
        vac['salary'] = ''
    else:
        sal_from = '' if sal.get('from') is None else sal['from']
        sal_to = '' if sal.get('to') is None else sal['to']
        vac['salary'] = f'{sal_from} - {sal_to}'

    vac['description'] = []
    soup = BeautifulSoup(vac_data['description'], 'html.parser')
    for string in soup:
        if '<p>' in repr(string):
            if '<strong>' in repr(string):
                for _ in range(repr(string).count('<strong>')):
                    string.strong.unwrap()
            vac['description'].append(string.text)
        if '<li>' in repr(string):
            for li in string.stripped_strings:
                vac['description'].append(f'- {li}')

    with open(file, 'w') as f:
        json.dump(vac, f, ensure_ascii=False)
