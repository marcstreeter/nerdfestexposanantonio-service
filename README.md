# nerdfestexposanantonio-service

## dev set up

The following environment is expected:

- Docker (with kubernetes enabled)
- Tilt
- VSCode (for debugging)
- `.env` file is populated with required supabase details

## prod set up

The following environment is expected:

- AWS Account with:
  - Lambda function created (name used in Github Repository secrets)
- Supabase account with schema created as is shown in `main.py`
- Github Actions Permissions must be enabled (e.g "Allow all actions and reusable workflows")
- Github has Repository secrets set on the following
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_LAMBDA_FUNCTION_NAME // ex: nerdfestexpo-sanantonio-rsvp, should match the name of the lambda created earlier
  - AWS_LAMBDA_REGION // ex: us-west-2
  - SUPABASE_KEY // ex: eySuperL0ngKeY4U.Ev2nL0Ng3rSTuFF.Ok_that1z@ll
  - SUPABASE_URL // ex: https://yxeboogwqtadffzmiozm.supabase.co

## testing

Call the lambda service with commandline:

```commandline
curl "http://localhost:18080/2015-03-31/functions/function/invocations" -d '{"rsvp_name":"SomeName","rsvp_total":4}'
```

Call the lambda service from the `requests.rest` from within PyCharm
