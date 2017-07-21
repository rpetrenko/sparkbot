## Message processor

### webhooks
#### Cisco spark
* should be on public IP
* Currently only Cisco spark is supported
* Start webhooks/bot-flask.py on a server with public IP
* register webhook on spark

### mp_server
* start message processing server
* mp_server/mp_server.py
* create ssh reverse tunnel to the server where webhook is running

Currently supported APIs: jenkins, gerrit
