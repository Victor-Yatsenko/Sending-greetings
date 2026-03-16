import config
from O365 import Account, FileSystemTokenBackend
import json

credentials = (config.CLIENT_ID, config.SECRET_VALUE)  # 'client_id', 'client_secret'
# account = Account(credentials, tenant_id=config.TENANT_ID)
# TEST
token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
account = Account(
    credentials,
    auth_flow='client_credentials',
    tenant_id=config.TENANT_ID,
    token_backend=token_backend
)

def send_email():
    # credentials = (config.CLIENT_ID, config.SECRET_VALUE) # 'client_id', 'client_secret'
    # account = Account(credentials, tenant_id=config.TENANT_ID)
    # Перевірка наявності токену Entra ID
    if not account.is_authenticated:
        print("Авторизація через браузер")
        account.authenticate(scopes=config.SCOPES)
        print("Токен отримано успішно!")
    else:
        account.connection.refresh_token()
        print("Доступ підтверджено.")

    message = account.new_message()

    image_path = "happy_birthday.png"
    message.attachments.add(image_path)
    attachment = message.attachments[-1]
    attachment.is_inline = True
    attachment.content_id = "happy_birthday_img"

    name = "Віктор"
    html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="font-family:Segoe UI, Arial, sans-serif; font-size:14px; color:#000; line-height:1.6;">
                    <img src="cid:happy_birthday_img" alt="Привітання" style="width: 100%; max-width: 600px; border-radius: 10px;">
                    <p><strong>{name}, з Днем народження!</strong></p>
                    <p>
                        Сьогодні особливий день – день, коли світ став трохи кращим, бо в ньому з’явилися Ви.
                        Ми щиро раді, що частинка цього світу – ЦУМ – має Вас у своїй команді.
                    </p>
                        Бажаємо, щоб у новому році життя було більше моментів, які надихають.
                        Щоб робота давала відчуття сенсу, люди поруч – підтримку, а плани – простір для росту.
                    </p>
                    <p>
                        І щоб завжди знаходився час для того, що наповнює саме Вас.
                    </p>
                    <p>
                        Нехай цей рік принесе впевненість у собі, внутрішній баланс і приємні несподіванки.
                    </p>
                    <p>
                        Просто будьте собою, пам’ятайте про свою унікальність –
                        і нехай кожен день дарує Вам радість, натхнення та моменти,
                        які залишаються у серці назавжди!
                    </p>
                    <p>
                        З найтеплішими побажаннями,<br>
                        <strong>Команда ЦУМ</strong>
                    </p>
                </div>
            </body>
        </html>
        """

    # Send message
    message.to.add('Viktor.Yatsenko@tsum.com.ua')
    message.subject = f'Привітання з Днем народження від команди ЦУМ'
    message.body = html_content
    message.content_subtype = 'html'
    message.sender.address = config.SEND_AS  # Щоб листи відправлялись від імені службової пошти
    message.send()

    print("Привітання надіслано")


name = "Віктор"
html_text = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="font-family:Segoe UI, Arial, sans-serif; font-size:14px; color:#000; line-height:1.6;">
                <img src="cid:happy_birthday_img" alt="Привітання" style="width: 100%; max-width: 600px; border-radius: 10px;">
                <p><strong>{name}, з Днем народження!</strong></p>
                <p>
                    Сьогодні особливий день – день, коли світ став трохи кращим, бо в ньому з’явилися Ви.
                    Ми щиро раді, що частинка цього світу – ЦУМ – має Вас у своїй команді.
                </p>
                    Бажаємо, щоб у новому році життя було більше моментів, які надихають.
                    Щоб робота давала відчуття сенсу, люди поруч – підтримку, а плани – простір для росту.
                </p>
                <p>
                    І щоб завжди знаходився час для того, що наповнює саме Вас.
                </p>
                <p>
                    Нехай цей рік принесе впевненість у собі, внутрішній баланс і приємні несподіванки.
                </p>
                <p>
                    Просто будьте собою, пам’ятайте про свою унікальність –
                    і нехай кожен день дарує Вам радість, натхнення та моменти,
                    які залишаються у серці назавжди!
                </p>
                <p>
                    З найтеплішими побажаннями,<br>
                    <strong>Команда ЦУМ</strong>
                </p>
            </div>
        </body>
    </html>
    """


