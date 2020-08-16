import logging.config

import yaml
from flask import Flask
from flask_restful import Api

from db import db
from resources.item import Item, ItemList

with open('logging_config.yml') as lc:
    logging_config = yaml.load(lc, Loader=yaml.FullLoader)
    logging.config.dictConfig(logging_config)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, '/item', endpoint='post')
api.add_resource(Item, '/item/<string:uuid>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
