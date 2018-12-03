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

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

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
        item = {"name": name, "price": data["price"]}
        try:
            type(self).insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.get_item_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

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
