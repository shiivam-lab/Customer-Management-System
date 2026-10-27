# Customer Management System

A Python-based Customer Management System built with Streamlit to demonstrate customer account management, product browsing, order processing, and administrative operations through an interactive web interface.

**Live Demo:** [Open Customer Management System](https://customer-management-system-mrscfcucpevv3qufx5grgb.streamlit.app/)

**GitHub Repository:** [View Source Code](https://github.com/shiivam-lab/Customer-Management-System)

---

## Project Overview

The Customer Management System is a web application designed to demonstrate common customer and order management workflows.

The application provides separate customer-facing and administrative features, allowing users to explore customer information, manage orders, browse products, and review management information.

The project also demonstrates Python application development, interactive UI design, data handling, and cloud deployment using Streamlit Community Cloud.

## Key Features

### Customer Management
- Customer login and profile access
- View and update customer information
- Password update functionality
- Access customer order information

### Product Management
- Browse available products
- Administrative product management
- Product information management

### Order Management
- Place orders using the demo interface
- View existing orders
- Cancel eligible orders
- Explore order management workflows

### Admin Panel
- Customer management operations
- Product management operations
- Order management
- Search and review records
- Analytics and data export features

### Interactive Interface
- Built with Streamlit
- Interactive forms and tables
- CSV export options for supported views
- Cloud-hosted demonstration

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Pandas | Data handling and tabular operations |
| MySQL Connector | Database connectivity in the original implementation |
| SQL | Relational database schema and queries |
| GitHub | Source code management |
| Streamlit Community Cloud | Live demo hosting |

> **Deployment note:** The current hosted portfolio demo uses sample data and in-memory session state instead of requiring a separately hosted MySQL server. The original repository also contains database-related files. The deployed demo and the original database-backed implementation should therefore be treated as distinct configurations.

## Live Demo

Try the application here:

**[Launch the Live Demo](https://customer-management-system-mrscfcucpevv3qufx5grgb.streamlit.app/)**

The live version is intended for portfolio demonstration and exploration.

### Demo Limitations
- Sample data is used for demonstration purposes.
- Changes made during a session may not persist after the app restarts.
- The demo is not intended for storing real customer information.
- Do not enter personal, confidential, or sensitive information.

## Project Structure

```text
Customer-Management-System/
│
├── main.py           # Streamlit application
├── backend.py        # Database-related backend operations
├── cms.sql           # SQL database schema / SQL setup
├── requirements.txt  # Python dependencies
├── .env.example      # Example environment configuration
├── .gitignore        # Git exclusions
├── CMS.jpg           # Project image
└── README.md         # Project documentation
```

## Run the Project Locally

### Prerequisites

- Python 3.9 or a compatible version supported by the dependencies
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/shiivam-lab/Customer-Management-System.git
```

### 2. Open the project directory

```bash
cd Customer-Management-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run main.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

> The current demo version uses sample data. Running the original database-backed configuration may require additional MySQL setup and environment variables.

## Learning Outcomes

This project demonstrates practical experience with:

- Building interactive Python applications
- Developing user-facing forms and administrative interfaces
- Organizing customer, product, and order workflows
- Working with tabular data
- Understanding relational databases and SQL
- Managing source code with GitHub
- Deploying a Python application to the cloud
- Documenting a project for portfolio presentation

## Future Improvements

Potential enhancements include:

- Integrating a persistent cloud database
- Improving authentication and password security
- Adding role-based access controls
- Implementing input validation and error handling
- Expanding analytics and reporting
- Adding automated tests
- Improving the mobile user experience

## Author

**Shivam Pandya**

GitHub: [@shiivam-lab](https://github.com/shiivam-lab)

LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/digitalshiivam/)

---

*Built as a portfolio project to demonstrate Python application development, data handling, and cloud deployment.*
