from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from datetime import datetime,timedelta 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt,get_jwt_identity
from flask_cors import CORS

stock=Flask(__name__) 
CORS(stock)
stock.config['MYSQL_USER']="root"
stock.config['MYSQL_PASSWORD']="Anuja@2005"
stock.config['MYSQL_DB']="stock"
stock.config['MYSQL_HOST']="localhost"
mysql=MySQL(stock)
@stock.route("/addproducts",methods=["POST"])
def addproducts():
    data=request.json
    productname=data['productname']
    quantity=data['quantity']
    price =data['price']
    status="available"
    cur=mysql.connection.cursor()
    cur.execute("insert into products(productname,quantity,price,status)values(%s,%s,%s,%s)",(productname,quantity,price,status))
    mysql.connection.commit()
    return "addproducts"       

@stock.route("/addcustomers",methods=["POST"])
def addcustomers():
    data=request.json
    customername=data['customername']
    phonenumber=data['phonenumber']
    cur=mysql.connection.cursor()
    cur.execute("insert into customer(customername,phonenumber)values(%s,%s)",(customername,phonenumber))
    mysql.connection.commit()
    return "addcustomers"

@stock.route("/addorders", methods=["POST"])
def addorders():
    data = request.json
    customerid = data['customerid']
    productid = data['productid']
    quantity = int(data['quantity'])  

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM products WHERE productid = %s", (productid,))
    product = cur.fetchone()

    cur.execute("SELECT * FROM customer WHERE customerid = %s", (customerid,))
    customer = cur.fetchone()

    if not product:
        return jsonify({"error": "Product not found"}), 404
    if not customer:
        return jsonify({"error": "Customer not found"}), 404


    cur.execute("SELECT * FROM products WHERE productid = %s AND quantity >= %s", (productid, quantity))
    available_product = cur.fetchone()
    if not available_product:
        return jsonify({"message": "Not enough quantity to order"}), 400

    price = float(product[3])  
    amount = price * quantity

    cur.execute("INSERT INTO orders (customerid, productid, quantity, amount) VALUES (%s, %s, %s, %s)",
                (customerid, productid, quantity, amount))
    cur.execute("UPDATE products SET quantity = quantity - %s WHERE productid = %s",
                (quantity, productid))

    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "success", "message": "Order added successfully"}), 200



@stock.route("/viewallproducts",methods=["GET"])
def viewallproducts():
    cur=mysql.connection.cursor()
    cur.execute("select * from products")
    rows=cur.fetchall()
    col_name=[desc[0] for desc in cur.description]
    results=[dict(zip(col_name,row))for row in rows]
    return jsonify(results)


@stock.route("/viewallcustomers",methods=["GET"])
def viewallcustomers():
    cur=mysql.connection.cursor()
    cur.execute("select * from customer")
    rows=cur.fetchall()
    col_name=[desc[0] for desc in cur.description]
    results=[dict(zip(col_name,row))for row in rows]
    return jsonify(results)


@stock.route("/viewallorders",methods=["GET"])
def viewallorders():
    cur=mysql.connection.cursor()
    cur.execute("select * from orders")
    rows=cur.fetchall()
    col_name=[desc[0] for desc in cur.description]
    results=[dict(zip(col_name,row))for row in rows]
    return jsonify(results)


@stock.route("/getparticularproduct/<int:id>",methods=["GET"])
def getparticularproduct(id):
    cur=mysql.connection.cursor()
    cur.execute("select * from products where productid=%s",(id,))
    row=cur.fetchone()
    col_name=[desc[0] for desc in cur.description]
    if row:
        return jsonify(row)
    return jsonify({"error":"no record found"})

@stock.route("/getparticularcustomer/<int:id>",methods=["GET"])
def getparticularcustomer(id):
    cur=mysql.connection.cursor()
    cur.execute("select * from customer where customerid=%s",(id,))
    row=cur.fetchone()
    col_name=[desc[0] for desc in cur.description]
    if row:
        return jsonify(row)
    return jsonify({"error":"no record found"})

@stock.route("/getparticularorder/<int:id>",methods=["GET"])
def getparticularorder(id):
    cur=mysql.connection.cursor()
    cur.execute("select * from orders where orderid=%s",(id,))
    row=cur.fetchone()
    col_name=[desc[0] for desc in cur.description]
    if row:
        return jsonify(row)
    return jsonify({"error":"no record found"})


