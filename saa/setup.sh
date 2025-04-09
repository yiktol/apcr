#!/usr/bin/bash

directory=/home/ubuntu/environment/apcr/saa
cd $directory

python -m venv .env

source .env/bin/activate

pip install -r requirements.txt

"/home/ubuntu/environment/apcr/saa/.env/bin"/streamlit run /home/ubuntu/environment/apcr/saa/Home.py --server.port 8095 &

deactivate