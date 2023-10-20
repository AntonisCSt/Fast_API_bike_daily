

# Building our CI workflow

For a CI workflow we would like to build the image and run the dockerfile successfully. After that we would like to perform our tests.

## Build and test locally

`docker build . -t fast-api-bike-daily:0.0.1`
`docker run -p 8000:8000 fast-api-bike-daily:0.0.1`

activate environment

`python send_data.py`
`pytest ./`

## Build and test in Github Actions

For our this simple case we are going to upload our model in the repo. Note: This generally is not a best practice since we would like to hide this information. However, we are going to see in a later, optional chapter, how to address this even if it is not within the scope of foundations course.

```yml
name: Build-Test
run-name: Fast-Api Docker build and test
env:
  DOCKER_IMAGE_NAME: fast-api-bike-daily:0.0.2
  REGISTRY: antonisst
on:
  push:
    branches:
      - main  # The default branch name in your repository
jobs:
  build-docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker
        uses: docker/setup-buildx-action@v1

      - name: Build Docker
        run: docker build . -t $DOCKER_IMAGE_NAME

      - name: Run Docker
        run: docker run -d -p 8000:8000 $DOCKER_IMAGE_NAME

      - name: Wait for the server to start
        run: sleep 6  

      - name: install dev requirements to run pytest
        run: pip install -r dev-requirements.txt

      - name: Test container with pytest
        run: pytest ./


```

As you can see, we created a dev-requirements.txt that installs the required libraries to run pytest.

## Continous Deployment

Let's check the commands locally first:

Make sure you have an account on https://hub.docker.com/

In your terminal log in to dockerhub via:
`docker login`

push the image on Dockerhub with the tag:

`docker images`

create a repository with:

`docker tag fast-api-bike-daily:0.0.1 [yourdockerhubname]/fast-api-bike-daily:0.0.1`

`docker push [yourdockerhubname]/fast-api-bike-daily:0.0.1`

in case you have an error: `denied: requested access to the resource is denied` check this solution:
https://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker

Note: If it takes too long to push you can cancel the push with ctrl+C. Github Actions network will be much faster.

Let's edit the Github Actions based on: https://github.com/docker/build-push-action
It uses docker/build-push-action@v5

Requirment: We first add the DockerHub username and password as secrets like this guide: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

```yml

name: Build-Test
run-name: Fast-Api Docker build and test
env:
  DOCKER_IMAGE_NAME: fast-api-bike-daily:0.0.2
  REGISTRY: antonisst
on:
  push:
    branches:
      - main  # The default branch name in your repository
jobs:
  build-docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker
        uses: docker/setup-buildx-action@v1

      - name: Build Docker
        run: docker build . -t $DOCKER_IMAGE_NAME

      - name: Run Docker
        run: docker run -d -p 8000:8000 $DOCKER_IMAGE_NAME

      - name: Wait for the server to start
        run: sleep 6  

      - name: install dev requirements to run pytest
        run: pip install -r dev-requirements.txt

      - name: Test container with pytest
        run: pytest ./
      
  push_to_registry:
    name: Push Docker image to Docker Hub
    needs: build-docker
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
        
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.DOCKER_IMAGE_NAME }}

          
```

In this new job we first log it to Docker Hub using Github secrets. and then we use from marketplace the `docker/build-push-action@v5` adding the information required for the registry and the tags!


EXERCISE 1: Write again the job push_to_registry using docker/build-push-action@v4. Try find it yourself, it might be required by a company with legacy code. Help: check out https://github.com/marketplace/actions/build-and-push-docker-images?version=v5.0.0



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
