import pickle

from lib.redis import redis
from lib.logger import Logger
from lib.services.load.base_service import BaseService

class AlsService(BaseService):
    def __init__(self, account_id):
        self.account_id = account_id

    def perform(self):
        model_and_utils = super(AlsService, self).perform()
        serialized = redis.get(self.key('product_ids'))
        model_and_utils['product_ids'] = pickle.loads(serialized)
        serialized = redis.get(self.key('product_id_to_index'))
        model_and_utils['product_id_to_index'] = pickle.loads(serialized)
        return model_and_utils

    @property
    def name(self):
        return 'als'
