import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @staticmethod
    def get_item_by_name(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items where name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return row if row else None

    @jwt_required()
    def get(self, name):
        row = self.get_item_by_name(name)
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200

        return {"message": "Item not found"}, 404

    def post(self, name):
        row = self.get_item_by_name(name)
        if row:
            return {'message': "An item with name {} exists".format(name)}, 400

        data = type(self).parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, data['price']))
        connection.commit()
        connection.close()
        return {"item": {"name": name, "price": data['price']}}, 201


    def put(self, name):
        data = type(self).parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "An item with name {} deleted".format(name)}, 200


class Items(Resource):
    def get(self):
        return {'items': items}, 200
