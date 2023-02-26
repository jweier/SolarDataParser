import requests
import json
from datetime import datetime, date
from dateutil import rrule
import calendar
import aws_actions

def get_new_token(deployment_type):
    
    if (deployment_type == "s3"):
        refresh_token = aws_actions.get_refresh_token_from_secrets_manager()
    else:
        #Put your refresh token in here if running locally and can safely put the refresh token in the code
        #Refresh token can be obtain by following the steps on https://tesla-info.com/tesla-token.php
        refresh_token = ""

    tesla_auth_url = "https://auth.tesla.com/oauth2/v3/token"
    tesla_auth_response = requests.post(tesla_auth_url, json={
        "grant_type": "refresh_token",
	    "client_id": "ownerapi",
        "refresh_token": refresh_token,
	    "scope": "openid email offline_access"
    })

    tesla_auth_response = tesla_auth_response.json()
    new_access_token = tesla_auth_response["access_token"]

    return(new_access_token)

def get_energy_site_id(access_token):
    tesla_energy_site_id_url = "https://owner-api.teslamotors.com/api/1/products"

    tesla_headers = {
        'Authorization': 'Bearer ' + access_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    tesla_energy_site_id_response = requests.get(tesla_energy_site_id_url, headers=tesla_headers)
    energy_site_id_data = tesla_energy_site_id_response.json()

    for site_id in energy_site_id_data["response"]:
        if site_id["energy_site_id"] is not None:
            energy_site_id = site_id["energy_site_id"]
            print(energy_site_id)

    return energy_site_id

#By default, call the Tesla API to get the current months data
def call_tesla_api(current_year = datetime.now().year, month_in_two_digits = '{:%m}'.format(datetime.today()), code_base="", deployment_type=""):

    #Get the last day of a month
    res = calendar.monthrange(current_year, int(month_in_two_digits))
    last_day_of_month = str(res[1])

    new_access_token = get_new_token(deployment_type)
    energy_site_id = get_energy_site_id(new_access_token)
    
    tesla_headers = {
        'Authorization': 'Bearer ' + new_access_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    data_key_name = f'assets/rawjsondata/{current_year}-{month_in_two_digits}.json'
    tesla_url = f'https://owner-api.teslamotors.com/api/1/energy_sites/{energy_site_id}/calendar_history?period=month&kind=energy&time_zone=America/New_York&start_date={current_year}-{month_in_two_digits}-01T00%3A00%3A00-05%3A00&end_date={current_year}-{month_in_two_digits}-{last_day_of_month}T23%3A59%3A59-05%3A00'
    tesla_response = requests.get(tesla_url, headers=tesla_headers)
    data = tesla_response.json()

    #Write the JSON file to either local storage or S3 storage, depending on deployment type
    if(deployment_type == "local"):
        with open(f'{code_base}/{data_key_name}', 'w') as file:
            file.write(json.dumps(data))
    elif (deployment_type == "s3"):
        import boto3
        s3 = boto3.resource('s3')
        month_object = s3.Object(
        bucket_name=code_base, 
        key=data_key_name
        )
        month_object.put(Body=json.dumps(data))


def seed_data(code_base = "", deployment_type=""):
    year = int(input('Please enter the number of the year (YYYY) you first got solar: '))
    month = int(input('Please enter the number of the month you first got solar: '))
    day = 1
    start_date = date(year, month, day)
    end_date = date(datetime.now().year, datetime.now().month, datetime.now().day)

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        month_in_two_digits = '{:02d}'.format(dt.month)
        call_tesla_api(current_year = dt.year, month_in_two_digits = month_in_two_digits, code_base = code_base, deployment_type=deployment_type)
        print(f"Downloaded data for {month_in_two_digits}-{dt.year}")

        
