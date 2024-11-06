import psycopg2
from log.logger import logger

#----------------------------------------------------------------------------------------------------
# Настройки для подключения к базе данных
DB_HOST = 'localhost'
DB_NAME = 'shop_db'
DB_USER = 'shop_admin'
DB_PASSWORD = '0000'
#----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------
def connect_to_db():
    try:
        logger.info(f"Подключение к базе данных {DB_NAME} на {DB_HOST}")
        conn = psycopg2.connect(host=DB_HOST,
                                database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASSWORD)
        logger.info("Подключение к базе данных успешно установлено")
        return conn
    
    except Exception as e:
        logger.error(f"Ошибка при подключении к базе данных: {e}")
        raise
#----------------------------------------------------------------------------------------------------
class Requests:
    @staticmethod
    def get_products():
        query = ("""SELECT p.name as product_name,
                    p.description, p.price, p.stock_quantity, p.is_active, p.category_id, p.image_name, c.name as collections_name, p.id
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
        query = ("""INSERT INTO Products (name, description, price, stock_quantity, is_active, category_id, image_name)
                SELECT name, description, price, stock_quantity, is_active, category_id, image_name
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
        # print(set_clause)
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
    @staticmethod
    def add_product(product_data):
        if not product_data:
            logger.error(f"Не переданы данные для добавления товара")
            return False
        else:
            logger.info(f"Тип product_data: {type(product_data)}")
            logger.info(f"Содержимое product_data: {product_data}")
        
        if not product_data:
            logger.error(f"Не переданы данные для добавления товара")
            return False
        
        columns = ', '.join(product_data.keys())
        values = ', '.join(f"'{value}'" for value in product_data.values())
        query = f"INSERT INTO Products ({columns}) VALUES ({values});"

        logger.info(f"query: {query}")
        
        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(product_data.values()))
                    conn.commit()
                    return True

        except Exception as e:
            logger.error(f"Ошибка при добавлении товара: {str(e)}")
            return False
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def get_categories():
        query = "SELECT name, id as category_id FROM Categories;"
        conn = None
        cursor = None  

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()

                    data = [{'name': row[0], 'category_id': row[1]} for row in result]
                    
                    # logger.info(f"Данные категорий: {data}")
                    # logger.info(f"Тип данных категорий: {type(data)}")
                    
                    return data

        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса к БД для выборки всех категорий: {e}")
            raise
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def add_new_category(category_name):
        query = "INSERT INTO Categories (name, is_deleted) VALUES (%s, %s);"
        conn = None
        cursor = None

        print(f"category_name: {category_name}")
        
        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (category_name, False))
                    conn.commit()
                    return True
            
        except Exception as e:
            logger.error(f"Ошибка при добавлении новой категории: {str(e)}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def get_category_id(category_name):
        query = "SELECT id FROM Categories WHERE name = %s;"
        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (category_name,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса к БД для получения id категории: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
    @staticmethod
    def search_products(search_query, search_filter):
        if not search_query:
            logger.error(f"Не передан поисковый запрос для поиска товаров")
            return None
        
        logger.info(f"search_filter: {search_filter}")
        logger.info(f"search_query: {search_query}")

        # Словарь для выбора поля поиска
        search_fields = {
            'name': "SELECT * FROM Products WHERE name LIKE %s;",
            'category': "SELECT * FROM Products WHERE category_id = %s;",
            'description': "SELECT * FROM Products WHERE description LIKE %s;",
            'price': "SELECT * FROM Products WHERE price = %s;",
            'stock': "SELECT * FROM Products WHERE stock_quantity = %s;"
        }

        query = search_fields.get(search_filter)
        if not query:
            logger.error(f"Не передан параметр для поиска товаров")
            return None
        
        conn = None
        cursor = None

        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (search_query,))
                    result = cursor.fetchall()
                    return result

        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса к БД для поиска товаров: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
#----------------------------------------------------------------------------------------------------