@stock.route("/deleteproduct/<int:id>",methods=["DELETE"])
def deleteproduct(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE productid=%s", (id,))
    mysql.connection.commit()
    cur.execute("DELETE FROM products WHERE productid=%s", (id,))

    mysql.connection.commit()
    rowcount = cur.rowcount
    if rowcount == 0:
        return jsonify({"error": "product not found to delete"}), 404
    return jsonify({"message": "product and associated orders deleted successfully", "id": id}), 200
    cur.close()

@stock.route("/deletecustomer/<int:id>", methods=["DELETE"])
def deletecustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE customerid=%s", (id,))
    mysql.connection.commit()
    cur.execute("DELETE FROM customer WHERE customerid=%s", (id,))
    mysql.connection.commit()
    rowcount = cur.rowcount
    if rowcount == 0:
        return jsonify({"error": "Customer not found to delete"}), 404
    return jsonify({"message": "Customer and associated orders deleted successfully", "id": id}), 200
    cur.close()


@stock.route("/deleteorder/<int:id>",methods=["DELETE"])
def deleteorder(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from orders where orderid=%s",(id,))
    mysql.connection.commit()
    rowcount=cur.rowcount
    if rowcount==0:
        return jsonify({"error":"order not found to delete"})#404
    return jsonify({"message":"order deleted successfully","id":id})#200

@stock.route("/updateproduct/<int:id>",methods=["PUT"])
def updateproduct(id):
    cur=mysql.connection.cursor()
    data=request.json
    productname=data['productname']
    quantity=data['quantity']
    price =data['price']
    cur.execute("update products set productname=%s,quantity=%s,price=%s where productid=%s",(productname,quantity,price,id))
    mysql.connection.commit()
    rowcount=cur.rowcount
    if rowcount==0:
        return jsonify({"error":"product not found to update"})#404
    return jsonify({"message":"product updated successfully","id":id})#200

@stock.route("/updatecustomer/<int:id>",methods=["PUT"])
def updatecustomer(id):
    cur=mysql.connection.cursor()
    data=request.json
    customername=data['customername']
    phonenumber=data['phonenumber']
    cur.execute("update customer set customername=%s,phonenumber=%s where customerid=%s",(customername,phonenumber,id))
    mysql.connection.commit()
    rowcount=cur.rowcount
    if rowcount==0:
        return jsonify({"error":"customer not found to update"})#404
    return jsonify({"message":"customer updated successfully","id":id})#200

@stock.route("/updateorder/<int:id>",methods=["PUT"])
def updateorder(id):
    cur=mysql.connection.cursor()
    data=request.json
    customerid=data['customerid']
    productid=data['productid']
    quantity =data['quantity']
    cur.execute("update orders set customerid=%s,productid=%s,quantity=%s where orderid=%s",(customerid,productid,quantity,id))
    mysql.connection.commit()
    rowcount=cur.rowcount
    if rowcount==0:
        return jsonify({"error":"product not found to update"})#404
    return jsonify({"message":"product updated successfully","id":id})#200

@stock.route("/viewproductsort", methods=["GET"])
def getProductSort():
    quantity = request.args.get("quantity", type=int)  
    sort = request.args.get("sort", "productid")       
    sort_order = "ASC"
    if sort.startswith("-"):
        sort_order = "DESC"
        sort = sort[1:]  

    allowed_columns = ["productid", "productname", "quantity", "price", "status"]
    if sort not in allowed_columns:
        
        return jsonify({"error": "Invalid sort column"}), 400
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM products WHERE 1=1"
    sql += f" ORDER BY {sort} {sort_order}"
    cur.execute(sql)
    rows = cur.fetchall()
    col_name = [desc[0] for desc in cur.description]
    results = [dict(zip(col_name, row)) for row in rows]
    return jsonify(results)

@stock.route("/userhistory", methods=['GET'])
def userhistory():
    customer_id = request.args.get('customerid')

    if not customer_id:
        return jsonify({"error": "Missing customer ID"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT o.productid, o.customerid, o.quantity, o.amount, p.productname, u.customername FROM orders o JOIN products p ON o.productid = p.productid JOIN customer u ON o.customerid = u.customerid WHERE o.customerid = %s", (customer_id,))
    rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    results = [dict(zip(col_names, row)) for row in rows]
    return jsonify(results)



@stock.route("/customerlogin", methods=['POST'])
def customerlogin():
    data = request.json
    customername = data.get('customername')
    phonenumber = data.get('phonenumber')  # Fixed: match key in HTML/script

    if not customername or not phonenumber:
        return jsonify({"error": "Missing credentials"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT customerid, customername, phonenumber FROM customer WHERE phonenumber=%s", (phonenumber,))
    customer = cur.fetchone()
    cur.close()

    if not customer:
        return jsonify({"Message": "Customer not found"}), 404

    customerid, db_customername, db_phonenumber = customer

    if customername == db_customername:
        return jsonify({
            "Message": "Login success",
            "customerid": customerid,
            "customername": db_customername,
            "phoneno": db_phonenumber
        })
    else:
        return jsonify({"Message": "Login failed"}), 401



@stock.route("/adminregister", methods=["POST"])
def adminregister():
    data = request.json
    adminname = data['adminname']
    emailid = data['emailid']
    password = data['password']

    if not adminname or not emailid or not password:
        return jsonify({"error": "All fields are required"}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO admin (adminname, emailid, password) VALUES (%s, %s, %s)",(adminname, emailid, password))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Admin added successfully"}), 201


@stock.route("/adminlogin", methods=['POST'])
def adminlogin():
    data = request.json
    emailid = data.get('emailid')
    password = data.get('password')  # Fixed: match key in HTML/script

    if not emailid or not password:
        return jsonify({"error": "Missing credentials"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT adminid, adminname, emailid FROM admin WHERE emailid=%s", (emailid,))
    admin = cur.fetchone()
    cur.close()

    if not admin:
        return jsonify({"Message": "admin not found"}), 404

    adminid, db_adminname, db_emailid = admin

    if emailid == db_emailid:
        return jsonify({
            "Message": "Login success"
        })
    else:
        return jsonify({"Message": "Login failed"}), 401


 
if __name__=="__main__":
    stock.run(debug=True)