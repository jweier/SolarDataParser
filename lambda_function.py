import boto3
import tesla
import requests 
s3 = boto3.resource('s3')

def lambda_handler(event, context):

    new_access_token = tesla.get_new_token()

    tesla_monthly_data = tesla.call_tesla_api("monthly", new_access_token)
    tesla_lifetime_data = tesla.call_tesla_api("lifetime", new_access_token)

    time_series_list = []
    time_series_dict = {"Date": time_series_list}
    solar_energy_exported_list = []
    solar_energy_exported_dict = {"kWhCreated": solar_energy_exported_list}
    consumer_energy_imported_from_grid_list = []
    consumer_energy_imported_from_grid_dict = {"kWh": consumer_energy_imported_from_grid_list}
    consumer_energy_imported_from_solar_list = []
    consumer_energy_imported_from_solar_dict = {"kWh": consumer_energy_imported_from_solar_list}
    total_consumer_energy_list = []
    total_consumer_energy_dict = {"kWhUsed": total_consumer_energy_list}

    #Parse through the current month JSON reply and extract the data that is valuable
    for entry in tesla_monthly_data['response']['time_series']:
        if entry['solar_energy_exported'] != 0:

            #Parsing the timestamp
            timestamp_unformatted = entry['timestamp']
            timestamp_year = timestamp_unformatted[0:4]
            timestamp_month = timestamp_unformatted[5:7]
            timestamp_day = timestamp_unformatted[8:10]
            timestamp_formatted = f'{timestamp_month}-{timestamp_day}-{timestamp_year}'                        
            time_series_list.append(timestamp_formatted)
            
            #Amount of solar produced for that day
            solar_energy_exported_rounded = round(int(entry['solar_energy_exported'])/1000,2)
            solar_energy_exported_list.append(solar_energy_exported_rounded)

            #Amount of electricty used by house from Eversource that day
            consumer_energy_imported_from_grid_rounded = round(int(entry['consumer_energy_imported_from_grid'])/1000,2)
            consumer_energy_imported_from_grid_list.append(consumer_energy_imported_from_grid_rounded)

            #Amount of electricty used by house from solar that day
            consumer_energy_imported_from_solar_rounded = round(int(entry['consumer_energy_imported_from_solar'])/1000,2)
            consumer_energy_imported_from_solar_list.append(consumer_energy_imported_from_solar_rounded)

            #Total amount of electricity used by house that day
            total_consumer_energy_rounded = round((consumer_energy_imported_from_grid_rounded + consumer_energy_imported_from_solar_rounded),2)
            total_consumer_energy_list.append(total_consumer_energy_rounded)

    #Store data into strings that can be output to Javascript variables
    time_series_var_string = f'var date = {time_series_dict}'
    solar_energy_exported_var_string = f'var solar_energy_exported = {solar_energy_exported_dict}'
    consumer_energy_imported_from_grid_var_string = f'var consumer_energy_imported_from_grid = {consumer_energy_imported_from_grid_dict}'
    consumer_energy_imported_from_solar_var_string = f'var consumer_energy_imported_from_solar = {consumer_energy_imported_from_solar_dict}'
    total_consumer_energy_var_string = f'var total_consumer_energy = {total_consumer_energy_dict}'


    #Parse through the lifetime JSON reply and extract the data that is valuable
    for entry in tesla_lifetime_data['response']['time_series']:   
        
        #How many kWh the system has produced in its lifetime
        lifetime_solar_energy_exported = tesla_lifetime_data['response']['time_series'][0]['solar_energy_exported']
        lifetime_solar_energy_exported_rounded = round(int(lifetime_solar_energy_exported)/1000,2)
        lifetime_solar_energy_exported_rounded_var_string = f'var lifetime_solar_energy_exported = {lifetime_solar_energy_exported_rounded}'
        
        #The value of all of the solar energy produced by the system
        lifetime_solar_energy_exported_value = round(lifetime_solar_energy_exported_rounded * .31)
        lifetime_solar_energy_exported_value_var_string = f'var lifetime_solar_energy_exported_value = {lifetime_solar_energy_exported_value}'

        #The amount of electricy that was sent to Eversource from Solar
        lifetime_grid_energy_exported_from_solar = tesla_lifetime_data['response']['time_series'][0]['grid_energy_exported_from_solar']
        lifetime_grid_energy_exported_from_solar_rounded = round(int(lifetime_grid_energy_exported_from_solar)/1000,2)

        #The mount of electricity that was used by house from Eversource
        lifetime_grid_energy_imported = tesla_lifetime_data['response']['time_series'][0]['grid_energy_imported']
        lifetime_grid_energy_imported_rounded = round(int(lifetime_grid_energy_imported)/1000,2)

        #The difference between the amount of electricty sent to Eversource and used by the house from Eversource
        lifetime_net_energy_exported_grid = round((lifetime_grid_energy_exported_from_solar_rounded - (lifetime_grid_energy_imported_rounded - 420)))
        lifetime_net_energy_exported_grid_var_string = f'var lifetime_net_energy_exported_grid = {lifetime_net_energy_exported_grid}'
        
        #The value of the difference of between the amount of electricty sent to Eversource and used by the house from Eversource
        lifetime_net_energy_exported_grid_value = round(lifetime_net_energy_exported_grid * .26)
        lifetime_net_energy_exported_grid_value_var_string = f'var lifetime_net_energy_exported_grid_value = {lifetime_net_energy_exported_grid_value}'
        


    #Download the existing data file
    scripts_url = "http://jayweier.com/assets/scripts.js"
    scripts_response = requests.get(scripts_url)
    scripts_text = scripts_response.text

    #Splitting and removing the first 9 lines
    scripts_text = scripts_text.split("\n",9)[9]

    #Write all variables and the script body to a string, so it can be output to S3 file
    updated_scripts_text = (
        f"{time_series_var_string}\n"
        f"{solar_energy_exported_var_string}\n"
        f"{total_consumer_energy_var_string}\n"
        f"{lifetime_solar_energy_exported_rounded_var_string}\n"
        f"{lifetime_solar_energy_exported_value_var_string}\n"
        f"{consumer_energy_imported_from_grid_var_string}\n"
        F"{consumer_energy_imported_from_solar_var_string}\n"
        f"{lifetime_net_energy_exported_grid_var_string}\n"
        f"{lifetime_net_energy_exported_grid_value_var_string}\n"
        f"{scripts_text}"
    )

    #Upload the new copy of scripts.js with the new variables in it
    object = s3.Object(
        bucket_name='jayweier.com', 
        key='assets/scripts.js'
    )

    object.put(Body=updated_scripts_text)

lambda_handler("Any", "Any")

#Jay was here!
