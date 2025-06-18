# 🧾 Commission Forecast App

This is a Flask-based web application that uses a SARIMA model to forecast future sales and automatically calculate commission amounts based on business rules.

---

## 🚀 Features

- 📁 Upload CSV file with historical sales data
- 📊 Predict future sales using a trained SARIMA model
- 💰 Automatically apply commission rules:
  - ≤ ₹10,000 → 5%
  - ≤ ₹50,000 → 10%
  - > ₹50,000 → 15%
- 📥 Download forecast and commission results as CSV
- 🌐 Deployable on Render (or any cloud platform)

---

## 🛠 Tech Stack

- Python
- Flask
- Pandas
- Statsmodels (SARIMAX)
- Gunicorn
- HTML/CSS (Jinja templates)
- Render.com (for deployment)

---

## 🗂 Project Structure
commission-forecast-app/
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
├── static/
│ └── style.css
├── model/
│ └── final_sarima_model.pkl
├── uploads/
├── downloads/
└── .render.yaml


---

## 📄 Input Format

Upload a CSV file that contains at least one column:

| Column Name   | Description          |
|---------------|----------------------|
| `Sales_Amount`| Monthly sales values |

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/VineethReddy1997/commission-forecast-app.git
cd commission-forecast-app

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

Go to http://localhost:5000 in your browser.

🌍 Live Demo
👉 https://commission-forecast-app.onrender.com

📦 Deploy to Render
Create a free Render account: https://render.com

Connect your GitHub repo

Set build & start commands:

Setting	Value
Build Command	pip install -r requirements.txt
Start Command	gunicorn app:app

Enable Auto Deploy

Done!

🧠 Business Logic
Forecasted Sale	Commission %
≤ ₹10,000	5%
≤ ₹50,000	10%
> ₹50,000	15%

---

## 📧 Contact

## Created by [Vineeth Reddy](https://github.com/VineethReddy1997)


Feel free to raise issues or suggestions!
