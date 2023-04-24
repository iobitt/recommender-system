import numpy as np
from datetime import datetime

from lib.logger import Logger
from lib.services.fit.base_service import BaseService
from lib.metrics import normalized_average_precision

class GlobalTopService(BaseService):
    def perform(self):
        sql = "SELECT product_id FROM orders JOIN order_lines ON order_lines.order_id = orders.id WHERE orders.account_id = ? GROUP BY product_id ORDER BY COUNT(*) DESC LIMIT 100"
        top_products = self.cursor.execute(sql, str(self.account_id)).fetchall()
        top_products = list(map(lambda x: x[0], top_products))

        period_start = datetime.strptime(self.cursor.execute('SELECT MIN(transaction_created_at) FROM orders WHERE account_id = ?', str(self.account_id)).fetchone()[0], '%Y-%m-%d %H:%M:%S')
        period_end = datetime.strptime(self.cursor.execute('SELECT MAX(transaction_created_at) FROM orders WHERE account_id = ?', str(self.account_id)).fetchone()[0], '%Y-%m-%d %H:%M:%S')
        threshold = period_start + (period_end - period_start) * 0.85

        client_ids = self.cursor.execute("SELECT DISTINCT client_id FROM orders WHERE account_id = ? ORDER BY id", str(self.account_id)).fetchall()
        client_ids = list(map(lambda x: x[0], client_ids))

        scores = []
        for client_id in client_ids:
            recommended_items = top_products[:30]

            sql = f"SELECT DISTINCT product_id FROM orders JOIN order_lines ON order_lines.order_id = orders.id \
                    WHERE orders.account_id = ? AND client_id = ? AND transaction_created_at > ? ORDER BY orders.id"
            target_product_ids = self.cursor.execute(sql, (str(self.account_id), str(client_id), threshold)).fetchall()
            target_product_ids = list(map(lambda x: x[0], target_product_ids))

            scores.append(normalized_average_precision(target_product_ids, recommended_items, k=30))
        mapk = np.mean(scores)
        Logger.info(f'MAP@K metric for fited GlobalTop model is {mapk}', *self.tags)

        return [top_products, mapk]
