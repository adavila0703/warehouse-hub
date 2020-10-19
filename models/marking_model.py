from db import db
from datetime import datetime


class MarkingModel(db.Model):
    """Marking data structure"""
    __tablename__ = 'marking_table'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.String())
    employee = db.Column(db.String())
    item = db.Column(db.String())
    serial_num = db.Column(db.String())
    ins_type = db.Column(db.String())
    rec_date = db.Column(db.String())
    start_date = db.Column(db.String())
    accessories = db.Column(db.String())
    appearance = db.Column(db.String())
    functions = db.Column(db.String())
    cleaning = db.Column(db.String())
    complete = db.Column(db.String())
    notes = db.Column(db.String(1000))
    complaint = db.Column(db.String())
    admin_notes = db.Column(db.String(1000))
    rec_to_start = db.Column(db.String())
    start_to_comp = db.Column(db.String())

    def __init__(self, date_created, employee, item, serial_num, ins_type, rec_date, start_date, accessories,
                 appearance, functions, cleaning, complete, notes):
        """Marking constructor"""
        self.date_created = date_created
        self.employee = employee
        self.item = item
        self.serial_num = serial_num
        self.ins_type = ins_type
        self.rec_date = rec_date
        self.start_date = start_date
        self.accessories = accessories
        self.appearance = appearance
        self.functions = functions
        self.cleaning = cleaning
        self.complete = complete
        self.notes = notes

    @classmethod
    def get_all_data(cls):
        """Get all marking data"""
        obj = cls.query.filter(MarkingModel.complete == '')
        return obj

    @classmethod
    def get_single_data(cls, id):
        """Get single line data from a given id"""
        obj = cls.query.filter_by(id=id).first()
        return obj

    @classmethod
    def update_db(cls, id, date_created, employee, item, serial_num, ins_type, rec_date, start_date, accessories,
                  appearance, functions, cleaning, complete, notes):
        """Updates all items in marking data table"""
        obj = cls.query.filter_by(id=id).first()
        obj.date_created = date_created
        obj.employee = employee
        obj.item = item
        obj.serial_num = serial_num
        obj.ins_type = ins_type
        obj.rec_date = rec_date
        obj.start_date = start_date
        obj.accessories = accessories
        obj.appearance = appearance
        obj.functions = functions
        obj.cleaning = cleaning
        obj.complete = complete
        obj.notes = notes
        db.session.commit()
        return None

    @classmethod
    def update_rec_date(cls, id, rec_date):
        """Updates the receive date for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.rec_date = rec_date
        db.session.commit()
        return None

    @classmethod
    def update_start_date(cls, id, start_date):
        """Updates the start date for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.start_date = start_date
        obj.rec_to_start = MarkingModel.lt_check(obj.rec_date, start_date)
        db.session.commit()
        return None

    @classmethod
    def update_accessories(cls, id, accessories):
        """Updates the accessories for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.accessories = accessories
        db.session.commit()
        return None

    @classmethod
    def update_appearance(cls, id, appearance):
        """Updates the appearance for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.appearance = appearance
        db.session.commit()
        return None

    @classmethod
    def update_functions(cls, id, functions):
        """Updates the functions for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.functions = functions
        db.session.commit()
        return None

    @classmethod
    def update_cleaning(cls, id, cleaning):
        """Updates the cleaning for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.cleaning = cleaning
        db.session.commit()
        return None

    @classmethod
    def update_complete(cls, id, complete):
        """Updates the complete for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.complete = complete
        obj.start_to_comp = MarkingModel.lt_check(obj.start_date, complete)
        db.session.commit()
        return None

    @classmethod
    def update_notes(cls, id, notes):
        """Updates the notes"""
        obj = cls.query.filter_by(id=id).first()
        obj.notes = notes
        db.session.commit()
        return None

    @classmethod
    def update_transfer(cls, id, complete):
        """Update transfer status for an entry"""
        obj = cls.query.filter_by(id=id).first()
        obj.complete = complete
        obj.start_to_comp = MarkingModel.lt_check(obj.rec_date, complete)
        db.session.commit()
        return None

    @classmethod
    def lt_check(cls, time1, time2):
        """Calculates time between 2 dates"""
        tm1 = datetime(int(time1.split()[0].split('-')[0]), int(time1.split()[0].split('-')[1]),
                       int(time1.split()[0].split('-')[2]), int(time1.split()[1].split(':')[0]),
                       int(time1.split()[1].split(':')[1]), int(time1.split()[1].split(':')[2].split('.')[0]))

        tm2 = datetime(int(time2.split()[0].split('-')[0]), int(time2.split()[0].split('-')[1]),
                       int(time2.split()[0].split('-')[2]), int(time2.split()[1].split(':')[0]),
                       int(time2.split()[1].split(':')[1]), int(time2.split()[1].split(':')[2].split('.')[0]))
        return str(tm2 - tm1)

    @classmethod
    def count_completed(cls, name, date, year):
        """Function which counts how many entries have been completed"""
        count = 0
        obj = cls.query.filter_by(employee=name).filter(MarkingModel.complete != '').all()
        for o in obj:
            if o.complete.split('-')[1] == date and o.complete.split('-')[0] == year:
                count += 1
        return count

    @classmethod
    def count_failed(cls, month, year):
        """Function which counts how many entries have failed"""
        count = 0
        obj = cls.query.filter(MarkingModel.complete != '').all()
        for o in obj:
            if o.complete.split('-')[1] == month and o.complete.split('-')[0] == year:
                if o.appearance == 'Fail' or o.functions == 'Fail':
                    count += 1
        return count

    @classmethod
    def total_count(cls, name, date):
        """Counts the total amount of entries"""
        count = 0
        obj = cls.query.filter(MarkingModel.complete != '').all()
        for o in obj:
            if o.complete.split('-')[1] == date:
                count += 1
        return count

    @classmethod
    def process_fail(cls, month, year):
        """Counts the failed process"""
        app = 0
        func = 0
        obj = cls.query.filter(MarkingModel.complete != '').all()
        for o in obj:
            if o.complete.split('-')[1] == month and o.complete.split('-')[0] == year:
                if o.appearance == 'Fail':
                    app += 1
                if o.functions == 'Fail':
                    func += 1
        return [app, func]

    def save_to_db(self):
        """Save all db information"""
        db.session.add(self)
        db.session.commit()
        return None
