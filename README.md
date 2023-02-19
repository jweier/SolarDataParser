# SolarDataParser
A dashboard for Tesla Solar customers that don't have a PowerWall/Energy Gateway. These instructions are written to deploy locally to a system. The code is also easy to run via AWS Lambda/S3/CloudFront if you're familiar with those services.

## Download the code repository
* Go to https://github.com/jweier/SolarDataParser/archive/refs/heads/main.zip
* Unzip the file
* Move to your desired directory
  * If using a webserver, the root of this zip file contains the index.html page that you will want to serve up
* Make note of the path to the directory you chose as it will be needed later

## Environment Setup
* Install Python 3
  * Windows - https://www.python.org/downloads/
  * Pi OS - sudo apt-get install python3
* Open a command prompt or terminal window and go to the directory where you unzipped the code
* Run the following command to install the required Python packages
python install -r requirements.txt

## Get your Tesla API Refresh Token
This token should be kept private as it allows anyone with the token to generate more API tokens to access your data.

* Browse to https://tesla-info.com/tesla-token.php
* Under Step 1, click Tesla Logon
* Login with your Tesla Credentials
* You will receive an error page
* Copy the URL of that page and paste it into the tesla-info website that you originally opened
* Scroll down and copy the text under Refresh Token (do not get your access token, this will not work)
* Keep that text for the setup process

## Seed the data
This step should only be performed once and is only needed for initial setup. You will be asked the month/year you first started generating solar energy and then it will call the Tesla API and download the data for each month since you specified. Unfortunately, it has to be downloaded per month because if the time period is any larger Tesla summarizes the data and you don't get the daily level of detail.
* Find the seed_data.py file in the root of the code and edit it
* At the very top, there is a variable named json_data_folder. Update this variable to point to the full path of the rawjsondata folder that was unzipped from the code.
python seed_data.py

## Setup the code
* Find the main.py file in the root of the code and edit it
* At the very top, there is a variable named json_data_folder. Update this variable to point to the full path of the rawjsondata folder that was unzipped from the code.
* At the very top, there is another variable named scripts_js_path. Update this variable to point to the full path (including scripts.js) where the scripts.js file lives. By default, it's in the code base under the assets folder.
  * For Windows paths, be sure to use a double backslash instead of a single backslash (i.e. C:\\MyCodebase instead of C:\MyCodebase)
* 
