import datetime
import logging
import uuid

from db import db


class ItmeModel(db.Model):
    __tablename__ = 'items'

    logging = logging.getLogger(__name__)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(300), unique=True, nullable=False)
    name = db.Column(db.String(300), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __init__(self, name):
        self.uuid = str(uuid.uuid4())
        self.name = name

    def json(self):
        return {'id': self.id, 'uuid': self.uuid, 'name': self.name, 'created': self.created.__str__(),
                'updated': self.updated.__str__()}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_uuid(cls, _uuid):
        return cls.query.filter_by(uuid=_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
