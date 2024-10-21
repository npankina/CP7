from flask import Flask, render_template, request, jsonify
from data_adapter import DataAdapter
from logger import setup_logger

#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key'
logger = setup_logger('product_logger', 'app.log')
#----------------------------------------------------------------------------------------------------
# Инициализация адаптера данных
data_adapter = DataAdapter(source_type='json', source_path='data/products.json')
#----------------------------------------------------------------------------------------------------
@app.route('/admin')
def admin_products():
    products = data_adapter.load_data()
    return render_template('admin.html', products=products)
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/add', methods=['POST'])
def add_product():
    try:
        product_data = request.form
        new_product = {
            "id": int(product_data.get('id')),
            "name": product_data.get('name'),
            "description": product_data.get('description'),
            "price": float(product_data.get('price')),
            "stock": int(product_data.get('stock'))
        }
        data_adapter.add_product(new_product)
        logger.info(f'Product {new_product["id"]} added successfully')
        return jsonify({'message': 'Product added successfully'}), 200

    except Exception as e:
        logger.error(f'Error adding product: {e}')
        return jsonify({'message': 'Error adding product'}), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/edit', methods=['POST'])
def edit_product():
    try:
        product_data = request.form
        product_id = int(product_data.get('id'))
        updated_product = {
            "id": product_id,
            "name": product_data.get('name'),
            "description": product_data.get('description'),
            "price": float(product_data.get('price')),
            "stock": int(product_data.get('stock'))
        }
        data_adapter.update_product(product_id, updated_product)
        logger.info(f'Product {product_id} updated successfully')
        return jsonify({'message': 'Product updated successfully'}), 200

    except Exception as e:
        logger.error(f'Error updating product: {e}')
        return jsonify({'message': 'Error updating product'}), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products/delete', methods=['POST'])
def delete_product():
    try:
        data = request.get_json()
        product_id = int(data.get('id'))
        data_adapter.delete_product(product_id)
        logger.info(f'Product {product_id} deleted successfully')
        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        logger.error(f'Error deleting product: {e}')
        return jsonify({'message': 'Error deleting product'}), 500
#----------------------------------------------------------------------------------------------------
# Маршрут для страницы заказов
@app.route('/admin/orders')
def admin_orders():
    orders = load_orders()  # Загрузка заказов (примерная функция)
    return render_template('orders.html', orders=orders)
#----------------------------------------------------------------------------------------------------
# Маршрут для страницы пользователей
@app.route('/admin/users')
def admin_users():
    users = load_users()  # Загрузка пользователей (примерная функция)
    return render_template('users.html', users=users)
#----------------------------------------------------------------------------------------------------
# Маршрут для страницы настроек
@app.route('/admin/settings')
def admin_settings():
    settings = load_settings()  # Загрузка настроек (примерная функция)
    return render_template('settings.html', settings=settings)
#----------------------------------------------------------------------------------------------------
# Маршрут для выхода из системы
@app.route('/admin/logout')
def admin_logout():
    # Реализация выхода, возможно, очистка сессии или перенаправление на страницу входа
    return render_template('logout.html')
#----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
