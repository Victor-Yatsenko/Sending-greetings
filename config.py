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
    'https://graph.microsoft.com/Mail.Send',
    'https://graph.microsoft.com/Chat.ReadWrite',
    'https://graph.microsoft.com/Chat.Create',
    'https://graph.microsoft.com/User.Read',
    'offline_access'  # щоб токен міг оновлюватися сам
]

#Email
SEND_AS = os.getenv('SEND_AS')
TARGET_USER = os.getenv('TARGET_USER')

# 1C
date = datetime.date.today().strftime('%d-%m-%Y')
# date = ""
ZUP_URL = f"{os.getenv('ZUP_URL')}{date}"

