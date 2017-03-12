# Cornell Research System 

## Local installation

1. ```pip install -r requirements.txt```

2. Download virtual env.py to create a virtual environment

    ```sudo easy_install virtualenv```

3. create virtual env

	```virtualenv venv```

4. install the flask extensions

    ```
    flask/bin/pip install flask
    flask/bin/pip install flask-login
    flask/bin/pip install flask-openid
    flask/bin/pip install flask-mail
    flask/bin/pip install flask-sqlalchemy
    flask/bin/pip install sqlalchemy-migrate
    flask/bin/pip install flask-whooshalchemy
    flask/bin/pip install flask-wtf
    flask/bin/pip install flask-babel
    flask/bin/pip install guess_language
    flask/bin/pip install flipflop
    flask/bin/pip install coverage
    flask/bin/pip install argparse
    flask/bin/pip install rauth
    ```

5. Create the db locally - not connected to a server!
	* If you must give the permission to the file-
		```chmod a+x db_create.py``` then excecute it ```./db_create.py```

6. ```./run.py``` ("./run.pu debug" is needed for templates to update without restarting the server)

7. ```sass --watch app/assets/scss:app/static/css``` (if updating SASS, must also have SASS installed)