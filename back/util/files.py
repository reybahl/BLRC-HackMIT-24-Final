import boto3
from botocore.client import Config

access_key_id = '47111b0f99db6690ed0b7d340979de56'
secret_access_key = '77b487eb3acc7dbc4d8701ce9e62f4a7c44716d38116d061dc5a229395f239a0'
endpoint_url = 'https://752c3dd4c8e27b1f472a31fc8c6aad68.r2.cloudflarestorage.com'
bucket_name = 'hackmit2024'


class CloudflareR2:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = bucket_name

    def list_objects(self):
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []

    def get_object(self, object_key):
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
        return response['Body'].read()

    def upload_object(self, object_key, data):
        self.s3_client.put_object(Bucket=self.bucket_name, Key=object_key, Body=data)

    def delete_object(self, object_key):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)

    def generate_presigned_url(self, object_key, expiration=3600, http_method='put'):
        """
        Generate a presigned URL for the S3 object.

        :param bucket_name: Name of the bucket
        :param object_key: Name of the object/file
        :param expiration: Time in seconds for the presigned URL to remain valid
        :param http_method: HTTP method to use ('get' or 'put')
        :return: Presigned URL as string
        """
        return self.s3_client.generate_presigned_url(
            'put_object' if http_method == 'put' else 'get_object',
            Params={'Bucket': self.bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )

# Example usage
if __name__ == "__main__":
    
    r2 = CloudflareR2()
    
    
    # Examples for using the CloudflareR2 class
    # List all objects in the bucket
    objects = r2.list_objects()
    print(f"Objects in the bucket: {objects}")
    
    
    # Upload an object
    object_key = 'example_upload.txt'
    data = b'Hello, World!'
    r2.upload_object(object_key, data)
    print(f"Uploaded object '{object_key}'")
    
    # Get the object
    object_data = r2.get_object(object_key)
    print(f"Object data: {object_data}")
    
    # Delete the object
    r2.delete_object(object_key)
    print(f"Deleted object '{object_key}'")
    

    # Generate a presigned URL for uploading
    object_key = 'example_upload.txt'
    presigned_url = r2.generate_presigned_url(bucket_name, object_key)
    print(f"Presigned URL for uploading: {presigned_url}")

    # You can now use this presigned URL to upload a file directly to R2
