# Flask Template 
This template lays out a basic flask app that allows users to input, update and delete information into a PostgreSQL database. All html files that are to be rendered should go in the '/templates' directory and all css files should go in the '/static' directory. Make sure 'database.ini' and your '/data' directory are in .gitignore. 

## Directories
	/flaskr
		/templates 
		/static 
		__init__.py 
		db.py 
		flask_schema.sql
	/data
		/flaskr_db 
	database.ini
	.ignore 

## Data
All data inputted by the user is stored in a local database. You must login into the postgresql as a user with access to create a database. Store user login information in the database.ini in this form so that the app can access your database: 
	
	[development]
	host=<hostname>
	database=<databasename>
	user=<username>
	password=<password>

### Initializing the Database
To initiate your postgresql database, run the following commands in terminal from within the data directory to initialize the data tables as in flask_schema.sql: 

	cd data
	Initdb -D flaskr_db 
	sudo chmod 700 flaskr_db
	pg_ctl -D flaskr_db -l logfile start

	psql -d template1

	template1=# CREATE DATABASE flaskrdb;
	CREATE DATABASE
	template1=# \q
	template1=# \c flaskrdb;
	
	flaskrdb=# \i ../flaskr/flask_schema.sql

## Running the flask app 
To run the app, type the following commands in terminal. Make sure you're currently in the 'flask_template' directory to avoid export errors: 

	export FLASK_APP=flask
	export FLASK_ENV=development 
	flask run 

Alternatively, you might have to use 

	python3 -m flask run


