# Database Interactions
_Still finding a good place for documenting this_

Much of the work that this service provides is database entries into remote database (supabase in this case).


## Considerations - Supabase
Given supabase's free tier the problem that remains is that data stored and not used is only allowed to live for limited time. After a period it will be disabled/erased.  Calls to it will come back in error and you'll need to log back in and re-enable.


## Initial Setup

The database is currently being set up like so:


```
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
```