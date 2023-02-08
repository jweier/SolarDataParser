import json
import requests
import re
import boto3
from day import Day

auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5ZdVZJWTJTN3gxVHRYM01KMC1QMDJad3pXQSJ9.eyJpc3MiOiJodHRwczovL2F1dGgudGVzbGEuY29tL29hdXRoMi92MyIsImF1ZCI6WyJodHRwczovL293bmVyLWFwaS50ZXNsYW1vdG9ycy5jb20vIiwiaHR0cHM6Ly9hdXRoLnRlc2xhLmNvbS9vYXV0aDIvdjMvdXNlcmluZm8iXSwiYXpwIjoib3duZXJhcGkiLCJzdWIiOiJmOTQ4ZWExMi02MDE4LTRiMzgtOTdlYi00NTZkNjBhNTY5NjMiLCJzY3AiOlsib3BlbmlkIiwiZW1haWwiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl0sImV4cCI6MTY3NTkxNDI3MywiaWF0IjoxNjc1ODg1NDczLCJhdXRoX3RpbWUiOjE2NzU4ODU0Njl9.ryH43MvTW_vhRrjU4m5o66T93la-EPJa_NAOoOw7F8BahdsrOEKRKJeOpjYIlf8npTsj9l_oAuk3lfwHnaBqmo-IttIvXvpXN4Thsh5qyIQKc9biC_AbfSedix7GnBCJlaQtkcT7Zzq5x0sIssrSTZMbU1DGQE6tLlNfIjmqPIGlAApPJ8259aqyyyZImlVUAv8vxaFL-imLm1UEn-Orm5To_KskacAeAETPWICZwgPTwPG08HQKo-5f48IL8E_V_IdI3un3e3ZS7eLFu75y33Py3eXE0INM0xLWlTK0-4j2HwShwkq2JUFyM3Hbi19zo_EGV3cMWn0uZOxIQU4vBw"

def lambda_handler(event, context):
        
    tesla_url = 'https://owner-api.teslamotors.com/api/1/energy_sites/2252180269197839/calendar_history?start_date=2023-02-07T00%3A00%3A00-05%3A00&end_date=2023-02-07T23%3A59%3A59-05%3A00&period=day&time_zone=America/New_York&kind=energy'
    tesla_headers = {
        'Authorization': 'Bearer ' + auth_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }


    tesla_response = requests.get(tesla_url, headers=tesla_headers)

    data = tesla_response.json()
    
    date = data['response']['time_series'][0]['timestamp']
    date_formatted = re.findall("^\d{4}[-]\d{2}[-]\d{2}", date)[0]
    solar_energy_exported = data['response']['time_series'][0]['solar_energy_exported']
    grid_energy_imported = data['response']['time_series'][0]['grid_energy_imported']
    grid_energy_exported_from_solar = data['response']['time_series'][0]['grid_energy_exported_from_solar']
    consumer_energy_imported_from_grid = data['response']['time_series'][0]['consumer_energy_imported_from_grid']
    consumer_energy_imported_from_solar = data['response']['time_series'][0]['consumer_energy_imported_from_solar']


    day = Day()
    day.create_day(date_formatted, solar_energy_exported, grid_energy_imported, grid_energy_exported_from_solar, consumer_energy_imported_from_grid, consumer_energy_imported_from_solar)

    print(day.consumer_energy_imported_from_grid)

    # print(date)
    # print(date_formatted)
    # print(solar_energy_exported)
    # print(grid_energy_imported)
    # print(grid_energy_exported_from_solar)
    # print(consumer_energy_imported_from_grid)
    # print(consumer_energy_imported_from_solar)

    # #Download the existing data file
    # data_url = "http://jayweier.com/assets/data.js"

    # data_response = requests.get(data_url)

    # js_parser = JS_Parser(data_response.text)



    #Upload the data file to S3
    # resource = boto3.resource('s3')
    # my_bucket.upload_file("data.js", "assets/data1.js")

lambda_handler("Any", "Any")

#Jay was here!
