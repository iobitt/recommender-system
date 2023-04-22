import implicit
import numpy as np
from datetime import datetime
from scipy import sparse as sp

from lib.db import connection
from lib.logger import Logger
from lib.metrics import normalized_average_precision


class FitAlsModelService:
    def __init__(self, account_id):
        self.account_id = account_id
        self.cursor = connection.cursor()

    def call(self):
        Logger.info('Create matrix', *self.tags)
        maxrix = self.create_matrix()

        params = { 'factors': 16, 'regularization': 0.0, 'iterations': 8 }
        Logger.info('Fit ALS model', *self.tags, **params)
        model = implicit.als.AlternatingLeastSquares(**params)
        model.fit(maxrix)

        Logger.info('Calculate metrics', *self.tags)
        mapk = self.calculate_metrics(model)
        Logger.info(f'MAP@K metric for fited ALS model is {mapk}', *self.tags)

        return [model, mapk]

    def create_matrix(self):
        period_start = datetime.strptime(self.cursor.execute('SELECT MIN(transaction_created_at) FROM orders WHERE account_id = ?', str(self.account_id)).fetchone()[0], '%Y-%m-%d %H:%M:%S')
        period_end = datetime.strptime(self.cursor.execute('SELECT MAX(transaction_created_at) FROM orders WHERE account_id = ?', str(self.account_id)).fetchone()[0], '%Y-%m-%d %H:%M:%S')
        self.threshold = period_start + (period_end - period_start) * 0.85

        self.product_ids = self.cursor.execute("SELECT DISTINCT id FROM products WHERE account_id = ? ORDER BY id", str(self.account_id)).fetchall()
        self.product_ids = list(map(lambda x: x[0], self.product_ids))
        self.product_id_to_index = dict()
        for product_index, product_id in enumerate(self.product_ids):
            self.product_id_to_index[product_id] = product_index

        self.client_ids = self.cursor.execute("SELECT DISTINCT client_id FROM orders WHERE account_id = ? ORDER BY id", str(self.account_id)).fetchall()
        self.client_ids = list(map(lambda x: x[0], self.client_ids))
        self.client_id_to_index = dict()

        rows = []
        for client_index, client_id in enumerate(self.client_ids):
            self.client_id_to_index[client_id] = client_index
            rows.append(self.make_coo_row(client_id))
        return sp.vstack(rows).tocsr()

    def calculate_metrics(self, model):
        m_ap = []
        for client_id in self.client_ids:
            row_sparse = self.make_coo_row(client_id).tocsr()
            raw_recs = model.recommend(0, row_sparse, N=30, filter_already_liked_items=False, recalculate_user=True)
            recommended_items = [self.product_ids[int(x)] for x in raw_recs[0]]

            sql = f"SELECT DISTINCT product_id FROM orders JOIN order_lines ON order_lines.order_id = orders.id \
                    WHERE orders.account_id = ? AND client_id = ? AND transaction_created_at > ? ORDER BY orders.id"
            target_product_ids = self.cursor.execute(sql, (str(self.account_id), str(client_id), self.threshold)).fetchall()
            target_product_ids = list(map(lambda x: x[0], target_product_ids))

            m_ap.append(normalized_average_precision(target_product_ids, recommended_items, k=30))
        return np.mean(m_ap)

    def make_coo_row(self, client_id):
        client_row = [0] * len(self.product_ids)
        sql = f"SELECT product_id FROM 'orders' JOIN order_lines ON order_lines.order_id = orders.id \
                WHERE orders.account_id = ? AND client_id = ? AND transaction_created_at <= ? ORDER BY orders.id"
        client_product_ids = self.cursor.execute(sql, (str(self.account_id), str(client_id), self.threshold)).fetchall()
        client_product_ids = list(map(lambda x: x[0], client_product_ids))
        for client_product_id in client_product_ids:
            product_index = self.product_id_to_index[client_product_id]
            client_row[product_index] = 1
        return sp.coo_matrix(client_row)

    @property
    def tags(self):
        return [self.account_id, type(self).__name__]
