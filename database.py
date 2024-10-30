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
        conn = None
        cursor = None

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
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def get_orders():
        query = ("""SELECT 
                            o.id AS order_id,
                            o.user_id,
                            o.order_date,
                            o.total_price,
                            os.name AS status,
                            oi.product_id,
                            p.name AS product_name,
                            oi.quantity,
                            oi.price_at_purchase,
                            u.username,
                            u.email
                        FROM 
                            Orders o
                        JOIN 
                            Order_statuses os ON o.status_id = os.id
                        JOIN 
                            Order_items oi ON o.id = oi.order_id
                        JOIN 
                            Products p ON oi.product_id = p.id
                        JOIN
                            Users u ON o.user_id = u.id
                        ORDER BY 
                            o.order_date DESC;
                        """)
        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()

                    data = [{'order_id': row[0],
                             'username': row[9],
                             'order_date': row[2],
                             'total_price': row[3],
                             'status': row[4],
                             'quantity': row[5],
                             'email': row[10]
                             }
                            for row in result]

                    return data

        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса к БД для выборки всех заказов: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def get_users():
        query = ("""SELECT 
                    u.id,
                    u.username,
                    u.email,
                    u.created_at as registration,
                    r.name AS role
                    FROM Users u
                    JOIN Roles r ON u.role_id = r.id;""")
        conn = None
        cursor = None   

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()

                    data = [{'id': row[0],
                             'username': row[1],
                             'email': row[2],
                             'registration': row[3],
                             'role': row[4]
                             }
                            for row in result]

                    return data

        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса к БД для выборки всех пользователей: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def duplicate_product(product_id):
        query = ("""INSERT INTO Products (name, description, price, stock_quantity, is_active, category_id, image_path)
                SELECT name, description, price, stock_quantity, is_active, category_id, image_path
                FROM Products
                WHERE id = %s;""")
        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (product_id,))
                    conn.commit()
                    return True

        except Exception as e:
            logger.error(f"Ошибка при дублировании товара с id {product_id}: {str(e)}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def delete_product(product_id):
        query = "UPDATE Products SET is_active = FALSE WHERE id = %s;"
        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (product_id,))
                    conn.commit()
                    return True

        except Exception as e:
            logger.error(f"Ошибка при удалении товара с id {product_id}: {str(e)}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def edit_product(product_id, updates):
        if not updates:
            logger.error(f"Не переданы данные для редактирования товара с id {product_id}")
            return False

        set_clause = ', '.join(f"{key} = %s" for key in updates.keys())
        query = f"UPDATE Products SET {set_clause} WHERE id = %s;"

        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (*updates.values(), product_id,))
                    conn.commit()
                    return True

        except Exception as e:
            logger.error(f"Ошибка при редактировании товара с id {product_id}: {str(e)}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------

