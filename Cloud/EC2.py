import boto3
import base64
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from botocore.config import Config
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
from dotenv import load_dotenv
load_dotenv(verbose=True)

Max = {0:0}
instance_Storage = {}


client = boto3.client('ec2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME'))
        
Myec2=client.describe_instances()

for pythonins in Myec2['Reservations']:
    
    for printout in pythonins['Instances']:

        if ((str(printout['State']['Name']) == 'running' or str(printout['State']['Name']) == 'pending') and str(printout['InstanceId']) != 'i-06340a90561e1390f'):
                print(printout['InstanceId'])
                i = 1
                Max[0] = Max[0] + 1
                instance_Storage[i] = printout['InstanceId']
                i = i + 1


# info = {}


def create_EC2_Instance():
    
    if (Max[0] < 8):

        ec2  = boto3.resource('ec2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME'))

        instance_params = {'ImageId': os.getenv('EC2_IMAGEID'), 'InstanceType': os.getenv('EC2_INSTANCETYPE'),
        'KeyName': os.getenv('EC2_KEYPAIR'), 
        'SecurityGroupIds': [os.getenv('SECURITYGROUPIDS1'),os.getenv('SECURITYGROUPIDS2'),os.getenv('SECURITYGROUPIDS3')]}

        ec2.create_instances (**instance_params, MinCount=1, MaxCount=1)[0]
        # instance.wait_until_running()

        print("New Instance Created")
        Max[0] = Max[0] + 1

        client = boto3.client('ec2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME'))
        
        Myec2=client.describe_instances()

        for pythonins in Myec2['Reservations']:
            
            for printout in pythonins['Instances']:

                if ((str(printout['State']['Name']) == 'running' or str(printout['State']['Name']) == 'pending') and str(printout['InstanceId']) != 'i-06340a90561e1390f'):

                    print(printout['InstanceId'])
                    i = Max[0]
                    instance_Storage[i] = printout['InstanceId']
                    i = i - 1
        

    else:
        print("Max numbers on instance has reached!")

def terminate_EC2_Instance():

    ec2  = boto3.client('ec2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('REGION_NAME'))
    
    if (Max[0] > 0):
        

        ec2.terminate_instances(InstanceIds= [instance_Storage[Max[0]]])

        Max[0] = Max[0] - 1
        print("Instance terminated")
    else:
        print("No instances exist to terminate")

# create_EC2_Instance()