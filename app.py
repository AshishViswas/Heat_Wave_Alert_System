from flask import Flask, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from data import Heat_Wave_Update
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from flaskext.mysql import MySQL
import urllib.parse

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'db_password' # replace with actual password
app.config['MYSQL_DATABASE_DB'] = 'heat_wave_alert_system'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Replace with your 2Factor API key provided in your account's API key section after u signup
API_KEY = '2FACTOR_api_key' 

# Define a global variable to store the return value
job_return_value = None

def send_sms(job_return_value):
  if job_return_value == True:  # only when prediction is True, Heat Wave Alert is sent
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("Select phone_number from signup")

    # Fetch all results
    phone_numbers = [str(result[0]) for result in cursor.fetchall()]
    
    # 2Factor API endpoint for sending SMS
    SMS_TEXT = 'Heat Wave Alerts! Stay indoors and avoid going out. keep yourself Hydrated!'
    encoded_SMS_TEXT = urllib.parse.quote_plus(SMS_TEXT)
    print(encoded_SMS_TEXT)
    
    for i in phone_numbers:
     url = 'https://2factor.in/API/R1/?module=PROMO_SMS&apikey={}&to={}&from=ACFJOU&msg={}'.format(API_KEY,i,encoded_SMS_TEXT) 
     
     # Make the API request to 2Factor
     response = requests.post(url)
      
      # Check if the request was successful
     if response.status_code == 200:
        # Parse the response to JSON
        response_data = response.json()
        print(response_data)
     else:
        print('Failed to send SMS')   
  else:
        print('No heat wave')

def my_listener(event):
    global job_return_value
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')
        print('Return value:', event.retval)
        if event.retval is not None:
            job_return_value = event.retval[0]
            scheduler.add_job(send_sms, args=(job_return_value,))
        else:
            print('No return value from job')
        

scheduler = BackgroundScheduler()
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

# Schdeuling a cron job to be run every morning at 10:00 AM which runs code for heat wave predictions and alerts subscribers if prediction outcome is True
scheduler.add_job(Heat_Wave_Update,'cron', hour = 10,minute = 0)

# Start the scheduler
scheduler.start()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Register')
def signup():
    return render_template('index.html')

@app.route('/home')
def heat():
    return render_template('home.html')

@app.route('/Register', methods=['POST'])
def Register():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        print(phone_number)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO signup (phone_number) VALUES (% s)", (phone_number,))
        conn.commit()
        msg='You have successfully registered'
        return render_template('home.html',msg=msg)
    else:
        msg='Registration not successful. Please Try Again'
        return render_template('index.html',msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
