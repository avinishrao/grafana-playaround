import json
import requests
import boto3
import time
import random
import os

timestream = boto3.client('timestream-write', region_name= os.environ['REGION_NAME']) 
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

#Lambda function for checking if email exists
def lambda_handler(event, context):
    try:
        email = event['queryStringParameters']['email'] #Extract URL query parameter

        if userExisting(email):
            return {'statusCode': 200, 'body': json.dumps(f"User with email '{email}' exists in Grafana database")}

        createUser(email) #Creates new user 
        return {'statusCode': 200, 'body': json.dumps(f"User with email '{email}' has been created in Grafana database with viewer access")}

    #Error handling
    except KeyError as e:
        return processError(f"Unable to process - missing URL query parameters: '{str(e)}")

    except requests.exceptions.RequestException as e:
        return processError(f"An error occured while processing request to the Grafana API: {str(e)}")

    except Exception as e:
        return processError(f"Internal Server Error: {str(e)}")

#Function for checking the email existence
 def userExisting(email):
    try:
        headers = {
            "Authorization": f"Bearer {apiToken}",
            "Content-Type" : "application/json"
        }
        response = requests.get(f"{grafanaURL}/org/users", headers=headers) 
        responseJson = response.json()
        tableUsers = [user.get('email') for user in responseJson]
        emailExists = email in tableUsers
        return emailExists

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error while processing user name: {str(e)}")
        
#Function for creating new user in the database    
def createUser(email):
    try:
        user_data = {
            'name': email.split('@')[0],
            'email': email,
            'login': email.split('@')[0],
            'password': email.split('@')[0]+'@'+str(reqCounter),
            'role': 'Viewer'
        }
        response = requests.post(f"{grafanaURL}/admin/users", auth=(grafanaUsername, grafanaPwd), headers={"Content-Type" : "application/json"}, json=user_data) 
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error while creating user: {str(e)}")        

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
requestData = {
    'requestId': str(reqCounter),
    'timestamp': currentTime,
    'statusCode': reqCounter
}

logToTimestream(requestData)
