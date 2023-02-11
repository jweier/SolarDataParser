import requests
import json
from datetime import datetime
import calendar
import boto3

s3 = boto3.resource('s3')

auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5ZdVZJWTJTN3gxVHRYM01KMC1QMDJad3pXQSJ9.eyJpc3MiOiJodHRwczovL2F1dGgudGVzbGEuY29tL29hdXRoMi92MyIsImF1ZCI6WyJodHRwczovL293bmVyLWFwaS50ZXNsYW1vdG9ycy5jb20vIiwiaHR0cHM6Ly9hdXRoLnRlc2xhLmNvbS9vYXV0aDIvdjMvdXNlcmluZm8iXSwiYXpwIjoib3duZXJhcGkiLCJzdWIiOiJmOTQ4ZWExMi02MDE4LTRiMzgtOTdlYi00NTZkNjBhNTY5NjMiLCJzY3AiOlsib3BlbmlkIiwiZW1haWwiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl0sImV4cCI6MTY3NjA4MzU1OSwiaWF0IjoxNjc2MDU0NzU5LCJhdXRoX3RpbWUiOjE2NzYwNTQ3NTN9.rD2NHmXlbbthmhr4TmPPugCwnhhdGzKyUDLGYxEXAygTBnzFBkb1Gw0JxONOJqVSDRgVvu3jg56mH94a7pnBwv8ppY6hwtl02KKyXtsAtXPk4SyurQcvtwALdqtwJ9EQxBpzlrSIZ6p99TbyeocQpQSBZoNoHxWvvl8KmAbeds6sntsOJFmztWEtYJ9OFAP4VKCR5PVntMsjHEefANHexN7R4t96TDEEK59Iyz2cahrlwlOjqv43xzDpJcDBLpTcxBPugrJl31rg598lPlK1DvMUYHEIFJCwnhYpvaB-492BsV233UJzGjZhnqGsyH2McTwD0AnguONgD5cEqHZitg"
tesla_headers = {
        'Authorization': 'Bearer ' + auth_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

currentYear = datetime.now().year
input_dt = datetime.today()

#Get the month in two digits
month_in_two_digits = '{:%m}'.format(input_dt)

#Get the last day of a month
res = calendar.monthrange(input_dt.year, input_dt.month)
last_day_of_month = str(res[1])

def call_tesla_api(duration):
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
        