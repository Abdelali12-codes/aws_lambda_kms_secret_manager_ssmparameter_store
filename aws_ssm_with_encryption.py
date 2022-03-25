import boto3
import os

from base64 import b64decode

ENCRYPTED = os.environ['NAME']
# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container
DECRYPTED = boto3.client('kms').decrypt(
    CiphertextBlob=b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    
    value = ssm.get_parameter(
    Name='/my-db/dev/password',
     WithDecryption=True
   )
    # TODO handle the event here
    print("-------------NAME-------")
    print(DECRYPTED)
    
    print("------------db-SSM-------------")
    print(value['Parameter']['Value'])
    
    return DECRYPTED