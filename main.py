#from app import server_request
from app import email_sending
import config

if __name__ == '__main__':
    # server_request.print_start()
    email_sending.send_email()
    target_user = config.TARGET_USER
    greeting_text = 'Привіт! Це <b>тестове</b> повідомлення від скрипта.'

    email_sending.send_teams_message_direct(target_user, greeting_text)
    # email_sending.send_teams_message_from_app(target_user, greeting_text)
    # recipient_email = ""
    # email_sending.send_teams_private_message(recipient_email)