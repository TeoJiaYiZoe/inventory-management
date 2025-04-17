import boto3
from core.config import settings
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def get_db():
    return boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',
        region_name='ap-southeast-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    
    # AWS dynamoDB
    # return boto3.resource(
    #     'dynamodb',
    #     region_name=settings.AWS_REGION
    # )

def init_db():
    db = get_db()
    
    try:
        # Verify table exists
        table = db.Table(settings.DYNAMODB_TABLE)
        table.load()
        logger.info(f"Using existing table {settings.DYNAMODB_TABLE}")
        return table
        
    except db.meta.client.exceptions.ResourceNotFoundException:
        try:
            logger.info(f"Creating table {settings.DYNAMODB_TABLE}")
            table = db.create_table(
                TableName=settings.DYNAMODB_TABLE,
                KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'item_name', 'AttributeType': 'S'},
                ],
                BillingMode='PAY_PER_REQUEST',
                GlobalSecondaryIndexes=[{
                    'IndexName': 'NameIndex',
                    'KeySchema': [{'AttributeName': 'item_name', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                }],
                Tags=[{
                    'Key': 'Environment',
                    'Value': settings.ENVIRONMENT
                }]
            )
            table.wait_until_exists()
            return table
        except ClientError as e:
            logger.error(f"Table creation failed: {str(e)}")
            raise RuntimeError(f"DynamoDB initialization failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise RuntimeError(f"DynamoDB initialization failed: {str(e)}")