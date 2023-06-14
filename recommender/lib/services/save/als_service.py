import pickle

from lib.redis import redis
from lib.logger import Logger
from lib.services.save.base_service import BaseService

class AlsService(BaseService):
    def perform(self):
        super(AlsService, self).perform()
        serialized = pickle.dumps(self.model_and_utils['product_ids'])
        redis.set(self.key('product_ids'), serialized)
        serialized = pickle.dumps(self.model_and_utils['product_id_to_index'])
        redis.set(self.key('product_id_to_index'), serialized)

    @property
    def name(self):
        return 'als'
