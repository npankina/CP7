from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_wtf import CSRFProtect
from database import Requests
from utils import load_data
import logging

#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)
#----------------------------------------------------------------------------------------------------
# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
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
@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    try:
        updates = {}
        # Получение данных из формы
        updates['name'] = request.form.get('product_name')
        updates['category'] = request.form.get('category')
        updates['description'] = request.form.get('description')
        updates['price'] = request.form.get('price')
        updates['stock'] = request.form.get('stock')
        
        # Обработка изображения, если оно загружено
        # image = request.files.get('image')
        # if image:
        #     updates['image_path'] = image.filename  # Или сохраните файл на сервере

        # Обновление данных в базе данных
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