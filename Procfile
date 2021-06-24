web: daphne DjangoChat.asgi:application --settings=DjangoChat.settings
worker: python manage.py runworker channel_layer --settings=DjangoChat.settings -v2