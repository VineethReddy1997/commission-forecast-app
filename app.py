from flask import Flask, render_template, request, send_file, redirect, url_for, session
from datetime import datetime
import pandas as pd
import os
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', results=None, error=None, download_file=None, year=datetime.now().year)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    steps = request.form.get('steps', '12')
    
    if not file or file.filename == '':
        session['error'] = "No file selected."
        return redirect(url_for('results'))

    try:
        forecast_steps = int(steps)
        if forecast_steps < 1 or forecast_steps > 36:
            session['error'] = "Forecast steps must be between 1 and 36."
            return redirect(url_for('results'))
    except ValueError:
        session['error'] = "Invalid number for forecast steps."
        return redirect(url_for('results'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = pd.read_csv(filepath)
        if 'Date' not in df.columns or 'Sales_Amount' not in df.columns:
            session['error'] = "CSV must contain 'Date' and 'Sales_Amount' columns."
            return redirect(url_for('results'))

        # df['Date'] = pd.to_datetime(df['Date'], dayfirst=False)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

        df.set_index('Date', inplace=True)
        df = df.sort_index()
        monthly = df['Sales_Amount'].resample("MS").sum()

        if len(monthly) < 24:
            session['error'] = "At least 24 months of data is required."
            return redirect(url_for('results'))

        model = SARIMAX(monthly, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)

        forecast = model_fit.forecast(steps=forecast_steps)
        forecast.index = pd.date_range(start=monthly.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq='MS')

        def calculate_commission(s):
            if s <= 10000:
                return round(s * 0.05, 2)
            elif s <= 50000:
                return round(s * 0.10, 2)
            else:
                return round(s * 0.15, 2)

        commissions = [calculate_commission(s) for s in forecast]
        result_df = pd.DataFrame({
            'Forecast Month': forecast.index.strftime('%Y-%m-%d'),
            'Forecasted Sale': forecast.round(2),
            'Commission': commissions
        })

        filename = f"forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        result_df.to_csv(output_path, index=False)

        session['results'] = result_df.values.tolist()
        session['download_file'] = filename
        return redirect(url_for('results'))

    except Exception as e:
        session['error'] = f"Error processing file: {str(e)}"
        return redirect(url_for('results'))

@app.route('/results')
def results():
    results = session.pop('results', None)
    error = session.pop('error', None)
    download_file = session.pop('download_file', None)
    return render_template('index.html', results=results, error=error, download_file=download_file, year=datetime.now().year)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
