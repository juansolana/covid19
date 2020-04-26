#!/bin/bash

# Build image and tag it
docker build -t us.gcr.io/ethereal-yen-274604/appengine/c19tracker:latest -f Dockerfile .

# Push image to gcloud run
docker push us.gcr.io/ethereal-yen-274604/appengine/c19tracker:latest
