import psycopg2
from flask import jsonify
from psycopg2 import sql, connect
from logger import logger


#----------------------------------------------------------------------------------------------------
def connect():
    """Создание подключения к базе данных."""
    try:
        connection = psycopg2.connect(
            dbname="test_shop_db",
            user="admin",
            # password="0000",
            host="localhost",
            port="5432",
        )

        if not connection:
            logger.error("Не удалось подключиться к базе данных")
            return None

        logger.info("Успешное подключение к базе данных")
        return connection

    except Exception as e:
        logger.error(f"Ошибка при подключении к базе данных: {e}")
        return None
# ----------------------------------------------------------------------------------------------------
#     def execute_query(query, params=None, fetch_one=False, fetch_all=False):
#         """Выполнение SQL-запроса."""
#         try:
#             with connect() as conn:
#                 with conn.cursor() as cursor:
#                     cursor.execute(query, params)
#
#                     if fetch_one:
#                         return cursor.fetchone()
#                     elif fetch_all:
#                         return cursor.fetchall()
#
#         except Exception as e:
#             logger.error(f"Ошибка при выполнении запроса: {e}")
#             return None
#
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------
class Queries:
    """Класс для выполнения запросов к базе данных"""

    # В классе Queries
    @staticmethod
    def get_all_products():
        query = """
            SELECT 
                p.id, 
                p.name, 
                p.description, 
                p.price, 
                p.stock_quantity, 
                p.is_active, 
                p.image_path, 
                c.name AS category_name
            FROM 
                products p
            LEFT JOIN 
                categories c ON p.category_id = c.id
            WHERE 
                p.is_active = TRUE;
        """
        try:
            with connect() as conn:
                with conn.cursor() as cursor:
                    logger.info("Выполнение запроса к базе данных...")
                    cursor.execute(query)
                    products = cursor.fetchall()

                    # Преобразование данных в список словарей
                    data = []
                    for product in products:
                        product_dict = {
                            'id': product[0],
                            'name': product[1],
                            'description': product[2],
                            'price': product[3],
                            'category_name': product[4],
                            'stock_quantity': product[5],
                            'image_path': product[6]
                        }
                        data.append(product_dict)

                    # logger.info("Список товаров успешно получен")
                    logger.info(f"Полученные товары: {data}")
                    return data

        except Exception as e:
            logger.error(f"Ошибка при получении списка товаров: {e}")
            return []
# ----------------------------------------------------------------------------------------------------
    @staticmethod
    def add_user():
        query = ""
        try:
            with connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)

        except Exception as e:
            logger.error(f" {e}")
            return #
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def login():
        pass
# ----------------------------------------------------------------------------------------------------
    @staticmethod
    def login():
        pass
#----------------------------------------------------------------------------------------------------