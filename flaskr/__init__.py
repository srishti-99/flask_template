from pathlib import Path

from flask import Flask, request, url_for, render_template, redirect, flash
import psycopg2 as pg
from psycopg2 import connect, Error
import pandas as pd
from . import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    ipath = Path(app.instance_path)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=ipath/'flaskr.sqlite',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        ipath.mkdir(exist_ok=True)
    except OSError:
        pass
    
    dataObj = db.Data()

    @app.route('/')
    def hello():
        return redirect('/users')
    
    @app.route('/users')
    def users():
        dataObj.update_df()
        return render_template('user_table.html', tables=[dataObj.df.reset_index()])

    
    @app.route('/insert', methods=['GET', 'POST'])
    def insert_user(): 
        """
        Send username, firstname, lastname, description to html form as a post request
        """
        dataObj.update_df()
        username = request.form.get("user_name","").lower().replace(" ", "_")
        ids = list(dataObj.df.index.values)
        
        if request.method == 'POST':
            if username != "" and username not in ids:
                flash("Username: " + username)
                description = request.form.get("description","")
                firstname = request.form.get("firstname","")
                lastname = request.form.get("lastname","")
                db.insert_user(firstname, lastname, username, description)
                return redirect('/users')
            elif username in ids:
                flash("This username already exists. Please try again with different username")

        return render_template('insert.html', users=ids)

    @app.route('/update/<username>', methods=['GET', 'POST'])
    def update(username):
        """
        Send username, firstname, lastname, description to html form as a post request
        """
        dataObj.update_df()
        username = username.lower().replace(" ", "_")
        ids = list(dataObj.df.index.values)
        if request.method == 'POST' and username in ids:
            description = request.form.get("description", dataObj.df.loc[username]['description'])
            if description == "":
                description = dataObj.df.loc[username]['description']
            
            firstname = request.form.get("firstname", dataObj.df.loc[username]['firstname'])
            if firstname == "":
                firstname = dataObj.df.loc[username]['firstname']
            
            lastname = request.form.get("lastname", dataObj.df.loc[username]['lastname'])
            if lastname == "":
                lastname = dataObj.df.loc[username]['lastname']
            
            db.update_user(firstname, lastname, username, description)
            flash("Your data was updated")
            return redirect('/users')       
        elif request.method == 'PUT' and username not in ids: 
            flash("This username does not exist. Choose one from this list to update:")
            return render_template('user_table.html', tables=[dataObj.df.reset_index()])
        return render_template('update.html', username=username)

    @app.route('/delete/<username>', methods=['GET', 'POST'])
    def delete(username): 
        """
        Send deletion to html form as a post request 
        """
        dataObj.update_df()
        username = username.lower().replace(" ", "_")
        ids = list(dataObj.df.index.values)
        if request.method == 'POST' and username in ids:
            deletion = request.form.get("deletion", "")
            if deletion == "Delete": 
                db.delete_user(username)
                flash("user: " + username + " has been deleted.")
                return redirect('/users')
            elif deletion == "Cancel": 
                flash("user: " + username + " NOT deleted.")
                return redirect('/users')
        return render_template('delete.html', username=username)


    return app

