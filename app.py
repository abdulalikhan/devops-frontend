from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    response = requests.get(
        'https://devops-backend-staging.azurewebsites.net/products')
    products = response.json()
    totalProducts = len(products)
    return render_template('product_table.html', products=products, totalProducts=totalProducts)


@app.route('/add_product', methods=['POST'])
def add_product():
    newProduct = {
        'name': request.form['name'],
        'description': request.form['description'],
        'quantity': int(request.form['quantity']),
        'price': float(request.form['price']),
    }
    response = requests.post(
        'https://devops-backend-staging.azurewebsites.net/products', json=newProduct)
    #product = response.json()
    response = requests.get(
        'https://devops-backend-staging.azurewebsites.net/products')
    products = response.json()
    totalProducts = len(products)
    return render_template('product_table.html', products=products, totalProducts=totalProducts)


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    payload = {'quantity': int(request.form['quantity'])}
    response = requests.patch(
        f"https://devops-backend-staging.azurewebsites.net/products/{request.form['id']}", json=payload)
    #product = response.json()
    # return jsonify(product)
    response = requests.get(
        'https://devops-backend-staging.azurewebsites.net/products')
    products = response.json()
    totalProducts = len(products)
    return render_template('product_table.html', products=products, totalProducts=totalProducts)


@app.route('/delete_product', methods=['POST'])
def delete_product():
    requests.delete(
        f"https://devops-backend-staging.azurewebsites.net/products/{request.form['id']}")
    # return jsonify({'status': 'success'})
    response = requests.get(
        'https://devops-backend-staging.azurewebsites.net/products')
    products = response.json()
    totalProducts = len(products)
    return render_template('product_table.html', products=products, totalProducts=totalProducts)


if __name__ == '__main__':
    app.run(debug=True)
