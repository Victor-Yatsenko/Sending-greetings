import config
from O365 import Account
import json

credentials = (config.CLIENT_ID, config.SECRET_VALUE)
account = Account(credentials, tenant_id=config.TENANT_ID)


def send_email():
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




def send_teams_message(recipient_email: str):
    try:
        # Знаходимо отримувача
        target_email = recipient_email.strip().lower()
        users = account.directory().get_users(query=f"mail eq '{target_email}'")
        recipient_user = next(iter(users), None)

        if not recipient_user:
            print(f"Користувача {target_email} не знайдено.")
            return

        recipient_id = recipient_user.object_id
        # Беремо ID аккаунта з якого будемо надсилати повідомлення
        my_id = account.get_current_user_data().object_id

        # Створюємо або отримуємо чат 1-на-1
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
            msg_endpoint = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"

            # Формуємо картку
            attachment_id = "birthday_card"
            name = "Віктор"
            card_payload = {
                "body": {
                    "contentType": "html",
                    "content": f'<attachment id="{attachment_id}"></attachment>'
                },
                "attachments": [
                    {
                        "id": attachment_id,
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": json.dumps(
                            {
                                "type": "AdaptiveCard",
                                "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                                "version": "1.2",
                                "body": [
                                    {
                                        "type": "TextBlock",
                                        "text": f"{name}, з Днем народження! 🎉",
                                        "weight": "Bolder",
                                        "size": "ExtraLarge",
                                        "wrap": True,
                                        "color": "Accent"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Сьогодні особливий день – день, коли світ став трохи кращим, бо в ньому з’явилися Ви. Ми щиро раді, що частинка цього світу – ЦУМ – має Вас у своїй команді.",
                                        "wrap": True,
                                        "spacing": "Medium"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Бажаємо, щоб у новому році життя було більше моментів, які надихають. Щоб робота давала відчуття сенсу, люди поруч – підтримку, а плани – простір для росту. І щоб завжди знаходився час для того, що наповнює саме Вас.",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Нехай цей рік принесе впевненість у собі, внутрішній баланс і приємні несподіванки. Просто будьте собою, пам’ятайте про свою унікальність – і нехай кожен день дарує Вам радість, натхнення та моменти, які залишаються у серці назавжди!",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "З найтеплішими побажаннями",
                                        "wrap": True,
                                        "spacing": "Large"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Команда ЦУМ",
                                        "weight": "Bolder",
                                        "size": "Medium",
                                        "wrap": True,
                                        "spacing": "None"
                                    }
                                ]
                            }
                        )
                    }
                ]
            }

            msg_response = account.connection.post(msg_endpoint, json=card_payload)

            if msg_response.status_code in [200, 201]:
                print(f"Успішно надіслано від Ricoh для {recipient_user.display_name}!")
            else:
                print(f"Помилка відправки: {msg_response.status_code}")
        else:
            print(f"Помилка створення чату: {chat_response.status_code} - {chat_response.text}")

    except Exception as e:
        print(f"Помилка: {e}")

