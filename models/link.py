import datetime
import uuid

from db import db


class LinkModel(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(300), unique=True, nullable=False)
    url = db.Column(db.String(300), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __init__(self, url):
        self.uuid = str(uuid.uuid4())
        self.url = url

    def json(self):
        return {'id': self.id, 'uuid': self.uuid, 'url': self.url, 'created': self.created.__str__(),
                'updated': self.updated.__str__()}

    @classmethod
    def find_by_url(cls, url):
        return cls.query.filter_by(url=url).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
