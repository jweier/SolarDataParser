import json
import requests
import re
import boto3

auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5ZdVZJWTJTN3gxVHRYM01KMC1QMDJad3pXQSJ9.eyJpc3MiOiJodHRwczovL2F1dGgudGVzbGEuY29tL29hdXRoMi92MyIsImF1ZCI6WyJodHRwczovL293bmVyLWFwaS50ZXNsYW1vdG9ycy5jb20vIiwiaHR0cHM6Ly9hdXRoLnRlc2xhLmNvbS9vYXV0aDIvdjMvdXNlcmluZm8iXSwiYXpwIjoib3duZXJhcGkiLCJzdWIiOiJmOTQ4ZWExMi02MDE4LTRiMzgtOTdlYi00NTZkNjBhNTY5NjMiLCJzY3AiOlsib3BlbmlkIiwiZW1haWwiLCJvZmZsaW5lX2FjY2VzcyIsInBob25lIl0sImFtciI6WyJwd2QiXSwiZXhwIjoxNjc1ODgzNzI3LCJpYXQiOjE2NzU4NTQ5MjcsImF1dGhfdGltZSI6MTY3NTM0NzY0NX0.ui-ao5A3pinn05wuKkdIITXlwTVrX2pcUB8WIZZJF0DRXfHgwUmRCLo1rKEOkzdyPuPbjG6Otliv4bCoLBzl6aWvBXgXvwgQApc43deupIbgXy2nTw1UQ4JndoS8eG4A4VTyxfN31hhnFUYHOsRAvlBsOpLzRlMxAv1NVdohtMqn71qq6MwS6xotdSiESOWMmVjksQdWcHJhUdJST_He5AXUmo5nsseV35h_r7QxwIC5Jw5hz2kbt5KNxdJg2-TZB0keHcSA6K7AIutnSDSx-MTP4hISAL9PmmJVkGUEPQ1NqVvUTyapodiizUb4W0tUFzfcWT9EazfgSjyPuKaEOQ"

def lambda_handler(event, context):
        
    # url = 'https://owner-api.teslamotors.com/api/1/energy_sites/2252180269197839/calendar_history?start_date=2023-02-07T00%3A00%3A00-05%3A00&end_date=2023-02-07T23%3A59%3A59-05%3A00&period=day&time_zone=America/New_York&kind=energy'
    # headers = {
    #     'Authorization': 'Bearer ' + auth_token,
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    # }


    # response = requests.get(url, headers=headers)

    # data = response.json()
    
    # date = data['response']['time_series'][0]['timestamp']
    # date_formatted = re.findall("^\d{4}[-]\d{2}[-]\d{2}", date)[0]
    # solar_energy_exported = data['response']['time_series'][0]['solar_energy_exported']
    # grid_energy_imported = data['response']['time_series'][0]['grid_energy_imported']
    # grid_energy_exported_from_solar = data['response']['time_series'][0]['grid_energy_exported_from_solar']
    # consumer_energy_imported_from_grid = data['response']['time_series'][0]['consumer_energy_imported_from_grid']
    # consumer_energy_imported_from_solar = data['response']['time_series'][0]['consumer_energy_imported_from_solar']

    # print(date)
    # print(date_formatted)
    # print(solar_energy_exported)
    # print(grid_energy_imported)
    # print(grid_energy_exported_from_solar)
    # print(consumer_energy_imported_from_grid)
    # print(consumer_energy_imported_from_solar)

    #Download the data file from S3
    resource = boto3.resource('s3')
    my_bucket = resource.Bucket('jayweier.com')
    my_bucket.download_file("assets/data.js", "data.js")

    #Upload the data file to S3
    my_bucket.upload_file("data.js", "assets/data1.js")

lambda_handler("Any", "Any")

#Jay was here!
