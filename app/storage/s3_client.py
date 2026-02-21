import boto3
from functools import lru_cache
from app.config import get_config
from urllib.parse import quote

def create_s3_client():
    return boto3.client(
        service_name="s3",
        region_name=get_config().storage_region,
        endpoint_url=get_config().storage_endpoint_url,
        aws_access_key_id=get_config().access_key_id,
        aws_secret_access_key=get_config().access_key_secret,
    )

@lru_cache
def get_s3_client():
    return create_s3_client()

#function to be used by services

def generate_upload_url(key:str,content_type:str):
    client=get_s3_client()
    return client.generate_presigned_url(
            'put_object',
            Params={'Bucket': get_config().bucket_name, 'Key':str(key),'ContentType':content_type},
            ExpiresIn=get_config().bucket_url_expire_seconds,
        )

def generate_download_url(key:str,filename:str):
    client = get_s3_client()
    safe_filename=quote(filename)
    return client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': get_config().bucket_name,
            'Key':str(key),
            'ResponseContentDisposition':f"attachment; filename*=UTF-8''{safe_filename}"},
        ExpiresIn=get_config().bucket_url_expire_seconds,
    )