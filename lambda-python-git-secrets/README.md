# Secret Leak Prevention in an AWS Lambda Function

This demo uses
[python-git-secrets](https://github.com/mbacchi/python-git-secrets) in an AWS
Lambda function to clone a GitHub repository, then scan the repository for
secrets.

## Prerequisites

- [Serverless Framework](https://serverless.com)

- AWS account

## Deploying the Lambda Function

To deploy, first export your AWS profile and region:

```
export AWS_PROFILE=profile_name && export AWS_REGION=us-east-2
```

Then run the deploy:

```
$ sls deploy
Serverless: Generated requirements from ./secret-leak-prevention-demo/lambda-python-git-secrets/requirements.txt in ./secret-leak-prevention-demo/lambda-python-git-secrets/.serverless/requirements.txt...
Serverless: Installing requirements from ./secret-leak-prevention-demo/lambda-python-git-secrets/.serverless/requirements/requirements.txt ...
Serverless: Running ...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
.....
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service lambda-python-git-secrets.zip file to S3 (1.36 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
.....................
Serverless: Stack update finished...
Service Information
service: lambda-python-git-secrets
stage: dev
region: us-east-2
stack: lambda-python-git-secrets-dev
resources: 7
api keys:
  None
endpoints:
  None
functions:
  python-git-secrets: lambda-python-git-secrets-dev-python-git-secrets
layers:
  None
Serverless Enterprise: Run `serverless login` and deploy again to explore, monitor, secure your serverless project for free.


$ sls info
Service Information
service: lambda-python-git-secrets
stage: dev
region: us-east-2
stack: lambda-python-git-secrets-dev
resources: 7
api keys:
  None
endpoints:
  None
functions:
  python-git-secrets: lambda-python-git-secrets-dev-python-git-secrets
layers:
  None
```

## Removing the Function

```
$ sls remove
Serverless: Getting all objects in S3 bucket...
Serverless: Removing objects in S3 bucket...
Serverless: Removing Stack...
Serverless: Checking Stack removal progress...
........
Serverless: Stack removal finished...
```
