import requests
import datetime
import  os
from  dotenv import load_dotenv

load_dotenv()

date = datetime.date.today().strftime('%d-%m-%Y')
ZUP_URL = f"{os.getenv('ZUP_URL')}{date}"

response = requests.get(ZUP_URL)


def print_start():
    print(f'{response.text}')


if __name__ == '__main__':
    print_start()