def send_teams_message_direct(recipient_email: str, message_text: str):
    try:
        # 1. Знаходимо точного отримувача
        target_email = recipient_email.strip().lower()
        users = account.directory().get_users(query=f"mail eq '{target_email}'")
        recipient_user = next(iter(users), None)

        if not recipient_user:
            print(f"Користувача {target_email} не знайдено.")
            return

        recipient_id = recipient_user.object_id
        my_id = account.get_current_user_data().object_id

        # 2. Створюємо або отримуємо чат
        chat_endpoint = "https://graph.microsoft.com/v1.0/chats"
        chat_payload = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{my_id}')"
                },
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{recipient_id}')"
                }
            ]
        }

        chat_response = account.connection.post(chat_endpoint, json=chat_payload)

        if chat_response.status_code in [200, 201]:
            chat_id = chat_response.json().get('id')

            # 3. НАДСИЛАЄМО ПОВІДОМЛЕННЯ НАПРЯМУ (без get_chat)
            msg_endpoint = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
            msg_payload = {
                "body": {
                    "contentType": "html",
                    "content": message_text
                }
            }

            msg_response = account.connection.post(msg_endpoint, json=msg_payload)

            if msg_response.status_code in [200, 201]:
                print(f"Успішно надіслано для {recipient_user.display_name}!")
            else:
                print(f"Помилка відправки повідомлення: {msg_response.status_code}")
        else:
            print(f"Помилка створення чату: {chat_response.status_code}")

    except Exception as e:
        print(f"Критична помилка: {e}")

# def send_teams_message_from_app(recipient_email: str, message_text: str):
#     try:
#         # 1. Знаходимо ID отримувача
#         target_email = recipient_email.strip().lower()
#         users = account.directory().get_users(query=f"mail eq '{target_email}'")
#         recipient_user = next(iter(users), None)
#
#         if not recipient_user:
#             print(f"Користувача {target_email} не знайдено.")
#             return
#
#         recipient_id = recipient_user.object_id
#
#         # 2. Створюємо чат від імені додатка (Application Context)
#         # ВАЖЛИВО: В members вказуємо ТІЛЬКИ отримувача.
#         # Додаток (Бот) стає власником чату автоматично.
#         chat_endpoint = "https://graph.microsoft.com/v1.0/chats"
#         app_id = credentials[0]
#         chat_payload = {
#             "chatType": "oneOnOne",
#             "members": [
#                 {
#                     # Учасник 1: Користувач-отримувач
#                     "@odata.type": "#microsoft.graph.aadUserConversationMember",
#                     "roles": ["owner"],
#                     "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{recipient_id}')"
#                 },
#                 {
#                     # Учасник 2: САМ БОТ
#                     # Для ботів використовується саме такий тип і формат ID
#                     "@odata.type": "#microsoft.graph.aadUserConversationMember",
#                     "roles": ["owner"],
#                     "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{app_id}')"
#                 }
#             ]
#         }
#
#         # Відправляємо запит на створення чату
#         chat_response = account.connection.post(chat_endpoint, json=chat_payload)
#
#         # 409 означає, що чат уже існує, це теж ок
#         if chat_response.status_code in [200, 201, 409]:
#             chat_id = chat_response.json().get('id')
#
#             # 3. Формуємо картку повідомлення
#             msg_endpoint = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
#             attachment_id = "birthday_card_01"
#
#             card_payload = {
#                 "body": {
#                     "contentType": "html",
#                     "content": f'<attachment id="{attachment_id}"></attachment>'
#                 },
#                 "attachments": [
#                     {
#                         "id": attachment_id,
#                         "contentType": "application/vnd.microsoft.card.adaptive",
#                         "content": json.dumps({
#                             "type": "AdaptiveCard",
#                             "version": "1.4",
#                             "body": [
#                                 {
#                                     "type": "TextBlock",
#                                     "text": "З Днем Народження!",
#                                     "weight": "Bolder",
#                                     "size": "ExtraLarge",
#                                     "color": "Accent"
#                                 },
#                                 {
#                                     "type": "TextBlock",
#                                     "text": f"Шановний колего! Команда ЦУМ Київ щиро вітає вас зі святом!",
#                                     "wrap": True
#                                 }
#                             ],
#                             "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
#                         })
#                     }
#                 ]
#             }
#
#             # Відправка картки
#             msg_response = account.connection.post(msg_endpoint, json=card_payload)
#
#             if msg_response.status_code in [200, 201]:
#                 print(f"Бот успішно надіслав вітання для {recipient_user.display_name}!")
#             else:
#                 # Якщо 403 - перевірте, чи дозволено ботам писати першими в Teams Admin Center
#                 print(f"Помилка відправки повідомлення: {msg_response.status_code} - {msg_response.text}")
#         else:
#             print(f"Помилка створення чату ботом: {chat_response.status_code} - {chat_response.text}")
#
#     except Exception as e:
#         print(f"Критична помилка бота: {e}")