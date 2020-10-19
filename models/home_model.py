from db import db


class HomeModel(db.Model):
    """Home model"""
    __tablename__ = 'homepage'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    new_feat = db.Column(db.String())
    eye_out = db.Column(db.String())

    def __init__(self, new_feat, eye_out):
        """Home model constructor"""
        self.new_feat = new_feat
        self.eye_out = eye_out

    @classmethod
    def data(cls, id):
        """Function to grab all data for homepage"""
        obj = cls.query.filter_by(id=id).first()
        return obj
