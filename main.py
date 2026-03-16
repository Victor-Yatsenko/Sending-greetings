#from app import server_request
from app import email_sending
import config

if __name__ == '__main__':
    # server_request.print_start()

    # Відправка повідомлень
    email_sending.send_email()
    target_user = config.TARGET_USER
    email_sending.send_teams_message(target_user)
