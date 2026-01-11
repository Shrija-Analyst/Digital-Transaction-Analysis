from sqlalchemy import create_engine
engine=create_engine( "mysql+pymysql://root:Shri%401202@localhost:3306/digital_transaction")
import pandas as pd

df=pd.read_sql("select * from transactions ",engine)
print(df.columns)
df["txn_date"]=pd.to_datetime(df["txn_date"])
df["year_month"]=df["txn_date"].dt.to_period("M")
df["status"]=df["status"].str.lower()

df=df[df["status"]=="success"]
print(df.isnull().sum())

print("Total transactions:",df.shape[0])
print("Total revenue:",df["amount"].sum())
print("Average amount:",df["amount"].mean())

platform_sales=df.groupby("payment_mode")["amount"].sum()
print(platform_sales)

df["month"]=df["txn_date"].dt.month
monthly_sales=df.groupby("month")["amount"].sum().reindex(range(1,13),fill_value=0)
print(monthly_sales)

mean=df["amount"].mean()
std=df["amount"].std()
outliers=df[df["amount"]>mean+2*std]
print(outliers)

import matplotlib.pyplot as plt

monthly_sales.plot(kind="line",marker="o",title="Monthly Trend Transaction")
plt.xlabel("Month")
plt.ylabel("Total Amount")
plt.show()

platform_sales.plot(kind="bar",title="Platform sales Trend")
plt.show()

platform_sales_df=platform_sales.reset_index()
platform_sales_df.to_sql(
    "platform_summary",
    con=engine,
    if_exists="replace",
    index=False
)


