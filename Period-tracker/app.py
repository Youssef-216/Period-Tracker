

# from flask import Flask, render_template, request, redirect
# import pandas as pd
# from datetime import datetime

# app = Flask(__name__)
# file_path = 'PeriodTracker_db.csv'  # Ensure this path is correct

# def calculate_cycle_phase(lmp, avg_cycle_length, variability, period_duration):
#     today = datetime.today().date()
#     lmp_date = lmp.date() if isinstance(lmp, pd.Timestamp) else lmp  # Ensure lmp is a date
#     cycle_day = (today - lmp_date).days % avg_cycle_length

#     if cycle_day <= period_duration:
#         return 'Menstrual Phase'
#     elif (avg_cycle_length // 2) - variability <= cycle_day <= (avg_cycle_length // 2) + variability:
#         return 'Ovulation Phase'
#     elif cycle_day > (avg_cycle_length // 2) + variability:
#         return 'Luteal Phase'
#     else:
#         return 'Follicular Phase'

# def days_until_next_period(lmp, avg_cycle_length):
#     today = datetime.today().date()
#     lmp_date = lmp.date() if isinstance(lmp, pd.Timestamp) else lmp  # Ensure lmp is a date
#     next_period = lmp_date + pd.DateOffset(days=avg_cycle_length)
#     next_period_date = next_period.date()  # Convert to date
#     days_remaining = (next_period_date - today).days
#     while days_remaining < 0:
#         days_remaining += avg_cycle_length

#     return days_remaining

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/update', methods=['POST'])
# def update():
#     try:
#         print(f"Reading CSV file from: {file_path}")
#         df = pd.read_csv(file_path)
#         df['LMP (YYYY-MM-DD)'] = pd.to_datetime(df['LMP (YYYY-MM-DD)'])
#         for index, row in df.iterrows():
#             lmp = row['LMP (YYYY-MM-DD)']
#             lmp_date = lmp.date() if isinstance(lmp, pd.Timestamp) else lmp  # Ensure lmp is a date
#             df.at[index, 'Current Phase'] = calculate_cycle_phase(lmp_date, row['Average Cycle Length'], row['Cycle Length Variability'], row['Average Period Duration'])
#             df.at[index, 'Next period (in days)'] = days_until_next_period(lmp_date, row['Average Cycle Length'])
#         df.to_csv(file_path, index=False)
#         return render_template('index.html', data=df.to_html())
#     except Exception as e:
#         return str(e)

# @app.route('/add', methods=['POST'])
# def add():
#     try:
#         df = pd.read_csv(file_path)
#         name = request.form['name']
#         lmp_input = request.form['lmp']
#         avg_cycle_length = int(request.form['avg_cycle_length'])
#         variability = int(request.form['variability'])
#         period_duration = int(request.form['period_duration'])

#         lmp = datetime.strptime(lmp_input, '%Y-%m-%d').date()
#         cycle_phase = calculate_cycle_phase(lmp, avg_cycle_length, variability, period_duration)
#         next_period_days = days_until_next_period(lmp, avg_cycle_length)

#         new_data = {
#             'Client ID': df['Client ID'].max() + 1 if not df['Client ID'].isnull().all() else 1,
#             'Name': name,
#             'LMP (YYYY-MM-DD)': lmp.strftime('%Y-%m-%d'),
#             'Average Cycle Length': avg_cycle_length,
#             'Cycle Length Variability': variability,
#             'Average Period Duration': period_duration,
#             'Current Phase': cycle_phase,
#             'Next period (in days)': next_period_days
#         }

#         df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
#         df.to_csv(file_path, index=False)
#         return render_template('index.html', data=df.to_html())
#     except Exception as e:
#         return str(e)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime

app = Flask(__name__)
file_path = 'PeriodTracker_db.csv'  # Ensure this path is correct

def calculate_cycle_phase(lmp, avg_cycle_length, variability, period_duration):
    today = datetime.today().date()
    lmp_date = lmp.date() if isinstance(lmp, pd.Timestamp) else lmp  # Ensure lmp is a date
    cycle_day = (today - lmp_date).days % avg_cycle_length

    if cycle_day <= period_duration:
        return 'Menstrual Phase'
    elif (avg_cycle_length // 2) - variability <= cycle_day <= (avg_cycle_length // 2) + variability:
        return 'Ovulation Phase'
    elif cycle_day > (avg_cycle_length // 2) + variability:
        return 'Luteal Phase'
    else:
        return 'Follicular Phase'

def days_until_next_period(lmp, avg_cycle_length):
    today = datetime.today().date()
    lmp_date = lmp.date() if isinstance(lmp, pd.Timestamp) else lmp  # Ensure lmp is a date
    next_period = lmp_date + pd.DateOffset(days=avg_cycle_length)
    next_period_date = next_period.date()  # Convert to date
    days_remaining = (next_period_date - today).days
    while days_remaining < 0:
        days_remaining += avg_cycle_length

    return int(days_remaining)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    try:
        print(f"Reading CSV file from: {file_path}")
        df = pd.read_csv(file_path)
        df['LMP (YYYY-MM-DD)'] = pd.to_datetime(df['LMP (YYYY-MM-DD)'])
        for index, row in df.iterrows():
            lmp = row['LMP (YYYY-MM-DD)']
            lmp_date = lmp.date() if isinstance(lmp, pd.Timestamp) else lmp  # Ensure lmp is a date
            df.at[index, 'Current Phase'] = calculate_cycle_phase(lmp_date, row['Average Cycle Length'], row['Cycle Length Variability'], row['Average Period Duration'])
            df.at[index, 'Next period (in days)'] = days_until_next_period(lmp_date, row['Average Cycle Length'])
        df.to_csv(file_path, index=False)
        return render_template('index.html', data=df.to_html(classes="table table-striped"))
    except Exception as e:
        return str(e)

@app.route('/add', methods=['POST'])
def add():
    try:
        df = pd.read_csv(file_path)
        name = request.form['name']
        lmp_input = request.form['lmp']
        avg_cycle_length = int(request.form['avg_cycle_length'])
        variability = int(request.form['variability'])
        period_duration = int(request.form['period_duration'])

        lmp = datetime.strptime(lmp_input, '%Y-%m-%d').date()
        cycle_phase = calculate_cycle_phase(lmp, avg_cycle_length, variability, period_duration)
        next_period_days = days_until_next_period(lmp, avg_cycle_length)

        new_data = {
            'Client ID': df['Client ID'].max() + 1 if not df['Client ID'].isnull().all() else 1,
            'Name': name,
            'LMP (YYYY-MM-DD)': lmp.strftime('%Y-%m-%d'),
            'Average Cycle Length': avg_cycle_length,
            'Cycle Length Variability': variability,
            'Average Period Duration': period_duration,
            'Current Phase': cycle_phase,
            'Next period (in days)': next_period_days
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(file_path, index=False)
        return render_template('index.html', data=df.to_html(classes="table table-striped"))
    except Exception as e:
        return str(e)

@app.route('/delete', methods=['POST'])
def delete():
    try:
        df = pd.read_csv(file_path)
        client_id = int(request.form['client_id'])
        df = df[df['Client ID'] != client_id]
        df.to_csv(file_path, index=False)
        return render_template('index.html', data=df.to_html(classes="table table-striped"))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
