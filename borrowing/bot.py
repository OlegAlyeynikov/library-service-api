import telebot
from django.conf import settings
from borrowing.scraper import get_books_with_overdue_borrow


class TelegramBot:
    def __init__(self) -> None:
        self.bot = telebot.TeleBot(settings.BOT_TOKEN)

    def send_message_(self, message: str) -> None:
        self.bot.send_message(text=message, chat_id=settings.CHAT_ID)

    def send_message_overdue_borrow(self) -> None:
        text_list: str or list = get_books_with_overdue_borrow()
        for text in text_list:
            self.bot.send_message(text=text, chat_id=settings.CHAT_ID)
