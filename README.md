# Customer Management System

A Streamlit-based Customer Management System built with Python, MySQL Connector, and pandas. The application has Home, Customer, and Admin sections for customer accounts, products, orders, and reporting/analytics.

## Features

- Customer login and account/profile features
- Customer order viewing and order actions
- Admin workflows for managing customers, products, and orders
- Reporting and analytics, including CSV export options

## Tech stack

- Python
- Streamlit
- MySQL
- mysql-connector-python
- pandas

## Setup

1. Install Python and MySQL Server, and create/configure the local MySQL database named `cms`.
2. Install dependencies from this folder:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Set these environment variables on your own computer (do not put the password in source code):
   - `DB_HOST` = `localhost`
   - `DB_USER` = your MySQL username (often `root` locally)
   - `DB_PASSWORD` = your actual MySQL password
   - `DB_NAME` = `cms`
4. Ensure your database has the tables/columns expected by `main.py`. **The original CMS database SQL export was not included in the files available for packaging**, so this ZIP does not invent a schema. Export the working `cms` database from MySQL Workbench and add the SQL export to this project if you want to publish it. Remove any personal/customer data before sharing.
5. Run the app from this folder:
   ```bash
   python -m streamlit run main.py
   ```
6. Streamlit will show a local address, usually `http://localhost:8501`. Open it in your browser.

## Image asset

The app can display `CMS.jpg` or `cms.jpg` on the Home page if you add that image to this folder. The application will still run if the image is absent.

## Security notes

- Never commit your real database password, `.env` file, database dumps with private data, or virtual-environment folders.
- This project currently uses a local MySQL database. A public deployment needs a separately configured database and appropriate access/security settings.
