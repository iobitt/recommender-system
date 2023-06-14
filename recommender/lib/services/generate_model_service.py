from lib.logger import Logger
from lib.services.application_service import ApplicationService
from lib.services.fit.als_service import AlsService as FitAlsService
from lib.services.save.als_service import AlsService as SaveAlsService
from lib.services.fit.global_top_service import GlobalTopService as FitGlobalTopService
from lib.services.save.global_top_service import GlobalTopService as SaveGlobalTopService
from lib.services.fit.item_to_item_service import ItemToItemService as FitItemToItemService
from lib.services.fit.user_to_user_service import UserToUserService as FitUserToUserService


class GenerateModelService(ApplicationService):
    def __init__(self, account_id):
        self.account_id = account_id

    def perform(self):
        models = {
            'global_top': { 'fit_service': FitGlobalTopService, 'save_service': SaveGlobalTopService },
            'als': { 'fit_service': FitAlsService, 'save_service': SaveAlsService },
            'i2i': { 'fit_service': FitItemToItemService, 'save_service': SaveItemToItemService },
            'u2u': { 'fit_service': FitUserToUserService, 'save_service': SaveUserToUserService }
        }

        model_name = None
        max_metric_value = 0
        for name in models:
            service = models[name]
            fit_service = service['fit_service'](self.account_id)
            model, mapk = fit_service.perform()
            service['model'] = model
            service['score'] = mapk
            service['product_ids'] = fit_service.product_ids
            service['product_id_to_index'] = fit_service.product_id_to_index
            if mapk > max_metric_value:
                model_name = name
                max_metric_value = mapk
        Logger.info(f"Favorite model is {model_name}. Metric is {max_metric_value}", *self.tags)
        model_and_utils = models[model_name]
        model_and_utils['save_service'].call(self.account_id, **model_and_utils)

    @property
    def tags(self):
        return [self.account_id, type(self).__name__]
