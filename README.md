### Before Launch Required Software MacOS
```
pip
pip install aws-cli
pip install j2cli
brew install gnu-sed
```

### To Launch:

go to the .env file, and change the default values. Even if your s3 bucket doesn't exist it will create the bucket for you on the first pass through.

```
DEFAULT_REGION
AWS_ACCOUNT_ID
AWS_STATE_BUCKET
MESH_NAME
```

Then you can execute the entire stack+deploy with

```
make launch
```

This will take a good 15-20 minutes depending on your internet speeds, so go grab a coffee or check your email while you wait on this one.

If you want to re-deploy then you can run, or manually push a docker image with the tag of latest. Then you need to navigate to your codepipeline, to followthrough with the blue/green deployment.

```
make build
```
### To Destroy
```
make destroy
```



TODO

# Change Virtual Service to use Virtual router as the target

# IAM ROLE