
# chown ubuntu:root /home/ubuntu/environment/ -R

# git config --global --add safe.directory /home/ubuntu/environment/genaionaws/

cd /home/ubuntu/environment/apcr

pip install -U -r /home/ubuntu/environment/apcr/requirements.txt

cd /home/ubuntu/environment/apcr/saa
streamlit run Home.py --server.port 8080 &



