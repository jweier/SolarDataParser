import requests
import json
from datetime import datetime
import calendar
import boto3
from botocore.exceptions import ClientError


s3 = boto3.resource('s3')

currentYear = datetime.now().year
input_dt = datetime.today()

#Get the month in two digits
month_in_two_digits = '{:%m}'.format(input_dt)

#Get the last day of a month
res = calendar.monthrange(input_dt.year, input_dt.month)
last_day_of_month = str(res[1])

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
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secrets = json.loads(get_secret_value_response['SecretString'])

    return secrets['refresh_token']

def get_new_token():
    
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

def call_tesla_api(duration, new_access_token):
    tesla_headers = {
        'Authorization': 'Bearer ' + new_access_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}
    if duration == "monthly":
        data_key_name = f'assets/rawjsondata/{currentYear}-{month_in_two_digits}.json'
        tesla_url = f'https://owner-api.teslamotors.com/api/1/energy_sites/2252180269197839/calendar_history?period=month&kind=energy&time_zone=America/New_York&start_date=2023-{month_in_two_digits}-01T00%3A00%3A00-05%3A00&end_date=2023-{month_in_two_digits}-{last_day_of_month}T23%3A59%3A59-05%3A00'

    elif duration == "lifetime":
        data_key_name = f'assets/rawjsondata/lifetime.json'
        tesla_url = 'https://owner-api.teslamotors.com/api/1/energy_sites/2252180269197839/calendar_history?end_date=2023-12-31T23%3A59%3A59-05%3A00&start_date=2023-01-01T00%3A00%3A00-05%3A00&period=lifetime&time_zone=America/New_York&kind=energy'

    tesla_response = requests.get(tesla_url, headers=tesla_headers)
    data = tesla_response.json()

    month_object = s3.Object(
        bucket_name='jayweier.com', 
        key=data_key_name
    )

    month_object.put(Body=json.dumps(data))

    return data
        