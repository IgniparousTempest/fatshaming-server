import argparse
import random

from flask import Flask, request, json
from twython import Twython

from config import Config

app = Flask(__name__)

config: Config = None
jokes = None
twitter = None


def fat_joke() -> str:
    return random.choice(jokes)


@app.route('/')
def home():
    return 'Fatshaming is wrong!'


@app.route('/api/weight', methods=['POST'])
def api_weight():
    """
    """
    data = request.form
    weight = float(data["weight"])
    status = f'{weight} Kg'
    if config.last_weight is None:
        status = status + '\n\nFirst Weighing! I am trying to lose weight. Everyday my weight will be posted and if ' \
                          'my weight loss is not monotonically decreasing, an insult will accompany it.'
    elif weight > config.last_weight:
        status = status + '\n\n' + fat_joke()
    try:
        twitter.update_status(status=status)
    except ValueError:
        print(f'Posted weight: {weight}')

    config.set_weight(weight)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Runs a fatshaming server, to tweet nasty things when your weight '
                                                 'goes up.')
    parser.add_argument('ip_address', metavar='IP', type=str, nargs='?', default='127.0.0.1',
                        help='The IP address to host the server.')
    parser.add_argument('port', metavar='PORT', type=int, nargs='?', default=5000, help='The port of the server.')

    with open('jokes.json', 'r') as f:
        jokes = json.load(f)
    with open('secrets.json', 'r') as f:
        keys = json.load(f)
    args = parser.parse_args()
    twitter = Twython(keys['consumer_key'], keys['consumer_secret'], keys['access_token'], keys['access_secret'])
    config = Config('config.json')
    app.run(host=args.ip_address, port=args.port)
