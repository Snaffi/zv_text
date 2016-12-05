from django.conf import settings
from gevent import monkey
monkey.patch_all()

import requests

from django.core.management import BaseCommand
from gevent.pool import Pool

from redis_client import redis_client

pool = Pool(1000)


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        def process_message(msg):
            key = msg['data']
            response = requests.get(
                'https://vast-eyrie-4711.herokuapp.com',
                params={'key': key}
            )
            print response.status_code, msg
            if 200 <= response.status_code <= 299:
                redis_client.set(
                    key,
                    response.text,
                    ex=settings.CACHE_EXPIRATION
                )
            else:
                redis_client.delete(key)
        
        pubsub_obj = redis_client.pubsub()
        pubsub_obj.subscribe('zvooq_tasks')
        for message in pubsub_obj.listen():
            pool.spawn(process_message, message)
