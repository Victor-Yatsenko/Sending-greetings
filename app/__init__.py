import os
from  pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env_path = Path(__file__).parent.parent / '.env'

# Перевірка наявності файлу .env
if not env_path.exists():
    raise ImportError(
        f".env файл не знайдено за шляхом: {env_path}\n"
        "Будь ласка, створіть його"
    )

# Перевірка обов'язкових змінних
REQUIRED_SETTINGS = ['ZUP_URL']
missint_settings = [s for s in REQUIRED_SETTINGS if not os.getenv(s)]

if missint_settings:
    raise RuntimeError(
        f"\nВідсутні обов'язкові змінні оточення: {', '.join(missint_settings)}\n"
        "Перевірте ваш .env файл!"
    )