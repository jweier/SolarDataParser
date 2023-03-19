import boto3
import tesla
import requests
import pandas
import os
s3 = boto3.resource('s3')
conn = boto3.client('s3')

deployment_type = 's3'
code_base = os.getenv('BUCKET_NAME')
print(code_base)

def lambda_handler(event, context):

    #Call to Tesla to get the latest copy of the monthly data and store in S3
    tesla.call_tesla_api(deployment_type = deployment_type, code_base=code_base)

    all_variables = ""

    previous_months_json_files_list = []
    time_series = pandas.DataFrame()

    #Parse through the S3 bucket and find JSON files for previous months data
    for key in conn.list_objects(Bucket=code_base)['Contents']:
        if key['Key'].startswith("assets/rawjsondata/202") and ".json":
            previous_months_json_files_list.append(key['Key'])

    #Download the previous months files and merge into a single dataframe
    for previous_month in previous_months_json_files_list:
        s3_url = f"https://s3.amazonaws.com/{code_base}/{previous_month}"
        data = pandas.read_json(s3_url)
        time_series_data = pandas.DataFrame(data["response"]["time_series"])
        time_series = pandas.concat([time_series,time_series_data], ignore_index=True)
        time_series = time_series[time_series["solar_energy_exported"]!=0]


    #Drop columns that aren't applicable
    time_series = time_series.drop([
        'generator_energy_exported',
        'grid_services_energy_imported',
        'grid_services_energy_exported',
        'grid_energy_exported_from_generator',
        'grid_energy_exported_from_battery',
        'battery_energy_exported',
        'battery_energy_imported_from_grid',
        'battery_energy_imported_from_solar',
        'battery_energy_imported_from_generator',
        'consumer_energy_imported_from_battery',
        'consumer_energy_imported_from_generator'], axis=1)

    #Add new calculated values to dataframe
    time_series["net_energy"] = time_series["grid_energy_exported_from_solar"] - time_series["grid_energy_imported"]
    time_series["consumer_energy_imported_from_everywhere"] = time_series["consumer_energy_imported_from_solar"] + time_series["consumer_energy_imported_from_grid"]

    #Calculate lifetime energy used by sum'ing 
    lifetime_energy_imported_from_everywhere = round((time_series["consumer_energy_imported_from_everywhere"].sum()/1000),2)
    all_variables += f'var lifetime_energy_imported_from_everywhere = {lifetime_energy_imported_from_everywhere}\n'

    #Calculate lifetime net energy by sum'ing the columns and finding the difference
    lifetime_net_energy = int((time_series["grid_energy_exported_from_solar"].sum() - time_series["grid_energy_imported"].sum())/1000)
    print(f'Lifetime Net Energy: {lifetime_net_energy}')
    all_variables += f'var lifetime_net_energy = {lifetime_net_energy}\n'

    #The value of the the net energy sent back to Eversource
    lifetime_net_energy_value = round(lifetime_net_energy * .2395)
    print(f'Lifetime Net Energy Value: {lifetime_net_energy_value}')
    all_variables += f'var lifetime_net_energy_value = {lifetime_net_energy_value}\n'

    #The total of all of the solar energy produced by the system in kWh
    lifetime_solar_energy_exported = round(time_series["solar_energy_exported"].sum()/1000)
    print(f'Lifetime Solar Energy Created: {lifetime_solar_energy_exported}')
    all_variables += f'var lifetime_solar_energy_exported = {lifetime_solar_energy_exported}\n'

    #The value of all of the solar energy produced by the system
    lifetime_solar_energy_exported_value = round((time_series["solar_energy_exported"].sum()/1000) * .29636)
    print(f'Lifetime Solar Energy Created Value: {lifetime_solar_energy_exported_value}')
    all_variables += f'var lifetime_solar_energy_exported_value = {lifetime_solar_energy_exported_value}\n'

    #Lifetime daily electricity used in house
    lifetime_avg_daily_electricity_usage = round((time_series["consumer_energy_imported_from_everywhere"].mean()/1000),2)
    print(f'Daily Average Electricity Usage: {lifetime_avg_daily_electricity_usage}')
    all_variables += f'var lifetime_avg_daily_electricity_usage = {lifetime_avg_daily_electricity_usage}\n'

    #Lifetime daily electricity produced from solar
    lifetime_avg_daily_produced_by_solar = round((time_series["solar_energy_exported"].mean()/1000),2)
    print(f'Daily Average Electricity Produced from Solar: {lifetime_avg_daily_produced_by_solar}')
    all_variables += f'var lifetime_avg_daily_produced_by_solar = {lifetime_avg_daily_produced_by_solar}\n'

    #Format and output the dataframe in a JS variable compatible format
    for column in time_series:
        if column != "timestamp":
            time_series[column] = time_series[column].div(1000)
            # time_series[column] = time_series[column].astype('int')
            time_series[column] = time_series[column].apply(lambda x: format(float(x),".2f"))
        elif column == "timestamp":
            time_series[column]=time_series[column].str[:10]
            time_series[column] = pandas.to_datetime(time_series[column], format='%Y-%m-%d')
            time_series[column] = time_series[column].dt.strftime('%m-%d-%Y')
        column_in_list = time_series[column].values.tolist()
        column_with_var_prefix = f"var {column} = {column_in_list}"
        print(column_with_var_prefix)
        all_variables += f'{column_with_var_prefix}\n'
        # all_variables += "\n"

    #Download the existing data file
    scripts_url = f"http://{code_base}/assets/scripts.js"
    scripts_response = requests.get(scripts_url)
    scripts_text = scripts_response.text

    #Splitting and removing the first n lines based on the number of variables in all_variables
    nlines = all_variables.count('\n')
    scripts_text = scripts_text.split("\n",nlines)[nlines]

    #Adding the rest of the .js script to all_variables so it can be output as one file
    all_variables += scripts_text


    #Upload the new copy of scripts.js with the new variables in it
    object = s3.Object(
        bucket_name=code_base, 
        key='assets/scripts.js'
    )
    object.put(Body=all_variables)


lambda_handler("Any", "Any")

#Jay was here!
