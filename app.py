from flask import Flask, render_template
from database import Requests
from utils import load_data
from log.logger import logger 
#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
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
@app.route('/logout')
def logout():
    # return {"message": "Logout Page"}
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