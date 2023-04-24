import pickle

from lib.redis import redis
from lib.logger import Logger
from lib.services.application_service import ApplicationService

class BaseService(ApplicationService):
    def __init__(self, account_id, model, score):
        self.account_id = account_id
        self.model = model
        self.score = score

    def perform(self):
        serialized = pickle.dumps(self.model)
        redis.set(self.key('name'), NAME)
        redis.set(self.key('score'), self.score)
        redis.set(self.key('model'), serialized)

    def key(self, param):
        return f"models:{self.account_id}:{param}"

    @property
    def name(self):
        raise NotImplementedError
