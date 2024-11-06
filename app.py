from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_wtf import CSRFProtect
from database import Requests
from werkzeug.utils import secure_filename
import os
import logging

#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Секретный ключ для защиты от CSRF-атак
csrf = CSRFProtect(app) # Защита от CSRF-атак
#----------------------------------------------------------------------------------------------------
UPLOAD_FOLDER = 'static/images/' # Папка для сохранения загруженных изображений
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Установка конфигурации для папки загрузки изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Разрешённые расширения файлов
#----------------------------------------------------------------------------------------------------
# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
#----------------------------------------------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#----------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return {"message": "Hello, world!!\nThis is Main Page"}
#----------------------------------------------------------------------------------------------------
@app.route('/admin')
def admin_panel():
    return  {"message": "Hello, Admin!!"}
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products', methods=['GET'])
def admin_products():
    data = Requests.get_products()
    if not data:
        logger.error("Нет доступных товаров")
        return {"message": "Нет доступных товаров"}
    return render_template('admin_products.html', products=data)
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/duplicate/<int:product_id>', methods=['POST'])
def duplicate_product(product_id):
    try:
        success = Requests.duplicate_product(product_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Товар успешно дублирован'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Не удалось дублировать товар с id {product_id}'
            }), 400

    except Exception as e:
        logger.error(f"Ошибка при дублировании товара с id {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при дублировании товара'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        success = Requests.delete_product(product_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Товар успешно удален'
            }), 200 
        else:
            return jsonify({
                'success': False,
                'message': f'Не удалось удалить товар с id {product_id}'
            }), 400 

    except Exception as e:
        logger.error(f"Ошибка при удалении товара с id {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при удалении товара'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/add', methods=['POST'])
def add_product():
    try:
        # Логируем полученные данные для отладки
        logger.info(f"Получены данные для добавления товара: {request.form}")
        logger.info(f"Получены файлы для добавления товара: {request.files}")
        
        # Обработка изображения
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        mapping_fields = {
            'product_name': 'name',
            'description': 'description',
            'price': 'price',
            'stock': 'stock_quantity',
            'category': 'category_id',
            'image_name': 'image_name'
        }

        product_data = {}
        for form_field, db_field in mapping_fields.items():
            value = request.form.get(form_field)
            if value:
                product_data[db_field] = value

        logger.info(f"product_data: {product_data}")
        # Добавление продукта
        success = Requests.add_product(product_data)
        if success:
            return jsonify({
                'success': True,
                'message': 'Товар успешно добавлен'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить товар'
            }), 400


    except ValueError as ve:
        logger.error(f"Ошибка при добавлении товара: {str(ve)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при добавлении товара'
        }), 500
    
    except Exception as e:
        logger.error(f"Ошибка при добавлении товара: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при добавлении товара'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/categories', methods=['GET'])
def categories():
    try:
        success = Requests.get_categories()
        # print("@app.route('/admin/products/categories')", success)
        if not success:
            return jsonify({
                'success': False,
                'message': 'Нет доступных категорий'
            }), 400
        else:
            return jsonify({
                'success': True,
                'categories': success,
                'message': 'Категории успешно получены'
            }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при получении категорий: {str(e)}")
        return {"message": "Произошла ошибка при получении категорий"}
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/categories/add', methods=['POST'])
def add_category():
    try:
        data = request.get_json()
        logger.info(f"Полученные данные: {data}")

        if not data or 'category_name' not in data:
            return jsonify({
                'success': False,
                'message': 'Отсутствует название категории'
            }), 400
    
        category_name = data['category_name']
        logger.info(f"category_name: {category_name}")

        if not category_name:
            return jsonify({
                'success': False,
                'message': 'Название категории не может быть пустым'
            }), 400

        success = Requests.add_new_category(category_name)
        if not success:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить категорию'
            }), 400
        
        category_id = Requests.get_category_id(category_name)
        if success:
            return jsonify({
                'success': True,
                'message': 'Категория успешно добавлена',
                'category_id': category_id
            }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении категории: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при добавлении категории'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    try:
        image = request.files.get('image')
       
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        

        field_mapping = {
            'product_name': 'name',
            'description': 'description',
            'price': 'price',
            'stock': 'stock_quantity',
            'category': 'category_id',
            'image_name': 'image'  
        }

        updates = {}
        for form_field, db_field in field_mapping.items():
           value = request.form.get(form_field)
           if value:
               updates[db_field] = value

        if image:
            updates['image_name'] = image.filename
        
        # print(updates)

        success = Requests.edit_product(product_id, updates)
        if success:
            return jsonify({
                'success': True,
                'message': 'Товар успешно отредактирован'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Не удалось отредактировать товар с id {product_id}'
            }), 400

    except Exception as e:
        logger.error(f"Ошибка при редактировании товара с id {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при редактировании товара'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/search', methods=['POST'])
def search_products():
    try:
        search_query = request.form.get('search_query')
        search_filter = request.form.get('search_filter')
        data = Requests.search_products(search_query, search_filter)
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Товары не найдены'
            }), 400
        else:
            return jsonify({
                'success': True,
                'products': data,
                'message': 'Товары успешно найдены'
            }), 200
    
    except Exception as e:
        logger.error(f"Ошибка при поиске товаров: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при поиске товаров'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/get_all', methods=['GET'])
def get_all_products():
    try:
        products = Requests.get_products()
        return jsonify(products), 200
    except Exception as e:
        logger.error(f"Ошибка при получении всех товаров: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при получении данных'}), 500
@app.route('/logout')
def logout():
    return render_template('logout.html')
#----------------------------------------------------------------------------------------------------
@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    data = Requests.get_orders()
    
    if not data:
        logger.error("Нет доступных заказов")
        return {"message": "Нет доступных заказов"}

    return render_template('admin-orders.html', orders=data)
#----------------------------------------------------------------------------------------------------
@app.route('/admin/users', methods=['GET'])
def admin_users():
    data = Requests.get_users()
    if not data:
        logger.error("Нет доступных пользователей")
        return {"message": "Нет доступных пользователей"}
    return render_template('admin-users.html', users=data)
#----------------------------------------------------------------------------------------------------
@app.route('/admin/settings', methods=['GET'])
def admin_settings():
    return  {"message": "Hello, Admin!!"}
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#----------------------------------------------------------------------------------------------------