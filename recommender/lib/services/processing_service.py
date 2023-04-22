import json
from redis import Redis

QUEUE_NAME = 'queue:create_recommender_model'
TIMEOUT = 3

class ProcessingService:
    @staticmethod
    def call():
        redis = Redis()
        while True:
            result = redis.blpop(QUEUE_NAME, timeout=TIMEOUT)
            if not result:
                continue

            queue_name, params = result
            params = json.loads(params)
            print(params)
