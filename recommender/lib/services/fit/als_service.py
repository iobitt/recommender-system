import implicit

from lib.logger import Logger
from lib.services.fit.base_service import BaseService

class AlsService(BaseService):
    def fit(self, matrix):
        params = { 'factors': 16, 'regularization': 0.0, 'iterations': 8 }
        Logger.info('Fit ALS model', *self.tags, **params)
        model = implicit.als.AlternatingLeastSquares(**params)
        model.fit(matrix)
        return model
