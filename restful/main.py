#-*- coding:UTF-8 -*-
from flask import Flask
from flask_restful import Api
from api.ApiTest import ApiTest

app = Flask(__name__)
api = Api(app)

api.add_resource(ApiTest, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)