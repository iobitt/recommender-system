from lib.logger import Logger
from lib.services.application_service import ApplicationService
from lib.services.load.global_top_service import GlobalTopService as LoadGlobalTopService

class GlobalTopService(ApplicationService):
    def __init__(self, account_id, client_id):
        self.account_id = account_id
        self.client_id = client_id

    def perform(self):
        model = LoadGlobalTopService.call(self.account_id)
        return model['model'][:30]
