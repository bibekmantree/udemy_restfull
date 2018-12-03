import sqlite3
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
        row = ItemModel.get_item_by_name(name)
        if row:
            return {'message': "An item with name {} exists".format(name)}, 400

        data = type(self).parser.parse_args()
        item = ItemModel(name,  data["price"])
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}
        return updated_item.json()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "An item with name {} deleted".format(name)}, 200


class Items(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}