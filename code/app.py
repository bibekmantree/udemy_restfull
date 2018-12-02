from flask_restful import Resource, Api
from flask import Flask


app = Flask(__name__)
api = Api(app)


class Student(Resource):
    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/student/<string:name>')

if __name__ == '__main__':
    app.run(port=5000)
