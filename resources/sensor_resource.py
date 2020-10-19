from flask_restful import Resource, reqparse
from flask import make_response, render_template, redirect, request
from models.sensor_model import SensorModel
from datetime import datetime
import resources.home_resource as h
import sqlite3
from sqlite3 import OperationalError
from fpdf import FPDF
import os
import pathlib


class SensorResource(Resource):
    """Communication for main Sensor requests"""
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
            return make_response(render_template('Sensor_form.html'))
        else:
            return redirect('/shutdown')

    def post(self):
        time = datetime.today()
        data = SensorResource.parse.parse_args()
        entry = SensorModel(time, data['employee'], data['model'], data['rp_serial'], data['ins_type'], '', '', '',
                            '', '', '', '', '')
        entry.save_to_db()
        return redirect('/Sensorlog')


class SensorLog(Resource):
    """Communication for Sensor log"""

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
            return make_response(render_template('Sensor_log.html', data=SensorModel.get_all_data()[::-1]))
        else:
            return redirect('/shutdown')


class SensorEdit(Resource):
    """Communication for Sensor edit form"""

    def get(self, id, name):
        obj = SensorModel.get_single_data(id)
        try:
            connection = sqlite3.connect('data.db')
        except OperationalError:
            connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = cursor.execute('SELECT version FROM version')
        check = str(query.fetchone()[0])
        connection.close()
        if h.version == check:
            return make_response(render_template('Sensor_edit.html', data=obj))
        else:
            return redirect('/shutdown')

    def post(self, id, name):
        parse = reqparse.RequestParser()
        parse.add_argument('notes',
                           type=str)
        data = parse.parse_args()
        time = datetime.today()
        if name == 'rec_date':
            SensorModel.update_rec_date(id, time)
        elif name == 'start_date':
            SensorModel.update_start_date(id, str(time))
        elif name == 'accessories':
            SensorModel.update_accessories(id, 'stuff')
        elif name == 'appearance':
            SensorModel.update_appearance(id, 'good')
        elif name == 'functions':
            SensorModel.update_functions(id, 'funcs')
        elif name == 'cleaning':
            SensorModel.update_cleaning(id, 'complete')
        elif name == 'complete':
            SensorModel.update_complete(id, str(time))
        elif name == 'notes':
            SensorModel.update_notes(id, data['notes'])
        else:
            pass
        return redirect(f'/Sensor/{id}/null')


class SensorTransfer(Resource):
    """Class to handle a transfer log to be printed for a proof of transfer (NOT IN USE)"""

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
            if not request.args.getlist('test'):
                return make_response(render_template('sensor_transfer.html',
                                                     data=SensorModel.get_transfer_data()[::-1]))
            else:
                pdf = FPDF()
                pdf.add_page()
                count = 0
                time = datetime.today()
                nums = request.args.getlist('test')
                pdf.set_font('Arial', 'B', 16)
                pdf.multi_cell(50, 10, 'Employee')
                pdf.multi_cell(45, 10, 'Model')
                pdf.multi_cell(45, 10, 'Serial')
                pdf.multi_cell(45, 10, 'Date')
                for n in nums:
                    obj = SensorModel.get_multi_data(n)
                    pdf.set_font('Arial', 'B', 12)
                    pdf.ln()
                    pdf.multi_cell(50, 10, obj[0].employee)
                    pdf.multi_cell(45, 10, obj[0].item)
                    pdf.multi_cell(45, 10, obj[0].serial_num)
                    pdf.multi_cell(45, 10, str(time).split()[0])
                    pdf.ln()
                    if count == 10:
                        pdf.add_page()
                        pdf.set_font('Arial', 'B', 16)
                        pdf.multi_cell(50, 10, 'Employee')
                        pdf.multi_cell(45, 10, 'Model')
                        pdf.multi_cell(45, 10, 'Serial')
                        pdf.multi_cell(45, 10, 'Date')
                    count += 1
                pdf.output('print.pdf', 'F')
                os.system(f'cmd /c "print.pdf"')
                pdf.close()
                os.remove(f'{pathlib.Path().absolute()}/print.pdf')
                return make_response(render_template('sensor_transfer.html',
                                                     data=SensorModel.get_transfer_data()[::-1]))
        else:
            return redirect('/shutdown')
