import boto3
import base64
from botocore.exceptions import NoCredentialsError
import io
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

bucket_name = "cloud1-project-bucket"

def download_file_from_bucket(s3_key):
   
    
    s3  = boto3.resource('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION_NAME'))

    obj = s3.Object(bucket_name, s3_key)
    io_stream = io.BytesIO()
    obj.download_fileobj(io_stream)

    io_stream.seek(0)
    data = base64.b64encode(io_stream.read()).decode("utf-8")

    print ("Download Successful")

    return data

def delete_file_from_bucket(s3_key):

    s3  = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION_NAME'))

    s3.delete_object(
        Bucket= bucket_name,
        Key= s3_key,
    )   

# s3.download_file(Key=s3_key, Bucket="cloud1-project-bucket", Filename=dst_path)

# download_file_from_bucket('tci-s3-demo', 'children_download.csv')
# with open('children_download.csv') as fo:
#     print(fo.read())




def upload_to_aws(local_file, s3_key):

    
    s3  = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION_NAME'))

    try:
        s3.upload_fileobj(Fileobj=local_file, Bucket="cloud1-project-bucket", Key=s3_key)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# upload_to_aws('local_file', 's3_file_name')


# for bucket in s3.buckets.all():
#     print(bucket.name)

# s3.download_file(
#     Bucket= s3, Key="train.csv", Filename="data/downloaded_from_s3.csv"
# )



