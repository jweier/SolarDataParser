import boto3
import json 

s3 = boto3.resource('s3')
from botocore.exceptions import ClientError

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
        raise e

    secrets = json.loads(get_secret_value_response['SecretString'])

    return secrets['refresh_token']