import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    SerializeImageData Lambda Function

    This function retrieves an image from a specified Amazon S3 bucket, encodes the image data
    in Base64 format, and returns the serialized data along with relevant metadata to be consumed
    by AWS Step Functions or other downstream processes.

    Args:
        event (dict): The event payload triggering the Lambda function. It must contain the following keys:
            - 's3_bucket' (str): The name of the S3 bucket where the image is stored.
            - 's3_key' (str): The key (path) to the image file within the S3 bucket.
        context (object): The runtime information provided by AWS Lambda (not used in this function).

    Returns:
        dict: A dictionary containing the HTTP status code and a body with the serialized image data
              and associated metadata.
              - 'statusCode' (int): HTTP status code indicating the result of the operation (e.g., 200 for success).
              - 'body' (dict): A dictionary with the following keys:
                  - 'image_data' (str): Base64-encoded string of the image data.
                  - 's3_bucket' (str): The name of the S3 bucket from which the image was retrieved.
                  - 's3_key' (str): The key of the image within the S3 bucket.
                  - 'inferences' (list): An empty list reserved for future inference results.
    """
    
    # Extract S3 bucket name and key from the event
    key =event["s3_key"] 
    bucket =event["s3_bucket"] 
    
    # Download the image from S3 to the temporary directory
    boto3.resource('s3').Bucket(bucket).download_file(key, "/tmp/image.png")
    
    # Read and encode the image data in Base64
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Construct the response payload
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
