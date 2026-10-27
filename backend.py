import mysql.connector
import os

mydb=mysql.connector.connect(
    host=os.getenv("DB_HOST","localhost"),
    user=os.getenv("DB_USER","root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME","cms")
)

print(mydb)

name=input("Enter Customer Name: ")
email=input("Enter Email: ")
phone=input("Enter Phone: ")
city=input("Enter City: ")
pwd=input("Enter Password: ")

c=mydb.cursor()

c.execute(
    "insert into customers(customer_name,email,phone,city,customer_pwd) values(%s,%s,%s,%s,%s)",
    (name,email,phone,city,pwd)
)

mydb.commit()

print("Customer Added Successfully")

c.close()
mydb.close()

