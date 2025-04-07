#!/usr/bin/python3

pip install -U -r /home/ubuntu/environment/apcr/requirements.txt

streamlit run /home/ubuntu/environment/apcr/saa/Home.py --server.port 8095 &

streamlit run /home/ubuntu/environment/genaionaws/01-BedrockAPI/Home.py --server.port 8080 &

streamlit run /home/ubuntu/environment/apcr/aip/session1/Home.py --server.port 8094 &

streamlit run /home/ubuntu/environment/apcr/aip/session2/Home.py --server.port 8082 &

streamlit run /home/ubuntu/environment/genaionaws/04-Embedding/Home.py --server.port 8084 &

streamlit run /home/ubuntu/environment/apcr/aip/session3/Home.py --server.port 8081 &

# crontab -e
#@reboot /bin/sh /home/ubuntu/environment/apcr/setup.sh
#@hourly /bin/sh /home/ubuntu/environment/apcr/setup.sh