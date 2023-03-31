from celery import shared_task

from borrowing.bot import TelegramBot


@shared_task
def run_sync_with_api() -> None:
    bot = TelegramBot()
    bot.send_message_overdue_borrow()
