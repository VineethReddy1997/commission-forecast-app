# # from flask import Flask, render_template, request
# # import pandas as pd
# # import os
# # import joblib

# # app = Flask(__name__)
# # app.config['UPLOAD_FOLDER'] = 'uploads'
# # os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # import joblib
# # model = joblib.load(r"D:\Time series Analysis\model\final_sarima_model.pkl")


# # @app.route('/')
# # def home():
# #     return render_template('index.html')

# # @app.route('/predict', methods=['POST'])
# # def predict():
# #     if 'file' not in request.files:
# #         return 'No file part in request.'

# #     file = request.files['file']
# #     if file.filename == '':
# #         return 'No selected file.'

# #     if file:
# #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# #         file.save(filepath)

# #         try:
# #             df = pd.read_csv(filepath)

# #             # ✅ Check if 'Sales' column exists
# #             if 'Sales_Amount' not in df.columns:
# #                 return render_template("index.html", error="Error: CSV must contain a 'Sales' column.")

# #             if df['Sales_Amount'].isnull().any():
# #                 return render_template("index.html", error="Error: 'Sales' column contains missing values.")

# #             if len(df) < 10:
# #                 return render_template("index.html", error="Error: At least 10 rows of data required.")

# #             # Forecast future values
# #             steps = int(request.form.get('steps', 5))
# #             forecast = model.get_forecast(steps=steps)
# #             forecast_values = forecast.predicted_mean.tolist()

# #             # Commission logic
# #             def calculate_commission(sale):
# #                 if sale <= 10000:
# #                     return round(sale * 0.05, 2)
# #                 elif sale <= 50000:
# #                     return round(sale * 0.10, 2)
# #                 else:
# #                     return round(sale * 0.15, 2)

# #             commissions = [calculate_commission(s) for s in forecast_values]
# #             results = list(zip(forecast_values, commissions))

# #             return render_template("index.html", results=results)

# #         except Exception as e:
# #             return render_template("index.html", error=f"Prediction error: {str(e)}")

# #     return render_template("index.html", error="Unexpected error.")
# # if __name__ == '__main__':
# #     app.run(debug=True)






# from flask import Flask, render_template, request, redirect, url_for, session
# from datetime import datetime
# import pandas as pd
# import os
# import joblib

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Required for session
# app.config['UPLOAD_FOLDER'] = 'uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# import joblib
# model = joblib.load(r"D:\Time series Analysis\model\final_sarima_model.pkl")


# @app.route('/')
# def home():
#     results = session.pop('results', None)
#     error = session.pop('error', None)
#     return render_template('index.html', results=results, error=error, year=datetime.now().year)

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         session['error'] = 'No file part in request.'
#         return redirect(url_for('home'))

#     file = request.files['file']
#     if file.filename == '':
#         session['error'] = 'No selected file.'
#         return redirect(url_for('home'))

#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)

#         try:
#             df = pd.read_csv(filepath)

#             if 'Sales_Amount' not in df.columns:
#                 session['error'] = "Error: CSV must contain a 'Sales' column."
#                 return redirect(url_for('home'))

#             if df['Sales_Amount'].isnull().any():
#                 session['error'] = "Error: 'Sales' column contains missing values."
#                 return redirect(url_for('home'))

#             if len(df) < 10:
#                 session['error'] = "Error: At least 10 rows of data required."
#                 return redirect(url_for('home'))

#             steps = int(request.form.get('steps', 5))
#             forecast = model.get_forecast(steps=steps)
#             forecast_values = forecast.predicted_mean.tolist()

#             def calculate_commission(sale):
#                 if sale <= 10000:
#                     return round(sale * 0.05, 2)
#                 elif sale <= 50000:
#                     return round(sale * 0.10, 2)
#                 else:
#                     return round(sale * 0.15, 2)

#             commissions = [calculate_commission(s) for s in forecast_values]
#             session['results'] = list(zip(forecast_values, commissions))

#         except Exception as e:
#             session['error'] = f"Prediction error: {str(e)}"

#         return redirect(url_for('home'))

#     session['error'] = 'Unexpected error.'
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime
import pandas as pd
import os
import joblib
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# model = joblib.load(r"D:\Time series Analysis\model\final_sarima_model.pkl")
model = joblib.load(os.path.join("model", "final_sarima_model.pkl"))

# store temporary file name globally
latest_file = {"filename": None, "results": None, "error": None}

@app.route('/', methods=['GET'])
def home():
    results = latest_file["results"]
    error = latest_file["error"]
    download_file = latest_file["filename"]

    # Clear results after displaying once
    latest_file["results"] = None
    latest_file["error"] = None
    latest_file["filename"] = None

    return render_template('index.html', results=results, error=error, download_file=download_file, year=datetime.now().year)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        latest_file["error"] = 'No file part in request.'
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        latest_file["error"] = 'No selected file.'
        return redirect(url_for('home'))

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)

            if 'Sales_Amount' not in df.columns:
                latest_file["error"] = "Error: CSV must contain a 'Sales_Amount' column."
                return redirect(url_for('home'))

            if df['Sales_Amount'].isnull().any():
                latest_file["error"] = "Error: 'Sales_Amount' column contains missing values."
                return redirect(url_for('home'))

            if len(df) < 10:
                latest_file["error"] = "Error: At least 10 rows of data required."
                return redirect(url_for('home'))

            steps = int(request.form.get('steps', 5))
            forecast = model.get_forecast(steps=steps)
            forecast_values = forecast.predicted_mean.tolist()

            def calculate_commission(sale):
                if sale <= 10000:
                    return round(sale * 0.05, 2)
                elif sale <= 50000:
                    return round(sale * 0.10, 2)
                else:
                    return round(sale * 0.15, 2)

            commissions = [calculate_commission(s) for s in forecast_values]
            results = list(zip(forecast_values, commissions))

            output_df = pd.DataFrame(results, columns=["Forecasted_Sale", "Commission"])
            unique_id = uuid.uuid4().hex[:8]
            filename = f"forecast_{unique_id}.csv"
            download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            output_df.to_csv(download_path, index=False)

            # Store for one-time use on GET
            latest_file["results"] = results
            latest_file["filename"] = filename

        except Exception as e:
            latest_file["error"] = f"Prediction error: {str(e)}"

    return redirect(url_for('home'))

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


