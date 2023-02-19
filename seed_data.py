import tesla
import json
import requests
from datetime import datetime



def call_tesla_api():
    new_access_token = tesla.get_new_token()
    tesla_headers = {
        'Authorization': 'Bearer ' + new_access_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    data_key_name = f'{current_year}-{month_in_two_digits}.json'
    tesla_url = f'https://owner-api.teslamotors.com/api/1/energy_sites/2252180269197839/calendar_history?period=month&kind=energy&time_zone=America/New_York&start_date={current_year}-{month_in_two_digits}-01T00%3A00%3A00-05%3A00&end_date={current_year}-{month_in_two_digits}-{last_day_of_month}T23%3A59%3A59-05%3A00'
    tesla_response = requests.get(tesla_url, headers=tesla_headers)
    data = tesla_response.json()

    with open(f'{json_data_folder}\{data_key_name}', 'w') as file:
        file.write(json.dumps(data))

month = starting_month
year = starting_year

print(current_year)

while year <= current_year:
        if month < 12:
            print(f'{month} {year}')
            month +=1
        elif month == 12:
            print(f'{month} {year}')
            month = 1
            year += 1