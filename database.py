import psycopg2
from flask import jsonify

from log.logger import logger

# Настройки для подключения к базе данных
DB_HOST = 'localhost'
DB_NAME = 'shop_db'
DB_USER = 'shop_admin'
DB_PASSWORD = '0000'

def connect_to_db():
    conn = psycopg2.connect(host=DB_HOST,
                             database=DB_NAME,
                             user=DB_USER,
                             password=DB_PASSWORD)
    return conn


class Requests:
    @staticmethod
    def get_products():
        query = ("""SELECT p.name as product_name,
                    p.description, p.price, p.stock_quantity, p.is_active, p.category_id, p.image_path, c.name as collections_name, p.id
                FROM Products p
                JOIN Categories c ON p.category_id = c.id
                WHERE p.is_active = true
                ORDER BY p.id ASC;""")

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()

                    data = [{'name': row[0],
                             'description': row[1],
                             'price': row[2],
                             'stock': row[3],
                             'category': row[7],
                             'image': row[6],
                             'id': row[8]
                             }
                            for row in result]

                    return data

        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса к БД для выборки всех товаров: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()