import os
import datetime
import  dotenv
dotenv.load_dotenv()

date = datetime.date.today().strftime('%d-%m-%Y')
# date = ""

ZUP_URL = f"{os.getenv('ZUP_URL')}{date}"

