#!/usr/bin/python3

python -m venv /home/ubuntu/environment/apcr/aip/session2/.env

source /home/ubuntu/environment/apcr/aip/session2/.env/bin/activate

pip install -U -r /home/ubuntu/environment/apcr/aip/session2/requirements.txt
streamlit run /home/ubuntu/environment/apcr/aip/session2/Home.py --server.port 8082 &


