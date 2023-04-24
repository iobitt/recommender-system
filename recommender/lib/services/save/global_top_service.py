from lib.services.save.base_service import BaseService

class GlobalTopService(BaseService):
    @property
    def name(self):
        return 'global_top'
