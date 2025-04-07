#!/usr/bin/bash

cd /home/ubuntu/environment/apcr/aip/session3

python -m venv .env

source .env/bin/activate

pip install -r requirements.txt

streamlit run Home.py --server.port 8081 &

deactivate

