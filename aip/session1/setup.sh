#!/usr/bin/bash

directory=/home/ubuntu/environment/apcr/aip/session1/

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

/home/ubuntu/environment/apcr/aip/session1/.env/bin/streamlit run /home/ubuntu/environment/apcr/aip/session1/Home.py --server.port 8094 &
