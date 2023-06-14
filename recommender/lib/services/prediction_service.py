from lib.redis import redis
from lib.logger import Logger
from lib.services.application_service import ApplicationService
from lib.services.predict.global_top_service import GlobalTopService
from lib.services.predict.als_service import AlsService

class PredictionService(ApplicationService):
    def __init__(self, account_id, client_id):
        self.account_id = account_id
        self.client_id = client_id

    def perform(self):
        models = {
            'global_top': GlobalTopService,
            'als': AlsService
        }

        model_name = redis.get(self.key('name')).decode('utf-8')
        Logger.info(f"Used model is {model_name}", *self.tags)
        if not model_name:
            return []

        return models[model_name].call(self.account_id, self.client_id)

    def key(self, param):
        return f"models:{self.account_id}:{param}"

    @property
    def tags(self):
        return [self.account_id, type(self).__name__]
