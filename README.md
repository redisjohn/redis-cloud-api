


# Getting Started with the Redis Enteprise Cloud API


### Overview

The Redis Cloud API is a RESTFUL API that can be used to managed your Redis Enterprise Cloud Flexible subscriptions.  You can use the API to create and manage subscription and databases, change credentials, backup and import databases, and access audit logs.  

> NOTE: The API is not supported for Fixed or Free Subscriptions
> 

Anyone who might be developing plugins for other provisioning tools such as Terraform, AWS CDK or Pulumi would leverage the API.

### Getting Started

The first step in using the Redis Cloud API is Obtaining an API keys.  API keys are used for authentication of a request.  Each account has it's own set of API keys that are managed in the Redis Enterprise System Manager. 

    (INSERT SCREENSHOT HERE)

When making an API request, the API keys are stored in the HTTP request header.   There are two types of keys. These are account and user keys.   The Account key is associated with the account.   The User key also known as the secret key) is associated with a user and can be revoked.

These keys are inserted into the header with the following names:

      X-API-KEY (Account Key)  
      X-API-SECRET-KEY (Revokable User Key)


### API documentation

The API is documented using Swagger.  For more information on Swagger see [https://swagger.io](http://swagger.io "Swagger").   Once you have API keys generated, you can the Swagger document to get basic information about your subscriptions and databases.  Take a look at:  [https://api.redislabs.com/v1/swagger-ui.html](https://api.redislabs.com/v1/swagger-ui.html "Redis Cloud API Documentation")


### API LifeCycle 

There are two types of API calls. These are asynchronous and synchronous.   For operations that do not modify resources, the API calls are synchronous and will return the results immediately.  

Asynchronous operations are long running tasks that and do not return immediately.  There will return a HTTP Status code of 201 along with a task ID.   The task ID can be used to track the status of a specific request using the following API call. 

    
    GET "https://api.redislabs.com/v1/tasks/<taskId>"

### Making API Calls 

API requests that create or modify resources require a JSON formatted request.  Sample requests can be found in the swagger document.   On important parameter is the "dryrun" flag.  This can be set to true to do a dry run without actually executing the request.   A task will be created but the resources will not be created or modified.  This allows you to test using an API call without changing the account associated with the keys provided.   Some of the API calls such as create subscription are long running and allocate resources on the cloud provider so "dryrun" is essential for testing.  


### Introducing rediscapi

rediscapi is a simple python command line interface to the Redis Cloud API.  It can be used to create and delete subscriptions, create, modify and delete databases, and it allows you to monitor a long running task.  Here's the documentation: 

### Examples

Before we can use rediscapi we have to edit **keys.json** and insert our api keys.

    { "apikey" : "InsertApikeyHere",  "secretkey": "InsertSecretkeyHere"}


##### Getting information about the account.  



    
#####  Create a subscription


  

### Conclusion


The Redis Cloud API provide a mechanism for DevOps teams and plugin developers to provide automated orchestration of common Redis Cloud tasks.   


This video provides a hands on tutorial to get you started:

[https://app.guidde.co/playbooks/mkMaxEzzwyDHzH7MWyvZ6J
](https://app.guidde.co/playbooks/mkMaxEzzwyDHzH7MWyvZ6J "Introduction to the Redis Cloud API")

   



