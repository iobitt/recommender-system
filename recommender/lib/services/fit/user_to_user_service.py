import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

from lib.logger import Logger
from lib.services.fit.base_service import BaseService
from lib.metrics import normalized_average_precision

NCOMPONENTS = 128
NUM_NEIGHBOURS = 256

class UserToUserService(BaseService):
    def fit(self, matrix):
        self.X_stored = matrix.tocsr()
        self.svd = TruncatedSVD(n_components=NCOMPONENTS)
        X_dense = self.svd.fit_transform(matrix)
        params = { 'n_neighbors': NUM_NEIGHBOURS, 'metric': 'cosine' }
        Logger.info('Fit U2U model', *self.tags, **params)
        knn = NearestNeighbors(**params)
        knn.fit(X_dense)
        return knn

    def calculate_metrics(self, knn):
        m_ap = []
        for client_id in self.client_ids:
            row_sparse = self.make_coo_row(client_id)
            row_dense = self.svd.transform(row_sparse)
            knn_result = knn.kneighbors(row_dense, n_neighbors=NUM_NEIGHBOURS)
            neighbors = knn_result[1]
            scores = np.asarray(self.X_stored[neighbors[0]].sum(axis=0)[0]).flatten()
            top_indices = np.argsort(-scores)
            recommended_items = [self.product_ids[int(x)] for x in top_indices[:30]]

            sql = f"SELECT DISTINCT product_id FROM orders JOIN order_lines ON order_lines.order_id = orders.id \
                    WHERE orders.account_id = ? AND client_id = ? AND transaction_created_at > ? ORDER BY orders.id"
            target_product_ids = self.cursor.execute(sql, (str(self.account_id), str(client_id), self.threshold)).fetchall()
            target_product_ids = list(map(lambda x: x[0], target_product_ids))

            m_ap.append(normalized_average_precision(target_product_ids, recommended_items, k=30))
        return np.mean(m_ap)
