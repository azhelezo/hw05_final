from bs4 import BeautifulSoup
import requests, json, os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(THIS_FOLDER, 'qotd.txt')


def get_quote(*args, **kwargs):
    url = 'http://bash.im/random'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    quote_out = {}
    quote = soup.findAll('article', class_='quote')[0]

    quote_id = quote.a.text[1:]
    quote_out['id'] = quote_id
    quote_out['link'] = f'https://bash.im/quote/{quote_id}'

    quote_date = next(list(quote.descendants)[8].stripped_strings)
    quote_out['date'] = quote_date

    quote_text = list(quote.descendants)[12]
    quote_out['text'] = []

    for br in quote_text.find_all("br"):
        br.replace_with("\n")

    for string in quote_text.stripped_strings:
        quote_out['text'].append(string)

    with open(file, 'w') as f:
        json.dump(quote_out, f, ensure_ascii=False)
