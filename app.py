import webbrowser
import os
import pathlib

from flask import Flask, render_template, request
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from resources.marking_resource import MarkingResource, MarkingLog, MarkingEdit
from resources.micro_resource import MicroResource, MicroLog, MicroEdit
from resources.printing_resource import PrintingResource, PrintingLog, PrintingEdit
from resources.sensor_resource import SensorResource, SensorLog, SensorEdit, SensorTransfer
from resources.home_resource import HomeResource
from resources.dash_resource import DashResource

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = 'key'


class LMTView(ModelView):
    page_size = 50
    can_export = True


class MAGView(ModelView):
    page_size = 50
    can_export = True


class PCTView(ModelView):
    page_size = 50
    can_export = True


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    os.system(f'start cmd /c "{pathlib.Path().absolute()}/update.exe"')
    shutdown_server()
    return render_template('version.html')


# Routes
api.add_resource(HomeResource, '/')
api.add_resource(PrintingResource, '/printing')
api.add_resource(MarkingResource, '/marking')
api.add_resource(MicroResource, '/micro')
api.add_resource(SensorResource, '/sensor')

api.add_resource(MarkingLog, '/markinglog')
api.add_resource(MicroLog, '/microlog')
api.add_resource(PrintingLog, '/printinglog')
api.add_resource(SensorLog, '/sensorlog')
api.add_resource(SensorTransfer, '/sensor_transfer')

api.add_resource(MarkingEdit, '/marking/<int:id>/<string:name>')
api.add_resource(MicroEdit, '/micro/<int:id>/<string:name>')
api.add_resource(PrintingEdit, '/printing/<int:id>/<string:name>')
api.add_resource(SensorEdit, '/sensor/<int:id>/<string:name>')

api.add_resource(DashResource, '/dash')


@app.before_first_request
def create_tables():
    """Creates all tables in the database"""
    db.create_all()


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)
    app.run(port=5000, debug=False)
else:
    from db import db

    db.init_app(app)
