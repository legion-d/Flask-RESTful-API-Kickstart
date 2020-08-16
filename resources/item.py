import logging
from sqlite3 import IntegrityError

from flask_restful import Resource, reqparse

from models.item import ItmeModel


class Item(Resource):
    logging = logging.getLogger(__name__)
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This name field can not left blank "
                        )

    # TODO - @jwt_required()
    def get(self, uuid):
        item = ItmeModel.find_by_uuid(uuid)
        if item:
            return item.json()
        return {'message': 'Item with uuid = {} was not found'.format(uuid)}, 404

    # TODO - @jwt_required()
    def delete(self, uuid):
        item = ItmeModel.find_by_uuid(uuid)
        if item:
            item.delete_from_db()
            return {'message': 'item deleted >> {}'.format(item.json())}
        return {'message': 'Item with uuid = {} not found.'.format(uuid)}, 404

    # TODO - @jwt_required()
    def put(self, uuid):
        data = Item.parser.parse_args()
        item = ItmeModel.find_by_uuid(uuid)

        if item:
            item.name = data['name']
        else:
            return {'message': 'Item with uuid = {} was not found'.format(uuid)}, 404

        item.save_to_db()

        return item.json()

    def post(self):
        data = Item.parser.parse_args()
        item = ItmeModel(**data)
        try:
            item.save_to_db()

        except IntegrityError as err:
            # TODO - check why in case of "UNIQUE constraint failed" the exception is NOT catch
            return {"message": "item with name = {} already exists . item >> {})".format(data['name'], err)}
        except Exception as e:
            return {"message": "An error occurred during inserting the item (error message = {})".format(e)}

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItmeModel.query.all()]}
