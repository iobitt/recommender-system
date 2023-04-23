from lib.logger import Logger
from lib.services.fit.als_service import AlsService
from lib.services.application_service import ApplicationService
from lib.services.fit.global_top_service import GlobalTopService
from lib.services.fit.item_to_item_service import ItemToItemService
from lib.services.fit.user_to_user_service import UserToUserService


class GenerateModelService(ApplicationService):
    def __init__(self, account_id):
        self.account_id = account_id

    def perform(self):
        services = {
            'global_top': { 'class': GlobalTopService },
            'als': { 'class': AlsService },
            'i2i': { 'class': ItemToItemService },
            'u2u': { 'class': UserToUserService }
        }

        model_name = None
        max_metric_value = 0
        for name in services:
            service = services[name]
            model, mapk = service['class'].call(self.account_id)
            service['model'] = model
            service['mapk'] = mapk
            if mapk > max_metric_value:
                model_name = name
                max_metric_value = mapk
        Logger.info(f"Favorite model is {model_name}. Metric is {max_metric_value}", *tags)

    @property
    def tags(self):
        return [self.account_id, type(self).__name__]
