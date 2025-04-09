#!/usr/bin/bash

directory=/home/ubuntu/environment/apcr/aip/session3/

# cd /home/ubuntu/environment/apcr/aip/session3/
cd $directory

if [ -d $directory/.env ]; 
    then
        echo "Directory exists."
    else
        echo "Directory does not exists."

        python -m venv .env
        source .env/bin/activate
        pip install -U pip
        pip install -r requirements.txt
        deactivate
fi

/home/ubuntu/environment/apcr/aip/session3/.env/bin/streamlit run /home/ubuntu/environment/apcr/aip/session3/Home.py --server.port 8081 &


