import streamlit as st
import sqlite3
import os
import pandas as pd
import datetime
st.set_page_config(page_title="Customer Management System")
DB_PATH = os.path.join(os.path.dirname(__file__), "cms_demo.db")


def get_connection():
    """Connect to a local SQLite database so the public demo needs no paid MySQL host."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    init_demo_database(conn)
    return conn


def init_demo_database(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            city TEXT,
            customer_pwd TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_status TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
    """)
    if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO customers(customer_name,email,phone,city,customer_pwd) VALUES(?,?,?,?,?)",
            [
                ("Aarav Patel", "aarav@example.com", "9000000001", "Anand", "demo123"),
                ("Mira Shah", "mira@example.com", "9000000002", "Ahmedabad", "demo123"),
                ("Dev Mehta", "dev@example.com", "9000000003", "Vadodara", "demo123"),
                ("Riya Desai", "riya@example.com", "9000000004", "Nadiad", "demo123"),
                ("Kabir Joshi", "kabir@example.com", "9000000005", "Anand", "demo123"),
            ],
        )
    if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO products(product_name,price) VALUES(?,?)",
            [("Wireless Mouse", 799), ("Keyboard", 1299), ("USB-C Hub", 1899), ("Laptop Stand", 999), ("Headphones", 2499)],
        )
    if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        customers = [r[0] for r in conn.execute("SELECT customer_id FROM customers ORDER BY customer_id").fetchall()]
        products = [r for r in conn.execute("SELECT product_id,price FROM products ORDER BY product_id").fetchall()]
        demo_orders = [
            (customers[0], products[0][0], 2, "2026-10-01 10:30:00", products[0][1] * 2, "Completed"),
            (customers[1], products[1][0], 1, "2026-10-03 14:15:00", products[1][1], "Shipped"),
            (customers[2], products[2][0], 1, "2026-10-05 09:20:00", products[2][1], "Confirmed"),
            (customers[0], products[4][0], 1, "2026-10-08 16:00:00", products[4][1], "Completed"),
            (customers[3], products[3][0], 3, "2026-10-10 12:00:00", products[3][1] * 3, "Processing"),
            (customers[4], products[1][0], 2, "2026-10-12 11:45:00", products[1][1] * 2, "Confirmed"),
            (customers[1], products[0][0], 1, "2026-10-15 15:30:00", products[0][1], "Cancelled"),
            (customers[2], products[4][0], 2, "2026-10-18 13:10:00", products[4][1] * 2, "Completed"),
        ]
        conn.executemany(
            "INSERT INTO orders(customer_id,product_id,quantity,order_date,total_amount,order_status) VALUES(?,?,?,?,?,?)",
            demo_orders,
        )
    conn.commit()

st.title("CUSTOMER MANAGEMENT SYSTEM")
choice=st.sidebar.selectbox("My Menu",("Home","Customer","Admin"))
if(choice=="Home"):
    st.image("CMS.jpg")
    st.info("Free portfolio demo mode: uses sample data. Changes may reset when the app restarts.")
    st.caption("Demo customer login: ID 1–5 | Password: demo123")
    st.write("This is a web Application developed by Shivam Pandya as a Part of Training Project.")
    st.write("This system is used to manage customers, products and orders.")
    st.write("Customer can login and check their profile, orders and order status.")
    st.write("Admin can manage customers, products, orders and analytics.")
