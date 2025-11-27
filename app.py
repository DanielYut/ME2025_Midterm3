from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

# ============================
# 首頁：顯示訂單列表（含 warning）
# ============================
@app.route('/', methods=['GET'])
def index():
    orders = db.get_all_orders()
    warning = request.args.get('warning')
    return render_template('form.html', orders=orders, warning=warning)


# ============================
# Part2 API：/product
# ============================
@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():

    # ----------------------------------
    # GET：兩種情況
    # 1. /product?category=飲料 → 回傳 product list
    # 2. /product?product=紅茶 → 回傳 price
    # ----------------------------------
    if request.method == "GET":
        category = request.args.get("category")
        product_name = request.args.get("product")

        # 查商品清單
        if category:
            results = db.get_product_names_by_category(category)
            product_list = [row[0] for row in results]
            return jsonify({"product": product_list})

        # 查商品價格
        if product_name:
            price = db.get_product_price(product_name)
            return jsonify({"price": price})

        return jsonify({"error": "missing parameter"}), 400


    # ----------------------------------
    # POST：新增訂單
    # ----------------------------------
    if request.method == "POST":
        order_data = {
            "product_date": request.form.get("product_date"),
            "customer_name": request.form.get("customer_name"),
            "product_name": request.form.get("product_name"),
            "product_amount": int(request.form.get("product_amount", 0)),
            "product_total": float(request.form.get("product_total", 0)),
            "product_status": request.form.get("product_status"),
            "product_note": request.form.get("product_note"),
        }

        db.add_order(order_data)

        return redirect(url_for("index", warning="Order placed successfully"))


    # ----------------------------------
    # DELETE：刪除訂單
    # ----------------------------------
    if request.method == "DELETE":
        order_id = request.args.get("order_id")

        if not order_id:
            return jsonify({"error": "order_id is required"}), 400

        success = db.delete_order(order_id)

        if success:
            return jsonify({"message": "Order deleted successfully"})
        else:
            return jsonify({"error": "order not found"}), 404



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
