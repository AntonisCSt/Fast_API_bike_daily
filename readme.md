# Commands to run docker locally
`docker build . -t fast_api`
`docker run -p 8000:8000 fast_api`

activate environment

`python send_data.py`
`pytest ./`


There is an issue here on where we are going to add the model. We want to build the image with GithubActions (one their server). But the problem here is that size of the trained model is larger than 100MB (the maximum file size on GitHub). Therefore, we decided o upload the model in the cloud. Allowing, only ourselves to access it.

# Upload model to the cloud

We are going to use AWS.

Step 1. Create an account with free-tier.

So we are going to save our model in the cloud storage (s3 bucket). We want only us to access it with a special code. To do that, we are going to create a special user that does that.

Step 2. Go to `IAM` and to the` Users` a user that is going to access the S3 bucket. Don't add any policy just continue.

Step 3. Add a keypair for CLI aws (the first one from the list). Download the keypair to save place in your folder. Make sure you don not share it with anyone.

Step 4: Go to S3 bucket, create a new bucket (just name it and continue until is create). I name it `bike-model/`. Create a new folder inside the bucket (for me it was `bike_model`)

Step 5: Now we are going to create a policy for this bucket. It will only allow people/Users with the key we downloaded to download and upload files in the bucket. Go to IAM roles services--> Policies--> Create policy. In Specify Permission, select the JSON and add this:


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
 
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```
add a name (remember it cause you will use it in the next step).

Step 6. Now we are going to attach the policy to the User we created. Go to
IAM -> Users -> your user mine is s3-reader-inspiron -> Add permissions
In `Permissions options` select `Attach policies directly` and search for the policy you created. Once you fine it, select it and press `next`, In `Review` press `add permissions`.

So, now, instead of using the volume data, we are going to configure the docker image to download the model. 
