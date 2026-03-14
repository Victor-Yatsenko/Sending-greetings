import requests
import config

response = requests.get(config.ZUP_URL)


def print_start():
    print(f'{response.text}')
