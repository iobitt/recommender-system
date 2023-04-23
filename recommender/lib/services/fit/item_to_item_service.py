import implicit

from lib.logger import Logger
from lib.services.fit.base_service import BaseService

class ItemToItemService(BaseService):
    def fit(self, matrix):
        params = { 'K': 10 }
        Logger.info('Fit I2I model', *self.tags, **params)
        model = implicit.nearest_neighbours.CosineRecommender(**params)
        model.fit(matrix.tocsr())
        return model
