import implicit

from lib.logger import Logger
from lib.services.fit.base_service import BaseService

class AlsService(BaseService):
    def call(self):
        Logger.info('Create matrix', *self.tags)
        maxrix = self.create_matrix().tocsr()

        params = { 'factors': 16, 'regularization': 0.0, 'iterations': 8 }
        Logger.info('Fit ALS model', *self.tags, **params)
        model = implicit.als.AlternatingLeastSquares(**params)
        model.fit(maxrix)

        Logger.info('Calculate metrics', *self.tags)
        mapk = self.calculate_metrics(model)
        Logger.info(f'MAP@K metric for fited ALS model is {mapk}', *self.tags)

        return [model, mapk]
