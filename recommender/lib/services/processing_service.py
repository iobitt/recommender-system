import json

from lib.redis import redis
from lib.logger import Logger
from lib.services.generate_model_service import GenerateModelService

QUEUE_NAME = 'queue:create_recommender_model'
TIMEOUT = 3

class ProcessingService:
    @staticmethod
    def call():
        while True:
            result = redis.blpop(QUEUE_NAME, timeout=TIMEOUT)
            if not result:
                continue

            queue_name, params = result
            params = json.loads(params)
            Logger.info('New task', **params)
            GenerateModelService.call(params['account_id'])
