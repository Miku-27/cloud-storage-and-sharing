import boto3
from botocore.config import Config
from functools import lru_cache
from urllib.parse import quote

def create_s3_client():
    return boto3.client(
        service_name="s3",
        region_name="eu-central-003",
        endpoint_url="https://s3.eu-central-003.backblazeb2.com",
        aws_access_key_id="00318e9082e0ac90000000004",
        aws_secret_access_key="K003FxVy4Mc02UyZbF5O4BBYa+QkBdE",
        config=Config(
            signature_version="s3v4",
        ),
    )

@lru_cache
def get_s3_client():
    return create_s3_client()

#function to be used by services

def generate_upload_url(key:str,mime_type):
    client=get_s3_client()
    return client.generate_presigned_url(
            'put_object',
            Params={'Bucket': "Major-project-bucket", 'Key':str(key)},
            ExpiresIn="600",
        )

def generate_download_url(key:str,filename:str):
    client = get_s3_client()
    safe_filename=quote(filename)
    return client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': "Major-project-bucket",
            'Key':str(key),
            'ResponseContentDisposition':f"attachment; filename*=UTF-8''{safe_filename}"},
        ExpiresIn=600,
    )


print(generate_download_url("test2.html","test2.hmtl"))