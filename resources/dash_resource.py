from flask_restful import Resource
from flask import render_template, make_response, redirect
from models.printing_model import PrintingModel
from models.micro_model import MicroModel
from models.marking_model import MarkingModel
from models.sensor_model import SensorModel
from flask_httpauth import HTTPBasicAuth
import resources.home_resource as h
import sqlite3
from sqlite3 import OperationalError

auth = HTTPBasicAuth()

users = {
    "admin": "admin",
}


@auth.get_password
def get_pw(username):
    """Function to check password from user dictionary"""
    if username in users:
        return users.get(username)
    return None


class DashResource(Resource):
    """Dash structure when you requests anything from the dashboard"""
    @auth.login_required
    def get(self):
        """Dash get function to return main page and returns a bunch of data"""
        try:
            connection = sqlite3.connect('data.db')
        except OperationalError:
            connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = cursor.execute('SELECT version FROM version')
        check = str(query.fetchone()[0])
        connection.close()
        if h.version == check:
            return None
        else:
            return redirect('/shutdown')
