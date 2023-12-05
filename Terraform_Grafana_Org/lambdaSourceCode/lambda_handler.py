import json
import requests
import boto3
import time
import random
import os

timestream = boto3.client('timestream-write', region_name=os.environ['REGION_NAME']) 
sns = boto3.client('sns')
grafanaURL = os.environ['GRAFANA_URL']
grafanaUsername = os.environ['GRAFANA_UNAME']
grafanaPwd = os.environ['GRAFANA_PWD']
snsARN = os.environ['SNS_ARN']
apiToken = os.environ['API_TOKEN'] 
timestreamDB = os.environ['TS_DB']
timestreamDBTable = os.environ['TS_TABLE']
reqCounter = random.randint(0, 100)

#Function for getting time in ms
def millisecondTime():
    return int(round((time.time() * 1000)))
currentTime = millisecondTime()

#Lambda function for checking if organization exists
def lambda_handler(event, context):
    try:
        orgs = event['queryStringParameters']['org'] #Extract URL query parameter

        #Checking if organization is present 
        if orgExisting(orgs):
            return {'statusCode': 200, 'body': json.dumps(f" '{orgs}' exists in Grafana database")}
        else:
            return {'statusCode': 404, 'body': json.dumps(f" '{orgs}' does not exist in Grafana database")}

    #Error handling
    except KeyError as e:
        return processError(f"Unable to process - missing URL query parameters: '{str(e)}")
        
    except Exception as e:
        return processError(f"Internal Server Error: {str(e)}")

#Function for checking the organization existence
def orgExisting(orgs):
    try:
        headers = {
            "Authorization": f"Bearer {apiToken}",
            "Content-Type" : "application/json"
        }
        response = requests.get(f"{grafanaURL}/org", headers=headers) 
        org_name = response.json().get('name')
        org_exist = orgs in org_name
        return org_exist

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error while processing organization: {str(e)}")

#Function to log errors and publis to sns
def processError(errorMessage):
    publishToSNS(errorMessage)
    return {'statusCode': 500, 'body': json.dumps(errorMessage)}
    
def publishToSNS(message):
    sns.publish(TopicArn=snsARN, Message=message, Subject='Log error to SNS ERR_TOPIC')

#Function to log data to timestream
def logToTimestream(request_data):
    try:
        timestream.write_records(
            DatabaseName=timestreamDB,
            TableName=timestreamDBTable,
            Records=[
                {
                    'Dimensions': [
                        {'Name': 'requestId', 'Value': request_data.get('requestId', 'unknown')},
                        {'Name': 'timestamp', 'Value': str(request_data.get('timestamp', 'unknown'))},
                    ],
                    'MeasureName': 'statusCode',
                    'MeasureValue': str(request_data.get('statusCode', 'unknown')),
                    'Time': str(request_data.get('timestamp', 'unknown')),
                }
            ]
        )
        print(f"Request added to the timestream successfully: {request_data}")

    except timestream.exceptions.RejectedRecordsException as e:
        print(f"Error - records are rejected: {e.response['RejectedRecords']}")

    except Exception as e:
        print(f"Error while processing logs to the timestream: {str(e)}")

#Request data for the timestream
request_data = {
    'requestId': str(reqCounter),
    'timestamp': currentTime,
    'statusCode': reqCounter
}
logToTimestream(request_data)