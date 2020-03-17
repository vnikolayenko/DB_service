from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import yaml
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource("dynamodb", region_name='us-east-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Employees')


types="manager"
emp_id=1

try:
    response = table.get_item(
        Key={
            'types': types,
            'emp_id': emp_id
            
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    item = response['Item']#Python Dictionary
    print("GetItem succeeded:")
    #print(json.dumps(item, indent=4, cls=DecimalEncoder))#Other converter method YAML
    print(yaml.dump(item, indent=4))