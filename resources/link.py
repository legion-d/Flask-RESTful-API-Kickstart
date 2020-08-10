from sqlite3 import IntegrityError

from flask_restful import Resource, reqparse

from models.link import LinkModel


class Link(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help="This URL field can not left blank "
                        )

    # TODO - @jwt_required()
    def get(self, uuid):
        link = LinkModel.find_by_uuid(uuid)
        if link:
            return link.json()
        return {'message': 'Link with uuid = {} was not found'.format(uuid)}, 404

    # TODO - @jwt_required()
    def delete(self, uuid):
        link = LinkModel.find_by_uuid(uuid)
        if link:
            link.delete_from_db()
            return {'message': 'link deleted >> {}'.format(link.json())}
        return {'message': 'Link with uuid = {} not found.'.format(uuid)}, 404

    # TODO - @jwt_required()
    def put(self, uuid):
        data = Link.parser.parse_args()
        link = LinkModel.find_by_uuid(uuid)

        if link:
            link.url = data['url']
        else:
            return {'message': 'Link with uuid = {} was not found'.format(uuid)}, 404
            # link = LinkModel(data['url'], **data)

        link.save_to_db()

        return link.json()

    def post(self):
        data = Link.parser.parse_args()
        link = LinkModel(**data)
        try:
            link.save_to_db()

        except IntegrityError as err:
            # TODO - check why in case of "UNIQUE constraint failed" the exception is NOT catch
            return {"message": "link with url = {} already exists . link >> {})".format(data['url'], err)}
        except Exception as e:
            return {"message": "An error occurred inserting the link (error message = {})".format(e)}

        return link.json(), 201


class LinkList(Resource):
    def get(self):
        return {'links': [link.json() for link in LinkModel.query.all()]}
