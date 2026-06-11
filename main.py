import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# CSV File Load

try:
    # Apne hisaab se path change kar sakta hu
    df = pd.read_csv("PROJECT TABLES/crime_data.csv")
except FileNotFoundError:
    print("crime_data.csv file nahi mili.")
    exit()


# Data Preview

print(" First 5 Records ")
print(df.head())


# Duplicate aur Missing Data

df = df.drop_duplicates()
df = df.fillna("Unknown")

# Date se Year nikal rahe hain

df["Year"] = pd.to_datetime(df["Date"]).dt.year

print("Total Records :", len(df))


# City Wise Crime Count

print("Crime Count by City")
print(df["City"].value_counts())


# Crime Type Count
print("Crime Type Count")
print(df["Crime_Type"].value_counts())


# SQLite Database
conn = sqlite3.connect("crime_database.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS crimes")

cursor.execute("""
CREATE TABLE IF NOT EXISTS crimes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    state TEXT,
    crime_type TEXT,
    year INTEGER,
    status TEXT
)
""")


# Data Database me Save

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO crimes(city,state,crime_type,year,status)
    VALUES(?,?,?,?,?)
    """, (
        row["City"],
        row["State"],
        row["Crime_Type"],
        int(row["Year"]),
        row["Status"]
    ))

conn.commit()

print("Data Successfully Saved!")


# Top 5 Cities

print("Top 5 Cities")
print(df["City"].value_counts().head())


# Graph - City Wise Crime

plt.figure(figsize=(8,5))
df["City"].value_counts().plot(kind="bar")
plt.title("Crime Count by City")
plt.xlabel("City")
plt.ylabel("Cases")
plt.tight_layout()
plt.show()


# Graph - Crime Type
plt.figure(figsize=(7,7))
df["Crime_Type"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.ylabel("")
plt.title("Crime Type Distribution")
plt.tight_layout()
plt.show()


# Save Final Report

df.to_csv("crime_report.csv", index=False)

print("ncrime_report.csv save ho gayi.")
print("Project Successfully Completed.")

conn.close()