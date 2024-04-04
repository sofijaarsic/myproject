from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_domaci'

mysql = MySQL(app)

def init_db():
    cur = mysql.connection.cursor()
    cur.execute(
        """ 
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        address VARCHAR(255),
        telephone VARCHAR(10)
        )
        """
    )
    cur.execute(
        """ 
        CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        item VARCHAR(100),
        quantity INT,
        total_amount INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    mysql.connection.commit()
    cur.close()

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.form
    name = data["name"]
    address = data["address"]
    telephone = data["telephone"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, address, telephone) VALUES (%s, %s, %s)", (name, address, telephone))
    mysql.connection.commit()
    cur.close()
    return "User added"

@app.route("/users")
def get_users():
    init_db()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template("users.html", users=users)

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return "User deleted"

@app.route("/update_user_tel/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.form
    telephone = data["telephone"]
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET telephone=%s WHERE id=%s", (telephone, user_id))
    mysql.connection.commit()
    cur.close()
    return "User updated"

@app.route("/add_order", methods=["POST"])
def add_order():
    data = request.form
    user_id = data["user_id"]
    item = data["item"]
    quantity = data["quantity"]
    total_amount = data["total_amount"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders (user_id, item, quantity, total_amount) VALUES (%s, %s, %s, %s)", (user_id, item, quantity, total_amount))
    mysql.connection.commit()
    cur.close()
    return "Order added"

@app.route("/orders")
def get_orders():
    init_db()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    return render_template("orders.html", orders=orders)

@app.route("/delete_order/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    mysql.connection.commit()
    cur.close()
    return "Order deleted"

@app.route("/update_order/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.form
    user_id = data["user_id"]
    item = data["item"]
    quantity = data["quantity"]
    total_amount = data["total_amount"]
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET user_id=%s, item=%s, quantity=%s, total_amount=%s WHERE id=%s", (user_id, item, quantity, total_amount, order_id))
    mysql.connection.commit()
    cur.close()
    return "Order updated"

@app.route("/search_orders", methods=["GET"])
def search_orders():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Keyword parameter is required"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE item LIKE %s", ("%" + keyword + "%",))
    orders = cur.fetchall()
    cur.close()

    return render_template("orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
