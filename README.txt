This is prepped to run in a VPC Linux Ubuntu server.

To run the API and make it be available 24/7 carry out the next steps:

1 Install docker if it is not installed in your server
2 docker build -t kavak_webhook .
3 docker run -d -p 5000:5000 kavak_webhook
