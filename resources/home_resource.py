from flask_restful import Resource
from flask import make_response, render_template, redirect
from models.home_model import HomeModel
import sqlite3
from sqlite3 import OperationalError
import version as v

version = v.version_final


class HomeResource(Resource):
    """Resource for home page"""
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
        except OperationalError:
            connection = sqlite3.connect('data.db')

        cursor = connection.cursor()
        query = cursor.execute('SELECT version FROM version')
        check = str(query.fetchone()[0])
        obj = HomeModel.data('1')
        connection.close()
        if version == check:
            return make_response(render_template('home.html', home_data=obj))
        else:
            return redirect('/shutdown')
