import json

# Confidence threshold for inferences
THRESHOLD = .93

def lambda_handler(event, context):
    """
    FilterInferences Lambda Function

    This function evaluates the confidence scores (inferences) provided by the ImageClassification
    Lambda function. It filters out low-confidence inferences by checking if any inference meets
    or exceeds a predefined threshold. If the threshold is met, the function passes the data
    back to the AWS Step Functions workflow. Otherwise, it raises an error to terminate the workflow.

    Args:
        event (dict): The event payload triggering the Lambda function. It must contain the following keys within the 'body' key:
            - 'image_data' (str): Base64-encoded string of the image data.
            - 's3_bucket' (str): The name of the S3 bucket where the image is stored.
            - 's3_key' (str): The key (path) to the image file within the S3 bucket.
            - 'inferences' (list): A list of confidence scores returned by the SageMaker endpoint.
        context (object): The runtime information provided by AWS Lambda (not used in this function).

    Returns:
        dict: A dictionary containing the HTTP status code and the original event data if the threshold is met.
              - 'statusCode' (int): HTTP status code indicating the result of the operation (e.g., 200 for success).
              - 'body' (str): JSON-serialized string of the original event data.
    """
  
    # Get the inferences from the event
    inferences = event["body"]["inferences"]
    
    # Check if any inference meets or exceeds the threshold
    meets_threshold = (max(inferences) > THRESHOLD)
    
    # Threshold met; pass the data back to the Step Function
    if meets_threshold:
        pass
    else:
        # Threshold not met; raise a custom error to terminate the Step Function
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
