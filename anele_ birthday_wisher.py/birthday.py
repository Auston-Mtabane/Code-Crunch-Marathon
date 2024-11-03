import os
import smtplib
from email.mime.text import MIMEText
import datetime
import requests,json
from dotenv import load_dotenv


load_dotenv()


def fetch_data():
    
    ENDPOINT = os.getenv('ENDPOINT')
    response = requests.get(url=ENDPOINT)
    dictionary_in_text =response.text
    data = json.loads(dictionary_in_text)
    return data

def send_email(name, email):
    subject = f'Happy birthday {name}'
    body = f'Dear {name},\n we are wishing you a wonderful birthday \n filled with love , joy and many memories. \n Enjoy your day to the fullest!'
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = os.getenv('email_user')
    message['To'] = email

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            server.sendmail(os.getenv('EMAIL_USER'), email, message.as_string())
            print(f"Email sent to {name} at {email}")
    except Exception as e:
        print(f"Failed to send email to {name}: {e}")
        
def check_birthdays(data):
    """Check for upcoming birthdays within the next 7 days."""
    today = datetime.date.today()
    upcoming_birthdays = []

    for entry in data:
        birthday = entry['Birthday']
        if birthday and birthday.startswith(str(today.year)):  # Simplified check for this year's birthdays
            upcoming_birthdays.append((entry['Name'], entry['Email']))

    return upcoming_birthdays

def job():
    """Fetch data and send birthday emails."""
    data = fetch_data()
    birthdays = check_birthdays(data)
    for name, email in birthdays:
        send_email(name, email)

if __name__ == "__main__":
    print("Birthday Wisher is running...")
    job()


















