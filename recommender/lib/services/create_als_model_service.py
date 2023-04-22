import sqlite3
from datetime import datetime
from scipy import sparse as sp

connection = sqlite3.connect("../db/development.sqlite3")

class CreateAlsModelService:
    def __init__(self, account_id):
        self.account_id = account_id

    def call(self):
        cursor = connection.cursor()
        period_start = datetime.strptime(cursor.execute('SELECT MIN(transaction_created_at) FROM orders WHERE account_id = ?', str(self.account_id)).fetchone()[0], '%Y-%m-%d %H:%M:%S')
        period_end = datetime.strptime(cursor.execute('SELECT MAX(transaction_created_at) FROM orders WHERE account_id = ?', str(self.account_id)).fetchone()[0], '%Y-%m-%d %H:%M:%S')
        threshold = period_start + (period_end - period_start) * 0.85

        product_ids = cursor.execute("SELECT DISTINCT id FROM products WHERE account_id = ? ORDER BY id", str(self.account_id)).fetchall()
        product_ids = list(map(lambda x: x[0], product_ids))
        product_id_to_index = dict()
        for product_index, product_id in enumerate(product_ids):
            product_id_to_index[product_id] = product_index

        client_ids = cursor.execute("SELECT DISTINCT client_id FROM orders WHERE account_id = ? ORDER BY id", str(self.account_id)).fetchall()
        client_ids = list(map(lambda x: x[0], client_ids))
        client_id_to_index = dict()

        rows = []
        for client_index, client_id in enumerate(client_ids):
            client_id_to_index[client_id] = client_index
            client_row = [0] * len(product_ids)
            sql = "SELECT product_id FROM 'orders' JOIN order_lines ON order_lines.order_id = orders.id WHERE orders.account_id = ? AND client_id = ? AND transaction_created_at <= ? ORDER BY orders.id"
            client_product_ids = cursor.execute(sql, (str(self.account_id), str(client_id), threshold)).fetchall()
            client_product_ids = list(map(lambda x: x[0], client_product_ids))
            for client_product_id in client_product_ids:
                product_index = product_id_to_index[client_product_id]
                client_row[product_index] = 1
            rows.append(sp.coo_matrix(client_row))
        X_sparse = sp.vstack(rows).tocsr()