elif(choice=="Customer"):
    if "login" not in st.session_state:
        st.session_state["login"]=False
    if "customer_id" not in st.session_state:
        st.session_state["customer_id"]=None
    if(not st.session_state["login"]):
        st.caption("Demo login: Customer ID 1–5 and password demo123")
        cid=st.text_input("Enter Customer ID")
        cpwd=st.text_input("Enter Password",type="password")
        btn=st.button("Login")
        if(btn):
            mydb=get_connection()
            c=mydb.cursor()
            c.execute("select * from customers")
            for r in c:
                if(str(r[0])==cid and r[5]==cpwd):
                    st.session_state["login"]=True
                    st.session_state["customer_id"]=r[0]
                    break
            if(not st.session_state["login"]):
                st.error("Incorrect ID or Password")
            else:
                st.success("Login Successful")
                st.rerun()
            mydb.close()
    if(st.session_state["login"]):
        st.success("Login Successful")
        choice2=st.selectbox(
            "Features",
            (
                "View My Profile",
                "View My Orders",
                "Place New Order",
                "Order Status",
                "Cancel My Order",
                "Update My Profile",
                "Change Password",
                "Logout"
            )
        )
        if(choice2=="View My Profile"):
            mydb=get_connection()
            q="select customer_id,customer_name,email,phone,city from customers where customer_id=?"
            df=pd.read_sql(
                q,
                mydb,
                params=(st.session_state["customer_id"],)
            )
            st.subheader("My Profile")
            if(len(df)>0):
                st.dataframe(df,use_container_width=True)
            else:
                st.info("Profile not found")
            mydb.close()
        elif(choice2=="View My Orders"):
            mydb=get_connection()
            q="""
            select
            o.order_id,
            p.product_name,
            o.quantity,
            o.order_date,
            o.total_amount,
            o.order_status
            from orders o,products p
            where o.product_id=p.product_id
            and o.customer_id=?
            order by o.order_date desc
            """
            try:
                df=pd.read_sql(
                    q,
                    mydb,
                    params=(st.session_state["customer_id"],)
                )
                st.subheader("My Orders")
                if(len(df)>0):
                    st.dataframe(df,use_container_width=True)
                else:
                    st.info("No orders found")
            except Exception as e:
                st.error(str(e))
            mydb.close()
        elif(choice2=="Place New Order"):
            mydb=get_connection()
            products=pd.read_sql(
                "select product_id,product_name,price from products",
                mydb
            )
            st.subheader("Place New Order")
            if(len(products)>0):
                product_name=st.selectbox(
                    "Select Product",
                    products["product_name"].tolist()
                )
                row=products[
                    products["product_name"]==product_name
                ].iloc[0]
                pid=int(row["product_id"])
                price=float(row["price"])
                st.write("Product Price:",price)
                qty=st.number_input(
                    "Enter Quantity",
                    min_value=1,
                    step=1
                )
                amount=price*qty
                st.write("Total Amount:",amount)
                btn2=st.button("Place Order")
                if(btn2):
                    c=mydb.cursor()
                    c.execute(
                        """
                        insert into orders
                        (customer_id,product_id,quantity,order_date,total_amount,order_status)
                        values(?,?,?,?,?,?)
                        """,
                        (
                            st.session_state["customer_id"],
                            pid,
                            qty,
                            datetime.datetime.now(),
                            amount,
                            "Confirmed"
                        )
                    )
                    mydb.commit()
                    st.success("Order Placed Successfully")
                    st.info("Your order has been confirmed.")
            else:
                st.info("No products available")
            mydb.close()
        elif(choice2=="Order Status"):
            mydb=get_connection()
            q="""
            select
            o.order_id,
            p.product_name,
            o.quantity,
            o.order_date,
            o.total_amount,
            o.order_status
            from orders o,products p
            where o.product_id=p.product_id
            and o.customer_id=?
            order by o.order_date desc
            """
            try:
                df=pd.read_sql(
                    q,
                    mydb,
                    params=(st.session_state["customer_id"],)
                )
                st.subheader("My Order Status")
                if(len(df)>0):
                    for i in range(len(df)):
                        st.write(
                            "Order ID:",
                            df.iloc[i]["order_id"]
                        )
                        st.write(
                            "Product:",
                            df.iloc[i]["product_name"]
                        )
                        st.write(
                            "Quantity:",
                            df.iloc[i]["quantity"]
                        )
                        st.write(
                            "Order Date:",
                            df.iloc[i]["order_date"]
                        )
                        st.write(
                            "Amount:",
                            df.iloc[i]["total_amount"]
                        )
                        st.write(
                            "Status:",
                            df.iloc[i]["order_status"]
                        )
                        st.write("-------------------------")
                else:
                    st.info("No orders found")
            except Exception as e:
                    st.error(str(e))
            mydb.close()
        elif(choice2=="Cancel My Order"):
            mydb=get_connection()
            q="""
            select
            o.order_id,
            p.product_name,
            o.quantity,
            o.order_date,
            o.total_amount,
            o.order_status
            from orders o,products p
            where o.product_id=p.product_id
            and o.customer_id=?
            and o.order_status='Confirmed'
            order by o.order_date desc
            """
            try:
                df=pd.read_sql(
                    q,
                    mydb,
                    params=(st.session_state["customer_id"],)
                )
                st.subheader("Cancel My Order")
                if(len(df)>0):
                    st.dataframe(
                        df,
                        use_container_width=True
                    )
                    oid=st.selectbox(
                        "Select Order to Cancel",
                        df["order_id"].tolist()
                    )
                    cancel=st.button("Cancel Order")
                    if(cancel):
                        c=mydb.cursor()
                        c.execute(
                            """
                            update orders
                            set order_status='Cancelled'
                            where order_id=?
                            and customer_id=?
                            and order_status in ('Pending','Confirmed')
                            """,
                            (
                                oid,
                                st.session_state["customer_id"]
                            )
                        )
                        mydb.commit()
                        st.success("Order Cancelled Successfully")
                        st.rerun()
                else:
                    st.info("No cancellable orders found")
            except Exception as e:
                st.error(str(e))
            mydb.close()
        elif(choice2=="Update My Profile"):
            mydb=get_connection()
            c=mydb.cursor()
            c.execute(
                "select * from customers where customer_id=?",
                (st.session_state["customer_id"],)
            )
            data=c.fetchone()
            st.subheader("Update My Profile")
            if(data):
                name=st.text_input(
                    "Enter Customer Name",
                    value=data[1]
                )
                email=st.text_input(
                    "Enter Email",
                    value=data[2]
                )
                phone=st.text_input(
                    "Enter Phone",
                    value=data[3]
                )
                city=st.text_input(
                    "Enter City",
                    value=data[4]
                )
                update=st.button("Update Profile")
                if(update):
                    c.execute(
                        """
                        update customers
                        set customer_name=?,
                        email=?,
                        phone=?,
                        city=?
                        where customer_id=?
                        """,
                        (
                            name,
                            email,
                            phone,
                            city,
                            st.session_state["customer_id"]
                        )
                    )
                    mydb.commit()
                    st.success("Profile Updated Successfully")
            mydb.close()
        elif(choice2=="Change Password"):
            st.subheader("Change Password")
            old_password=st.text_input(
                "Enter Old Password",
                type="password"
            )
            new_password=st.text_input(
                "Enter New Password",
                type="password"
            )
            confirm_password=st.text_input(
                "Confirm New Password",
                type="password"
            )
            change=st.button("Change Password")
            if(change):
                mydb=get_connection()
                c=mydb.cursor()
                c.execute(
                    """
                    select customer_pwd
                    from customers
                    where customer_id=?
                    """,
                    (st.session_state["customer_id"],)
                )
                data=c.fetchone()
                if(data and data[0]==old_password):
                    if(new_password==confirm_password):
                        c.execute(
                            """
                            update customers
                            set customer_pwd=?
                            where customer_id=?
                            """,
                            (
                                new_password,
                                st.session_state["customer_id"]
                            )
                        )
                        mydb.commit()
                        st.success("Password Changed Successfully")
                    else:
                        st.error(
                            "New Password and Confirm Password are different"
                        )
                else:
                    st.error("Old Password is incorrect")
                mydb.close()
        elif(choice2=="Logout"):
            st.session_state["login"]=False
            st.session_state["customer_id"]=None
            st.success("Logged Out Successfully")
            st.rerun()
