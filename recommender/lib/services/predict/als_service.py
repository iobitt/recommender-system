import sqlite3
import numpy as np
from scipy import sparse as sp

from lib.logger import Logger
from lib.services.application_service import ApplicationService
from lib.services.load.als_service import AlsService as LoadAlsService

class AlsService(ApplicationService):
    def __init__(self, account_id, client_id):
        self.account_id = account_id
        self.client_id = client_id
        connection = sqlite3.connect("../db/development.sqlite3")
        self.cursor = connection.cursor()

    def perform(self):
        model_and_utils = LoadAlsService.call(self.account_id)
        model = model_and_utils['model']
        self.product_ids = model_and_utils['product_ids']
        self.product_id_to_index = model_and_utils['product_id_to_index']

        row_sparse = self.make_coo_row(self.client_id).tocsr()
        raw_recommendations = model.recommend(0, row_sparse, N=30, filter_already_liked_items=False, recalculate_user=True)
        return [self.product_ids[int(x)] for x in raw_recommendations[0]]

    def make_coo_row(self, client_id):
        client_row = [0] * len(self.product_ids)
        sql = f"SELECT product_id FROM 'orders' JOIN order_lines ON order_lines.order_id = orders.id \
                WHERE orders.account_id = ? AND client_id = ? ORDER BY orders.id"
        client_product_ids = self.cursor.execute(sql, (str(self.account_id), str(client_id))).fetchall()
        client_product_ids = list(map(lambda x: x[0], client_product_ids))
        for client_product_id in client_product_ids:
            product_index = self.product_id_to_index[client_product_id]
            client_row[product_index] = 1
        return sp.coo_matrix(np.array(client_row).astype(np.float32))
