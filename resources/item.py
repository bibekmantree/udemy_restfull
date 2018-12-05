from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    def post(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return {'message': "An item with name {} exists".format(name)}, 400

        data = type(self).parser.parse_args()
        item = ItemModel(name, data["price"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "An item with name {} deleted".format(name)}, 200


class Items(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {'items': items}
