import requests
import os
from twilio.rest import Client

KEY = os.environ.get("OWM_API_KEY")
LAT = "51.5109947"
LONG = "-0.0749509"
EXC = "current,minutely,daily"

account_sid = os.environ.get("ACCT_SID")
auth_token = os.environ.get("AUTH_TOKEN")


def check_for_rain(data):
    """Checks for rain codes in the data. ID codes below 700 are for rain."""
    for x in range(len(data)):
        if data[x]['weather'][0]['id'] < 700:
            return True
    return False


response = requests.get(
    f"https://api.openweathermap.org/data/2.8/onecall?lat={LAT}&lon={LONG}&exclude={EXC}&appid={KEY}"
)

response.raise_for_status()
weather_data = response.json()['hourly'][:12]
is_rain = check_for_rain(weather_data)
if is_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                         body="It's going to 🌧️ today. Bring an umbrella.",
                         from_='***Your Twilio Number***',
                         to='***Number to receive text from Twilio number***'
                    )