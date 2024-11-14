import json
import os


def lambda_handler(event, context):
    print(locals())
    return {
        'statusCode': 200,
        'body': json.dumps(dict(os.environ))
    }
