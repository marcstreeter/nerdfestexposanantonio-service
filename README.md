# nerdfestexposanantonio-service


# testing

Call the lambda service with commandline:

```commandline
curl "http://localhost:18080/2015-03-31/functions/function/invocations" -d '{"rsvp_name":"SomeName","rsvp_total":4}'
```

Call the lambda service from the `requests.rest` from within PyCharm