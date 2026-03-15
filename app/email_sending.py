import config
from O365 import Account

def send_email():
    credentials = (config.CLIENT_ID, config.SECRET_VALUE) # 'client_id', 'client_secret'
    account = Account(credentials, tenant_id=config.TENANT_ID)
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