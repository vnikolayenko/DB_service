from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
#class DecimalEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            if o % 1 > 0:
#                return float(o)
#            else:
#                return int(o)
#        return super(DecimalEncoder, self).default(o)
# Helper class to convert a DynamoDB item to YAML.
class DecimalEncoder(yaml.YAMLObject):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Employees')

fe = Key('emp_id').between(1, 4)
pe = "types, first_name, second_name, default_salary, experience "
# Expression Attribute Names for Projection Expression only.
esk = None


response = table.scan(
    FilterExpression=fe,
    ProjectionExpression=pe
    )

for i in response['Items']:
    if isinstance(i, decimal.Decimal):
            if i % 1 > 0:
                print (float(i))
            else:
                print (int(i))
    #print(json.dumps(i, cls=DecimalEncoder))
    #print(yaml.dump(DecimalEncoder(i)))
    #print (dump(i))
    #print(i)

while 'LastEvaluatedKey' in response:
    response = table.scan(
        ProjectionExpression=pe,
        FilterExpression=fe,
        ExclusiveStartKey=response['LastEvaluatedKey']
        )

    for i in response['Items']:
        if isinstance(i, decimal.Decimal):
            if i % 1 > 0:
                print (float(i))
            else:
                print (int(i))
        #print(json.dumps(i, cls=DecimalEncoder))
        #print(yaml.dump(DecimalEncoder(i)))
        #print(i)
        #print (dump(i))