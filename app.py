
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_database
from taxi_data import get_dashboard_data

app = Flask(__name__)
app.secret_key = "taxi_project_demo_secret_key"

DATABASE = "taxi_management.db"

create_database()


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = get_db_connection()
        user = connection.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        connection.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]
            return redirect(url_for("dashboard"))

        flash("Incorrect email or password.")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not fullname or not email or not password:
            flash("Please complete all required fields.")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO users (fullname, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (fullname, email, generate_password_hash(password))
            )
            connection.commit()
            flash("Account created successfully. Please log in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("This email address is already registered.")
            return redirect(url_for("register"))

        finally:
            connection.close()

    return render_template("register.html")



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    records = connection.execute(
        """
        SELECT
            month,
            taxi_name,
            SUM(income) AS income,
            SUM(expenses) AS expenses
        FROM taxi_records
        WHERE user_id = ?
        GROUP BY month, taxi_name
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly_summary = {}

    total_income = 0
    total_expenses = 0
    taxi1_profit = 0
    taxi2_profit = 0

    for record in records:
        month = record["month"]
        taxi = record["taxi_name"]
        income = float(record["income"] or 0)
        expenses = float(record["expenses"] or 0)
        profit = income - expenses

        total_income += income
        total_expenses += expenses

        if month not in monthly_summary:
            monthly_summary[month] = {
                "Month": month,
                "Total_Profit": 0,
                "Taxi1_Profit": 0,
                "Taxi2_Profit": 0
            }

        monthly_summary[month]["Total_Profit"] += profit

        if taxi == "Taxi 1":
            taxi1_profit += profit
            monthly_summary[month]["Taxi1_Profit"] += profit
        elif taxi == "Taxi 2":
            taxi2_profit += profit
            monthly_summary[month]["Taxi2_Profit"] += profit

    monthly_data = [
        monthly_summary[month]
        for month in month_order
        if month in monthly_summary
    ]

    total_profit = total_income - total_expenses

    return render_template(
        "dashboard.html",
        fullname=session.get("fullname", "User"),
        total_income=total_income,
        total_expenses=total_expenses,
        total_profit=total_profit,
        taxi1_profit=taxi1_profit,
        taxi2_profit=taxi2_profit,
        monthly_data=monthly_data
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/add_record", methods=["GET", "POST"])
def add_record():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        taxi_name = request.form.get("taxi_name", "")
        month = request.form.get("month", "")

        try:
            income = float(request.form.get("income", ""))
            expenses = float(request.form.get("expenses", ""))

            if income < 0 or expenses < 0:
                raise ValueError

        except (ValueError, TypeError):
            flash("Enter valid, non-negative amounts.")
            return redirect(url_for("add_record"))

        if taxi_name not in ("Taxi 1", "Taxi 2"):
            flash("Please select a valid taxi.")
            return redirect(url_for("add_record"))

        valid_months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        if month not in valid_months:
            flash("Please select a valid month.")
            return redirect(url_for("add_record"))

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO taxi_records
                (user_id, taxi_name, month, income, expenses)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session["user_id"], taxi_name, month, income, expenses)
        )
        connection.commit()
        connection.close()

        flash("Taxi record saved successfully.")
        return redirect(url_for("dashboard"))

    return render_template("add_record.html")


MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


@app.route("/set_target", methods=["GET", "POST"])
def set_target():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        taxi_name = request.form.get("taxi_name", "")
        month = request.form.get("month", "")

        try:
            target = float(request.form.get("target", ""))
            if target <= 0:
                raise ValueError
        except (ValueError, TypeError):
            flash("Enter a target greater than zero.")
            return redirect(url_for("set_target"))

        if taxi_name not in ("Taxi 1", "Taxi 2") or month not in MONTHS:
            flash("Please select a valid taxi and month.")
            return redirect(url_for("set_target"))

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO taxi_targets (user_id, taxi_name, month, target)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, taxi_name, month)
            DO UPDATE SET target = excluded.target
            """,
            (session["user_id"], taxi_name, month, target)
        )
        connection.commit()
        connection.close()

        flash("Monthly target saved successfully.")
        return redirect(url_for("performance"))

    return render_template("set_target.html", months=MONTHS)

@app.route("/performance")
def performance():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    records = connection.execute(
        """
        SELECT month, taxi_name,
               SUM(income) AS income,
               SUM(expenses) AS expenses
        FROM taxi_records
        WHERE user_id = ?
        GROUP BY month, taxi_name
        """,
        (session["user_id"],)
    ).fetchall()

    targets = connection.execute(
        """
        SELECT month, taxi_name, target
        FROM taxi_targets
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    target_lookup = {
        (row["month"], row["taxi_name"]): row["target"]
        for row in targets
    }

    performance_data = []

    for record in records:
        month = record["month"]
        taxi = record["taxi_name"]
        profit = float(record["income"]) - float(record["expenses"])
        target = target_lookup.get((month, taxi))

        if target is None:
            percentage = None
            status = "Target not set"
        else:
            percentage = round((profit / target) * 100, 1)

            if percentage >= 110:
                status = "Excellent"
            elif percentage >= 100:
                status = "Good"
            elif percentage >= 90:
                status = "Average"
            else:
                status = "Poor"

        performance_data.append({
            "month": month,
            "taxi": taxi,
            "profit": round(profit, 2),
            "target": target,
            "percentage": percentage,
            "status": status
        })

    performance_data.sort(
        key=lambda row: (MONTHS.index(row["month"]), row["taxi"])
    )

    return render_template(
        "performance.html",
        fullname=session.get("fullname", "User"),
        performance_data=performance_data
    )


if __name__ == "__main__":
    app.run(debug=True)