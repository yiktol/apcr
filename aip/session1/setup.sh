#!/usr/bin/python3

python -m venv /home/ubuntu/environment/apcr/aip/session1/.env

source /home/ubuntu/environment/apcr/aip/session1/.env/bin/activate

pip install -U -r /home/ubuntu/environment/apcr/aip/session1/requirements.txt
streamlit run /home/ubuntu/environment/apcr/aip/session1/Home.py --server.port 8094 &


