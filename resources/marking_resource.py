from flask_restful import Resource, reqparse
from flask import make_response, render_template, redirect
from models.marking_model import MarkingModel
from datetime import datetime
import resources.home_resource as h
import sqlite3
from sqlite3 import OperationalError


class MarkingResource(Resource):
    """Communication for main marking requests"""
    parse = reqparse.RequestParser()
    parse.add_argument('employee',
                       type=str,
                       )
    parse.add_argument('model',
                       type=str,
                       )
    parse.add_argument('rp_serial',
                       type=str,
                       )
    parse.add_argument('ins_type',
                       type=str,
                       )
    parse.add_argument('rec_date',
                       type=str,
                       )
    parse.add_argument('start_date',
                       type=str,
                       )
    parse.add_argument('accessories',
                       type=str,
                       )
    parse.add_argument('appearance',
                       type=str,
                       )
    parse.add_argument('functions',
                       type=str,
                       )
    parse.add_argument('cleaning',
                       type=str,
                       )
    parse.add_argument('complete',
                       type=str,
                       )
    parse.add_argument('notes',
                       type=str,
                       )

    def get(self):
        try:
            connection = sqlite3.connect('data.db')
        except OperationalError:
            connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = cursor.execute('SELECT version FROM version')
        check = str(query.fetchone()[0])
        connection.close()
        if h.version == check:
            return make_response(render_template('marking_form.html'))
        else:
            return redirect('/shutdown')

    def post(self):
        time = datetime.today()
        data = MarkingResource.parse.parse_args()
        entry = MarkingModel(time, data['employee'], data['model'], data['rp_serial'], data['ins_type'], '', '', '',
                             '', '', '', '', '')
        entry.save_to_db()
        return redirect('/markinglog')


class MarkingLog(Resource):
    """Communication for marking log"""
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
        except OperationalError:
            connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = cursor.execute('SELECT version FROM version')
        check = str(query.fetchone()[0])
        connection.close()
        if h.version == check:
            return make_response(render_template('marking_log.html', data=MarkingModel.get_all_data()[::-1]))
        else:
            return redirect('/shutdown')


class MarkingEdit(Resource):
    """Communication for marking edit form"""
    def get(self, id, name):
        obj = MarkingModel.get_single_data(id)
        try:
            connection = sqlite3.connect('data.db')
        except OperationalError:
            connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = cursor.execute('SELECT version FROM version')
        check = str(query.fetchone()[0])
        connection.close()
        if h.version == check:
            return make_response(render_template('marking_edit.html', data=obj))
        else:
            return redirect('/shutdown')

    def post(self, id, name):
        parse = reqparse.RequestParser()
        parse.add_argument('notes',
                           type=str)
        data = parse.parse_args()
        time = datetime.today()
        if name == 'rec_date':
            MarkingModel.update_rec_date(id, time)
        elif name == 'start_date':
            MarkingModel.update_start_date(id, str(time))
        elif name == 'accessories':
            MarkingModel.update_accessories(id, 'stuff')
        elif name == 'appearance':
            MarkingModel.update_appearance(id, 'good')
        elif name == 'functions':
            MarkingModel.update_functions(id, 'funcs')
        elif name == 'cleaning':
            MarkingModel.update_cleaning(id, 'complete')
        elif name == 'complete':
            MarkingModel.update_complete(id, str(time))
        elif name == 'notes':
            MarkingModel.update_notes(id, data['notes'])
        else:
            pass
        return redirect(f'/marking/{id}/null')
