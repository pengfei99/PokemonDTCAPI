# PokemonDTCAPI

This project read a model from a mlflow model registry. Then exposed this model via a rest api 

## Docker image

The docker image is build and publish via github action. It's triggered after a new release is created. 

Note as it requires connecting to a mlflow model registry. It's hard for you to test locally

## k8s deployment

In k8s folder, you can find all your need to run the docker image in a k8s deployment, service and ingress.

### configure and deploy a k8s secret
Note, you need to create a k8s secret first. Because in our case, the model registry(mlflow) uses a s3(minio) 
to store the model. To read the model, you need to have a s3 credential. 

The template to create the secret is located in **templates/my-s3-creds.yaml**.
You need to replay it with your own s3 credentials.

Configure the deployment.yaml

### configure and deploy a k8s deployment

In **k8s/deployment**, you have **three principal env var** you need to configure,
- url of the model registry
- model name
- model version
```yaml
# the url of the model registry
- name: MLFLOW_TRACKING_URI
  value: https://user-pengfei-474302.kub.sspcloud.fr/
          
# env var for setting models uri which will be deployed
# model name
- name: MLFLOW_MODEL_NAME
  value: pokemon

# model version
- name: MLFLOW_MODEL_VERSION
  value: "2"
```

With these three parameters, the api can find the right model to answer the question.

### configure service and ingress

service.yaml expose your deployment to other services in the cluster. So other services can access the pod via a url, not
via an ip address(note ip is floating for pod, it changes after pod creation and deletion )

ingress.yaml exposes your deployment to other people which are external of your cluster. 

## Argo CD 

You can notice to deploy the service, you need to run `kubectl apply -f <file-name>`. If you update your config, you need 
to delete the old, and rerun the command `kubectl apply -f <file-name>` to deploy new version. 

Argo CD can help you to avoid this.

Argo CD can check the current deployment of your service with a repo git (in our case, it's all files under folder k8s). 
If I have a new model version 3. I need to update my api, I only need to go to my git repo, change the model version
in **deployment.yaml**. After commit, Argo CD will detect there is a difference between current deployment and version
in git repo. It will start an update which will update the current deployment to be identical with the git repo.


Note argo CD will monitor all files under k8s. If we put the `my-s3-creds.yaml` also in k8s, Argo CD will make sure
the secret in my cluster is identical with the git repo.

As we can't put the real password and login in git, so the 'my-s3-creds.yaml' is only a template that contains dummy
password and login. So we don't want the Argo CD to monitor this file. That's why we put it in another folder called
**template**



