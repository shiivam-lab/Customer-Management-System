CREATE DATABASE cms;
USE cms;

CREATE TABLE customers(
customer_id INT PRIMARY KEY AUTO_INCREMENT,
customer_name VARCHAR(100),
email VARCHAR(100),
phone VARCHAR(15),
city VARCHAR(50)
);

INSERT INTO customers(customer_name,email,phone,city)
VALUES
('Rahul Sharma','rahul@gmail.com','9876543210','Ahmedabad'),
('Priya Patel','priya@gmail.com','9876543211','Anand'),
('Amit Shah','amit@gmail.com','9876543212','Vadodara'),
('Neha Mehta','neha@gmail.com','9876543213','Surat'),
('Rohit Desai','rohit@gmail.com','9876543214','Rajkot'),
('Pooja Shah','pooja@gmail.com','9876543215','Ahmedabad'),
('Karan Patel','karan@gmail.com','9876543216','Anand'),
('Sneha Joshi','sneha@gmail.com','9876543217','Vadodara'),
('Vishal Mehta','vishal@gmail.com','9876543218','Surat'),
('Riya Desai','riya@gmail.com','9876543219','Rajkot');

ALTER TABLE customers
ADD customer_pwd VARCHAR(100);


UPDATE customers SET customer_pwd='rahul123' WHERE customer_id=1;
UPDATE customers SET customer_pwd='priya123' WHERE customer_id=2;
UPDATE customers SET customer_pwd='amit123' WHERE customer_id=3;
UPDATE customers SET customer_pwd='neha123' WHERE customer_id=4;
UPDATE customers SET customer_pwd='rohit123' WHERE customer_id=5;
UPDATE customers SET customer_pwd='pooja123' WHERE customer_id=6;
UPDATE customers SET customer_pwd='karan123' WHERE customer_id=7;
UPDATE customers SET customer_pwd='sneha123' WHERE customer_id=8;
UPDATE customers SET customer_pwd='vishal123' WHERE customer_id=9;
UPDATE customers SET customer_pwd='riya123' WHERE customer_id=10;

DELETE FROM customers
WHERE customer_id=11;

SELECT * FROM CUSTOMERS;


CREATE TABLE products(
product_id INT PRIMARY KEY AUTO_INCREMENT,
product_name VARCHAR(100),
price DECIMAL(10,2)
);

INSERT INTO products(product_name,price)
VALUES
('Laptop',55000),
('Smartphone',25000),
('Headphones',2500),
('Keyboard',1500),
('Mouse',800),
('Monitor',12000),
('Printer',15000),
('Webcam',3000),
('Tablet',18000),
('Smart Watch',5000);

SELECT * FROM products


CREATE TABLE admins(
admin_id INT PRIMARY KEY AUTO_INCREMENT,
admin_name VARCHAR(100),
admin_pwd VARCHAR(100)
);
INSERT INTO admins(admin_name,admin_pwd)
VALUES
('admin','admin123'),
('manager','manager123');

SELECT * FROM admins


CREATE TABLE orders(
order_id INT PRIMARY KEY AUTO_INCREMENT,
customer_id INT,
product_id INT,
quantity INT,
order_date DATE,
total_amount DECIMAL(10,2),

FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
FOREIGN KEY(product_id) REFERENCES products(product_id)
); 

INSERT INTO orders(customer_id,product_id,quantity,order_date,total_amount)
VALUES
(1,1,1,'2026-08-01',55000),
(2,3,2,'2026-08-02',5000),
(3,2,1,'2026-08-03',25000),
(4,6,1,'2026-08-04',12000),
(5,5,3,'2026-08-05',2400),
(6,4,2,'2026-08-06',3000),
(7,9,1,'2026-08-07',18000),
(8,8,2,'2026-08-08',6000),
(9,7,1,'2026-08-09',15000),
(10,10,1,'2026-08-10',5000),
(1,2,1,'2026-08-11',25000),
(3,3,3,'2026-08-12',7500),
(5,1,1,'2026-08-13',55000),
(7,5,2,'2026-08-14',1600),
(2,10,1,'2026-08-15',5000);


SELECT * FROM ORDERS; 


SELECT customer_id,customer_name,customer_pwd
FROM customers
WHERE customer_id=6; 

SELECT customer_id,customer_name,customer_pwd
FROM customers
WHERE customer_id=1; 

SELECT order_id,order_status FROM orders WHERE order_id=18; 

DESCRIBE orders; 

ALTER TABLE orders
MODIFY order_date DATETIME;