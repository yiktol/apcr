#!/usr/bin/bash

cd /home/ubuntu/environment/apcr/aip/session4

python -m venv .env

source .env/bin/activate

pip install -r requirements.txt

# streamlit run Home.py --server.port 8082 &

deactivate

