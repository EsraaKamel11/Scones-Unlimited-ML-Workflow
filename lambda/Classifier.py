import os
import io
import boto3
import json
import base64


ENDPOINT_NAME = 'image-classification-2024-12-22-09-40-10-368'

# AWS's lightweight runtime solution to invoke an endpoint.
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    """
    ImageClassification Lambda Function

    This function performs image classification by decoding the Base64-encoded image data
    received from the SerializeImageData Lambda function, invoking a SageMaker endpoint
    to obtain classification inferences, and returning the results to AWS Step Functions
    for further processing.

    Args:
        event (dict): The event payload triggering the Lambda function. It must contain the following keys within the 'body' key:
            - 'image_data' (str): Base64-encoded string of the image data.
            - 's3_bucket' (str): The name of the S3 bucket where the image is stored.
            - 's3_key' (str): The key (path) to the image file within the S3 bucket.
        context (object): The runtime information provided by AWS Lambda (not used in this function).
    """

    # Decode the Base64-encoded image data
    image = base64.b64decode(event["body"]["image_data"])
    
    # Invoke the SageMaker endpoint for image classification
    predictor = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                        ContentType='image/png',
                                        Body=image)
    
    # Read and decode the prediction results    
    event["inferences"] = json.loads(predictor['Body'].read().decode('utf-8'))
    # Construct the successful response payload
    return {
        'statusCode': 200,
        'body': {
            "image_data": event["body"]['image_data'],
            "s3_bucket": event["body"]['s3_bucket'],
            "s3_key": event["body"]['s3_key'],
            "inferences": event['inferences'],
       }
    }
