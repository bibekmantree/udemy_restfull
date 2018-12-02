from flask import Flask
from flask_restful import Api, Resource, request, reqparse
from flask_jwt import JWT, jwt_required, current_identity


from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)
jwt = JWT(app, authenticate, identity)
items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name {} exists".format(name)}, 400

        data = type(self).parser.parse_args()
        item = {"name": name,
                "price": data["price"]}
        items.append(item)
        return item, 201

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
        global items
        items = [item for item in items if name == item['name']]
        return {'message': "An item with name {} deleted".format(name)}, 200

class Items(Resource):
    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')


if __name__ == "__main__":
    app.run(debug=True)
