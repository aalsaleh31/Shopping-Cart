import sqlite3
#sqlite3 myDatabase.db ".read store_schema.sql"
#to reset database ^^
from flask import Flask, session, render_template, redirect, url_for, request
from datetime import datetime

app = Flask('app')
app.secret_key = "secret_item"
connection = sqlite3.connect("myDatabase.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
in_cart = 0

counter  = 0

#items
@app.route('/', methods=['GET', 'POST'])
def home():  # my home page can search
    # if(session['items'] == None):
    #     session['items'] =0 
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    roster = cursor.fetchall()
    
    return render_template("home.html", data=roster)


#update the cart
@app.route('/updateit', methods=['GET', 'POST'])
def updateit():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if request.method == "POST":
        session['quantity'] = request.form["quantity"]
        myid = request.form["mything"] 

        cursor.execute("SELECT * FROM items WHERE item_id = ?", (myid,))
        rows = cursor.fetchone()

        cart = session['cart']
        i = any(str(rows[1]) in sublist for sublist in cart)
        if i:
            for i in cart:
                if i[1] == str(rows[1]):
                    i[2] = str(int(session['quantity']))
                    print(i[3])
                    i[3] = str(int(i[2])*int(rows[2]))
                    
                    #in herea
                    session['cart'] = cart
                    return redirect('/checkout')
    

    
    return redirect('/checkout')

#checking out 
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    connection.commit()
    cart = []#list for my cart
    session['quantity'] = 0
    val = 0
    if request.method == "POST":#my implementation of search
        session['quantity'] = request.form["quantity"]
        
        print(request.form["quantity"])
        
        myid = request.form["mything"] 
        print(myid)
        cursor.execute("SELECT * FROM items WHERE item_id = ?", (myid,))
        rows = cursor.fetchone()
        print("whats this")
        print(str(rows[1]))
        print("should be 21 stock")
        print(str(rows[3]))

        cart = session['cart']
        i = any(str(rows[1]) in sublist for sublist in cart)
        if i:
            for i in cart:
                if i[1] == str(rows[1]):
                    if((int(session['quantity']) + int(i[2])) > int(rows[3])):
                        print("wewowewowewo")
                        i[2] = int(rows[3])
                        i[3] = str(int(i[2])*int(rows[2]))
                        session['cart'] = cart
                        val = 1
                        
                    else:
                        i[2] = str(int(session['quantity']) + int(i[2]))
                        print(i[3])
                        i[3] = str(int(i[2])*int(rows[2]))
                        session['cart'] = cart
        else:

            total = int(session['quantity'])*int(rows[2])
            
            cart.append([str(rows[0]), str(rows[1]), session['quantity'], total, str(rows[3])])#0 is id 1 is name 2 is quantity 3 is price
        if session['quantity'] == 0:
            print("pop it")
        session['cart'] = cart#until here
        
    
    session['total_items'] = 0
    session['total_price'] = 0
    cart = session['cart']
    print("does it reach here")
    index = 0
    for i in session['cart']:
        print(i[2])
        if (int(i[2]) == 0):
            print(i[2])
            cart.pop(index)
        session['total_price'] += int(i[3])
        session['total_items'] += int(i[2])
        index+=1

    session['cart'] = cart

    
    return render_template('checkout.html', maxi = val)

#once bought
@app.route('/orderit', methods=['GET', 'POST'])
def orderit():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY my_id DESC")
    rows = cursor.fetchall()
    if request.method == "POST":
        selection = str(request.form["selection"])
        print(selection)
        if selection == "reverse":
            print("start using desc when fetching the data")
            cursor.execute("SELECT * FROM orders ORDER BY my_id")
            rows = cursor.fetchall()

    return render_template("orders.html", data = rows, tried = 0)

#previous orders
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY my_id DESC")
    rows = cursor.fetchall()
    # for i in rows:
    #     print(i['my_date'])
    if request.method == "POST":#my implementation of search
        mysearch = str(request.form["my_search"])
        print(mysearch)
        cursor.execute("SELECT * FROM receipt WHERE products LIKE ?",('%'+ mysearch + '%',))
        mything = cursor.fetchall()
        ids = []
        for i in mything:
            ids.append(i["order_id"])
            print(i["order_id"])
        return render_template("orders.html", data = rows, searched = ids, tried = 1)
    #when searching for something i should only display the 
    

    return render_template("orders.html", data = rows, tried = 0)

#orders for a user
@app.route('/order/<my_id>', methods=['GET', 'POST'])
def info(my_id):
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM receipt WHERE order_id = ?", (my_id,))
    rows = cursor.fetchall()
    for i in rows:
        print(i['products'])
    return render_template('orderdetails.html', data = rows)

#remove an item from a cart
@app.route('/remove/<id>', methods=['GET', 'POST'])
def removed(id):
    # print(id) pop perfectly 
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cart = session['cart']
    index = 0
    for i in cart:
        if i[0] == id:
            print(i[2])
            cart.pop(index)
            print("this is a testto check")
        index +=1
    session['cart'] = cart
    
    return redirect('/checkout')

#once bough
@app.route('/bought', methods=['GET', 'POST'])
def bought():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if(session['total_items'] == 0):
        return redirect('/')
    cursor.execute("SELECT COUNT(my_id) FROM orders")
    ids = cursor.fetchone()
    for i in ids:
        print(i)
        count = i#number of ids how this works i have no idea
    connection.commit()
    cart = session['cart']
    products = []
    am = []
    quant = []
    cursor.execute("SELECT * FROM items")
    roster = cursor.fetchall()
    for i in cart:#check if something is more than the stock
        print(i[0])
        for j in roster:
            if (i[0] == j["item_id"]):
                if(int(i[2]) > j["item_stock"]):
                    print("huge error please fix")
                    ER = 1
                    return render_template('checkout.html', isit = ER )
    now = str(datetime.now())
    for i in cart:#1 is name 2 is quantity 3 is price
        print("does this break my shit")
        # mything = i[1:]#that is what i need to store in orders
        #i[1] is stored in product name i[2] is stored in quantity i[3] is stored in amount 
        #order_username is just the session["username"] order_date is now
        # now = str(datetime.now())

        # products.append(str(i[1]))
        am.append(str(i[3]))
        # quant.append(str(i[2]))
        # print(str(now))
        # print(mything)
        cursor.execute("INSERT INTO receipt (amount, products, quantity, order_date, order_username, order_id, product_id) VALUES(?,?,?,?,?,?,?)", (str(i[3]), str(i[1]), str(i[2]), now,session["username"], count, str(i[0],)))
        #maybe add the all the products as a list of lists also use the quantity and add it after the for loop
        connection.commit()
        # print("thats my items")mo
        amount = int(i[2])#this is the amount of each i
        # print(amount)
        cursor.execute("SELECT * from items where item_id = ?",(i[0],))
        row = cursor.fetchone()
        oldstock = row['item_stock']
        new_stock = oldstock-amount
        cursor.execute("UPDATE items SET item_stock = ? where item_id = ?",(new_stock,i[0],))
        connection.commit()

        # print(oldstock)
    
    # now = str(datetime.now())
   
    print("the end ")
    
    print(am)
    
    total = 0
    for i in am:
        total+=int(i)
    #insert into new table that just has order amount and total price and date and username and date should refrence the other date
    cursor.execute("INSERT INTO orders (total_amount, total_count, my_date, username_id, my_id) VALUES(?,?,?,?,?)", (total,session['total_items'] ,now, session["username"], count))
    connection.commit()
    print(now)
    print("after inserting the date\n\n\n\n")
    
    print(session['total_items'])
    
    #need to change the database value
    session['total_items'] = 0
    session['total_price'] = 0
    session['cart'] = []
    session['counter'] = 0
    
    return redirect('/orderit')

#clears the whole cart
@app.route('/clearcart', methods=['GET', 'POST'])
def clear():
    session['total_items'] = 0
    session['total_price'] = 0
    session['cart'] = []
    session['counter'] = 0
    
    return redirect('/')
#searching depending on categories
@app.route('/cat/<myids>')
def category(myids):
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM items WHERE item_type = ?", (myids,))
    roster = cursor.fetchall()
    
    return render_template("home.html", data=roster)

#add an item
@app.route('/addonly', methods=['GET', 'POST'])
def adder():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    session['total_price'] = 0
    for i in session['cart']:
        session['total_price'] += int(i[3])
    return render_template('checkout.html')

#search an item by name
@app.route('/search', methods=['GET', 'POST'])
def search():  #search again working
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if request.method == "POST":#my implementation of search
        mysearch = str(request.form["my_search"])
        print(mysearch)
        session['my_search'] = mysearch
        cursor.execute("SELECT * FROM items WHERE item_name LIKE ?",('%'+ mysearch + '%',))

        results = cursor.fetchall()
        for i in results:
            print(i["item_name"])
        return render_template("home.html", data = results)
    return render_template("search.html")
#logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    session['cart'] = []
    thing = 0  #checker for log in validity
    session['total_items'] = 0
    session['total_price'] = 0
    session['counter'] = 0
    if request.method == "POST":
        email = request.form["user_email"]
        password = request.form["user_pass"]
        cursor.execute("SELECT * FROM users WHERE username = ? and password = ?",
                       (email, password))
        rows = cursor.fetchone()
        if rows:  #if the entered information is in the database
            # print("this is right suiiiii")
            thing = 0
            session["name"] = rows["name"]
            session["username"] = rows["username"]
            session["password"] = rows["password"]

            # print(session["name"])
            return redirect('/')
        else:
            print("wrong idea")
            thing = 1
    return render_template("login.html", error=thing)

#signing up
@app.route('/sign_up', methods=["GET", "POST"])
def signup():  #maybe sign in after sign up immediately
    #if so then store them in session
    #perfectly works no issue name and passwords go into database
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * from users")
    rows = cursor.fetchall()

    connection.commit()
    if request.method == "POST":
        username = request.form["sign_email"]
        for i in rows:
            if(i["username"] == username):
                m = 1
                return render_template("signup.html", error = m)

        new_name = request.form["sign_name"]
        new_pass = request.form["sign_pass"]
        cursor.execute(
            "INSERT INTO users(username, name, password) VALUES (?,?,?)",
        (username, new_name, new_pass))
        connection.commit()
        return redirect('/login')
    return render_template("signup.html")

#logging out
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')


app.run(host='0.0.0.0', port=8080)
