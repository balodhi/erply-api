# Readme

This is an api usage implementation of erply.com with apache-kafka
Consumer receives the product from producer and use erply.com api to add the product if it is not already present.

# Packages Required

pip install kafka-python

pip install requests

# Running

REPLACE the values at line 29 with customized USERNAME, PASSWORD and CLIENTCODE

self.eap = eapi.EAPI(url='https://CLIENTCODE.erply.com/api/',clientCode='CLIENTCODE',username='USERNAME',password='PASSWORD',sslCACertPath=None)

and then

python ktest.py

# Note
1. Apache kafka must be configured and running before running the python script.
2. ubuntu may require the change the permission of the script. In that case use chmod +x ktest.py 

