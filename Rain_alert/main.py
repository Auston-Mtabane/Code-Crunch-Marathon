import os 
from dotenv import load_dotenv
import requests ,json
from twilio.rest import Client

def get_data(location): #location is a list of size two, containin lattitude and longitude coordinates
    
    load_dotenv()
    API_key = os.getenv('key')
    lat = location[0]
    lon = location[1]
    api_url =f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}' 
    response = requests.get(url=api_url)
    data = json.loads(response.text)

    return data

def sms(content,to_number):# sends an sms to the to_number
    load_dotenv()
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    messaging_service_sid=os.getenv('messaging_service_sid'),
    body=content,
    to= to_number,
    )
    return message
def main():
    rain_emoji = '🌧️'
    location = [-33.921579293740706, 18.419719274639686] #lat,lon
    data = get_data(location)

    weather = None

    if data and 'weather' in data:
        weather = data['weather'] #getting weather condition from json dictionarysky

    if weather:
        sky = weather[0]['main']
        print(f"The weather right now is: {sky}", '+27658544670')
            
        if sky.lower == 'rain':
            message = sms('ITS RAINING TODAY! make sure to find shelyer and stay safe!')
            print(f'{message.body}')
        else:
            print('no rain today')
    else:
        print('failed to retrieve weather information')
#sms("weather","+27696608792")

if __name__ == '__main__':
    main()