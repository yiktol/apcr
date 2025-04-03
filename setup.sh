
# chown ubuntu:root /home/ubuntu/environment/ -R

# git config --global --add safe.directory /home/ubuntu/environment/genaionaws/

cd /home/ubuntu/environment/apcr

pip install -U -r /home/ubuntu/environment/apcr/requirements.txt

# cd /home/ubuntu/environment/apcr/saa
# streamlit run Home.py --server.port 8080 &

cd /home/ubuntu/environment/genaionaws/01-BedrockAPI
streamlit run Home.py --server.port 8080 &

cd /home/ubuntu/environment/genaionaws/00-MLBasics
streamlit run Home.py --server.port 8094 &

cd /home/ubuntu/environment/apcr/aip/session2
streamlit run Home.py --server.port 8082 &

cd /home/ubuntu/environment/genaionaws/04-Embedding
streamlit run Home.py --server.port 8084 &