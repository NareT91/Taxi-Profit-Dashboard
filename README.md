# Taxi Profit & Driver Performance Management System

## About the Project

The Taxi Profit & Driver Performance Management System is a Python-based web application developed to help taxi operators monitor income, expenses, profit, and monthly performance targets for their taxis.

The system is designed to provide a simple way to record financial information and review taxi performance through a dashboard.

This personal project demonstrates my practical skills in Python, Flask, SQLite, and web application development. It was created to gain hands-on experience in building a web-based system for taxi financial management and performance tracking.


## Objectives

* Record taxi income and operating expenses.
* Calculate profit by subtracting expenses from income.
* Monitor the performance of individual taxis.
* Set monthly profit targets.
* Display financial summaries and charts on a dashboard.
* Provide user registration and login functionality.

## Technologies Used

* **Python** — application logic
* **Flask** — web application framework
* **SQLite** — database management
* **HTML** — web page structure
* **CSS** — user interface styling
* **Chart.js** — dashboard charts
* **Git and GitHub** — version control and project hosting

## Main Features

* User registration and login
* Taxi income and expense records
* Profit calculations
* Monthly profit targets
* Taxi performance monitoring
* Dashboard with financial summaries and charts

## Project Structure


taxi_profit_system/
├── app.py
├── database.py
├── templates/
├── static/
│   └── css/
├── .gitignore
└── README.md


## Installation and Setup

### 1. Clone the repository


git clone https://github.com/NareT91/Taxi-Profit-Dashboard.git
cd Taxi-Profit-Dashboard


### 2. Create a virtual environment


python3 -m venv .venv


### 3. Activate the virtual environment

On macOS or Linux:


source .venv/bin/activate


On Windows:


.venv\Scripts\activate


### 4. Install Flask


python -m pip install flask


### 5. Create the database tables


python database.py


### 6. Run the application


python app.py


Open the local address displayed in your terminal in your web browser. It will normally be:


http://127.0.0.1:5000


## Database

The application uses SQLite to store user accounts, taxi financial records, and monthly profit targets.

The database tables are created by the database setup script.

## Future Improvements

Potential improvements include enhanced reporting, exporting financial summaries, additional taxi management features, and improved performance analysis.

## Developer

**Name:** Nare Tlabela
**Qualification:** Advanced Diploma in Computer Systems Engineering
**Institution:** Tshwane University of Technology

## Project Status

This project is under development. Features and functionality may change as development continues.
