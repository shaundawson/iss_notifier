from config import password, my_email
from http.client import responses
import requests
from datetime import datetime as dt
import smtplib
import time

MY_LAT = 30.332184
MY_LNG = -81.655647

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # Your position is within +5 or -5 degrees of the ISS position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True
   
def is_night():        
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json",params=parameters )
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    
    time_now = dt.now().hour
    
    if time_now >= sunset or time_now <= sunrise:
        return True
        
while True: 
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.ehlo()
            connection.login(user=my_email, password=password)
            connection.sendmail(
            from_addr=my_email, 
            to_addrs="iamsdawson@gmail.com", 
            msg=f"Look up👆🏾\n\nThe ISS is above you in the sky"
        )
    



