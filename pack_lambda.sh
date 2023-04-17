#!/bin/bash

rm -rf lambda_src
mkdir lambda_src

cp -a src/. lambda_src
# copying venv dependencies
# cp -a venv/lib/python3.10/site-packages/. lambda_src
pip install -t lambda_src -r lambda-requirements.txt

rm lambda_output/lambda.zip || true
cd lambda_src && zip -r ../lambda_output/lambda.zip .
