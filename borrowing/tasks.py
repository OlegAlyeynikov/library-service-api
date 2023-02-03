from borrowing.bot import send_message_overdue_borrow
from celery import shared_task


@shared_task
def run_sync_with_api() -> None:
    send_message_overdue_borrow()
