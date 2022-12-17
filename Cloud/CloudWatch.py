import boto3
from botocore.exceptions import NoCredentialsError
import os
from datetime import datetime
from dotenv import load_dotenv
from app import *
from EC2 import *


load_dotenv(verbose=True)

# string = '12'
# string2 = '12'

noOfItems = len(memory_cache)
totalSize = Total_Size()
requestPerMin = requests[0]
missRate = miss[0]
hitRate = hit[0]
workers = Max[0]


client = boto3.client('cloudwatch',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME'))


client.put_metric_data(
    Namespace='WebPhotoStat',
    MetricData=[
        {
            'MetricName': 'WebChart',
            'Dimensions': [
                {
                    'Name': 'no. of items',
                    'Value': str(noOfItems)
                },
                {
                    'Name': 'TotalSize',
                    'Value': str(totalSize)
                },
                {
                    'Name': 'RequestPerMin',
                    'Value': str(requestPerMin)
                },
                {
                    'Name': 'MissRate',
                    'Value': str(missRate)
                },
                {
                    'Name': 'HitRate',
                    'Value': str(hitRate)
                },
                {
                    'Name': 'no. of workers',
                    'Value': str(workers)
                },
            ],
            'Values': [
                0,
            ],
            
            'Unit': 'Count',
            'StorageResolution': 60,
        },
    ]
)