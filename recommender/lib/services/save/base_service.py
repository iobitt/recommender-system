import pickle

from lib.redis import redis
from lib.logger import Logger
from lib.services.application_service import ApplicationService

class BaseService(ApplicationService):
    def __init__(self, account_id, **model_and_utils):
        self.account_id = account_id
        self.model_and_utils = model_and_utils

    def perform(self):
        serialized = pickle.dumps(self.model_and_utils['model'])
        redis.set(self.key('name'), self.name)
        redis.set(self.key('score'), self.model_and_utils['score'])
        redis.set(self.key('model'), serialized)

    def key(self, param):
        return f"models:{self.account_id}:{param}"

    @property
    def name(self):
        raise NotImplementedError
