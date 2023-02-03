import datetime
import os

import dotenv
import requests

from borrowing.scraper import get_books_with_overdue_borrow
from library_service_api.settings import BASE_DIR

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_message_overdue_borrow():
    text_list = get_books_with_overdue_borrow()
    print(text_list)
    for text in text_list:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)
        print(requests.get(url).json())


def send_message_create_borrowing(validated_data):
    print(validated_data)
    # text = "Hello"
    text = (
        f"You created new borrowing in the library: borrow date {validated_data['borrow_date']}, "
        f"expected return date {validated_data['expected_return_date']}, "
        f"book {validated_data['book']}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    requests.get(url)
    print(requests.get(url).json())
