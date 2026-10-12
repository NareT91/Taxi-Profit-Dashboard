
import pandas as pd

financial_data = {
    "Month": ["June", "July", "August", "September"],
    "Taxi1_Income": [42000, 45000, 47000, 44000],
    "Taxi1_Expenses": [18000, 19000, 20000, 18500],
    "Taxi2_Income": [40000, 43000, 45000, 42000],
    "Taxi2_Expenses": [17000, 18000, 19000, 18000]
}

df = pd.DataFrame(financial_data)

df["Taxi1_Profit"] = df["Taxi1_Income"] - df["Taxi1_Expenses"]
df["Taxi2_Profit"] = df["Taxi2_Income"] - df["Taxi2_Expenses"]

df["Total_Income"] = df["Taxi1_Income"] + df["Taxi2_Income"]
df["Total_Expenses"] = df["Taxi1_Expenses"] + df["Taxi2_Expenses"]
df["Total_Profit"] = df["Taxi1_Profit"] + df["Taxi2_Profit"]


def get_dashboard_data():
    total_income = int(df["Total_Income"].sum())
    total_expenses = int(df["Total_Expenses"].sum())
    total_profit = int(df["Total_Profit"].sum())

    taxi1_profit = int(df["Taxi1_Profit"].sum())
    taxi2_profit = int(df["Taxi2_Profit"].sum())

    monthly_data = df[
        ["Month", "Total_Profit", "Taxi1_Profit", "Taxi2_Profit"]
    ].to_dict(orient="records")

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "taxi1_profit": taxi1_profit,
        "taxi2_profit": taxi2_profit,
        "monthly_data": monthly_data
    }