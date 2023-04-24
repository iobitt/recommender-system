import pickle

from lib.redis import redis
from lib.logger import Logger
from lib.services.application_service import ApplicationService

class GlobalTopService(ApplicationService):
    def __init__(self, account_id):
        self.account_id = account_id

    def perform(self):
        score = redis.get(self.key('score'))
        serialized = redis.get(self.key('model'))
        model = pickle.loads(serialized)
        return { 'score': score, 'model': model }

    def key(self, param):
        return f"models:{self.account_id}:{param}"

    @property
    def name(self):
        return 'global_top'
