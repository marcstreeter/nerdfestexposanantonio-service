import base64
import json
import os
import sys
import uuid

import logging

from supabase.client import Client, create_client

# set up logger
logging.basicConfig(level=logging.INFO, force=True)
handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        entry = parse_entry(event)
    except Exception as e:
        logger.error(f"failed to parse {event=} because {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "failed to load event"})
        }
    try:
        return {
            'statusCode': 200,
            'body': json.dumps(rsvp(entry=entry))
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }


def parse_entry(event):
    if event.get('body'):  # lambda
        content = decode_base64(event.get('body')) if event.get('isBase64Encoded', False) else event.get('body')
        evt = json.loads(content)
    else:  # container
        evt = event
    
    if event.get("requestContext"):
        client_ip = event["requestContext"].get("http", {}).get("sourceIp")
    else:
        client_ip = "unknown"

    if "rsvp_name" not in evt:
        raise Exception('object missing required keys')

    return {
        'name': evt.get('rsvp_name', 'test name'),
        'uuid': str(uuid.uuid4()),
        'contact': evt.get('rsvp_contact', {'email': 'jane.smith@example.com'}),
        'total': evt.get('rsvp_total', 1),
        'interests': evt.get('rsvp_interests', ['1', '4']),
        'network': evt.get('rsvp_network', {'source': 'friend'}),
        'whoami': {**evt.get('rsvp_whoami', {}), "ip": client_ip}
    }


def decode_base64(content):
    return base64.b64decode(content).decode('utf-8')


def rsvp(entry):
    supabase_key = os.getenv('SUPABASE_KEY')
    supabase_url = os.getenv('SUPABASE_URL')

    if not all([supabase_url, supabase_key]):
        raise ValueError('Supabase URL and Key must be set as environment variables.')

    client: Client = create_client(supabase_url, supabase_key)
    response = client.table('rsvp').insert(entry).execute()
    return {'data': response.data}

# SUPABASE INSERT QUERY
# CREATE TABLE public.rsvp (
#     id serial PRIMARY KEY,
#     created_at timestamp DEFAULT NOW() NOT NULL,  -- Automatically adds the current timestamp
#     uuid uuid DEFAULT gen_random_uuid() NOT NULL, -- Unique public identifier for each RSVP, generated automatically
#     name varchar(100) NOT NULL,  -- Small string (100 characters), required, main person making the reservation
#     contact jsonb NOT NULL CHECK (
#         jsonb_typeof(contact) = 'object' AND (
#             (contact ? 'email' AND contact->>'email' IS NOT NULL AND contact->>'email' <> '') OR
#             (contact ? 'phone' AND contact->>'phone' IS NOT NULL AND contact->>'phone' <> '') OR
#             (contact ? 'discord' AND contact->>'discord' IS NOT NULL AND contact->>'discord' <> '') OR
#             (contact ? 'facebook' AND contact->>'facebook' IS NOT NULL AND contact->>'facebook' <> '') OR
#             (contact ? 'instagram' AND contact->>'instagram' IS NOT NULL AND contact->>'instagram' <> '') OR
#             (contact ? 'linkedin' AND contact->>'linkedin' IS NOT NULL AND contact->>'linkedin' <> '') OR
#             (contact ? 'whatsapp' AND contact->>'whatsapp' IS NOT NULL AND contact->>'whatsapp' <> '') OR
#             (contact ? 'x' AND contact->>'x' IS NOT NULL AND contact->>'x' <> '')
#         )
#     ),  -- JSON object, required, must include at least one of the contact types
#     total smallint NOT NULL CHECK (total >= 1 AND total <= 5),  -- Small integer, required, limits attendees to a max of 5
#     interests jsonb,  -- JSON object, optional, stores interests in events
#     network jsonb,    -- JSON object, optional, records who/what told the person about the event
#     whoami jsonb NOT NULL CHECK (
#         jsonb_typeof(whoami) = 'object' AND (
#             (whoami ? 'ip' AND whoami->>'ip' IS NOT NULL) OR
#             (whoami ? 'unique' AND whoami->>'unique' IS NOT NULL) OR
#             (whoami ? 'cookie' AND whoami->>'cookie' IS NOT NULL)
#         )
#     )  -- JSON object, required, must include at least one of the keys: 'ip', 'uuid', or 'cookie' with a non-empty value
# );
#
# Environment Variables:
#   AWS_LAMBDA_FUNCTION_VERSION = '$LATEST'
#   AWS_EXECUTION_ENV = 'AWS_Lambda_python3.12'
#   AWS_DEFAULT_REGION = 'us-west-2'
#   AWS_LAMBDA_LOG_STREAM_NAME = <...>
#   AWS_REGION = 'us-west-2'
#   PWD = '/var/task'
#   _HANDLER = 'main.lambda_handler'
#   SUPABASE_URL = <...>
#   TZ = ':UTC'
#   LAMBDA_TASK_ROOT = '/var/task'
#   LANG = 'en_US.UTF-8'
#   AWS_SECRET_ACCESS_KEY = <...>
#   AWS_LAMBDA_LOG_GROUP_NAME = '/aws/lambda/nerdfestexpo-sanantonio-rsvp'
#   AWS_LAMBDA_RUNTIME_API = '169.254.100.1:9001'
#   AWS_LAMBDA_FUNCTION_MEMORY_SIZE = '128'
#   LAMBDA_RUNTIME_DIR = '/var/runtime'
#   _AWS_XRAY_DAEMON_ADDRESS = '169.254.100.1'
#   AWS_XRAY_DAEMON_ADDRESS = '169.254.100.1:2000'
#   SHLVL = '0'
#   AWS_ACCESS_KEY_ID = <...>
#   SUPABASE_KEY = <...>
#   LD_LIBRARY_PATH = '/var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib'
#   AWS_LAMBDA_FUNCTION_NAME = 'nerdfestexpo-sanantonio-rsvp'
#   PATH = '/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin'
#   AWS_LAMBDA_INITIALIZATION_TYPE = 'on-demand'
#   AWS_SESSION_TOKEN = <...>
#   AWS_XRAY_CONTEXT_MISSING = 'LOG_ERROR'
#   _AWS_XRAY_DAEMON_PORT = '2000'
#   LC_CTYPE = 'C.UTF-8'
#   PYTHONPATH = '/var/runtime'
#   _X_AMZN_TRACE_ID = <...>
#
# Function Logs:
# {
#   'event': {'rsvp_name': 'poo', 'rsvp_last': 'bar', 'rsvp_interest': 'bam'},
#   'context': LambdaContext(
#     [
#       aws_request_id=<...>,
#       log_group_name=<...>,
#       log_stream_name=<...>,
#       function_name=<...>,
#       memory_limit_in_mb=128,
#       function_version=$LATEST,
#       invoked_function_arn=arn:aws:lambda:us-west-2:145172005480:function:<...>,
#       client_context=None,
#       identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])]
#   )
# }

