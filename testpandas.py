import pandas
from boto3 import client

conn = client('s3')

previous_months_json_files_list = []
time_series = pandas.DataFrame()

# Parse through the S3 bucket and find JSON files for previous months data
for key in conn.list_objects(Bucket='jayweier.com')['Contents']:
    if key['Key'].startswith("assets/rawjsondata/202") and ".json":
        previous_months_json_files_list.append(key['Key'])

#Download the previous months files and merge into a single dataframe
for previous_month in previous_months_json_files_list:
    s3_url = f"https://s3.amazonaws.com/jayweier.com/{previous_month}"
    data = pandas.read_json(s3_url)
    time_series_data = pandas.DataFrame(data["response"]["time_series"])
    time_series = pandas.concat([time_series,time_series_data], ignore_index=True)

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

#Add new net energy value
time_series["net_energy"] = time_series["grid_energy_exported_from_solar"] - time_series["grid_energy_imported"]

#Have to subtract 420 because of fluke when Net Meter was installed and caused readings to be incorrect
lifetime_net_energy = int((time_series["grid_energy_exported_from_solar"].sum() - (time_series["grid_energy_imported"].sum() - 420))/1000)
print(lifetime_net_energy)

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


#var solar_energy_exported = {'kWhCreated': [17.27, 28.31, 20.88, 31.01, 26.15, 23.7, 16.58, 23.77, 26.0, 8.82, 27.06, 31.2, 20.53, 27.74, 28.72]}
