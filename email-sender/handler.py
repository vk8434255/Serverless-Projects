import json
import boto3
from botocore.exceptions import ClientError

def send_email(receiver_email, subject, body_text):
    
    SENDER = "vk6200853@gmail.com"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name='ap-south-1')

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    receiver_email,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email successfully sent'})
        }

def email_handler(event, context):
    # Parse input from API Gateway
    try:
        body = json.loads(event['body'])
        receiver_email = body.get('receiver_email')
        subject = body.get('subject')
        body_text = body.get('body_text')
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

    # Check if required parameters are provided
    if not (receiver_email and subject and body_text):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required parameters'})
        }

    # Send the email
    result = send_email(receiver_email, subject, body_text)
    return result
