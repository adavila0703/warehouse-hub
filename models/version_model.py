from db import db


class VersionModel(db.Model):
    __tablename__ = 'version'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String())

    def __init__(self, version):
        self.version = version
