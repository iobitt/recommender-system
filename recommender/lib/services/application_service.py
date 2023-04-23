from lib.logger import Logger

# Base service for all application services
# Allows calling services as Service.call(arguments)
class ApplicationService:
    @classmethod
    def call(cls, *args, **kwargs):
        return cls(*args, **kwargs).perform()

    def __init__(*args, **kwargs):
        pass

    def perform(self):
        raise NotImplementedError

    @property
    def logger(self):
        Logger

    @property
    def tags(self):
        return [type(self).__name__]
