import boto3
import base64
from botocore.exceptions import NoCredentialsError
import io
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)

string = '10'
string2 = '10'
client = boto3.client('cloudwatch',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME'))


client.put_metric_data(
    Namespace='WebPhotoStat',
    MetricData=[
        {
            'MetricName': 'WebPhotoStat',
            'Dimensions': [
                {
                    'Name': 'string',
                    'Value': string
                },
                {
                    'Name': 'string2',
                    'Value': string2
                },
            ],
            
            'StatisticValues': {
                'SampleCount': 123.0,
                'Sum': 123.0,
                'Minimum': 123.0,
                'Maximum': 123.0
            },
            'Values': [
                123.0,
            ],
            'Counts': [
                123.0,
            ],
            'Unit': 'Count',
            'StorageResolution': 60,
        },
    ]
)