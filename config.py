import os
import datetime
import  dotenv
dotenv.load_dotenv()

# Entra ID
CLIENT_ID = os.getenv('APPLICATION_(CLIENT)_ID')
TENANT_ID = os.getenv('DIRECTORY_(TENANT)_ID')
SECRET_VALUE = os.getenv('SECRET_VALUE')

# Список прав (Scopes) для O365
SCOPES = [
    'User.Read',
    'User.Read.All',
    'Mail.ReadWrite',
    'Mail.Send',
    'Chat.Create',
    'Chat.ReadWrite',
    'offline_access'  # Додаємо offline_access для того, щоб токен міг оновлюватися сам
]


# 1C
date = datetime.date.today().strftime('%d-%m-%Y')
# date = ""
ZUP_URL = f"{os.getenv('ZUP_URL')}{date}"

