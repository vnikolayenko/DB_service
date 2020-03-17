from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Employees')

types = "designer"
emp_id = 4
first_name = "Korolenko"
second_name = "Konstantyn"
default_salary = 2000
experience = 3

response = table.put_item(
   Item={
        'types': types,
        'emp_id': emp_id,
        'first_name' : first_name,
        'second_name' : second_name,
        'default_salary': default_salary,
        'experience':experience
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))