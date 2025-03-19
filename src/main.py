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


def parse_entry(event) -> dict:
    default_uuid = uuid.uuid4()
    if event.get('body'):  # lambda
        content = decode_base64(event.get('body')) if event.get('isBase64Encoded', False) else event.get('body')
        evt = json.loads(content)
    else:  # container
        evt = event
    
    if event.get("requestContext"):
        context = event["requestContext"]
        client_ip = context.get("http", {}).get("sourceIp")
        client_uuid = str(context.get("timeEpoch", default_uuid))
    else:
        client_ip = "unknown"
        client_uuid = default_uuid
    
    if event.get("headers"):
        forwarded_ip = event.get("headers", {}).get("x-forwarded-for", "").split(",")[0]
    else:
        forwarded_ip = "unknown"
    
    if "rsvp_name" not in evt:
        raise Exception('object missing required keys')

    return {
        'name': evt.get('rsvp_name', 'test name'),
        'uuid': client_uuid,
        'contact': evt.get('rsvp_contact', {'email': 'jane.smith@example.com'}),
        'total': evt.get('rsvp_total', 1),
        'interests': evt.get('rsvp_interests', ['1', '4']),
        'network': evt.get('rsvp_network', {'source': 'friend'}),
        'whoami': {
            **evt.get('rsvp_whoami', {}),
            "ip": client_ip,
            "ip_forwarded": forwarded_ip,
        }
    }


def decode_base64(content):
    return base64.b64decode(content).decode('utf-8')


def rsvp(entry: dict) -> dict:
    supabase_key = os.getenv('SUPABASE_KEY')
    supabase_url = os.getenv('SUPABASE_URL')

    if not all([supabase_url, supabase_key]):
        raise ValueError('Supabase URL and Key must be set as environment variables.')

    client: Client = create_client(supabase_url, supabase_key)
    response = client.table('rsvp').insert(entry).execute()
    return {'data': response.data}
