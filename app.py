from flask import Flask, render_template
from database import Requests
from utils import load_data

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
# @app.route('/admin/products_json')
# def admin_products_json():
#     products = load_data()
#     # print(products)
#     return render_template('admin_products.html', products=products)
#     # return  {"message": "Products Page"}
#----------------------------------------------------------------------------------------------------
@app.route('/admin/products')
def admin_products():
    data = Requests.get_products()
    # print(data)
    return render_template('admin_products.html', products=data)
    # return  {"message": "Products Page - DB download"}
#----------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    return {"message": "Logout Page"}
#----------------------------------------------------------------------------------------------------
@app.route('/admin/orders')
def admin_orders():
    return  {"message": "Hello, Admin!!"}
#----------------------------------------------------------------------------------------------------
@app.route('/admin/users')
def admin_users():
    return  {"message": "Hello, Admin!!"}
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