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
@app.route('/admin/products')
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
        image = request.files.get('image')
        image_path = None

        if image and allowed_file(image.filename):
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            print(image_path)
            print(image.filename)
        

        product_data = {
            'name': request.form.get('product_name'),
            'description': request.form.get('description'),
            'price': request.form.get('price'),
            'stock': request.form.get('stock'),
            'category': request.form.get('category'),
            'image_name': image.filename

        }
        # print(product_data)
        
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


    except Exception as e:
        logger.error(f"Ошибка при добавлении товара: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при добавлении товара'
        }), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/categories')
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
@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    try:
        image = request.files.get('image')

        if image:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
            

        updates = {}
        for key, value in request.form.items():
            if key != 'csrf_token' and key != 'id':
                updates[key] = value
        
        print(updates)

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
@app.route('/logout')
def logout():
    return render_template('logout.html')
#----------------------------------------------------------------------------------------------------
@app.route('/admin/orders')
def admin_orders():
    data = Requests.get_orders()
    
    if not data:
        logger.error("Нет доступных заказов")
        return {"message": "Нет доступных заказов"}

    return render_template('admin-orders.html', orders=data)
#----------------------------------------------------------------------------------------------------
@app.route('/admin/users')
def admin_users():
    data = Requests.get_users()
    if not data:
        logger.error("Нет доступных пользователей")
        return {"message": "Нет доступных пользователей"}
    return render_template('admin-users.html', users=data)
#----------------------------------------------------------------------------------------------------
@app.route('/admin/settings')
def admin_settings():
    return  {"message": "Hello, Admin!!"}
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#----------------------------------------------------------------------------------------------------