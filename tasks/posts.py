import json, os, time
from posts.models import Post, User
from .get_rand_bashorg import get_quote
from .get_rand_hh import get_vac

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
quote = os.path.join(THIS_FOLDER, 'posts/qotd.txt')
vacancy = os.path.join(THIS_FOLDER, 'posts/votd.txt')


def load_data(source):
    with open(source, 'r+') as f:
        data = json.load(f)
        f.seek(0)
        f.truncate()
    return data


def parse_bash(q):
    quote_head = f"Цитата №{q['id']} - {q['link']} - {q['date']}"

    quote_body = ''
    for line in q['text']:
        quote_body += line
        if line != q['text'][-1]:
            quote_body += '\n'

    return quote_head + '\n' + quote_body


def parse_hh(v):
    v_name = f"{v['name']} - {v['link']}"
    v_employer = f"{v['employer_name']} - {v['employer_url']}"
    v_salary = f"{v['salary']}"

    v_body = ''
    for line in v['description']:
        v_body += line
        if line != v['description'][-1]:
            v_body += '\n'

    vac = v_name + '\n' + v_employer + '\n' + v_salary + '\n\n' + v_body
    return vac


BOTS = {
    'bash': ['bot-bashorg', get_quote, quote, parse_bash],
    'hh': ['bot-hh', get_vac, vacancy, parse_hh],
}


def make_post(bot):
    BOTS[bot][1]()
    time.sleep(10)
    data = load_data(BOTS[bot][2])
    text = BOTS[bot][3](data)

    Post.objects.create(
        author=User.objects.get(username=BOTS[bot][0]),
        text=text,
    )
