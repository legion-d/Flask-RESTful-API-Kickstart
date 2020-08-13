from flask import Flask
from flask_restful import Api

from db import db
from resources.link import Link, LinkList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///link.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# TODO - How to ignore an id in url - get >> post() got an unexpected keyword argument 'id'
api.add_resource(Link, '/link/', endpoint='post')
api.add_resource(Link, '/link/<string:uuid>')

# TODO - Add support to get link by url
# api.add_resource(Link, '/link/<string:url>')
api.add_resource(LinkList, '/links')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
