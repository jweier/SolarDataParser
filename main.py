# This file is only used if deploying locally. If using Lambda, ignore this file and reference lambda_function.py.

import tesla
import pandas
import os

code_base = "C:\\PersonalCode\\SolarDataParser\\"

json_data_folder = f"{code_base}\\assets\\rawjsondata\\"
scripts_js_path = f"{code_base}\\assets\\scripts.js"

deployment_type = "local"
seed_data = "n"

#Getting the list of directories
json_data_folder_dir = os.listdir(json_data_folder)

#Checking if the list is empty or not
if len(json_data_folder_dir) == 0:
    seed_data = input("The JSON data folder directory appears to be empty. Would you like to seed the historial data? Y or N?: ").lower()

#Call to Tesla to seed each previous months worth of data
if seed_data == "y":
    print(f"Seeding historical data into {json_data_folder}")
    tesla.seed_data(code_base = code_base, deployment_type = deployment_type)
    

#Call to Tesla to get the latest copy of the monthly data
tesla.call_tesla_api(code_base = code_base, deployment_type = deployment_type)

all_variables = ""

previous_months_json_files_list = []
time_series = pandas.DataFrame()

#Parse through the S3 bucket and find JSON files for previous months data
all_json_files = os.listdir(json_data_folder)
for file in all_json_files:
    previous_months_json_files_list.append(file)

#Download the previous months files and merge into a single dataframe
for previous_month in previous_months_json_files_list:
    json_file_path = f"{json_data_folder}{previous_month}"
    data = pandas.read_json(json_file_path)
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
lifetime_net_energy_value = round(lifetime_net_energy * .26)
print(f'Lifetime Net Energy Value: {lifetime_net_energy_value}')
all_variables += f'var lifetime_net_energy_value = {lifetime_net_energy_value}\n'

#The total of all of the solar energy produced by the system in kWh
lifetime_solar_energy_exported = round(time_series["solar_energy_exported"].sum()/1000)
print(f'Lifetime Solar Energy Created: {lifetime_solar_energy_exported}')
all_variables += f'var lifetime_solar_energy_exported = {lifetime_solar_energy_exported}\n'

#The value of all of the solar energy produced by the system
lifetime_solar_energy_exported_value = round((time_series["solar_energy_exported"].sum()/1000) * .31)
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
        time_series[column] = time_series[column].astype('int')
    elif column == "timestamp":
        time_series[column]=time_series[column].str[:10]
        time_series[column] = pandas.to_datetime(time_series[column], format='%Y-%m-%d')
        time_series[column] = time_series[column].dt.strftime('%m-%d-%Y')
    column_in_list = time_series[column].values.tolist()
    column_with_var_prefix = f"var {column} = {column_in_list}"
    print(column_with_var_prefix)
    all_variables += f'{column_with_var_prefix}\n'

#Download the existing scripts file
with open(scripts_js_path) as file:
    scripts_text = file.read()

#Splitting and removing the first n lines based on the number of variables in all_variables
nlines = all_variables.count('\n')
scripts_text = scripts_text.split("\n",nlines)[nlines]

#Adding the rest of the .js script to all_variables so it can be output as one file
all_variables += scripts_text

#Upload the new copy of scripts.js with the new variables in it
with open(scripts_js_path, 'w') as file:
    file.write(all_variables)