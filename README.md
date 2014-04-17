
## taassignment 

An application that allows faculty members to select teaching assistants for their classes

Clone this repository, cd into the project folder and run the following commands

    virtualenv-2.6 --no-site-packages .env
    source .env/bin/activate
    pip install -r requirements.txt
    chmod +x manage.py

Create an Mysql local database named taassignment and then synchronize the new database:
    
    ./manage.py syncdb

Now, you can start run server and test the site:
    
    ./manage.py runserver 0.0.0.0:5678
