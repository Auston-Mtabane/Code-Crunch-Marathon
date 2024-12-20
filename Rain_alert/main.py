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

def sms():# sends an sms to the to_number
    load_dotenv()
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    phone_number = os.getenv('phone_number')
    twilio_number = os.getenv('twilio_number')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    messaging_service_sid=os.getenv('messaging_service_sid'),
        body='Looks like its a clear sky today',
        from_ = twilio_number,
        to= phone_number ,
    )

    return message.sid
def main():
    location = [-29.846188212189613, 31.002883656151514] #lat,lon
    data = get_data(location)

    weather = None

    if data and 'weather' in data:
        weather = data['weather'] #getting weather condition from json dictionarysky

    if weather:
        sky = weather[0]['main']
        print(f"The weather right now is: {sky}")
        
        if sky.lower() == 'rain':
            message = sms('ITS RAINING TODAY 🌧️! make sure to find shelyer and stay safe!',os.getenv('phone_number'))
            print(f'{message.body}')
            
        elif sky.lower != 'rain':
            message = sms('Looks like its a clear sky today')
            print('no rain today')
    # else:
    #     print('failed to retrieve weather information')

sms()
if __name__ == '__main__':
    main()

