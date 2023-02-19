import requests
import json
from datetime import datetime
import calendar
import boto3
from botocore.exceptions import ClientError

#Put your refresh token in here if running locally and can safely put the refresh token in the code
#Refresh token can be obtain by following the steps on https://tesla-info.com/tesla-token.php
refresh_token = ""

s3 = boto3.resource('s3')

#Delete this function if running locally and refresh_token is defined at the top
def get_refresh_token_from_secrets_manager():

    secret_name = "SolarDataParser/refresh_token"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secrets = json.loads(get_secret_value_response['SecretString'])

    return secrets['refresh_token']

def get_new_token(deployment_type):
    
    if (deployment_type == "s3"):
        refresh_token = get_refresh_token_from_secrets_manager()

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

#By default, call the Tesla API to get the current months data
def call_tesla_api(current_year = datetime.now().year, month_in_two_digits = '{:%m}'.format(datetime.today()), code_base="", deployment_type=""
):

    #Get the last day of a month
    res = calendar.monthrange(current_year, int(month_in_two_digits))
    last_day_of_month = str(res[1])

    new_access_token = get_new_token(deployment_type)
    tesla_headers = {
        'Authorization': 'Bearer ' + new_access_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    data_key_name = f'assets/rawjsondata/{current_year}-{month_in_two_digits}.json'
    tesla_url = f'https://owner-api.teslamotors.com/api/1/energy_sites/2252180269197839/calendar_history?period=month&kind=energy&time_zone=America/New_York&start_date={current_year}-{month_in_two_digits}-01T00%3A00%3A00-05%3A00&end_date={current_year}-{month_in_two_digits}-{last_day_of_month}T23%3A59%3A59-05%3A00'
    tesla_response = requests.get(tesla_url, headers=tesla_headers)
    data = tesla_response.json()

    #Write the JSON file to either local storage or S3 storage, depending on deployment type
    if(deployment_type == "local"):
        with open(f'{code_base}\\{data_key_name}', 'w') as file:
            file.write(json.dumps(data))
    elif (deployment_type == "s3"):
        month_object = s3.Object(
        bucket_name=code_base, 
        key=data_key_name
        )
        month_object.put(Body=json.dumps(data))


def seed_data(json_data_folder):
    starting_month = int(input("Please enter the number of the month you first got solar: "))
    starting_year = int(input("Please enter the year you first got solar as 4 digits: "))
    current_year = datetime.now().year
    current_month = datetime.now().month
        
