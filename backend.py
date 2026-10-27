import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",password="123456789",database="customer_management_system")
print(mydb)

name=input("Enter Customer Name: ")
email=input("Enter Email: ")
phone=input("Enter Phone: ")
city=input("Enter City: ")
pwd=input("Enter Password: ")

c=mydb.cursor()

c.execute("insert into customers(customer_name,email,phone,city,customer_pwd) values(%s,%s,%s,%s,%s)",(name,email,phone,city,pwd))

mydb.commit()

print("Customer Added Successfully")
