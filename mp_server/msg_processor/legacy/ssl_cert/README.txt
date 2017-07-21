place ssl_cert and ssl_cert_key here

On server:
1. Generate self signed SSL key and certificate on the server

openssl genrsa 1024 > ssl_cert_key
openssl req -new -x509 -nodes -sha1 -days 365 -key ssl_cert_key > ssl_cert

On client:
1. Copy ssl_cert from server