elif(choice=="Admin"):
    choice3=st.selectbox(
        "Admin Features",
        (
            "View All Customers",
            "Add New Customer",
            "Update Customer",
            "Delete Customer",
            "Customer Search",
            "Customer Details",
            "View Products",
            "Add New Product",
            "Update Product",
            "Delete Product",
            "Product Search",
            "View All Orders",
            "Order Search",
            "Order Details",
            "Update Order Status",
            "Delete Order",
            "Date-wise Order Search",
            "Analytics Dashboard",
            "Sales by Product",
            "Customer Spending Analysis",
            "Customer Segmentation",
            "Date-wise Revenue",
            "Revenue by City",
            "Orders by City",
            "Dashboard Date Filter",
            "Low Sales Products",
            "Most Ordered Product",
            "Top 5 Customers",
            "Top 5 Products",
            "Product Revenue Percentage",
            "Export Analytics Report",
            "Download Reports"
        )
    )
    if(choice3=="View All Customers"):
        mydb=get_connection()
        df=pd.read_sql(
            "select customer_id,customer_name,email,phone,city from customers",
            mydb
        )
        st.dataframe(
            df,
            use_container_width=True
        )
        mydb.close()
    elif(choice3=="Add New Customer"):
        name=st.text_input("Enter Customer Name")
        email=st.text_input("Enter Email")
        phone=st.text_input("Enter Phone")
        city=st.text_input("Enter City")
        pwd=st.text_input(
            "Enter Password",
            type="password"
        )
        btn=st.button("Add Customer")
        if(btn):
            mydb=get_connection()
            c=mydb.cursor()
            c.execute(
                """
                insert into customers
                (customer_name,email,phone,city,customer_pwd)
                values(?,?,?,?,?)
                """,
                (
                    name,
                    email,
                    phone,
                    city,
                    pwd
                )
            )
            mydb.commit()
            st.success("Customer Added Successfully")
            mydb.close()
    elif(choice3=="Update Customer"):
        mydb=get_connection()
        customers=pd.read_sql(
            "select customer_id,customer_name from customers",
            mydb
        )
        if(len(customers)>0):
            cid=st.selectbox(
                "Select Customer",
                customers["customer_id"].tolist()
            )
            row=customers[
                customers["customer_id"]==cid
            ].iloc[0]
            name=st.text_input(
                "Enter New Customer Name",
                value=row["customer_name"]
            )
            update=st.button("Update Customer")
            if(update):
                c=mydb.cursor()
                c.execute(
                    """
                    update customers
                    set customer_name=?
                    where customer_id=?
                    """,
                    (
                        name,
                        cid
                    )
                )
                mydb.commit()
                st.success("Customer Updated Successfully")
        mydb.close()
    elif(choice3=="Delete Customer"):
        mydb=get_connection()
        customers=pd.read_sql(
            "select customer_id,customer_name from customers",
            mydb
        )
        if(len(customers)>0):
            cid=st.selectbox(
                "Select Customer",
                customers["customer_id"].tolist()
            )
            delete=st.button("Delete Customer")
            if(delete):
                c=mydb.cursor()
                c.execute(
                    "delete from customers where customer_id=?",
                    (cid,)
                )
                mydb.commit()
                st.success("Customer Deleted Successfully")
        mydb.close()
    elif(choice3=="Customer Search"):
        search=st.text_input("Search Customer")
        mydb=get_connection()
        value="%"+search+"%"
        q="""
        select *
        from customers
        where customer_name like ?
        or email like ?
        or phone like ?
        or city like ?
        """
        df=pd.read_sql(
            q,
            mydb,
            params=(
                value,
                value,
                value,
                value
            )
        )
        st.dataframe(
            df,
            use_container_width=True
        )
        mydb.close()
    elif(choice3=="Customer Details"):
        mydb=get_connection()
        customers=pd.read_sql(
            "select customer_id,customer_name from customers",
            mydb
        )
        if(len(customers)>0):
            cid=st.selectbox(
                "Select Customer",
                customers["customer_id"].tolist()
            )
            q="""
            select
            c.customer_id,
            c.customer_name,
            c.email,
            c.phone,
            c.city,
            o.order_id,
            p.product_name,
            o.quantity,
            o.order_date,
            o.total_amount,
            o.order_status
            from customers c
            left join orders o
            on c.customer_id=o.customer_id
            left join products p
            on o.product_id=p.product_id
            where c.customer_id=?
            """
            try:
                df=pd.read_sql(
                    q,
                    mydb,
                    params=(cid,)
                )
                st.dataframe(
                    df,
                    use_container_width=True
                )
            except Exception as e:
                st.error(str(e))
        mydb.close()
    elif(choice3=="View Products"):
        mydb=get_connection()
        df=pd.read_sql(
            "select * from products",
            mydb
        )
        st.dataframe(
            df,
            use_container_width=True
        )
        mydb.close()
    elif(choice3=="Add New Product"):
        pname=st.text_input("Enter Product Name")
        price=st.number_input(
            "Enter Product Price",
            min_value=0.0
        )
        btn=st.button("Add Product")
        if(btn):
            mydb=get_connection()
            c=mydb.cursor()
            c.execute(
                """
                insert into products(product_name,price)
                values(?,?)
                """,
                (
                    pname,
                    price
                )
            )
            mydb.commit()
            st.success("Product Added Successfully")
            mydb.close()
    elif(choice3=="Update Product"):
        mydb=get_connection()
        products=pd.read_sql(
            "select * from products",
            mydb
        )
        if(len(products)>0):
            pid=st.selectbox(
                "Select Product",
                products["product_id"].tolist()
            )
            row=products[
                products["product_id"]==pid
            ].iloc[0]
            pname=st.text_input(
                "Product Name",
                value=row["product_name"]
            )
            price=st.number_input(
                "Product Price",
                value=float(row["price"])
            )
            update=st.button("Update Product")
            if(update):
                c=mydb.cursor()
                c.execute(
                    """
                    update products
                    set product_name=?,
                    price=?
                    where product_id=?
                    """,
                    (
                        pname,
                        price,
                        pid
                    )
                )
                mydb.commit()
                st.success("Product Updated Successfully")
        mydb.close()
    elif(choice3=="Delete Product"):
        mydb=get_connection()
        products=pd.read_sql(
            "select product_id,product_name from products",
            mydb
        )
        if(len(products)>0):
            pid=st.selectbox(
                "Select Product",
                products["product_id"].tolist()
            )
            delete=st.button("Delete Product")
            if(delete):
                c=mydb.cursor()
                c.execute(
                    "delete from products where product_id=?",
                    (pid,)
                )
                mydb.commit()
                st.success("Product Deleted Successfully")
        mydb.close()
    elif(choice3=="Product Search"):
        search=st.text_input("Search Product")
        mydb=get_connection()
        q="""
        select *
        from products
        where product_name like ?
        """
        df=pd.read_sql(
            q,
            mydb,
            params=("%"+search+"%",)
        )
        st.dataframe(
            df,
            use_container_width=True
        )
        mydb.close()
    elif(choice3=="View All Orders"):
        mydb=get_connection()
        q="""
        select
        o.order_id,
        c.customer_name,
        p.product_name,
        o.quantity,
        o.order_date,
        o.total_amount,
        o.order_status
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        join products p
        on o.product_id=p.product_id
        order by o.order_date desc
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Order Search"):
        search=st.text_input(
            "Search Order ID / Customer / Product"
        )
        mydb=get_connection()
        value="%"+search+"%"
        q="""
        select
        o.order_id,
        c.customer_name,
        p.product_name,
        o.quantity,
        o.order_date,
        o.total_amount,
        o.order_status
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        join products p
        on o.product_id=p.product_id
        where cast(o.order_id as char) like ?
        or c.customer_name like ?
        or p.product_name like ?
        """
        try:
            df=pd.read_sql(
                q,
                mydb,
                params=(
                    value,
                    value,
                    value
                )
            )
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Order Details"):
        mydb=get_connection()
        orders=pd.read_sql(
            "select order_id from orders",
            mydb
        )
        if(len(orders)>0):
            oid=st.selectbox(
                "Select Order",
                orders["order_id"].tolist()
            )
            q="""
            select
            o.order_id,
            c.customer_name,
            c.email,
            c.phone,
            p.product_name,
            p.price,
            o.quantity,
            o.order_date,
            o.total_amount,
            o.order_status
            from orders o
            join customers c
            on o.customer_id=c.customer_id
            join products p
            on o.product_id=p.product_id
            where o.order_id=?
            """
            try:
                df=pd.read_sql(
                    q,
                    mydb,
                    params=(oid,)
                )
                st.dataframe(
                    df,
                    use_container_width=True
                )
            except Exception as e:
                st.error(str(e))
        mydb.close()
    elif(choice3=="Update Order Status"):
        mydb=get_connection()
        orders=pd.read_sql(
            """
            select
            order_id,
            order_status
            from orders
            """,
            mydb
        )
        if(len(orders)>0):
            oid=st.selectbox(
                "Select Order",
                orders["order_id"].tolist()
            )
            status=st.selectbox(
                "Select New Status",
                (
                    "Confirmed",
                    "Processing",
                    "Shipped",
                    "Completed",
                    "Cancelled"
                )
            )
            update=st.button("Update Status")
            if(update):
                c=mydb.cursor()
                c.execute(
                    """
                    update orders
                    set order_status=?
                    where order_id=?
                    """,
                    (
                        status,
                        oid
                    )
                )
                mydb.commit()
                st.success("Order Status Updated Successfully")
        mydb.close()
    elif(choice3=="Delete Order"):
        mydb=get_connection()
        q="""
        select
        o.order_id,
        c.customer_name,
        p.product_name,
        o.quantity,
        o.order_date,
        o.total_amount,
        o.order_status
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        join products p
        on o.product_id=p.product_id
        order by o.order_date desc
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.subheader("Delete Order")
            if(len(df)>0):
                st.dataframe(
                    df,
                    use_container_width=True
                )
                oid=st.selectbox(
                    "Select Order to Delete",
                    df["order_id"].tolist()
                )
                delete=st.button("Delete Order")
                if(delete):
                    c=mydb.cursor()
                    c.execute(
                        "delete from orders where order_id=?",
                        (oid,)
                    )
                    mydb.commit()
                    st.success("Order Deleted Successfully")
                    st.rerun()
            else:
                st.info("No orders found")
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Date-wise Order Search"):
        date=st.date_input("Select Date")
        mydb=get_connection()
        q="""
        select
        o.order_id,
        c.customer_name,
        p.product_name,
        o.quantity,
        o.order_date,
        o.total_amount,
        o.order_status
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        join products p
        on o.product_id=p.product_id
        where date(o.order_date)=?
        """
        try:
            df=pd.read_sql(
                q,
                mydb,
                params=(date,)
            )
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Sales by Product"):
        mydb=get_connection()
        q="""
        select
        p.product_name,
        sum(o.quantity) as total_quantity,
        sum(o.total_amount) as total_sales
        from orders o
        join products p
        on o.product_id=p.product_id
        where o.order_status!='Cancelled'
        group by p.product_id,p.product_name
        order by total_sales desc
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.subheader("Sales by Product")
            st.dataframe(
                df,
                use_container_width=True
            )
            if(len(df)>0):
                st.bar_chart(
                    df.set_index("product_name")["total_sales"]
                )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Customer Spending Analysis"):
        mydb=get_connection()
        q="""
        select
        c.customer_name,
        sum(o.total_amount) as total_spending
        from customers c
        join orders o
        on c.customer_id=o.customer_id
        where o.order_status!='Cancelled'
        group by c.customer_id,c.customer_name
        order by total_spending desc
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.subheader("Customer Spending Analysis")
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Customer Segmentation"):
        mydb=get_connection()
        q="""
        select
        c.customer_name,
        sum(o.total_amount) as total_spending
        from customers c
        join orders o
        on c.customer_id=o.customer_id
        where o.order_status!='Cancelled'
        group by c.customer_id,c.customer_name
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            df["segment"]="Low Value"
            df.loc[
                df["total_spending"]>=20000,
                "segment"
            ]="Medium Value"
            df.loc[
                df["total_spending"]>=50000,
                "segment"
            ]="High Value"
            st.subheader("Customer Segmentation")
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Date-wise Revenue"):
        date=st.date_input("Select Date")
        mydb=get_connection()
        q="""
        select
        sum(total_amount) as revenue
        from orders
        where date(order_date)=?
        and order_status!='Cancelled'
        """
        try:
            df=pd.read_sql(
                q,
                mydb,
                params=(date,)
            )
            revenue=df.iloc[0]["revenue"]
            if(pd.isna(revenue)):
                revenue=0
            st.metric(
                "Date-wise Revenue",
                "₹"+str(round(revenue,2))
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Revenue by City"):
        mydb=get_connection()
        q="""
        select
        c.city,
        sum(o.total_amount) as revenue
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        where o.order_status!='Cancelled'
        group by c.city
        order by revenue desc
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.subheader("Revenue by City")
            st.dataframe(
                df,
                use_container_width=True
            )
            if(len(df)>0):
                st.bar_chart(
                    df.set_index("city")["revenue"]
                )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Orders by City"):
        mydb=get_connection()
        q="""
        select
        c.city,
        count(o.order_id) as total_orders
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        group by c.city
        order by total_orders desc
        """
        df=pd.read_sql(
            q,
            mydb
        )
        st.subheader("Orders by City")
        st.dataframe(
            df,
            use_container_width=True
        )
        if(len(df)>0):
            st.bar_chart(
                df.set_index("city")["total_orders"]
            )
        mydb.close()
    elif(choice3=="Dashboard Date Filter"):
        filter_choice=st.selectbox(
            "Select Date Range",
            (
                "Today",
                "Last 7 Days",
                "Last 30 Days",
                "All Time"
            )
        )
        today=datetime.datetime.now().date()
        if(filter_choice=="Today"):
            start_date=today
        elif(filter_choice=="Last 7 Days"):
            start_date=today-datetime.timedelta(days=7)
        elif(filter_choice=="Last 30 Days"):
            start_date=today-datetime.timedelta(days=30)
        else:
            start_date=None
        mydb=get_connection()
        try:
            if(start_date):
                q="""
                select
                count(order_id) as total_orders,
                sum(total_amount) as revenue
                from orders
                where date(order_date)>=?
                and order_status!='Cancelled'
                """
                df=pd.read_sql(
                    q,
                    mydb,
                    params=(start_date,)
                )
            else:
                q="""
                select
                count(order_id) as total_orders,
                sum(total_amount) as revenue
                from orders
                where order_status!='Cancelled'
                """
                df=pd.read_sql(
                    q,
                    mydb
                )
            orders=df.iloc[0]["total_orders"]
            revenue=df.iloc[0]["revenue"]
            if(pd.isna(revenue)):
                revenue=0
            st.metric(
                "Total Orders",
                int(orders)
            )
            st.metric(
                "Total Revenue",
                "₹"+str(round(revenue,2))
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Low Sales Products"):
        mydb=get_connection()
        q="""
        select
        p.product_name,
        coalesce(sum(o.quantity),0) as total_quantity
        from products p
        left join orders o
        on p.product_id=o.product_id
        group by p.product_id,p.product_name
        order by total_quantity asc
        """
        df=pd.read_sql(
            q,
            mydb
        )
        st.subheader("Low Sales Products")
        st.dataframe(
            df,
            use_container_width=True
        )
        mydb.close()
    elif(choice3=="Most Ordered Product"):
        mydb=get_connection()
        q="""
        select
        p.product_name,
        sum(o.quantity) as total_quantity
        from orders o
        join products p
        on o.product_id=p.product_id
        where o.order_status!='Cancelled'
        group by p.product_id,p.product_name
        order by total_quantity desc
        limit 1
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            if(len(df)>0):
                st.subheader("Most Ordered Product")
                st.metric(
                    "Product",
                    df.iloc[0]["product_name"]
                )
                st.write(
                    "Total Quantity:",
                    df.iloc[0]["total_quantity"]
                )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Top 5 Customers"):
        mydb=get_connection()
        q="""
        select
        c.customer_name,
        sum(o.total_amount) as total_spending
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        where o.order_status!='Cancelled'
        group by c.customer_id,c.customer_name
        order by total_spending desc
        limit 5
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.subheader("Top 5 Customers")
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Top 5 Products"):
        mydb=get_connection()
        q="""
        select
        p.product_name,
        sum(o.quantity) as total_quantity
        from orders o
        join products p
        on o.product_id=p.product_id
        where o.order_status!='Cancelled'
        group by p.product_id,p.product_name
        order by total_quantity desc
        limit 5
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            st.subheader("Top 5 Products")
            st.dataframe(
                df,
                use_container_width=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Product Revenue Percentage"):
        mydb=get_connection()
        q="""
        select
        p.product_name,
        sum(o.total_amount) as revenue
        from orders o
        join products p
        on o.product_id=p.product_id
        where o.order_status!='Cancelled'
        group by p.product_id,p.product_name
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            total=df["revenue"].sum()
            if(total>0):
                df["percentage"]=(df["revenue"]/total)*100
            else:
                df["percentage"]=0
            df["percentage"]=df["percentage"].round(2)
            st.subheader("Product Revenue Percentage")
            st.dataframe(
                df.style.format(
                    {
                        "revenue":"₹{:,.2f}",
                        "percentage":"{:.2f}%"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Export Analytics Report"):
        mydb=get_connection()
        q="""
        select
        o.order_id,
        c.customer_name,
        c.email,
        c.phone,
        c.city,
        p.product_name,
        o.quantity,
        o.order_date,
        o.total_amount,
        o.order_status
        from orders o
        join customers c
        on o.customer_id=c.customer_id
        join products p
        on o.product_id=p.product_id
        """
        try:
            df=pd.read_sql(
                q,
                mydb
            )
            csv=df.to_csv(
                index=False
            )
            st.subheader("Export Analytics Report")
            st.download_button(
                "Download Analytics CSV",
                csv,
                "analytics_report.csv",
                "text/csv"
            )
        except Exception as e:
            st.error(str(e))
        mydb.close()
    elif(choice3=="Download Reports"):
        report_choice=st.selectbox(
            "Select Report",
            (
                "Customer Report",
                "Product Report",
                "Order Report"
            )
        )
        mydb=get_connection()
        if(report_choice=="Customer Report"):
            df=pd.read_sql(
                "select customer_id,customer_name,email,phone,city from customers",
                mydb
            )
            file_name="customer_report.csv"
        elif(report_choice=="Product Report"):
            df=pd.read_sql(
                "select * from products",
                mydb
            )
            file_name="product_report.csv"
        else:
            try:
                df=pd.read_sql(
                    "select * from orders",
                    mydb
                )
            except Exception as e:
                df=pd.DataFrame()
            file_name="order_report.csv"
        csv=df.to_csv(
            index=False
        )
        st.download_button(
            "Download Report",
            csv,
            file_name,
            "text/csv"
        )
        mydb.close()
    elif(choice3=="Analytics Dashboard"):
        mydb=get_connection()
        st.subheader("Customer Analytics Dashboard")
        c=mydb.cursor()
        c.execute(
            "select distinct city from customers"
        )
        cities=["All"]
        for r in c.fetchall():
            if(r[0] not in cities):
                cities.append(r[0])
        city=st.selectbox(
            "Select City",
            cities
        )
        if(city=="All"):
            q="select count(*) as total from customers"
            df1=pd.read_sql(
                q,
                mydb
            )
            total_customers=df1.iloc[0,0]
            q="""
            select count(*) as total
            from orders
            where order_status!='Cancelled'
            """
            df2=pd.read_sql(
                q,
                mydb
            )
            total_orders=df2.iloc[0,0]
            q="""
            select sum(total_amount) as total
            from orders
            where order_status!='Cancelled'
            """
            df3=pd.read_sql(
                q,
                mydb
            )
            total_revenue=df3.iloc[0,0]
            q="""
            select avg(total_amount) as total
            from orders
            where order_status!='Cancelled'
            """
            df4=pd.read_sql(
                q,
                mydb
            )
            avg_order=df4.iloc[0,0]
        else:
            q="""
            select count(*) as total
            from customers
            where city=?
            """
            df1=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
            total_customers=df1.iloc[0,0]
            q="""
            select count(*) as total
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            """
            df2=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
            total_orders=df2.iloc[0,0]
            q="""
            select sum(o.total_amount) as total
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            """
            df3=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
            total_revenue=df3.iloc[0,0]
            q="""
            select avg(o.total_amount) as total
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            """
            df4=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
            avg_order=df4.iloc[0,0]
        if(total_revenue is None):
            total_revenue=0
        if(avg_order is None):
            avg_order=0
        col1,col2,col3,col4=st.columns(4)
        col1.metric(
            "Total Customers",
            total_customers
        )
        col2.metric(
            "Total Orders",
            total_orders
        )
        col3.metric(
            "Total Revenue",
            "₹"+str(round(total_revenue,2))
        )
        col4.metric(
            "Average Order Value",
            "₹"+format(avg_order,",.2f")
        )
        st.write("")
        if(city=="All"):
            q="""
            select
            date(order_date) as order_date,
            sum(total_amount) as revenue
            from orders
            where order_status!='Cancelled'
            group by date(order_date)
            order by order_date
            """
            df=pd.read_sql(
                q,
                mydb
            )
        else:
            q="""
            select
            date(o.order_date) as order_date,
            sum(o.total_amount) as revenue
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            group by date(o.order_date)
            order by order_date
            """
            df=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
        st.write("Daily Revenue")
        if(len(df)>0):
            st.line_chart(
                df.set_index("order_date")["revenue"]
            )
        if(city=="All"):
            q="""
            select
            p.product_name,
            sum(o.total_amount) as revenue
            from orders o,products p
            where o.product_id=p.product_id
            and o.order_status!='Cancelled'
            group by p.product_id,p.product_name
            order by revenue desc
            """
            df=pd.read_sql(
                q,
                mydb
            )
        else:
            q="""
            select
            p.product_name,
            sum(o.total_amount) as revenue
            from orders o,products p,customers c
            where o.product_id=p.product_id
            and o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            group by p.product_id,p.product_name
            order by revenue desc
            """
            df=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
        st.write("Top Products")
        if(len(df)>0):
            st.bar_chart(
                df.set_index("product_name")["revenue"]
            )
        st.write("Top Customers")
        if(city=="All"):
            q="""
            select
            c.customer_name,
            sum(o.total_amount) as revenue
            from orders o,customers c
            where o.customer_id=c.customer_id
            and o.order_status!='Cancelled'
            group by c.customer_id,c.customer_name
            order by revenue desc
            """
            df=pd.read_sql(
                q,
                mydb
            )
        else:
            q="""
            select
            c.customer_name,
            sum(o.total_amount) as revenue
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            group by c.customer_id,c.customer_name
            order by revenue desc
            """
            df=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
        if(len(df)>0):
            st.bar_chart(
                df.set_index("customer_name")["revenue"]
            )
        st.write("Customers by City")
        q="""
        select
        city,
        count(*) as customers
        from customers
        group by city
        order by customers desc
        """
        df=pd.read_sql(
            q,
            mydb
        )
        if(len(df)>0):
            st.bar_chart(
                df.set_index("city")["customers"]
            )
        st.write("Monthly Orders")
        if(city=="All"):
            q="""
            select
            strftime('%Y-%m', order_date) as month,
            count(*) as orders
            from orders
            where order_status!='Cancelled'
            group by month
            order by month
            """
            df=pd.read_sql(
                q,
                mydb
            )
        else:
            q="""
            select
            strftime('%Y-%m', o.order_date) as month,
            count(*) as orders
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            group by month
            order by month
            """
            df=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
        if(len(df)>0):
            st.bar_chart(
                df.set_index("month")["orders"]
            )
        st.write("Monthly Revenue")
        if(city=="All"):
            q="""
            select
            strftime('%Y-%m', order_date) as month,
            sum(total_amount) as revenue
            from orders
            where order_status!='Cancelled'
            group by month
            order by month
            """
            df=pd.read_sql(
                q,
                mydb
            )
        else:
            q="""
            select
            strftime('%Y-%m', o.order_date) as month,
            sum(o.total_amount) as revenue
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            group by month
            order by month
            """
            df=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
        if(len(df)>0):
            st.bar_chart(
                df.set_index("month")["revenue"]
            )
        st.subheader("Customer Purchase Analysis")
        if(city=="All"):
            q="""
            select
            customer_id,
            count(*) as orders
            from orders
            where order_status!='Cancelled'
            group by customer_id
            """
            df=pd.read_sql(
                q,
                mydb
            )
        else:
            q="""
            select
            o.customer_id,
            count(*) as orders
            from orders o,customers c
            where o.customer_id=c.customer_id
            and c.city=?
            and o.order_status!='Cancelled'
            group by o.customer_id
            """
            df=pd.read_sql(
                q,
                mydb,
                params=(city,)
            )
        if(len(df)>0):
            repeat_customers=len(
                df[df["orders"]>1]
            )
            one_time_customers=len(
                df[df["orders"]==1]
            )
        else:
            repeat_customers=0
            one_time_customers=0
        st.write(
            "Repeat Customers:",
            repeat_customers
        )
        st.write(
            "One-Time Customers:",
            one_time_customers
        )
        data=pd.DataFrame(
            {
                "Customer Type":
                [
                    "One-Time Customers",
                    "Repeat Customers"
                ],
                "Customers":
                [
                    one_time_customers,
                    repeat_customers
                ]
            }
        )
        st.write("Customer Type Analysis")
        st.bar_chart(
            data.set_index("Customer Type")["Customers"]
        )
        mydb.close()
