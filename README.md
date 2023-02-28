# Library Service

Django project for a management system for book borrowing

* Added and manage books
* Added borrowing
* Added payments for borrowing
* Notifications for borrowing in telegram chat

## Architecture library service

![Architecture](architecture_library_api_service.png)


## Installing / Getting started
* git clone https://github.com/AlenOl/library-service-api
* cd library-service-api
* python -m venv venv
* source venv/bin/activate
* set SECRET_KEY=<your secret key>
* python manage.py migrate
* python manage.py runserver
* Initialize environment variables .env
* For retrieve the notifications you must create telegram bot and initialize his token in .env file
* You can use payment system. For this need initialize your Stripe Payment account.
* You can use celery for daily send messages to telegram chat if you want to know how many overdue borrowing are today.
* redis-server
* celery -A library_service_api worker -l INFO
* celery -A library_service_api beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
