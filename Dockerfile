#
FROM python:3.8

# set api as the current work dir
WORKDIR /api

# copy the requirements list
COPY ./requirements.txt /code/requirements.txt

# install all the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy the main code of fastapi
COPY ./app /api/app

# copy the model
COPY ./models /api/models


# launch the unicorn server to run the api
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it
# that the application is running behind HTTPS, etc.
CMD ["uvicorn", "app.main:pokemon_app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
