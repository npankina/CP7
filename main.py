# Контроллеры (Flask Views) `main.py` [ обработчики HTTP-запросов, которые принимают запросы от пользователя и передают их в сервисный слой.]
# Сервисный слой (Business Logic) `service_layer.py` [ обрабатывает бизнес-логику, проводит валидацию данных, вызывает необходимые методы DAL или ORM.]
# DAL или ORM (Data Access Layer) `data/` [ непосредственно взаимодействует с базой данных.]
# База данных
import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from db_connection import Queries
from config import config_by_name
from logger import logger

# Настройки
#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')  # Установка окружения (development, production, testing)
app.config.from_object(config_by_name[config_name])
#----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return "Main page"
#----------------------------------------------------------------------------------------------------
# Маршрут для отображения продуктов
@app.route('/admin', methods=['GET'])
def admin_panel():
    try:
        data = Queries.get_all_products()
        print(data)  # Вывод данных для отладки

        return render_template('admin.html', products=data)

    except Exception as e:
        return jsonify({'message': f'Ошибка при отображении админ-панели: {e}'}), 500
#----------------------------------------------------------------------------------------------------
# Маршрут для добавления нового продукта
@app.route('/admin/products/add', methods=['POST'])
def add_product():
    try:


        # logger.info(f'Продукт "{new_product.name}" успешно добавлен')
        return jsonify({'message': 'Продукт успешно добавлен'}), 200

    except Exception as e:
        logger.error(f'Ошибка при добавлении продукта: {e}')
        return jsonify({'message': f'Ошибка при добавлении продукта: {e}'}), 500
#----------------------------------------------------------------------------------------------------
# Маршрут для редактирования продукта
# @app.route('/admin/products/edit/<int:id>', methods=['PUT'])
@app.route('/admin/products/edit', methods=['POST'])
def edit_product():
    try:

        return jsonify({'message': 'Продукт успешно обновлен'}), 200

    except Exception as e:
        logger.error(f'Ошибка при обновлении продукта с ID {id}: {e}')
        return jsonify({'message': f'Ошибка при обновлении продукта: {e}'}), 500
#----------------------------------------------------------------------------------------------------
# Маршрут для удаления продукта
@app.route('/admin/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:

        logger.info(f'Продукт с ID {id} успешно удален')
        return jsonify({'message': 'Продукт успешно удален'}), 200

    except Exception as e:
        logger.error(f'Ошибка при удалении продукта с ID {id}: {e}')
        return jsonify({'message': f'Ошибка при удалении продукта: {e}'}), 500
#----------------------------------------------------------------------------------------------------
@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    pass
#----------------------------------------------------------------------------------------------------
@app.route('/admin/users', methods=['GET'])
def admin_users():
    pass
#----------------------------------------------------------------------------------------------------
@app.route('/admin/settings', methods=['GET'])
def admin_settings():
    pass
# #----------------------------------------------------------------------------------------------------
# def login():
#     pass
# # ----------------------------------------------------------------------------------------------------
# def register():
#     pass
#----------------------------------------------------------------------------------------------------
@app.route('/admin/logout', methods=['GET'])
def logout():
    pass
#----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
