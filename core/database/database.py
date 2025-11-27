import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # -----------------------------
    # 1. 根據種類取得商品名稱
    # -----------------------------
    def get_product_names_by_category(self, category):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT product 
                FROM commodity 
                WHERE category = ?
            """, (category,))
            return cur.fetchall()

    # -----------------------------
    # 2. 根據商品名稱取得價格
    # -----------------------------
    def get_product_price(self, product):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT price 
                FROM commodity 
                WHERE product = ?
            """, (product,))
            row = cur.fetchone()
            return row[0] if row else None

    # -----------------------------
    # 3. 新增訂單（正式DB欄位）
    # -----------------------------
    def add_order(self, order_data):
        order_id = self.generate_order_id()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO order_list
                    (order_id, date, customer_name, product, amount, total, status, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                order_data["product_date"],   # ← 前端傳來的是 product_date，寫入 date
                order_data["customer_name"],
                order_data["product_name"],
                order_data["product_amount"],
                order_data["product_total"],
                order_data["product_status"],
                order_data["product_note"]
            ))
            conn.commit()
        return order_id

    # -----------------------------
    # 4. 查所有訂單（JOIN commodity）
    # -----------------------------
    def get_all_orders(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    o.order_id,
                    o.date,
                    o.customer_name,
                    o.product,
                    c.price,
                    o.amount,
                    o.total,
                    o.status,
                    o.note
                FROM order_list o
                LEFT JOIN commodity c
                ON o.product = c.product
                ORDER BY o.order_id ASC
            """)
            return cur.fetchall()

    # -----------------------------
    # 5. 刪除訂單
    # -----------------------------
    def delete_order(self, order_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM order_list 
                WHERE order_id = ?
            """, (order_id,))
            conn.commit()
            return cur.rowcount > 0
